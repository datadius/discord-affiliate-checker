import discord
from fairdesk import Fairdesk
from phemex import Phemex
from bingx import BingX
from sql_storage import SQLAffiliate
import os
import logging

intent = discord.Intents.default()
bot = discord.Bot(intents=intent)
sql_db = SQLAffiliate()

logger = logging.getLogger("[CROWNBOT]")
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class MyModal(discord.ui.Modal):
    def __init__(self, uid_checker, *args, **kwargs) -> None:
        self.uid_checker = uid_checker
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="UID"))

    async def callback(self, interaction: discord.Interaction):
        is_allowed_as_vip = False
        already_claimed = True

        try:
            uid = int(self.children[0].value)
        except Exception as e:
            raise Exception(f"UID is not a number {e}")

        try:
            if (
                isinstance(self.uid_checker, Fairdesk)
                or isinstance(self.uid_checker, BingX)
                or isinstance(self.uid_checker, Phemex)
            ):
                is_allowed_as_vip = self.uid_checker.get_uid_info(uid)

        except Exception as e:
            logger.error("Could not get uid info", e)

        try:
            already_claimed = sql_db.check_user_exists(uid)
        except Exception as e:
            logger.error("Could not check user exists", e)

        try:
            if is_allowed_as_vip and not already_claimed:
                await self.change_role(interaction)
                # store to sqlite database
                sql_db.add_user(uid)
            else:
                await interaction.response.send_message(
                    content=f"UID {uid} not valid. Try again", ephemeral=True
                )
        except Exception as e:
            logger.error("Could not change role", e)

    async def change_role(self, interaction: discord.Interaction):
        if interaction.guild is not None:
            if isinstance(interaction.user, discord.Member):
                # 1202690292168392784
                role = interaction.guild.get_role(int(os.getenv("vip_role_id")))
                logger.info(f"{role} has been given to {interaction.user.name}")
                if role is not None:
                    await interaction.user.add_roles(role, reason="Has enough deposit")
                    # change to write to a specific channel
                    await interaction.response.send_message(
                        content=f"You received {role}", ephemeral=True
                    )


class MyView(discord.ui.View):
    @discord.ui.button(
        label="Phemex",
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji(name="Phemex", id=1202314403358445658),
    )
    async def phemex_callback(self, button, interaction):
        phemex = Phemex()
        await interaction.response.send_modal(
            MyModal(title="Phemex", uid_checker=phemex)
        )

    @discord.ui.button(
        label="Fairdesk",
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji(name="Fairdesk", id=1202314476855234662),
    )
    async def fairdesk_callback(self, button, interaction):
        fairdesk = Fairdesk()
        await interaction.response.send_modal(
            MyModal(title="Fairdesk", uid_checker=fairdesk)
        )


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
    sql_db.initialize_db()
    if os.getenv("vip_role_id") is None:
        logger.info("set the role id by using vip_role_id")
        exit()
    logger.info("Bot is ready")


bot.run(os.getenv("crown_bot_secret"))
