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
        transMap = str.maketrans('', '', '*\n')
        for line in f:
            if line.startswith('***'):
                line = line.translate(transMap)
                tokens[line] = next(f).translate(transMap)

    with open("config/commands.txt", "r") as f:
        transMap = str.maketrans('', '', '*\n')
        for line in f:
            if line.startswith("***"):
                name = line.split(' ')[0].lower().translate(transMap)
                commands[name] = {}
                continue
            if name is not None:
                if line != "\n":
                    command = line.split(' ')[0].replace('~', '')
                    commands[name][command] = line

async def sendhelp(message, client):
    try:
        if len(message.content.split(" ")) > 1:
            for i in range(1, len(message.content.split(" "))):
                lookFor = message.content.split(" ")[i]
                await message.author.send(lookFor + ": " + getCommand(lookFor))
        else:
            await message.author.send("For more help or to give feedback join Vinny's discord server at:"
                                      " https://discord.gg/XMwyzxZ", embed=defaultHelp(client))
    except:
        await message.channel.send("Error sending the message to your DMs. Posting help in channel.")
        await message.channel.send("For more help or to give feedback join Vinny's discord server at:"
                                  " https://discord.gg/XMwyzxZ", embed=defaultHelp(client))


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
        commandList = ""
        for command, desc in value.items():
            commandList += desc
        embed.add_field(name=key.upper() + " COMMANDS",
                        value=commandList,
                        inline=False)

    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    return embed

def getToken(tokenName):
    return tokens[tokenName]
