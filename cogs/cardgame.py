import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import Option, OptionChoice

import random

gain = 52


def bool_input(description: str) -> bool:
    while True:
        inp = input(f'{description}:')
        if inp.upper() == 'Y':
            return True
        elif inp.upper() == 'N':
            return False
        else:
            print(f'{inp} is not a valid')


def new_game() -> list[str]:
    cards = []
    marks = ['♥', '♠', '♦', '♣']
    for i in range(gain):
        cards.append(f'[{marks[int(i/13)]} {str(i % 13+1)}]')
    for i in range(len(marks)):
        print(','.join(cards[i*13:(i+1)*13]))
    random.shuffle(cards)
    return cards


class GameEnd(Exception):
    pass


class Button(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.n = 1
        self.result = 0
        self.card = gain
        self.cards = new_game()

    @discord.ui.button(label="0", style=discord.ButtonStyle.red)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):

        try:
            await Button.check(self)
        except GameEnd:
            self = None
            content = 'gameend'
        await interaction.response.edit_message(content=content, view=self)

    @discord.ui.button(label="0", style=discord.ButtonStyle.red)
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0
        if number >= 4:
            button.style = discord.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

    async def check(self) -> str:
        if gain > n and gain > n+result:
            r = []
            for i in range(gain):
                if n & i > 0:
                    r.append(cards[i])
            if len(r) != 0:
                return ','.join(sorted(r))
            raise GameEnd('GameEnd')


n = 1
result = 0
cards = new_game()

while gain > n and gain > n+result:
    r = []
    for i in range(gain):
        if n & i > 0:
            r.append(cards[i])
    print(','.join(sorted(r)))

    if bool_input('Exsits? Y/n'):
        result += n
    n = n << 1
print(cards[result])


class CardGameCog(commands.Cog):

    def __init__(self, bot):
        print('NBさんの初期化')
        self.bot = bot

    nb = SlashCommandGroup('game', 'test')

    @nb.command(name='card', description='カードあてる系のアレ')
    async def nb_home(self, ctx):
        ctx.respond(view=Button())


def setup(bot):
    bot.add_cog(CardGameCog(bot))
