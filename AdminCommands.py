from Util import DiscordUtil, Util
from discord_components import Button, ButtonStyle

async def clear(message, env, mongo):
    for voiceChannel in message.guild.voice_channels:
        await voiceChannel.delete()
    for txtChannel in message.guild.text_channels: 
        if txtChannel.name not in Util.getDoNotDeleteTextChannels(env):
            await txtChannel.delete()
    for category in message.guild.categories:
        if category.name not in Util.getDoNotDeleteCategories(env):
            await category.delete()
    for role in message.guild.roles:
        if role.name not in Util.getDoNotDeleteRoles(env):
            await role.delete()
    mongo.removeAllCharacters()

async def setGameMaster(message, env):
    gameMasterRoleName = env.getServerRole("gameMaster")
    gameMasterMember = await DiscordUtil.getMemberFromMention(message.guild, Util.getArguments(message.content)[0])
    await DiscordUtil.addRoleByNameToMember(message.guild, gameMasterMember, gameMasterRoleName)

async def setAdmin(message, env):
    adminName = env.getServerRole("admin")
    adminMember = await DiscordUtil.getMemberFromMention(message.guild, Util.getArguments(message.content)[0])
    await DiscordUtil.addRoleByNameToMember(message.guild, adminMember, adminName)

async def unsetAdmin(message, env):
    adminName = env.getServerRole("admin")
    adminMember = await DiscordUtil.getMemberFromMention(message.guild, Util.getArguments(message.content)[0])
    await DiscordUtil.removeRoleByNameToMember(message.guild, adminMember, adminName)

async def setPlayer(message, env):
    adminName = env.getServerRole("player")
    adminMember = await DiscordUtil.getMemberFromMention(message.guild, Util.getArguments(message.content)[0])
    await DiscordUtil.addRoleByNameToMember(message.guild, adminMember, adminName)

async def addDicesChannel(guild, env):
    category =  await DiscordUtil.createCategory(guild, env.getServerCategory("dices"))
    diceButtonsChannel = await  DiscordUtil.createTextChannel(guild, env.getServerTextChannel("dices"), category, env)
    diceResult = await  DiscordUtil.createTextChannel(guild, env.getServerTextChannel("diceResult"), category, env)
    await DiscordUtil.addRoleToTextChannel(diceButtonsChannel,  await DiscordUtil.getRole(guild, env.getServerRole("gameMaster")), True, False)
    await DiscordUtil.addRoleToTextChannel(diceButtonsChannel,  await DiscordUtil.getRole(guild, env.getServerRole("player")), True, False)
    await DiscordUtil.addRoleToTextChannel(diceResult,  await DiscordUtil.getRole(guild, env.getServerRole("gameMaster")), True, False)
    await DiscordUtil.addRoleToTextChannel(diceResult, await  DiscordUtil.getRole(guild, env.getServerRole("player")), True, False)
    (diceIntervals, diceValues) = env.getDiceButtonsDefinition()
    for diceValue in diceValues:
        buttons = []
        value = "D" + str(diceValue)
        for diceInterval in diceIntervals:
            buttons.append(Button(style=ButtonStyle.green, label=str(diceInterval) + value, custom_id="dices:" + str(diceInterval) + value))
        message = await diceButtonsChannel.send("Dés")
        await message.edit(type=4, content=value, components=[buttons])