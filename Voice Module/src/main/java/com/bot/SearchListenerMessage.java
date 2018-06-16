package com.bot;

import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.core.entities.TextChannel;


public class SearchListenerMessage {

    private long authorID;
    private AudioTrack[] tracks;
    private TextChannel channel;

    public SearchListenerMessage(long authorID, AudioTrack[] tracks, TextChannel channel){
        this.authorID = authorID;
        this.tracks = tracks;
        this.channel = channel;
    }

    public long getAuthorID() {
        return authorID;
    }

    public AudioTrack[] getTracks() {
        return tracks;
    }

    public TextChannel getChannel() {
        return channel;
    }

    public int getLowerBound() {
        return 1;
    }

    public int getUpperbound() {
        return this.tracks.length;
    }
}
