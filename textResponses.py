rolltext = '''Dicecord-VtM is able to respond to natural langauge commands for rolls.
For example, both '@Dicecord-VtM roll 8' and 'Hello @Dicecord-VtM roll a set of 8 dice' will roll 8 dice.
It will figure out the command based on the following priority:

1. Look for a phrase like "roll x"
2. Take first number after the @mention
3. Take first number in message
'''

helptext = '''**Commands must now include an @mention for the bot**
To make a roll use **@Dicecord-VtM roll *n*** where *n* is the number of dice you want to roll.

**Example:**
@Dicecord-VtM roll 8
Rolls 8 dice.

The bot can use simple natural language processing for rolling dice. For more info, reply with **roll** here.

By default the bot will send flavour text if you get 0 successes or 4+ successes.
For more info, reply with **flavour** here.

Type **info** to me here to general bot information.'''

flavText = '''Depending on your flavour setting the bot may add a quip to your rolls in certain situations.
You can turn flavour text off by writing **@Dicecord-VtM flavour off** in the channel. You can turn it back on with **@Dicecord-VtM flavour on**.
The bot will remember these settings. To check at any time write **@Dicecord-VtM flavour check**.
Settings are channel based, not server based.
To delete these settings for your character, write **@Dicecord-VtM delete user** in the channel you want deleted.
You can also use **@Dicecord-VtM delete channel** and *@Dicecord-VtM delete server* to delete all players' settings in a specific channel or server, but please make sure other players are okay with you performing these actions!'''

aboutText = '''Dicecord is a python based bot for rolling dice following the ruleset for Vampire: The Masquerade 5th edition.
(c) Roy Healy. Distributed under GNU General Public License v3.0.
Built using Discord.py package and running on Python 3.6.
See https://github.com/further-reading/Dicecord-Chatbot-VtM for source code.
Join us on Discord https://discordapp.com/invite/DRM9MT8'''