package com.bot;

import net.dv8tion.jda.core.AccountType;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDABuilder;

import java.util.Map;

/**
 * Created by Jess on 5/17/2017.
 */
public class ShardingManager {

    private static JDA[] shards;



    public ShardingManager(int numShards, Config config) throws Exception{
        shards = new JDA[numShards];

        for (int i = 0; i < numShards; i++){
            shards[i] = new JDABuilder(AccountType.BOT)
                    .setToken(config.getToken("Discord"))
                    .useSharding(i, numShards)
                    .buildBlocking();

            shards[i].addEventListener(new discordBot());
            System.out.println("Started shard: " + i);
        }
        System.out.println("Started all shards");
    }

    public static JDA[] getShards() {
        return shards;
    }

    public JDA getJDA(int shardId) {
        return shards[shardId];
    }

    public int getNumberActiveConnections(){
        int count = 0;
        for (int i = 0; i < shards.length; i++){
            discordBot db = (discordBot) shards[i].getRegisteredListeners().get(0);
            for (Map.Entry<Long, ServerMusicManager> entry : db.getMusicManagers().entrySet()){
                ServerMusicManager manager = entry.getValue();
                if (manager.scheduler.isPlaying()) {
                    count++;
                }
            }
        }
        return count;
    }

    public int getTotalConnections() {
        int count = 0;
        for (int i = 0; i < shards.length; i++) {
            discordBot db = (discordBot) shards[i].getRegisteredListeners().get(0);
            count += db.getMusicManagers().size();
        }
        return count;
    }

    public int[] getServersPerShard(){
        int[] totals = new int[shards.length];
        for (int i = 0; i < shards.length; i++){
            totals[i] = shards[i].getGuilds().size();
        }
        return totals;
    }
}
