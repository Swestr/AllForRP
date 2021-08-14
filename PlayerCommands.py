from Util import CharacterUtil, DiscordUtil
from discord_components import Button, ButtonStyle

async def createCharacter(ctx, args, env, mongo):
    if args in mongo.getDistinctCharacters():
        await ctx.channel.send(env.getErrorMessage("characterAlreadyExists"))
        return

    message = ctx.message
    characterName = args
    roleName = env.getConstants("characterRolePrefixe") + characterName
    character = { "_id": characterName, "owner": message.author.mention, "roleName": roleName, "equipments": [], "competences": [], "race": "-", "class": "-", "gender": "-" }

    # Create role, category and textChannels
    characterRole = await DiscordUtil.createRole(ctx.guild, roleName)
    txtChnlCategory = await DiscordUtil.createCategory(ctx.guild, characterName)
    commandsChannel = await DiscordUtil.createTextChannel(ctx.guild, env.getCharacterChannelName("commandsChannel"), txtChnlCategory, env)
    talkWithGameMasterChannel = await DiscordUtil.createTextChannel(ctx.guild, env.getCharacterChannelName("talkWithGameMaster"), txtChnlCategory, env)
    sheetChannel = await DiscordUtil.createTextChannel(ctx.guild, env.getCharacterChannelName("characterSheetChannel"), txtChnlCategory, env)
    statsChannel = await DiscordUtil.createTextChannel(ctx.guild, env.getCharacterChannelName("statsChannel"), txtChnlCategory, env)

    await DiscordUtil.addRoleToTextChannel(talkWithGameMasterChannel, characterRole, True, True)
    await DiscordUtil.addRoleToTextChannel(sheetChannel, characterRole, True, False)
    await DiscordUtil.addRoleToTextChannel(sheetChannel, ctx.guild.default_role, True, False)
    await DiscordUtil.addRoleToTextChannel(commandsChannel, characterRole, True, True)
    await DiscordUtil.addRoleToTextChannel(statsChannel, characterRole, True, False)
    await DiscordUtil.addRoleToMember(message.author, characterRole)
    
    character["roleId"] = str(characterRole.id)
    character["categoryName"] = characterName
    character["commandChannelId"] = str(commandsChannel.id)
    character["talkWithGameMasterChannelId"] = str(talkWithGameMasterChannel.id)
    character["sheetChannelId"] = str(sheetChannel.id)
    character["statsChannelId"] = str(statsChannel.id)

    defaultValues = env.getCharacterSheetNumericFieldsDefaultValues()
    for keyElm in defaultValues:
        key = keyElm["name"]
        character[key] = {}
        character[key]["value"] = keyElm["value"]
        character[key]["hasMax"] = keyElm["hasMax"]
        character[key]["maxValue"] = keyElm["value"]
    
    sheetMessage = await sheetChannel.send("Fiche personnage")
    character["sheetMessageId"] = str(sheetMessage.id)
    

    # Add button into the sheet channel
    characterSheetNumericFields = env.getCharacterSheetNumericFields()
    characterSheetNumericFieldsInterval = env.getCharacterSheetNumericFieldsInterval()
    for keyElm in characterSheetNumericFields:
        key = keyElm["name"]
        if (character[key]["hasMax"]):
            plus, minus = [], []
            for increment in characterSheetNumericFieldsInterval:
                plus.append(Button(style=ButtonStyle.blue, label="+" + str(increment), custom_id="stats:maxValue_" + characterName + "_" + key + "_+" + str(increment)))
                minus.append(Button(style=ButtonStyle.red, label="-" + str(increment), custom_id="stats:maxValue_" + characterName + "_" + key + "_-" + str(increment)))
            statsMessage = await statsChannel.send("Statistiques")
            await statsMessage.edit(type=4, content="...", components=[plus, minus])
            character[key]["maxMessageId"] = str(statsMessage.id)

    for keyElm in characterSheetNumericFields:
        key = keyElm["name"]
        plus, minus = [], []
        for increment in characterSheetNumericFieldsInterval:
            plus.append(Button(style=ButtonStyle.blue, label="+" + str(increment), custom_id="stats:value_" + characterName + "_" + key + "_+" + str(increment)))
            minus.append(Button(style=ButtonStyle.red, label="-" + str(increment), custom_id="stats:value_" + characterName + "_" + key + "_-" + str(increment)))
        statsMessage = await statsChannel.send(content=keyElm["label"] + " : " + str(keyElm["value"]), components=[plus, minus])
        character[key]["valueMessageId"] = str(statsMessage.id)
    
    await CharacterUtil.updateCharacterSheetChannel(ctx.guild, character)

    # Update the mongo document
    mongo.saveCharacter(character)