from Reddit import *
from help import *
from Moderation import *
from Giphy import *
from Memes import *
from Markov import *
from Stats import *
from nsfw import *
from Logger import *
from Config import *
from playing import *

import sys


async def parseCommand(message, client):
    try:
        if not message.channel.position:
            if not message.channel.permissions_for(message.guild.me).send_messages:
                return
    except AttributeError:
        return
        #Find which command has been given
    if message.content.startswith('~'):
        if message.author.bot:
            return

        elif message.content.startswith('~help'):
            await sendhelp(message, client)
            logCommand(message, client, '~help')

        elif message.content.startswith('~info'):
            await info(message, client)
            logCommand(message, client, '~info')

        elif message.content.startswith('~invite'):
            await invite(message, client)
            logCommand(message, client, '~invite')

        elif message.content.startswith('~stats'):
            await getStats(message, client)
            logCommand(message, client, '~stats')

        elif message.content.startswith('~permission'):
            logCommand(message, client, '~permission')
            if message.channel.permissions_for(message.guild.me).read_messages:
                await message.channel.send("I have permission")
            else:
                await message.channel.send("I do not have permission")

        elif message.content.startswith('~prune'):
            if message.channel.permissions_for(message.guild.me).manage_messages:
                if message.channel.permissions_for(message.author).manage_messages:
                    await prune(message, client)
                else:
                    await message.channel.send(":x: You do not have permissions to use this command :x:")
            else:
                await message.channel.send(":x: I don't have permissions to delete messages here. :x:")
            logCommand(message, client, '~prune')
            # await prune(message, client)

        elif message.content.startswith('~kick'):
            if message.channel.permissions_for(message.guild.me).kick_members:
                if message.channel.permissions_for(message.author).kick_members:
                    await kick(message, client)
                else:
                    await message.channel.send(":x: You do not have permissions to use this command :x:")
            else:
                await message.channel.send(":x: I don't have permissions to kick members here. :x:")
            logCommand(message, client, '~kick')
            # await kick(message, client)

        elif message.content.startswith('~ban'):
            if message.channel.permissions_for(message.guild.me).ban_members:
                if message.channel.permissions_for(message.author).ban_members:
                    await ban(message, client)
                else:
                    await message.channel.send(":x: You do not have permissions to use this command :x:")
            else:
                await message.channel.send(":x: I don't have permissions to ban members here. :x:")

            logCommand(message, client, '~ban')

        # Voice Commands (Currently removed and moved to Vinny's new JDA module)
        elif message.content.startswith('~summon'):
            await message.channel.send("Summon command no longer used. Just use the play command "
                                                       "to summon Vinny.")
            logCommand(message, client, '~summon')

        elif message.content.startswith('~playlist'):
            logCommand(message, client, '~playlist')

        elif message.content.startswith('~skip'):
            logCommand(message, client, '~skip')

        elif message.content.startswith("~volume "):
            logCommand(message, client, '~volume (val)')

        elif message.content.startswith("~volume"):
            logCommand(message, client, '~volume')

        elif message.content.startswith('~play'):
            logCommand(message, client, '~play')

        elif message.content.startswith('~pause'):
            logCommand(message, client, '~pause')

        elif message.content.startswith('~resume'):
            logCommand(message, client, '~resume')

        elif message.content.startswith('~stop'):
            logCommand(message, client, '~stop')

        elif message.content.startswith('~voicestats'):
            logCommand(message, client, '~voicestats')

        elif message.content.startswith('~search'):
            logCommand(message, client, message.content)

        elif message.content.startswith('~leave'):
            logCommand(message, client, '~leave')

        elif message.content.startswith('~volume'):
            logCommand(message, client, '~volume')

        elif message.content.startswith('~cancel'):
            logCommand(message, client, '~cancel')

        # Meme Commands
        elif message.content.startswith('~ayy'):
            await ayy(message, client)
            logCommand(message, client, '~ayy')

        elif message.content.startswith('~kappa'):
            await kappa(message, client)
            logCommand(message, client, '~kappa')

        elif message.content.startswith('~hammer'):
            await banHammer(message, client)
            logCommand(message, client, '~hammer')

        elif message.content.startswith('~doggo'):
            await doggo(message, client)
            logCommand(message, client, '~doggo')

        elif message.content.startswith('~lenny'):
            await lenny(message, client)
            logCommand(message, client, '~lenny')

        elif message.content.startswith('~hitler'):
            await hitler(message, client)
            logCommand(message, client, '~hitler')

        elif message.content.startswith('~mario'):
            await mario(message, client)
            logCommand(message, client, '~mario')

        elif message.content.startswith('~megaman'):
            await megaMan(message, client)
            logCommand(message, client, '~megaman')

        elif message.content.startswith('~salt'):
            await salt(message, client)
            logCommand(message, client, '~salt')

        elif message.content.startswith('~pikachu'):
            await pikachu(message, client)
            logCommand(message, client, '~pikachu')

        elif message.content.startswith('~feels'):
            await feels(message, client)
            logCommand(message, client, '~feels')

        elif message.content.startswith('~ascii'):
            await ascii(message, client)
            logCommand(message, client, '~ascii')

        elif message.content.startswith('~harambe'):
            await harambe(message, client)
            logCommand(message, client, '~harambe')

        elif message.content.startswith('~giphy'):
            await giphy(message, client)
            logCommand(message, client, '~giphy')

        elif message.content.startswith('~8ball'):
            await magic8ball(message, client)
            logCommand(message, client, "8ball")

        elif message.content.startswith('~praise'):
            await message.channel.send('https://media.giphy.com/media/fr42tarocsK6Q/giphy.gif')
            logCommand(message, client, '~praise')

        elif message.content.startswith('~whois'):
            await userInfo(message, client)
            logCommand(message, client, '~whois')

        elif message.content.startswith('~whohas'):
            await roleInfo(message, client)
            logCommand(message, client, '~whohas')

        elif message.content.startswith('~roll'):
            await roll(message, client)
            logCommand(message, client, '~roll')

        # Reddit Commands
        elif message.content.startswith('~shit'):
            with message.channel.typing():
                await message.channel.send(random_hot_post('shitpost', 20, message))
                logCommand(message, client, '~shit')

        elif message.content.startswith('~rr'):
            with message.channel.typing():
                try:
                    subreddit = message.content.split(' ')[1]
                except IndexError:
                    await message.channel.send("No subreddit mentioned, please enter a subreddit")
                    return
                post = random_hot_post(subreddit, 20, message)
                if post is not None:
                    await message.channel.send(post)
                else:
                    await message.channel.send("There was an error retrieving a post")

                logCommand(message, client, message.content)

        elif message.content.startswith('~tr'):
            with message.channel.typing():
                try:
                    subreddit = message.content.split(' ')[1]
                except IndexError:
                    await message.channel.send("No subreddit mentioned, please enter a subreddit")
                    return
                try:
                    await message.channel.send(random_top_post(subreddit, message, 75))
                except:
                    await message.channel.send("Oops. There was an error retriving a post :confounded:")
                    print('Error with Top reddit command: ' + sys.exc_info()[0] + '\n')
                logCommand(message, client, message.content)

        elif message.content.startswith('~cosplaygirls'):
            with message.channel.typing():
                await message.channel.send(getCosplayGirl(message, client))
                logCommand(message, client, '~cosplaygirls')

        elif message.content.startswith('~cosplay'):
            with message.channel.typing():
                await message.channel.send(getCosplay(message, client))
                logCommand(message, client, message.content)

        #Nsfw Commands TODO: Add permissions and nsfw lock
        elif message.content.startswith('~nsfw'):
            if isEnabled(message):
                await message.channel.send(":sweat_drops: NSFW is currently enabled :sweat_drops:")
            else:
                await message.channel.send(":x: NSFW is not currently enabled :x:")
            logCommand(message, client, "~nsfw")

        elif message.content.startswith('~r34 '):
            await postR34(message, client)
            logCommand(message, client, message.content)

        # elif message.content.startswith('~pixiv '):
        #    await pixivSearch(message, client)

        elif message.content.startswith("~togglensfw"):
            if message.channel.permissions_for(message.author).manage_channels:
                await toggleChannel(message, client)
            else:
                await message.channel.send(":x: You do not have permissions to use this command :x:")
            logCommand(message, client, "~togglensfw")

        # Markov Chain
        elif message.content.startswith('~comment'):
            await generateMarkovComment(message, client)
            logCommand(message, client, message.content)

        elif message.content.startswith('~ryzen'):
            await generateRyzen(message, client)
            logCommand(message, client, '~ryzen')

        elif message.content.startswith('~games'):
            await games(message, client)
            logCommand(message, client, '~games')

        elif message.content.startswith('~battleroyale'):
            await battle_royale(message, client)
            logCommand(message, client, '~battleroyale')

        elif message.content.startswith('~battle'):
            await battle(message, client)
            logCommand(message, client, '~battle')


    # else:
    #     if message.content.startswith('~help'):
    #         await help(message, client)
    #         commandCalled()
    #     elif message.author.bot:
    #         return
    #     else:
    #         await message.channel.send("Quit trying to slide into my DMs I only do ~help inside of DMs")
