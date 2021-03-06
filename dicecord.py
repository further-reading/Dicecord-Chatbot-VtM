import discord
import time
import asyncio
from character import Character
import datetime
from xml.dom import minidom
from xml.etree.ElementTree import Element, ParseError
from xml.etree import ElementTree as etree
import textResponses
import socket
import traceback
import re

class DicecordBot:
    def __init__(self, token, me):
        self.token = token
        self.me = me
        self.servers = {}
        try:
            self.readServers()
        except FileNotFoundError:
            self.servers = {}

    def startBot(self):
        self.loop = asyncio.new_event_loop()
        self.client = discord.Client(loop=self.loop)

        @self.client.event
        async def on_ready():
            """Print details and update server count when bot comes online."""
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')
            await self.client.change_presence(game=discord.Game(name='PM "help" for commands'))

        @self.client.event
        async def on_message(message):
            await self.on_message(message)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.client.user:
            return

        try:
            channel, content = await self.checkCommand(message)
        except TypeError:
            return

        await self.send(channel, content, message)

    async def send(self, channel, content, message):
        try:
            await self.client.send_message(channel, content)
        except discord.Forbidden:
            self.errorText(message, "Forbidden Error")
        except UnicodeEncodeError:
            self.errorText(message, "Unicode Error")
        except discord.errors.HTTPException:
            self.errorText(message, "HTTP Exception")

    async def checkCommand(self, message):
        username = self.client.user.name
        command = message.content.lower()
        if str(message.author) == self.me and "saveVtM" in command:
            # allows me to ask for a save of current settings at any time
            self.save_details()
            await self.client.send_message(message.channel, f'servers:{len(self.client.servers)}')
            await self.client.change_presence(game=discord.Game(name='PM "help" for commands'))
            return message.channel, "Saved details"

        if message.author.bot:
            return

        if not message.server:  # Private Message - message.server = None
            return self.pmCommands(message)

        # we only want bot to respond to @mentions
        if f"@{username}" not in message.clean_content:
            return

        character = self.check_server(message)

        if 'roll' in command:
            char = self.check_server(message)
            try:
                results = self.parse_roll(char, message.clean_content)
            except RuntimeError:
                self.errorText(message, "No dice amount found")
                return
            except:
                self.errorText(message, "Unknown error")
                return

            for result in results:
                # {0.author.mention} works better for bot implementation
                out = result.replace(char.ID, "{0.author.mention}")
                await self.send(message.channel, out.format(message), message)
                time.sleep(1)

        elif 'flavour' in command:
            out = self.set_flavour(message)
            if out:
                return message.author, out.format(message)

        elif "delete" in command:
            out = self.delete_content(message)
            if out:
                return message.author, out.format(message)

    def pmCommands(self, message):
        command = message.content.lower()

        if 'flavour' in command:
            return message.author, textResponses.flavText

        elif 'help' in command:
            return message.author, textResponses.helptext

        elif 'info' in command:
            return message.author, textResponses.aboutText

        elif 'roll' in command:
            return message.author, textResponses.rolltext

        else:
            return message.author, "Write 'help' for help or 'info' for bot info."

    def parse_roll(self, player, message):
        """Checks text for type of roll, makes that roll."""

        message = message.strip()
        message = message.lower()
        diceAmount = self.getDiceAmount(message)

        if diceAmount is None:
            # stop if no dice number found
            return

        if diceAmount >= 300:
            return ["Too many dice. Please roll less than 300."]

        return player.roll_set(diceAmount)

    def getDiceAmount(self, messageText):
        """
        Checks the message to figure out the maount of dice to roll
        Natural language processing used based on following priority:
        1. Check for roll x
        2. Get first number after the @mention
        3. Get first number in message
        Args:
            messageText (str): text of message

        Returns (int or None): amount of dice to roll
        """

        # First check for message of the form roll x
        matched = re.search(r'(?<=\broll )[0-9]+\b', messageText)
        if matched:
            return int(matched.group())

        # Check for first number after @mention and then first number in message
        splitMessage = messageText.split('@' + self.client.user.name.lower())
        for index in [-1, 0]:
            message = splitMessage[index]
            matched = re.search(r'\b[0-9]+\b', message)
            if matched is not None:
                return int(matched.group())

    def readServers(self):
        servers = {}

        try:
            dom = etree.parse("details.xml")
        except ParseError:
            self.servers = {}
            return
        except FileNotFoundError:
            self.servers = {}
            return

        servs = dom.findall('server')

        for server in servs:
            servname = server.find('name').text
            servers[servname] = {}
            channels = server.findall('channel')

            for channel in channels:
                channelname = channel.find('name').text
                servers[servname][channelname] = {}
                users = channel.findall('user')

                for user in users:
                    username = user.find('name').text
                    lasttime = user.find('time').text
                    lasttime = datetime.datetime.strptime(lasttime, "%Y-%m-%d %H:%M:%S.%f")
                    flavour = user.find('flavour').text

                    servers[servname][channelname][username] = [Character(username, bool(flavour)), lasttime]

        self.servers = servers

    def check_server(self, message):
        """Helper function that finds character object associated with a user."""

        server = message.server.id
        channel = message.channel.id
        author = message.author.id

        if server in self.servers:
            # check if channel is known
            if channel in self.servers[server]:
                # check if player is known
                if author in self.servers[server][channel]:
                    # update command time and return character
                    self.servers[server][channel][author][1] = datetime.datetime.now()
                    return self.servers[server][channel][author][0]

                else:  # if player not known make new entry
                    char = Character(author)
                    self.servers[server][channel][author] = [char, datetime.datetime.now()]
            else:  # make a new channel entry
                char = Character(author)
                self.servers[server][channel] = {author: [char, datetime.datetime.now()]}

        else:  # make new server entry
            char = Character(author)
            self.servers[server] = {channel: {author: [char, datetime.datetime.now()]}}
        return char

    def set_flavour(self, message):
        """Allows user to set existence of flavour text."""
        char = self.check_server(message)
        setting = message.content.lower()
        if 'off' in setting:
            char.flavour = False
            return "Flavour turned off in server " + str(message.server) + " - " + str(message.channel)

        elif 'on' in setting:
            char.flavour = True
            return "Flavour turned on in server " + str(message.server) + " - " + str(message.channel)

        elif 'check' in setting:
            if char.flavour:
                return "Flavour turned on in server " + str(message.server) + " - " + str(message.channel)
            else:
                return "Flavour turned off in server " + str(message.server) + " - " + str(message.channel)

    def delete_content(self, message):
        self.check_server(message)
        if "user" in message.content:
            del self.servers[str(message.server.id)][str(message.channel.id)][str(message.author.id)]
            return "Details for " + str(message.author) + " removed from " + str(message.server) + " - " + str(
                message.channel)

        elif "channel" in message.content:
            del self.servers[str(message.server.id)][str(message.channel.id)]
            return "All user details for channel **" + str(message.channel) + "** removed from **" + str(
                message.server) + "** by {0.author.mention}"

        elif "server" in message.content:
            del self.servers[str(message.server.id)]
            return "All user details for all channels removed from **" + str(message.server) + "** by {0.author.mention}"

    def save_details(self):
        """Save current server settings"""
        # remove characters who have not been used in more than 30 days
        # after the character loop it removes all empty channels
        # after channel loop it removes all empty servers
        for server in list(self.servers):
            for channel in list(self.servers[server]):
                for user in list(self.servers[server][channel]):
                    timeDifference = datetime.datetime.now() - self.servers[server][channel][user][1]
                    if timeDifference.days > 30:
                        del self.servers[server][channel][user]
                if not self.servers[server][channel]:
                    del self.servers[server][channel]
            if not self.servers[server]:
                del self.servers[server]

        # save anyone who remains
        root = Element('root')
        for server in self.servers:
            serv = Element('server')
            root.append(serv)

            servername = Element('name')
            serv.append(servername)
            servername.text = server

            for channel in self.servers[server]:
                chan = Element('channel')
                serv.append(chan)

                channame = Element('name')
                chan.append(channame)
                channame.text = channel

                for user in self.servers[server][channel]:
                    use = Element('user')
                    chan.append(use)

                    usename = Element('name')
                    use.append(usename)
                    usename.text = user

                    flavname = Element('flavour')
                    use.append(flavname)
                    flavname.text = str(self.servers[server][channel][user][0].flavour)

                    usetime = Element('time')
                    use.append(usetime)
                    usetime.text = str(self.servers[server][channel][user][1])

        # write file
        rough_string = etree.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        text = reparsed.toprettyxml(indent="  ")

        f = open("details.xml", 'w', encoding='utf-8')
        f.write(text)
        f.close()

    def errorText(self, message, error):
        print('Time: ' + str(datetime.datetime.now()) +
              '\nError: ' + error +
              '\nMessage: ' + str(message.clean_content) +
              '\nServer: ' + str(message.server) +
              '\nChannel: ' + str(message.channel) +
              '\nAuthor: ' + str(message.author) +
              '\n------\n')

def runner(token, me):
    """Helper function to run. Handles connection reset errors by automatically running again."""
    while True:
        try:
            bot = DicecordBot(token, me)
            bot.readServers()
            bot.startBot()
            bot.client.run(bot.token)
        except KeyboardInterrupt:
            file = open("error.txt", "w")
            print("here", file=file)
            file.close()
            bot.save_details()
            bot.loop.close()
            break
        except:
            file = open("error.txt", "w")
            print("there", file=file)
            file.close()
            traceback.format_exc()
            bot.loop.close()
            bot.save_details()
            checkConnection()
            bot = DicecordBot(token, me)


def checkConnection(host='8.8.8.8', port=53, timeout=53):
    while True:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            print("Connected")
            break
        except:
            print("No Connection")
            print(datetime.datetime.now())
            time.sleep(300)
