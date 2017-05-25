import os
import discord


tokens = {}
commands = {}
VINNY_COLOR = int('008cba', 16)


def initConfig():
    if not os.path.exists("config"):
        print("Config folder not present. Aborting")
        return None

    with open("config/tokens.txt", "r") as f:
        #Make translation map for removing new lines and *
        map = str.maketrans('', '', '*\n')
        for line in f:
            if line.startswith('***'):
                line = line.translate(map)
                tokens[line] = next(f).translate(map)

    with open("config/commands.txt", "r") as f:
        map = str.maketrans('', '', '*\n')
        for line in f:
            if line.startswith("***"):
                name = line.split(' ')[0].lower().translate(map)
                commands[name] = {}
                continue
            if name is not None:
                if line != "\n":
                    command = line.split(' ')[0].replace('~', '')
                    commands[name][command] = line

async def help(message, client):
    if len(message.content.split(" ")) > 1:
        for i in range(1, len(message.content.split(" "))):
            lookFor = message.content.split(" ")[i]
            await client.send_message(message.author, lookFor + ": " + getCommand(lookFor))
    else:
        await client.send_message(message.author, embed=defaultHelp(client))


def getCommand(command):
    for key, value in commands.items():
        try:
            if value[command] is not None:
                return value[command]
        except KeyError:
            continue

    return "Command not found"


def defaultHelp(client):
    embed = discord.Embed(title='Command List', colour=VINNY_COLOR)
    embed.add_field(name="Note", value="In all commands with *search_terms* replace it with what you want to search."
                                       "For a tag that is multiple words use _ instead of spaces.", inline=False)
    for key, value in commands.items():
        list = ""
        for command, desc in value.items():
            list += desc
        embed.add_field(name=key.upper() + " COMMANDS",
                        value=list,
                        inline=False)

    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    return embed

def getToken(tokenName):
    return tokens[tokenName]
