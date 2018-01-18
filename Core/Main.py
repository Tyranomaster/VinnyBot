from Config import getToken
from Config import initConfig
from Parser import *
from nsfw import initNsfw
from Reddit import initReddit


initConfig()
Token = getToken('Discord')
client = discord.AutoShardedClient()


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')
    await client.change_presence(game=discord.Game(name='~help for command list'))
    with open('res/vinny.jpg', 'rb') as fp:
        await client.user.edit(avatar=fp.read())
    initNsfw()
    initReddit()
    sendStatistics(client)



@client.event
async def on_message(message):
        if message.content.startswith('~'):
            await parseCommand(message, client)

        else:
            return


client.run(Token)
