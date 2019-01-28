# Vampire: The Masquarade Diceroller Bot for Discord
Python based diceroller bot for discord.

(add later)

## Use

To activate the bot go to (add later)

The bot will respond to any applicable commands made in the server that @mention it.

* **"roll n"** - Rolls n 10-sided dice. Returns results in a single line mentioning number of successes and each die value. Additional messaging depending on the results of the roll.
* **"one"** - Rolls a single 10-sided die and returns the value to the channel where the command was spoken.

The bot will respond to natural language commands as long as the keyword is present. For example, if you write "Hello @Dicecord can you roll me 4 dice please" it is the same as writing "@Dicecord roll 4".
It figures out the amount to roll based on the following logic where x is a number of dice:
1. Looks for a phrase like "roll x"
2. Takes first number after the @mention
3. Takes first number in message

## Flavour Text
The bot will send flavour text in the case of 0 successes or 4+ successes. This falvour text can be disabled completely if preferred. Here are the commands to change these settings.
* **flavour [on/off]** - Turn flavour text on or off. A confirmation will be sent as a DM.
* **flavour check** - Check your current flavour setting. Details will be sent as a DM.

You can also DM it the following commands to repeat these instructions.
* **"help"** - Replies with help text.  

## Information Saving
Flavour settings are specific to each channel on your server.

In addition, users can opt to delete their stored settings at any time. To do so write **!delete user** in the channel you want to delete information from. There are also commands to delete all players' settings from a channel or server, **!delete channel** or **!delete server**. Please make sure other players are okay with you deleting their settings before using it. If a character does not roll over the course of 30 days their settings will be automatically purged.

## Code Requirements
* Python 3.6+
* `Discord.py` API wrapper and its requirements. Github: [Rapptz](https://github.com/Rapptz/discord.py)
