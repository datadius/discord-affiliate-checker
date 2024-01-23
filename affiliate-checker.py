import discord
from fairdesk import Fairdesk
from discord.ext import commands
import os

intent = discord.Intents.default()
bot = discord.Bot(intents=intent)


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="UID"))
        self.add_item(
            discord.ui.InputText(label="Username", style=discord.InputTextStyle.long)
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="UID", value=self.children[0].value)
        embed.add_field(name="Username", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


class MyView(discord.ui.View):
    @discord.ui.button(label="Fairdesk")
    async def fairdesk_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Fairdesk"))

    @discord.ui.button(label="Phemex")
    async def phemex_callback(self, button, interaction):
        await interaction.response.send_message(MyModal(title="Phemex"))


@bot.slash_command()
async def modal(ctx):
    await ctx.respond(embed=discord.Embed(title="Modal via Command"), view=MyView())


@bot.event
async def on_ready():
    print("Bot is ready")


bot.run(os.getenv("TEST_DISCORD_BOT_TOKEN"))
