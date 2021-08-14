# CATEGORIES FUNCTIONS

async def createCategory(guild, categoryName):
    return await guild.create_category(categoryName)
    
# ROLES FUNCTIONS
async def createRole(guild, roleName):
    return await guild.create_role(name=roleName)

async def getRole(guild, roleName):
    return [role for role in guild.roles if role.name == roleName][0];

async def hasRole(member, role_name):
    role_names = [role.name for role in member.roles]
    return role_name in role_names

async def addRoleByNameToMember(guild, member, roleName):
    await member.add_roles(await getRole(guild, roleName))

async def removeRoleByNameToMember(guild, member, roleName):
    await member.remove_roles(await getRole(guild, roleName))

async def addRoleToMember(member, role):
    await member.add_roles(role)

async def isAdmin(member, env):
    return await hasRole(member, env.getServerRole("admin"))

async def isGameMaster(member, env):
    return await hasRole(member, env.getServerRole("gameMaster"))

async def isPlayer(member, env):
    return await hasRole(member, env.getServerRole("player"))

async def addRoleToTextChannel(textChannel, role, read, send):
    await textChannel.set_permissions(role, read_messages=read, send_messages=send)




# TEXT CHANNEL FUNCTIONS
async def createTextChannel(guild, textChannelName, category, env):
    textChannel = await guild.create_text_channel(textChannelName, category=category)
    await addRoleToTextChannel(textChannel, await getRole(guild, env.getServerRole("gameMaster")), True, True)
    await addRoleToTextChannel(textChannel, await getRole(guild, env.getServerRole("admin")), True, True)
    await addRoleToTextChannel(textChannel, await getRole(guild, env.getServerRole("bot")), True, True)
    await addRoleToTextChannel(textChannel, guild.default_role, False, False)
    return textChannel
    # the game master must have permission to write and send for each channel

async def getTextChannel(guild, textChannelName):
    channels = await guild.fetch_channels()
    return [channel for channel in channels if channel.name == textChannelName][0];

# MEMBER FUNCTIONS
async def getMemberFromMention(guild, mention):
    return await guild.fetch_member(mention[3:-1])

async def getMessage(guild, channelId, messageId):
    characterSheetChannel = guild.get_channel(int(channelId))
    characterMessages = await characterSheetChannel.fetch_message(int(messageId))
    return characterMessages