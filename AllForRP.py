import discord
from discord.ext import commands
from discord_components import DiscordComponents
import AdminCommands, PlayerCommands, AllCommands
from Util import EnvUtil, MongoUtil, DiscordUtil, CharacterUtil, Util

env = EnvUtil.Environment()
env.retrieveEnv()
mongo = MongoUtil.MongoConnection()
cmdPrefix = env.getCommandsPrefix()


bot = commands.Bot(command_prefix=cmdPrefix)
@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Game(name="JDR baby 😉"))


# COMMON COMMANDS
@bot.command(name=env.getGeneralCommonCommand("diceRoll"))
async def roll(ctx, args):
    await AllCommands.rollDice(ctx.message, args, env)


# ADMIN COMMANDS
@bot.command(name=env.getGeneralAdminCommand("reloadSheets"))
async def reloadSheets(ctx):
    return

@bot.command(name=env.getGeneralAdminCommand("clear"))
async def clear(ctx):
    if await DiscordUtil.isAdmin(ctx.message.author, env):
        await AdminCommands.clear(ctx.message, env, mongo)

@bot.command(name=env.getGeneralAdminCommand("setGameMaster"))
async def setGameMaster(ctx):
    if await DiscordUtil.isAdmin(ctx.message.author, env):
        await AdminCommands.setGameMaster(ctx.message, env)

@bot.command(name=env.getGeneralAdminCommand("setAdmin"))
async def setAdmin(ctx):
    if await DiscordUtil.isAdmin(ctx.message.author, env):
        await AdminCommands.setAdmin(ctx.message, env)

@bot.command(name=env.getGeneralAdminCommand("unsetAdmin"))
async def unsetAdmin(ctx):
    if await DiscordUtil.isAdmin(ctx.message.author, env):
        await AdminCommands.unsetAdmin(ctx.message, env)

@bot.command(name=env.getGeneralAdminCommand("setPlayer"))
async def setPlayer(ctx):
    if await DiscordUtil.isAdmin(ctx.message.author, env):
        await AdminCommands.setPlayer(ctx.message, env)

@bot.command(name=env.getGeneralAdminCommand("addDicesChannel"))
async def addDicesChannel(ctx):
    if await DiscordUtil.isAdmin(ctx.message.author, env):
        await AdminCommands.addDicesChannel(ctx.guild, env)


# PLAYER COMMANDS
@bot.command(name=env.getGeneralPlayerCommand("newCharacter"))
async def newCharacter(ctx, args):
    if await DiscordUtil.isPlayer(ctx.message.author, env):
        await PlayerCommands.createCharacter(ctx, args, env, mongo)


# GAME MASTER COMMANDS



@bot.event
async def on_button_click(interaction):
    buttonIdFunction, buttonIdName = interaction.component.custom_id.split(":")
    if (buttonIdFunction.startswith("stats")):
        (maxOrValue, characterId, key, calculation) = buttonIdName.split("_")
        character = mongo.getCharacter(characterId)
        hasMax = character[key]["hasMax"]
        currentValue = character[key][maxOrValue]
        modifiedValue = eval(str(currentValue) + calculation)
        if (hasMax and maxOrValue == "value"):
            maxValue = character[key]["maxValue"]
            if (maxValue < modifiedValue):
                notInRangeError = env.getErrorMessage("ValueNotInRange").format(env.getCharacterSheetNumericField(key)["label"].lower(), maxValue, currentValue, calculation, modifiedValue)
                await interaction.respond(type=4, ephemeral=True, content=notInRangeError)
                return
        character = mongo.updateCharacter(characterId, {key + "." + maxOrValue: modifiedValue})
        await interaction.respond(type=6, content=env.getCharacterSheetNumericField(key)["label"] + " : " + str(modifiedValue))
        
        await CharacterUtil.updateOneCharacterStatisticValue(interaction.guild, character, key, env)
        await CharacterUtil.updateCharacterSheetChannel(interaction.guild, character)


    if (buttonIdFunction.startswith("dices")):
        diceResultChannel = await DiscordUtil.getTextChannel(interaction.guild, env.getServerTextChannel("diceResult"))
        diceResult = Util.getDiceRollResponse(buttonIdName)
        diceResult.sort(key=int)
        diceResultString = "Résultat de " + buttonIdName + " :\t" +  ",\t".join(diceResult)
        await diceResultChannel.send(interaction.author.mention + " " +  diceResultString)
        await interaction.respond(type=4, ephemeral=True, content=diceResultString)


bot.run(env.getToken())