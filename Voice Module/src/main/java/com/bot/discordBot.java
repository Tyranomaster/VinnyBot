package com.bot;

import com.sedmelluq.discord.lavaplayer.player.AudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.player.DefaultAudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.source.AudioSourceManagers;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.entities.Member;
import net.dv8tion.jda.core.entities.PrivateChannel;
import net.dv8tion.jda.core.events.guild.voice.GuildVoiceLeaveEvent;
import net.dv8tion.jda.core.events.guild.voice.GuildVoiceMoveEvent;
import net.dv8tion.jda.core.exceptions.RateLimitedException;
import net.dv8tion.jda.core.hooks.ListenerAdapter;
import com.sedmelluq.discord.lavaplayer.player.AudioLoadResultHandler;
import com.sedmelluq.discord.lavaplayer.tools.FriendlyException;
import com.sedmelluq.discord.lavaplayer.track.AudioPlaylist;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.TextChannel;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.managers.AudioManager;

/**
 * Created by Jess on 3/28/2017.
 */

import java.awt.*;
import java.util.*;

import static com.bot.TrackScheduler.MAX_QUEUE_SIZE;

public class discordBot extends ListenerAdapter {
    private static String nickName;
    private static String avatarURL;
    private static final Color vinnyColor = new Color(0, 140, 186);
    private static final int NUM_SHARDS = 5;
    private static ShardingManager shardingManager;
    private final AudioPlayerManager playerManager;
    private final HashMap<Long, ServerMusicManager> musicManagers;
    private final HashMap<Long, SearchListenerMessage> searchListeners;
    private final HashMap<Long, Timer> searchTimers;
    private Timer purgeTimer;

    public static void main(String[] args) throws Exception {
        Config config = new Config();
        shardingManager = new ShardingManager(NUM_SHARDS, config);

        nickName = shardingManager.getJDA(0).getSelfUser().getName();
        avatarURL = shardingManager.getJDA(0).getSelfUser().getAvatarUrl();

    }

    protected discordBot() {
        this.musicManagers = new HashMap<>();
        this.searchListeners = new HashMap<>();
        this.searchTimers = new HashMap<>();
        this.playerManager = new DefaultAudioPlayerManager();
        AudioSourceManagers.registerRemoteSources(playerManager);
        AudioSourceManagers.registerLocalSource(playerManager);
        purgeInactiveConnections();
    }

    private synchronized ServerMusicManager getServerAudioPlayer(Guild guild) {
        long guildId = Long.parseLong(guild.getId());
        ServerMusicManager musicManager = musicManagers.computeIfAbsent(guildId, k -> new ServerMusicManager(playerManager));

        guild.getAudioManager().setSendingHandler(musicManager.getSendHandler());

        return musicManager;
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        String[] command = event.getMessage().getContent().split(" ", 2);
        Guild guild = event.getGuild();

        if (guild != null) {
            if ("~play".equals(command[0]) && command.length == 2) {
                if (event.getMember().getVoiceState().getChannel() == null) {
                    event.getTextChannel().sendMessage("You are not connected to a voice channel :cry:").queue();
                    return;
                }
                loadAndPlay(event.getTextChannel(), command[1], event.getMember());
            } else if ("~skip".equals(command[0])) {
                skipTrack(event.getTextChannel());
            } else if ("~playlist".equals(command[0])) {
                getPlaylist(event.getTextChannel());
            } else if ("~stop".equals(command[0])) {
                stopPlayer(event.getTextChannel());
            } else if ("~pause".equals(command[0])) {
                pauseTrack(event.getTextChannel());
            } else if ("~resume".equals(command[0])) {
                resumeTrack(event.getTextChannel());
            } else if ("~shardinfo".equals(command[0])) {
                printShardInfo(event.getTextChannel());
            } else if ("~voicestats".equals(command[0])) {
                voiceStats(event.getTextChannel());
            } else if ("~volume".equals(command[0])) {
                setVolume(event, command);
            }
            else if ("~search".equals(command[0])) {
                if (event.getMember().getVoiceState().getChannel() == null) {
                    event.getTextChannel().sendMessage("You are not connected to a voice channel :cry:").queue();
                    return;
                } else if (command.length < 2) {
                    event.getTextChannel().sendMessage("You need to give me something to search for.").queue();
                    return;
                }
                search(event.getTextChannel(), command[1], event.getMember());
                //event.getTextChannel().sendMessage("Search functionality coming soon. Checkout the discord server for frequent updates.").queue();
            } else if ("~cancel".equals(command[0])){
                searchListeners.remove(Long.parseLong(event.getMember().getUser().getId()));
                event.getTextChannel().sendMessage("Canceled all outstanding Listeners for " + event.getMember().getEffectiveName()).queue();
            } else if (command[0].length() == 1) {
                if (Character.isDigit(command[0].charAt(0))) {
                    handleSearchResponse(event, command);
                }
            } else if (command[0].equals("~leave")) {
                leaveChannel(event.getTextChannel());
            } else if (command[0].equals("~remove")) {
                if (command.length == 2)
                    removeTrack(event.getTextChannel(), command[1]);
                else
                    event.getTextChannel().sendMessage("Error: Formatting incorrect. Please type only the command and the number of the track to be removed. Separated by a space.").queue();
            }
        }

        super.onMessageReceived(event);
    }

    private void printShardInfo(TextChannel channel) {
        EmbedBuilder embedBuilder = new EmbedBuilder();
        int[] totals = shardingManager.getServersPerShard();
        for (int i = 0; i < NUM_SHARDS; i++){
            embedBuilder.addField("Shard " + i, "" + totals[i], true);
        }
        embedBuilder.setFooter("You are on shard: " + channel.getJDA().getShardInfo().getShardId(), null);
        embedBuilder.setColor(vinnyColor);
        channel.sendMessage(embedBuilder.build()).queue();
    }

    @Override
    public void onGuildVoiceLeave(GuildVoiceLeaveEvent event) {
        checkVoiceLobby(event.getGuild());
    }

    @Override
    public void onGuildVoiceMove(GuildVoiceMoveEvent event) {
        checkVoiceLobby(event.getGuild());
    }

    private void loadAndPlay(final TextChannel channel, final String trackUrl, final Member author) {
        final ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());
        String url = trackUrl.split(" ")[0];
        channel.sendTyping().queue();

        playerManager.loadItemOrdered(musicManager, url, new AudioLoadResultHandler() {
            @Override
            public void trackLoaded(AudioTrack track) {
                //Checking to make sure queue is not full
                if (musicManager.scheduler.getNumQueuedTracks() + 1 >= MAX_QUEUE_SIZE){
                    channel.sendMessage(":x: Cannot add song to queue. Queue Limit of " + MAX_QUEUE_SIZE + " reached.").queue();
                    return;
                }

                EmbedBuilder builder = new EmbedBuilder();
                builder.setTitle(track.getInfo().title, track.getInfo().uri);
                builder.addField("Added song to playlist", "Duration: " + msToMinSec(track.getDuration()), false);
                builder.setImage("https://img.youtube.com/vi/"+ track.getIdentifier() + "/mqdefault.jpg");
                builder.setColor(vinnyColor);

                channel.sendMessage(builder.build()).queue();

                play(channel.getGuild(), musicManager, track, author);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {

                if (trackUrl.split(" ").length == 1) {
                    channel.sendMessage("Playlist detected. Please try again but include the songs you want included.\n" +
                            "Example: `~play *playlist url* 1-5` This would load songs 1-5 on the playlist. Limited to loading up to 10 songs at a time.").queue();
                } else {
                    String songs = trackUrl.split(" ")[1];
                    if (songs.split("-").length == 2) {
                        int to;
                        int from;
                        try {
                            from = Integer.parseInt(songs.split("-")[0]);
                            to = Integer.parseInt(songs.split("-")[1]);
                        } catch (NumberFormatException e) {
                            channel.sendMessage(":x: NumberFormatException: Invalid number given, please only user numeric characters :x:").queue();
                            return;
                        }
                        if (from > to) {
                            channel.sendMessage(":x: Error: Beginning index is bigger than ending index :x:").queue();
                            return;
                        } else if (to > playlist.getTracks().size()) {
                            channel.sendMessage(":x: Error: Requesting tracks out of range. Only " + playlist.getTracks().size() + " tracks in playlist :x:").queue();
                            return;
                        } else if (to - from > 9) {
                            channel.sendMessage(":exclamation: Warning: Requesting number of tracks that is greater than 10. Trimming results to " +
                                    "" + from + "-" + (from + 9) +" :exclamation:").queue();
                            to = from + 9;
                        }
                        String msg = "Added " + (to - from + 1) + " songs to queue: ```";
                        int count = 1;
                        for (int i = from - 1; i < to; i++) {
                            if (musicManager.scheduler.getNumQueuedTracks() + 1 >= MAX_QUEUE_SIZE) {
                                msg = ":x: Queue size full. I was only able to add " + (i - from + 1) + " songs. ```" + msg.split("```")[1];
                                break;
                            }
                            play(channel.getGuild(), musicManager, playlist.getTracks().get(i), author);
                            msg += count + ": " +  playlist.getTracks().get(i).getInfo().title + "\n";
                            count++;
                        }
                        msg += "```";
                        channel.sendMessage(msg).queue();
                    } else {
                        channel.sendMessage(":x: Error: Incorrect number of parameters. Make sure that there are no spaces between your track numbers and the dash :x:").queue();
                    }
                }
            }

            @Override
            public void noMatches() {
                channel.sendMessage("Nothing found by " + trackUrl).queue();
                if (!musicManager.scheduler.isPlaying())
                    musicManagers.remove(Long.parseLong(channel.getGuild().getId()));
            }

            @Override
            public void loadFailed(FriendlyException exception) {
                channel.sendMessage("Could not play: " + exception.getMessage()).queue();
                if (!musicManager.scheduler.isPlaying())
                    musicManagers.remove(Long.parseLong(channel.getGuild().getId()));
            }
        });
    }

    private void play(Guild guild, ServerMusicManager musicManager, AudioTrack track, final Member author) {
        connectToVoiceChannel(guild.getAudioManager(), author);

        if (musicManager.scheduler.getNumQueuedTracks() >= 19) {

        }
        musicManager.scheduler.queue(track);
    }

    private void skipTrack(TextChannel channel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(channel.getGuild().getId()));
        if (musicManager == null) {
            channel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        musicManager.scheduler.nextTrack();

        channel.sendMessage("Skipped to next track.").queue();
    }

    private static void connectToVoiceChannel(AudioManager audioManager, final Member author) {
        if (!audioManager.isConnected() && !audioManager.isAttemptingToConnect()) {
            audioManager.openAudioConnection(author.getVoiceState().getChannel());
        }
    }

    private void pauseTrack(final TextChannel textChannel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(textChannel.getGuild().getId()));
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio.").queue();
            return;
        }
        musicManager.scheduler.pause();
        textChannel.sendMessage("Successfully paused stream.").queue();
    }

    private void resumeTrack(final TextChannel textChannel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(textChannel.getGuild().getId()));
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio.").queue();
            return;
        }
        musicManager.scheduler.resume();
        textChannel.sendMessage("Successfully resumed Stream.").queue();
    }

    private void stopPlayer(final TextChannel textChannel) {
        long guildId = Long.parseLong(textChannel.getGuild().getId());
        ServerMusicManager musicManager = musicManagers.get(guildId);
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio.").queue();
            return;
        }
        musicManager.scheduler.stopPlayer();
        textChannel.getGuild().getAudioManager().closeAudioConnection();
        textChannel.sendMessage("Stopping player.").queue();
        //System.out.println(musicManagers.size());
        musicManagers.remove(guildId);
        //System.out.println(musicManagers.size());
        System.gc();
    }

    private void leaveChannel(TextChannel textChannel) {
        long guildId = Long.parseLong(textChannel.getGuild().getId());
        ServerMusicManager musicManager = musicManagers.get(guildId);
        if (musicManager == null) {
            textChannel.sendMessage("I am currently not connected to a voice channel.").queue();
            return;
        }

        musicManager.scheduler.stopPlayer();
        textChannel.getGuild().getAudioManager().closeAudioConnection();
        textChannel.sendMessage("Leaving voice channel.").queue();
        //System.out.println(musicManagers.size());
        musicManagers.remove(guildId);
        //System.out.println(musicManagers.size());
        System.gc();
    }

    public HashMap<Long, ServerMusicManager> getMusicManagers() {
        return musicManagers;
    }

    private void getPlaylist(final TextChannel textChannel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(textChannel.getGuild().getId()));
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio.").queue();
        } else {
            String[] playlist = musicManager.scheduler.getPlaylist();
            String msg = (musicManager.scheduler.getNumQueuedTracks() + 1) + "/" + MAX_QUEUE_SIZE + " queue slots filled" + "```Playlist\n";
            for (int i = 0; i < playlist.length; i++) {
                if (i == 0)
                    msg += "Now Playing: " + playlist[i] + "\n";
                else if (i == 1) {
                    msg += "Next: " + playlist[i] + "\n";
                } else
                    msg += (i + 1) + ": " + playlist[i] + "\n";
            }
            msg += "```";
            textChannel.sendMessage(msg).queue();
        }
    }

    private void voiceStats(TextChannel textChannel) {
        int activeServers = shardingManager.getNumberActiveConnections();
        //getNumberActiveStreams();
        int totalServers = shardingManager.getTotalConnections();
        //musicManagers.size();
        String mem = (((Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1024) / 1024) + " MB";
        EmbedBuilder builder = new EmbedBuilder();
        builder.setAuthor(nickName, avatarURL, avatarURL);
        builder.addField("Total voice servers", "" + totalServers, true);
        builder.addField("Active voice servers", "" + activeServers, true);
        builder.addField("Memory used", "" + mem, true);
        builder.setColor(vinnyColor);
        textChannel.sendMessage(builder.build()).queue();
    }


    private void search(final TextChannel channel, final String trackUrl, final Member author) {
        final ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());

        playerManager.loadItemOrdered(channel.getGuild(), "ytsearch:" + trackUrl, new AudioLoadResultHandler() {
            @Override
            public void trackLoaded(AudioTrack track) {
                channel.sendMessage("Adding to queue " + track.getInfo().title).queue();

                play(channel.getGuild(), musicManager, track, author);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {
                //System.out.print("here: " + playlist.getTracks().size());
                EmbedBuilder builder = new EmbedBuilder();
                AudioTrack[] tracks = new AudioTrack[5];

                builder.setAuthor(nickName, avatarURL, avatarURL);
                builder.setTitle("Select a song to add by responding with the corresponding number.\n", null);
                String body = "";
                for (int i = 0; i < Math.min(5, playlist.getTracks().size()); i++) {
                    body += (i+1) + ": " + "`" + playlist.getTracks().get(i).getInfo().title + "`" + " Duration: " + msToMinSec(playlist.getTracks().get(i).getInfo().length) + "\n";
                    tracks[i] = playlist.getTracks().get(i);
                    //System.out.print("Track");
                }
                if (searchListeners.get(Long.parseLong(author.getUser().getId())) == null){
                    searchListeners.put(Long.parseLong(author.getUser().getId()), new SearchListenerMessage(Long.parseLong(author.getUser().getId()), tracks, channel));
                    builder.addField("Returned Videos:", body, false);
                    builder.setFooter("60 second timeout | ~cancel to cancel the search", null);
                    builder.setColor(vinnyColor);
                    channel.sendMessage(builder.build()).queue();
                    setSearchListenerTimer(channel, author);
                } else {
                    channel.sendMessage(":x: You already have an outstanding search in this or another channel. Please answer it or use the \"~cancel\" command to cancel it :x:").queue();
                }
            }

            @Override
            public void noMatches() {
                channel.sendMessage("Nothing found for " + trackUrl).queue();
                if (!musicManager.scheduler.isPlaying())
                    musicManagers.remove(Long.parseLong(channel.getGuild().getId()));
            }

            @Override
            public void loadFailed(FriendlyException exception) {
                channel.sendMessage("Could not play: " + exception.getMessage()).queue();
                if (!musicManager.scheduler.isPlaying())
                    musicManagers.remove(Long.parseLong(channel.getGuild().getId()));
            }
        });
    }

    //Helper method for song that takes length in Milliseconds and outputs it in a more readable HH:MM:SS format
    private String msToMinSec(long length) {
        int totSeconds = (int)length/1000;
        String seconds = "";
        String minutes = "";
        String hours = "";
        if (totSeconds%60 < 10)
            seconds = "0" + totSeconds%60;
        else
            seconds += totSeconds%60;
        if (totSeconds/60 < 10)
            minutes = "0" + totSeconds/60;
        else if (totSeconds/60 > 59)
            minutes += (totSeconds/60)%60;
        else
            minutes += totSeconds/60;
        if (totSeconds/3600 < 10)
            hours = "0" + (totSeconds/60)/60;
        else
            hours += (totSeconds/60)/60;

        if (hours.equals("00"))
            return minutes + ":" + seconds;
        else {
            if (minutes.length() == 1)
                minutes = "0" + minutes;
            return hours + ":" + minutes + ":" + seconds;
        }
    }

    private void handleSearchResponse(MessageReceivedEvent event, String[] command) {
        SearchListenerMessage s = searchListeners.get(Long.parseLong(event.getAuthor().getId()));
        if (s != null) {
            if (s.getChannel().equals(event.getTextChannel())){
                int selection = Integer.parseInt(command[0]);
                //check if selection is outside of range
                if (selection > s.getUpperbound() || selection < s.getLowerBound()){
                    event.getTextChannel().sendMessage("Selection was outside of range. Please select between " + s.getLowerBound() + " and " + s.getUpperbound()).queue();
                } else {
                    loadAndPlay(s.getChannel(), s.getTracks()[selection-1].getInfo().uri, event.getMember());
                    searchListeners.remove(Long.parseLong(event.getAuthor().getId()));
                    Timer t = searchTimers.get(Long.parseLong(event.getAuthor().getId()));
                    if (t != null){
                        t.cancel();
                        t.purge();
                        searchTimers.remove(Long.parseLong(event.getAuthor().getId()));
                    }
                }
            }
        }
    }

    private void setSearchListenerTimer(TextChannel channel, Member author){
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                if (searchListeners.get(Long.parseLong(author.getUser().getId())) != null) {
                    if (!author.getUser().hasPrivateChannel()){
                        author.getUser().openPrivateChannel().queue();
                    }
                    try {
                        PrivateChannel p = author.getUser().openPrivateChannel().complete(true);
                        p.sendMessage("Closed audio search in channel: " + channel.getName() + ". Due to inactivity").queue();
                    } catch (RateLimitedException e) {
                        e.printStackTrace();
                    }

                    timer.cancel();
                    timer.purge();
                    if (!musicManagers.get(Long.parseLong(channel.getGuild().getId())).scheduler.isPlaying())
                        musicManagers.remove(Long.parseLong(channel.getGuild().getId()));

                    Iterator it = searchListeners.entrySet().iterator();
                    while (it.hasNext()) {
                        Map.Entry<Long, ServerMusicManager> entry = (Map.Entry<Long, ServerMusicManager>) it.next();
                        if (entry.getKey() == Long.parseLong(author.getUser().getId())) {
                            it.remove();
                        }
                    }
                }
            }
        }, 60000);
        searchTimers.put(Long.parseLong(author.getUser().getId()), timer);
    }

    private void purgeInactiveConnections() {
        if (purgeTimer != null)
            return;

        purgeTimer = new Timer();
        purgeTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                Iterator it = musicManagers.entrySet().iterator();
                int numClosed = 0;
                while(it.hasNext()) {
                    Map.Entry<Long, ServerMusicManager> entry = (Map.Entry<Long, ServerMusicManager>) it.next();
                    ServerMusicManager musicManager = entry.getValue();
                    if (!musicManager.scheduler.isPlaying() && !musicManager.scheduler.getPlayer().isPaused()) {
                        musicManager.scheduler.stopPlayer();
                        for(int i = 0; i < NUM_SHARDS; i++){
                            Guild temp = shardingManager.getJDA(i).getGuildById(entry.getKey().toString());
                            if (temp != null)
                                temp.getAudioManager().closeAudioConnection();
                        }
                        it.remove();
                        numClosed++;
                    }
                }
                if (numClosed == 0)
                    System.out.println("No connections purged");
                else
                    System.out.println("Purged: " + numClosed + " inactive connections");
                System.gc();
            }
        }, 600000, 1800000);
    }

    private void checkVoiceLobby(Guild guild) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(guild.getId()));
        if (guild.getAudioManager().isConnected()) {
            if (guild.getAudioManager().getConnectedChannel().getMembers().size() == 1) {
                long guildId = Long.parseLong(guild.getId());
                musicManager.scheduler.stopPlayer();
                guild.getAudioManager().closeAudioConnection();
                musicManagers.remove(guildId);
                //System.out.print(musicManagers.size());
                System.gc();
            }
        }

    }

    private void setVolume(MessageReceivedEvent event, String[] command) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(event.getTextChannel().getGuild().getId()));
        if (musicManager == null) {
            event.getTextChannel().sendMessage("Error: No AudioManager detected in this server").queue();
            return;
        }
        try {
            int volume = Integer.parseInt(command[1]);
            musicManager.player.setVolume(volume);
            event.getTextChannel().sendMessage("Volume successfully set to: " + Math.min(150, Math.max(0, volume))).queue();
        } catch (Exception e) {
            event.getTextChannel().sendMessage("Error: Incorrect parameters. Please input a number between 0 and 100.").queue();
        }
    }

    private void removeTrack(final TextChannel channel, String command){
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(channel.getGuild().getId()));
        if (musicManager == null) {
            channel.sendMessage("Error: No AudioManager detected in this server.").queue();
        } else if (!command.matches("[0-9]+")) {
            channel.sendMessage("Error: Incorrect formatting. Please enter a number.").queue();
        } else {
            if (command.equals("0")) {
                skipTrack(channel);
                return;
            }
            if (Integer.parseInt(command) > musicManager.scheduler.getNumQueuedTracks() + 1){
                channel.sendMessage("Error: Given number larger than queue size.").queue();
                return;
            }
            String result = musicManager.scheduler.removeTrack(Integer.parseInt(command));
            if (result == null) {
                channel.sendMessage("Error: Failed to remove track.").queue();
            } else {
                channel.sendMessage("Successfully removed track: " + result).queue();
            }
        }
    }
}