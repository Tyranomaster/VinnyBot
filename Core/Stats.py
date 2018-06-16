import glob
import json
import os
import threading
import discord
from urllib.request import urlopen
from urllib.request import Request
from Config import getToken

commandsCalled = 0
members = {}

VINNY_COLOR = int('008cba', 16)

async def getStats(message, client):
    serverCount = 0
    channelCount = 0
    for server in client.guilds:
        serverCount += 1
        for channel in server.channels:
            channelCount += 1
        for member in server.members:
            members[member.id] = 1

    if message.channel.permissions_for(message.guild.me).embed_links:
        embed = discord.Embed(title='', colour=VINNY_COLOR)
        embed.add_field(name='Servers',
                        value='{}'.format(serverCount),
                        inline=True)
        embed.add_field(name='Channels', value=channelCount, inline=True)
        embed.add_field(name='Users', value=len(members), inline=True)
        try:
            embed.add_field(name='Shards', value=str(len(client.shard_ids)), inline=False)
        except TypeError:
            embed.add_field(name='Shards', value=5, inline=False)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)

        return await message.channel.send("Find more detailed stats at: https://goo.gl/Jct6uL", embed=embed)
    else:
        await message.channel.send(message.channel, "Vinny Stats:\n`Servers: " + str(serverCount) + "\nChannels: " + str(channelCount)
                                  + "\n`")


def sendStatistics(client):
    url = "https://bots.discord.pw/api/bots/" + getToken('Bot ID') + "/stats"
    serverCount = len(client.guilds)

    data = {
               "server_count": serverCount
           }

    req = Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', getToken('Bot API'))
    response = urlopen(req, json.dumps(data).encode('utf8'))
    print('Stats Posted Successfully')
    t = threading.Timer(3600.0, sendStatistics, args=(client,))
    t.setDaemon(True)
    t.start()
