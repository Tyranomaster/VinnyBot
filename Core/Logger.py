import os
import time
from datadog import statsd


def logCommand(message, client, command):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(time.strftime("logs/VinnyLog %m-%d-%Y.txt"), "a+") as f:
        f.write(time.strftime("[%H:%M:%S] ") + command + " called by: " + message.author.name + " in channel: " +
                message.channel.name + " in guild: " + message.guild.name + "\n")

    statsd.increment('vinny.commandCalled')
    statsd.increment('vinny.' + command.split(' ')[0])
    if command.split(' ')[0] is "r34":
        statsd.increment('vinny.r34.' + command.split(' ')[0])
