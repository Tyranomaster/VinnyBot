import discord

async def prune(message, client):
    params = message.content.split(' ')
    phrases = []
    num = None
    for param in params:
        if param.startswith('"'):
            phrases.append(param[1:-1])
        elif param.isdigit():
            num = int(param)

    if num is None:
        await message.channel.send("Please include a number of messages for me to look back through")
        return

    elif num > 500:
        await message.channel.send("I can only go through a max of 500 messages at a time. Please "
                                                   "enter a number 500 or less.")
        return
    elif len(params) == 2:
        try:
            await message.channel.purge(limit=num)
            await message.channel.send("Pruning the last `" + str(num) + "` messages.")
        except Exception as e:
            await message.channel.send(":x: Error pruning channel. :x: \n Error: `" + str(e) + "`")
            print("ERROR Occured on channel: " + message.channel.name + " user: " + message.author.name + str(e))

    elif len(message.mentions) != 0:
        if len(phrases) == 0:
            await pruneUsers(message, client, num)
            return
        else:
            await pruneUserPhrases(message, client, phrases, num)
            return

    elif len(phrases) > 0:
        await prunePhrases(message, client, phrases, num)
        return

    else:
        await message.channel.send("Argument Error: Please make sure you follow proper argument format."
                                             " For example:\n `~prune \"hey!\" @user 50` goes through the last `50`"
                                             " messages and removes all messages from `user` containing `hey!`")
async def kick(message, client):
    try:
        if len(message.mentions) == 0:
            text = "You must @mention a user to kick."
        else:
            text = "Successfully kicked: \n"
            for member in message.mentions:
                await message.guild.kick(member)
                text += "`" + member.name + "`\n"
        await message.channel.send(text)
    except discord.errors.Forbidden:
        await message.channel.send(":x: Error while trying to kick member (My Role may be lower ranked than a person I am trying to kick) :x:")

async def ban(message, client):
    try:
        if len(message.mentions) == 0:
            text = "You must @mention a user to ban."
            await message.channel.send(text)
        else:
            text = "Successfully banned:\n"
            for member in message.mentions:
                await message.guild.ban(member, 0)
                text += "`" + member.name + "`\n"
            await message.channel.send(text)
    except discord.errors.Forbidden:
        await message.channel.send(":x: Error while trying to ban member (My Role may be lower ranked than a person I am trying to ban) :x:")

async def count(message, client):
    counter = 0
    tmp = await message.channel.send('Calculating messages...')
    async for log in message.channel.history(limit=1000):
        if log.author == message.author:
            counter += 1

    await tmp.edit(content=message.author.name + ', you have {} messages.'.format(counter))

async def userInfo(message, client):
    text = ''
    if len(message.mentions) == 0:
        text = "You must @mention a user."
    elif len(message.mentions) > 1:
        text = "You may only @mention one user."
    else:
        user = message.mentions[0]
        text += user.mention + "\n"
        text += "avatar url: " + user.avatar_url + "\n"
        text += "username: " + user.name + "\n"
        text += "joined: " + str(user.joined_at) + "\n"
    await message.channel.send(text)

async def roleInfo(message, client):
    for role in message.role_mentions:
        text = discord.Embed(title=role.name, colour=role.colour)
        if len(role.members) > 0:
            for member in role.members:
                memberInfo = ""
                if member.nick is not None:
                    memberInfo += "Nickname: " + member.nick + "\n"
                memberInfo += "Status: " + member.status.value + "\n"
                if member.status.value == "online" and member.game is not None:
                    memberInfo += "In game: " + member.game.name + "\n"
                text.add_field(name=member.name, value=memberInfo, inline=False)
        else:
            text.add_field(name="Nobody...", value=":cry:")
        await message.channel.send(embed=text)

async def avatar(message, client):
    if len(message.mentions) == 0:
        text = "You must @mention a user."
    elif len(message.mentions) > 1:
        text = "You may only @mention one user."
    else:
        text = message.mentions[0].mention + " " + message.mentions[0].avatar_url
    await message.channel.send(text)

async def pruneUsers(message, client, num):
    delcount = 0
    async for log in message.channel.history(limit=num):
        if log.author in message.mentions:
            await log.delete()
            delcount += 1

    msg = "Removed `"+ str(delcount) +"` messages from the last `" + str(num) + "` messages from users: \n`"
    for member in message.mentions:
        msg += member.name + "\n"

    msg += "`"

    await message.channel.send(msg)


async def prunePhrases(message, client, phrases, num):
    delcount = 0
    async for log in message.channel.history(limit=num):
        for phrase in phrases:
            if phrase in log.content:
                await log.delete()
                delcount += 1

    msg = "Removed `" + str(delcount) + "` messages from the last `" + str(num) + "` messages containing one of the " \
                                                                               "following substrings: \n`"

    for phrase in phrases:
        msg += phrase + "\n"

    msg += "`"

    await message.channel.send(msg)

async def pruneUserPhrases(message, client, phrases, num):
    delcount = 0
    async for log in message.channel.history(limit=num):
        for phrase in phrases:
            if phrase in log.content:
                if log.author in message.mentions:
                    await log.delete()
                    delcount += 1

    msg = "Removed `"+ str(delcount) +"` messages in the last `" + str(num) + "` messages from users: \n`"
    for member in message.mentions:
        msg += member.name + "\n"

    msg += "`\ncontaining one of the following substrings: \n`"

    for phrase in phrases:
        msg += phrase + "\n"

    msg += "`"

    await message.channel.send(msg)
