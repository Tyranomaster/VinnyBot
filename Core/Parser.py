import urllib
import json
import urllib.request

import discord
from Reddit import *
from help import *
from Config import *
from Moderation import *
from VoiceCore import *
from Giphy import *
from Memes import *
from Markov import *
from WhoSaid import *
from Stats import *
from nsfw import *
from Logger import *


async def parseCommand(message, client):

    if not message.channel.is_private:
        if not message.channel.permissions_for(message.server.me).send_messages:
            return

        #Find which command has been given
        if message.content.startswith('~'):
            if message.author.bot:
                return
            if message.content.startswith('~test'):
                counter = 0
                tmp = await client.send_message(message.channel, 'Calculating messages...')
                async for log in client.logs_from(message.channel, limit=1000):
                    if log.author == message.author:
                        counter += 1

                await client.edit_message(tmp, message.author.name + ', you have {} messages.'.format(counter))

            elif message.content.startswith('~help'):
                await help(message, client)
                commandCalled()
                logCommand(message, client, '~help')

            elif message.content.startswith('~info'):
                await info(message, client)
                commandCalled()
                logCommand(message, client, '~info')

            elif message.content.startswith('~invite'):
                await invite(message, client)
                commandCalled()
                logCommand(message, client, '~invite')

            elif message.content.startswith('~stats'):
                await getStats(message, client)
                commandCalled()
                logCommand(message, client, '~stats')

            elif message.content.startswith('~permission'):
                commandCalled()
                logCommand(message, client, '~permission')
                if message.channel.permissions_for(message.server.me).read_messages:
                    await client.send_message(message.channel, "I have permission")
                else:
                    await client.send_message(message.channel, "I do not have permission")

            elif message.content.startswith('~prune'):
                if message.channel.permissions_for(message.server.me).manage_messages:
                    if message.channel.permissions_for(message.author).manage_messages:
                        await prune(message, client)
                    else:
                        await client.send_message(message.channel, ":x: You do not have permissions to use this command :x:")
                else:
                    await client.send_message(message.channel, ":x: I don't have permissions to delete messages here. :x:")
                commandCalled()
                logCommand(message, client, '~prune')
                # await prune(message, client)

            elif message.content.startswith('~kick'):
                if message.channel.permissions_for(message.server.me).kick_members:
                    if message.channel.permissions_for(message.author).kick_members:
                        await kick(message, client)
                    else:
                        await client.send_message(message.channel, ":x: You do not have permissions to use this command :x:")
                else:
                    await client.send_message(message.channel, ":x: I don't have permissions to kick members here. :x:")
                commandCalled()
                logCommand(message, client, '~kick')
                # await kick(message, client)

            elif message.content.startswith('~ban'):
                if message.channel.permissions_for(message.server.me).ban_members:
                    if message.channel.permissions_for(message.author).ban_members:
                        await ban(message, client)
                    else:
                        await client.send_message(message.channel, ":x: You do not have permissions to use this command :x:")
                else:
                    await client.send_message(message.channel, ":x: I don't have permissions to ban members here. :x:")

                commandCalled()
                logCommand(message, client, '~ban')

            # Voice Commands (Currently removed and moved to Vinny's new JDA module)
            elif message.content.startswith('~summon'):
                await client.send_message(message.channel, "Summon command no longer used. Just use the play command "
                                                           "to summon Vinny.")
                commandCalled()
                logCommand(message, client, '~summon')

            elif message.content.startswith('~playlist'):
                commandCalled()
                logCommand(message, client, '~playlist')

            elif message.content.startswith('~skip'):
                commandCalled()
                logCommand(message, client, '~skip')

            elif message.content.startswith("~volume "):
                commandCalled()
                logCommand(message, client, '~volume (val)')

            elif message.content.startswith("~volume"):
                commandCalled()
                logCommand(message, client, '~volume')

            elif message.content.startswith('~play'):
                commandCalled()
                logCommand(message, client, '~play')

            elif message.content.startswith('~pause'):
                commandCalled()
                logCommand(message, client, '~pause')

            elif message.content.startswith('~resume'):
                commandCalled()
                logCommand(message, client, '~resume')

            elif message.content.startswith('~stop'):
                commandCalled()
                logCommand(message, client, '~stop')

            elif message.content.startswith('~voicestats'):
                commandCalled()
                logCommand(message, client, '~voicestats')

            elif message.content.startswith('~search'):
                commandCalled()
                logCommand(message, client, message.content)

            elif message.content.startswith('~leave'):
                commandCalled()
                logCommand(message, client, '~leave')

            elif message.content.startswith('~cancel'):
                commandCalled()
                logCommand(message, client, '~cancel')

            # Meme Commands
            elif message.content.startswith('~ayy'):
                await ayy(message, client)
                commandCalled()
                logCommand(message, client, '~ayy')

            elif message.content.startswith('~kappa'):
                await kappa(message, client)
                commandCalled()
                logCommand(message, client, '~kappa')

            elif message.content.startswith('~hammer'):
                await banHammer(message, client)
                commandCalled()
                logCommand(message, client, '~hammer')

            elif message.content.startswith('~doggo'):
                await doggo(message, client)
                commandCalled()
                logCommand(message, client, '~doggo')

            elif message.content.startswith('~lenny'):
                await lenny(message, client)
                commandCalled()
                logCommand(message, client, '~lenny')

            elif message.content.startswith('~hitler'):
                await hitler(message, client)
                commandCalled()
                logCommand(message, client, '~hitler')

            elif message.content.startswith('~mario'):
                await mario(message, client)
                commandCalled()
                logCommand(message, client, '~mario')

            elif message.content.startswith('~megaman'):
                await megaMan(message, client)
                commandCalled()
                logCommand(message, client, '~megaman')

            elif message.content.startswith('~salt'):
                await salt(message, client)
                commandCalled()
                logCommand(message, client, '~salt')

            elif message.content.startswith('~pikachu'):
                await pikachu(message, client)
                commandCalled()
                logCommand(message, client, '~pikachu')

            elif message.content.startswith('~feels'):
                await feels(message, client)
                commandCalled()
                logCommand(message, client, '~feels')

            elif message.content.startswith('~harambe'):
                await harambe(message, client)
                commandCalled()
                logCommand(message, client, '~harambe')

            elif message.content.startswith('~giphy'):
                await giphy(message, client)
                commandCalled()
                logCommand(message, client, '~giphy')

            elif message.content.startswith('~8ball'):
                await magic8ball(message, client)
                commandCalled()
                logCommand(message, client, "8ball")

            elif message.content.startswith('~praise'):
                await client.send_message(message.channel, 'https://media.giphy.com/media/fr42tarocsK6Q/giphy.gif')
                commandCalled()
                logCommand(message, client, '~praise')

            elif message.content.startswith('~vote'):
                await vote(message, client)
                commandCalled()
                logCommand(message, client, '~vote')

            elif message.content.startswith('~whois'):
                await userInfo(message, client)
                commandCalled()
                logCommand(message, client, '~whois')

            # Reddit Commands
            elif message.content.startswith('~shit'):
                await client.send_typing(message.channel)
                await client.send_message(message.channel, random_hot_post('shitpost', 20, message))
                commandCalled()
                logCommand(message, client, '~shit')

            elif message.content.startswith('~rr'):
                await client.send_typing(message.channel)
                try:
                    subreddit = message.content.split(' ')[1]
                except IndexError:
                    await client.send_message(message.channel, "No subreddit mentioned, please enter a subreddit")
                    return
                post = random_hot_post(subreddit, 20, message)
                if post is not None:
                    await client.send_message(message.channel, post)
                else:
                    await client.send_message(message.channel, "There was an error retrieving a post")

                commandCalled()
                logCommand(message, client, message.content)

            elif message.content.startswith('~tr'):
                await client.send_typing(message.channel)
                try:
                    subreddit = message.content.split(' ')[1]
                except IndexError:
                    await client.send_message(message.channel, "No subreddit mentioned, please enter a subreddit")
                    return
                try:
                    await client.send_message(message.channel, random_hot_post(subreddit, 2, message.channel))
                except:
                    await client.send_message(message.channel, "Oops. There was an error retriving a post :confounded:")
                commandCalled()
                logCommand(message, client, message.content)

            elif message.content.startswith('~cosplaygirls'):
                await client.send_typing(message.channel)
                await client.send_message(message.channel, getCosplayGirl(message, client))
                commandCalled()
                logCommand(message, client, '~cosplaygirls')

            elif message.content.startswith('~cosplay'):
                await client.send_typing(message.channel)
                await client.send_message(message.channel, getCosplay(message, client))
                commandCalled()
                logCommand(message, client, message.content)

            #Nsfw Commands TODO: Add permissions and nsfw lock
            elif message.content.startswith('~nsfw'):
                if isEnabled(message):
                    await client.send_message(message.channel, ":sweat_drops: NSFW is currently enabled :sweat_drops:")
                else:
                    await client.send_message(message.channel, ":x: NSFW is not currently enabled :x:")
                commandCalled()
                logCommand(message, client, "~nsfw")

            elif message.content.startswith('~r34 '):
                await postR34(message, client)
                commandCalled()
                logCommand(message, client, message.content)

            elif message.content.startswith("~togglensfw"):
                if message.channel.permissions_for(message.author).manage_channels:
                    await toggleChannel(message, client)
                else:
                    await client.send_message(message.channel, ":x: You do not have permissions to use this command :x:")
                commandCalled()
                logCommand(message, client, "~togglensfw")

            # Markov Chain
            elif message.content.startswith('~comment'):
                await generateMarkovComment(message, client)
                commandCalled()
                logCommand(message, client, message.content)

            elif message.content.startswith('~ryzen'):
                await generateRyzen(message, client)
                commandCalled()
                logCommand(message, client, '~ryzen')

            elif message.content.startswith('~whosaid '):
                await findWhoSaid(message,client)
                commandCalled()
                logCommand(message, client, '~whosaid')


    else:
        if message.content.startswith('~help'):
            await help(message, client)
            commandCalled()
        elif message.author.bot:
            return
        else:
            await client.send_message(message.channel, "Quit trying to slide into my DMs I only do ~help inside of DMs")
