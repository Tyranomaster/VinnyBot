import discord

VINNY_COLOR = int('008cba', 16)
ABOUT_VINNY = "Vinny is an under development discord bot created by Kikkia. Since Vinny is under current development" \
              "Vinny may rarely crash or drop offline for short periods of time as I find/fix bugs and add features. " \
              "Vinny offers a wide set of features for " \
              "any discord server. Including Music, Memes, Comment generation, and Much more. For a full list type " \
              "'~help' in a channel vinny is in. " \
              " Vinny uses the Discord.py " \
              "framework, as well as voice with JDA and lavaplayer For some more detailed statistics run the '~stats' command."

VINNY_SERVER = "Vinny has his own discord server where you can suggest features, report bugs, or just talk with " \
               "other users and developers of vinny. Invite Link: https://discord.gg/XMwyzxZ"

VINNY_INVITE = "To invite Vinny to your server go to: https://discordapp.com/oauth2/authorize?client_id=276855867796881408&scope=bot&permissions=67628096"

async def info(message, client):
    info = discord.Embed(title='Info', colour=VINNY_COLOR)
    info.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    info.add_field(name="About Vinny", value=ABOUT_VINNY)
    info.add_field(name="Vinny Server", value=VINNY_SERVER)
    info.add_field(name="Invite Vinny", value=VINNY_INVITE)
    await message.channel.send(embed=info)

async def invite(message, client):
    await message.channel.send(VINNY_INVITE)





