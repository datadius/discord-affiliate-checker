import discord
from fairdesk import Fairdesk
from discord.ext import commands
import os

intent = discord.Intents.default()
bot = discord.Bot(intents=intent)


class MyModal(discord.ui.Modal):
    def __init__(self, uid_checker, *args, **kwargs) -> None:
        self.uid_checker = uid_checker
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="UID"))

    async def callback(self, interaction: discord.Interaction):
        print(self.children[0].value)
        if isinstance(self.uid_checker, Fairdesk):
            print("Fairdesk", self.uid_checker.get_uid_info(self.children[0].value))
        embed = discord.Embed(title="UID")
        embed.add_field(name="UID", value=self.children[0].value)
        await interaction.response.send_message(embeds=[embed])


class MyView(discord.ui.View):
    @discord.ui.button(label="Fairdesk", style=discord.ButtonStyle.primary)
    async def fairdesk_callback(self, button, interaction):
        fairdesk = Fairdesk()
        await interaction.response.send_modal(
            MyModal(title="Fairdesk", uid_checker=fairdesk)
        )

    @discord.ui.button(label="Phemex", style=discord.ButtonStyle.primary)
    async def phemex_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Phemex", source="Phemex"))

    @discord.ui.button(label="BingX", style=discord.ButtonStyle.primary)
    async def bingx_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="BingX", source="BingX"))


@bot.slash_command()
async def modal(ctx):
    description = ""
    with open("text_embed.txt", "r", encoding="utf8") as f:
        description = f.read()
    embed = discord.Embed(
        title="Claim Your VIP Access Today!",
        color=discord.Color.blurple(),
        description=description,
    )
    await ctx.respond(embed=embed, view=MyView())


@bot.event
async def on_ready():
    print("Bot is ready")


bot.run(os.getenv("TEST_DISCORD_BOT_TOKEN"))
