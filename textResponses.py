typetext = '''**roll**: a normal roll

1. Looks for a phrase like "roll x"
2. Looks for a phrase like "9again/8again/noagain x"
3. Takes first number after the @mention
4. Takes first number in message
'''

helptext = '''**Commands must now include an @mention for the bot**
To make a roll type **@Dicecord-VtM roll *n*** where *n* is the number of dice you want to roll.

**Example:**
@Dicecord-VtM roll 8
Rolls 8 dice.

The bot can use simple natural language processing for rolling dice. For example, '

1. Looks for a phrase like "roll x"
2. Looks for a phrase like "9again/8again/noagain x"
3. Takes first number after the @mention
4. Takes first number in message

Regardless of mode, by default the bot will send flavour text if you get 0 successes or 5+ successes.
You can specify splat specific flavour text, for example you could set it so a Mage character gets Mage themed flavour text.
For more info, write **flavourhelp** to me here.

Type **info** to me here to general bot information.'''

flavText = '''To specify a splat write **@Dicecord splat *splat name***. For example: **@Dicecord splat mage** for Mage.
You can turn flavour text off by writing **@Dicecord flavour off** in the channel. You can turn it back on with **@Dicecord flavour on**.
The bot will remember these settings. To check at any time write **@Dicecord flavour check** or **@Dicecord splat check**.
Settings are channel based, not server based. For example, you can set your splat to Mage in #Mage channel, but other channels on that server will have default settings.
To delete these settings for your character, write **@Dicecord delete user** in the channel you want deleted.
You can also use **@Dicecord delete channel** and *@Dicecord server* to delete all players' settings in a specific channel or server, but please make sure other players are okay with you performing these actions!'''

aboutText = '''Dicecord is a python based bot for rolling dice following the Chronicles of Darkness ruleset.
(c) Roy Healy. Distributed under GNU General Public License v3.0.
Built using Discord.py package and running on Python 3.6.
See https://github.com/further-reading/discord-dirceroller-bot for source code.
Join us on Discord https://discordapp.com/invite/DRM9MT8'''