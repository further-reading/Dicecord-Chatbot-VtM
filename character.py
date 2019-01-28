import random
import messaging

class Character:
    goodMessages = messaging.goodDefault.copy()
    badMessages = messaging.badDefault.copy()

    def __init__(self, ID, flavour=True):
        """
        Class for holding details of a player and making their rolls.
        Args:
            ID (str): discord ID of player
            flavour (bool): whether flavour messaging is active
        """

        self.ID = ID
        self.flavour = flavour

    def roll_set(self, dice):
        """
        Roll a set of dice
        Args:
            dice (int): amount of dice to roll

        Returns (list of str): roll messages to return
        """

        if dice < 1:
            return ['Select at least 1 die.']

        diceResults = ""
        successes = 0
        messages = []
        tenCount = 0
        
        # fail collector in case it is a rote

        for die in range(0, dice):
            # roll each die
            result = random.randrange(1, 11)
            if result == 10:
                tenCount += 1
                diceResults += f" **{result}**"
            elif result >= 6:
                successes += 1
                diceResults += f" {result}"
            else:
                diceResults += f" {result}"

        if tenCount % 2 == 0:
            # even amount of 10s
            successes += 2*tenCount
        else:
            successes += 1 + 2*(tenCount - 1)

        # add a summary message
        out = f"{self.ID} rolled {str(dice)} dice and got **{str(successes)} success"
        if successes != 1:
            out += "es**."
        else:
            out += "**."


        messages.append(out + diceResults)

        
        # check for positive or negative message
        if self.flavour:
            if successes == 0:
                messages.append(self.bot_message("bad"))
            elif successes >= 4:
                messages.append(self.bot_message("good"))
        
        return messages
        
    def bot_message(self, messagetype):
        """
        Sends a random positive/negative message with very good or very bad rolls
        Args:
            messagetype (str): type of messaging to add

        Returns (str): message to add
        """
        if messagetype == 'good':
                out = random.choice(self.goodMessages)
        elif messagetype == 'bad':
                out = random.choice(self.badMessages)

        return out.replace("[userID]", self.ID)

    
    def roll_special(self):
        """
        Roll a single die
        Returns (str): Result of roll
        """
        value = random.randrange(1, 11)
        return self.ID + " rolled a " + str(value) + "!"
