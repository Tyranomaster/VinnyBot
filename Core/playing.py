import discord
import operator
import time
import random
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


async def battle_royale(message, client, verbose):
    # get candidates from mention/role/guild list
    candidates = await get_player_list(message)
    # get fighters from candidates
    fighters = await populate_roster(candidates)

    # Weed out any fringe cases
    if len(fighters) < 3:
        await message.channel.send(":x:It's not a battle royal if you don't have at least 3 fighters:x:")
        return

    await enact_battle(message, fighters, verbose)
    # TODO - alphabatize fighters by name

    """
    if randint(1,20) is 1:
        damage = randint(1, 10)
        fighters[attacker]["hp"] -= damage
        battlerecord += "{:{x}} hits {:{y}} for {:>2}".format(fighters[attacker]["name"], "themself", str(damage), x=name_len, y=name_len)
        if fighters[attacker]["hp"] < 1:
            battlerecord += "\tCritical fail! " + fighters[attacker]["name"] + ", seeing no more opponents before them, decides to end it all.\n"
            fighters.pop(attacker, None)
        else:
            battlerecord += "\tCritical fail! " + fighters[attacker]["name"] + ", seeing no more opponents before them, attemps to end it all, but fails.\n"

    # roll to hit
    roll = randint(1, 20)
    # Hit self for 1-10 on fail
    if roll is 1:
        damage = randint(1, 10)
        fighters[attacker]["hp"] -= damage
        battlerecord += "{:{x}} hits {:{y}} for {:>2}".format(fighters[attacker]["name"], "themself", str(damage), x=name_len, y=name_len)
        if fighters[attacker]["hp"] < 1:
            battlerecord += "\tCritical fail! " + fighters[attacker]["name"] + " kills themself out of shame.\n"
        else:
            battlerecord += "\tCritical fail!\n"
    # Deal 1-10 extra damage on critical
    elif roll is 20:
        damage = roll + 10 + randint(1, 10)
        fighters[defender]["hp"] -= damage
        battlerecord += "{:{x}} hits {:{y}} for {:>2}".format(fighters[attacker]["name"], fighters[defender]["name"], str(damage), x=name_len, y=name_len)
        if fighters[defender]["hp"] < 1:
            battlerecord += "\tCritical hit! " + fighters[attacker]["name"] + " fucking murders " + fighters[defender]["name"] + "!\n"
        else:
            battlerecord += "\tCritical hit!\n"
    # Deal 12-29 on hit
    else:
        damage = roll + 10
        fighters[defender]["hp"] -= damage
        battlerecord += "{:{x}} hits {:{y}} for {:>2}".format(fighters[attacker]["name"], fighters[defender]["name"], str(damage), x=name_len, y=name_len)
        if fighters[defender]["hp"] < 1:
            battlerecord += "\t" + fighters[attacker]["name"] + " kills " + fighters[defender]["name"] + "!\n"
        else:
            battlerecord += "\n"
    """
    if len(fighters) is 0:
        await message.channel.send("```\nLoser, loser, chicken loser.\n```")
    else:
        victor = fighters[random.choice(list(fighters))]["name"]
        await message.channel.send("```\nBehold your champion, {} of {}!\n```".format(victor, message.guild.name))




async def role_mentioned(message):
    if len(message.content.split(" ")) > 1:
        find_role = message.content.split(" ")[1]
        for role in message.guild.roles:
            if role.mention == find_role:
                return role
    return None


async def get_player_list(message):
    candidates = list()
    # Get contestant list
    # if there are mentions, use them. Otherwise, use all guild members
    role = await role_mentioned(message)
    # add users by mention if here are mentions
    if len(message.mentions) > 0:
        candidates = message.mentions
    # add users by role if a role was mentioned
    elif role is not None:
        for applicant in message.guild.members:
            if role in applicant.roles:
                candidates.append(applicant)
    # add all users
    else:
        candidates = message.guild.members
    return candidates


async def populate_roster(candidates):
    # add eligible candidates to the fighters list
    fighters = {}
    for index, candidate in enumerate(candidates):
        # filter out bots
        if candidate.bot:
            continue
        name = candidate.nick
        if name is None:
            name = candidate.name
        # Each player has a dictionary with hp, name, and revenge key
        fighters[str(index)] = {}
        fighters[str(index)]["name"] = name
        fighters[str(index)]["hp"] = 100
        fighters[str(index)]["revenge"] = None
    return fighters


async def preform_attack(fighters, attacker, defender, verbose):
    # Person to take the damage, defender unless there is a critical fail
    target = defender
    # Was this a critical hit?
    critical = True
    # Roll to hit
    roll = randint(1, 20)
    # Damage total
    damage = randint(1, 10) + roll
    # Critical fail, hit self
    if roll is 1:
        target = attacker
    elif roll is 20:
        damage += 10
    else:
        critical = False
    # TODO - uncomment for testing
    # If there are no other defenders, and the attacker didn't hit themself
    if target is None:
        return ""
    # Target takes damage
    fighters[target]["hp"] -= damage
    battle_report = ""
    if verbose:
        battle_report += ""
        # TODO - do verbose things
    if fighters[target]["hp"] < 1:
        if target is attacker:
            battle_report += "{} kills themself out of shame.\n".format(fighters[attacker]["name"])
        elif critical:
            battle_report += "{} fucking murders {}!\n".format(fighters[attacker]["name"], fighters[defender]["name"])
        else:
            battle_report += "{} kills {}!\n".format(fighters[attacker]["name"], fighters[defender]["name"])
        # Remove the dead candidate form the roster
        fighters.pop(target, None)
    else:
        # Defender will attempt revenge
        fighters[defender]["revenge"] = attacker
    return battle_report


async def enact_round(message, fighters, round_count, verbose):
    # Text record of what happens during each round
    battle_report = ""
    # Shuffle the fighter attack order
    shuffled_fighters = list(fighters.keys())
    random.shuffle(shuffled_fighters)
    for attacker in shuffled_fighters:
        # if attacker is dead
        if fighters.get(attacker) is None:
            continue
        # Select defender
        defender = None
        # if there is a potential for revenge, 50% chance of hitting them
        if fighters[attacker]["revenge"] is not None and fighters.get(fighters[attacker]["revenge"]) is not None and randint(0,1) is 1:
            defender = fighters[attacker]["revenge"]
        # if there is no one left to hit, check for suicide
        elif len(fighters) is 1:
            # TODO - commit sepakku
            print("")  # TODO - remove once this is done
        # Otherwise, choose a random opponent
        else:
            while defender is attacker or defender is None:
                defender = random.choice(list(fighters))
        #
        battle_report += await preform_attack(fighters, attacker, defender, verbose)
    return battle_report


async def enact_battle(message, fighters, verbose):
    round_count = 0
    # As long as there is more than 1 fighter, do another round.
    while len(fighters) > 1:
        name_len = 0
        for fighter in fighters:
            if len(fighters[fighter]["name"]) > name_len:
                name_len = len(fighters[fighter]["name"])
        # TODO - change where the delay takes place
        if round_count is not 0:
            time.sleep(1.5)
        battle_report = await enact_round(message, fighters, round_count, verbose)
        # TODO - comment below here
        line_by_line = battle_report.split("\n")
        round_count += 1
        output = "```\n\tRound  {}:\tCombatants: {}\n".format(round_count, len(fighters))
        if len(line_by_line) is 1 and len(line_by_line[0]) is 0:
            output += "No fatalities.\n"
        for line in line_by_line:
            if len(output) + len(line) < 1900:
                output += line + "\n"
            else:
                output += "```"
                await message.channel.send(output)
                output = "```\n" + line + "\n"
        output += "```"
        await message.channel.send(output)

