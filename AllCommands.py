from Util import Util

async def rollDice(message, args, env):
    if (Util.checkRollDef(args)):
        diceRoll = Util.getDiceRollResponse(args)
        await message.channel.send(", ".join(diceRoll))
    else:
        await message.channel.send(env.getErrorMessage("commandError"))
