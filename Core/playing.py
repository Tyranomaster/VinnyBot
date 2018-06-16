import discord
import operator
import time
from random import randint

async def games(message, client):
    server = message.guild
    members = server.members
    gamelist = []
    for member in members:
        if member.game is not None and not member.bot:
            gamelist.append(member.game.name)
    if not gamelist:  # if list is empty
        await message.channel.send(":x: No one appears to be playing anything... :thinking:")
        return
    # Creates dictionary where word is the game and definition is # of people playing
    countedgames = {i: gamelist.count(i) for i in gamelist}
    # Sorts dict by # of people playing
    sortedgames = sorted(countedgames.items(), key=operator.itemgetter(1))
    finalstring = "Games being played by members now: \n"
    for (game, players) in sortedgames:
        finalstring += game + ": " + str(players) + "\n"
    await message.channel.send(finalstring)


async def battle(message, client):
    # Get the people that are fighting & initial error finding
    mentioned = message.mentions
    if len(mentioned) > 2 or len(mentioned) is 0:
        await message.channel.send(":x:Please mention only 1 or 2 members:x:")
        return
    if len(mentioned) is 2:
        user1 = mentioned[0]
        user2 = mentioned[1]
    else:
        user1 = message.author
        user2 = mentioned[0]
    if user1 is user2:  # If user mentions themself or the same person twice
        await message.channel.send("You'll have to fight your inner demons on your own...")
        return

    # Solve if user has a server nickname or not
    user1_name = user1.nick
    if user1_name is None:
        user1_name = user1.name
    user2_name = user2.nick
    if user2_name is None:
        user2_name = user2.name
    if user1_name == user2_name:  # If users have the same nickname on the server
        user1_name += "(1)"
        user2_name += "(2)"
    await message.channel.send(user1_name + " and " + user2_name + " are battling!")

    # players are given weapons randomly
    weapons = ["dagger :dagger:", "bow :bow_and_arrow:", "sword :crossed_swords:", "wits :thinking:"]
    user1_weapon = weapons[randint(0, 3)]
    user2_weapon = weapons[randint(0, 3)]
    await message.channel.send(user1_name + " wields their " + user1_weapon + ", while " + user2_name +
                               " takes in their trusty " + user2_weapon + ".")

    # initialize health and starting attacker (random)
    attacker_health = 100
    defender_health = 100
    if randint(0, 1) is 0:
        attacker = user1
        attacker_name = user1_name
        defender = user2
        defender_name = user2_name
    else:
        attacker = user2
        attacker_name = user2_name
        defender = user1
        defender_name = user1_name

    # Someday the great spaghetti code monster will be summoned and reap all our lives, And I will be a bit at fault.
    flipthis = False  # To keep users' HP on the same side each time

    # battle loop
    while attacker_health > 0 and defender_health > 0:
        time.sleep(2)  # Damn humans need time to read
        roll = randint(1, 20)
        battlerecord = ""
        if roll is 1:
            attacker_health -= 10
            if attacker_health < 0:
                attacker_health = 0
            battlerecord += "Critical fail! " + attacker_name + " hurts themself for 10!"

        elif roll is 20:
            defender_health -= 40
            if defender_health < 0:
                defender_health = 0
            battlerecord += "Critical hit! " + attacker_name + " hits " + defender_name + " for 40!"

        else:
            hit = roll + 10
            defender_health -= hit
            if defender_health < 0:
                defender_health = 0
            battlerecord += attacker_name + " strikes " + defender_name + " for " + str(hit)

        if flipthis:
            battlerecord += "\n" + defender_name + ": " + str(defender_health) + " | " + \
                            attacker_name + ": " + str(attacker_health)
        else:
            battlerecord += "\n" + attacker_name + ": " + str(attacker_health) + " | " + \
                            defender_name + ": " + str(defender_health)
        await message.channel.send(battlerecord)

        # Switch attacker <-> defender
        temp = attacker
        attacker = defender
        defender = temp

        temp = attacker_name
        attacker_name = defender_name
        defender_name = temp

        # Switch health to match player
        temp = attacker_health
        attacker_health = defender_health
        defender_health = temp

        flipthis = not flipthis

    # Announce winner
    if defender_health < 1:
        loser_name = defender_name
        winner_name = attacker_name
    else:
        loser_name = attacker_name
        winner_name = defender_name
    await message.channel.send(winner_name + " defeated " + loser_name + "!")
