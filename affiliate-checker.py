import discord
from fairdesk import Fairdesk
from phemex import Phemex
from bingx import BingX
from bybit import Bybit
from blofin import Blofin
from coinbaseimpact import CoinbaseImpact
from sql_storage import SQLAffiliate
import os
import logging
import pandas as pd
import io

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

        self.add_item(discord.ui.InputText(label="UID (User ID Number)"))

    async def callback(self, interaction: discord.Interaction):
        is_allowed_as_vip = False
        already_claimed = True
        try:
            uid = self.children[0].value
        except Exception as e:
            raise Exception(f"UID hasn't been found {e}")
        exchange = ""
        username = ""
        deposit = 0
        found = False

        try:
            if uid.isdigit() is False:
                await interaction.response.send_message(
                    content="UID should be a number, not email or any other type of word",
                    ephemeral=True,
                )
                logger.error(f"UID {uid} was not a digit")
                raise Exception(f"UID {uid} was not a digit")
            else:
                uid = int(uid)
        except Exception as e:
            raise Exception(f"Issues when converting the UID {uid} to integer {e}")

        try:
            if (
                isinstance(self.uid_checker, Fairdesk)
                or isinstance(self.uid_checker, Phemex)
                or isinstance(self.uid_checker, BingX)
                or isinstance(self.uid_checker, Bybit)
                or isinstance(self.uid_checker, Blofin)
            ):
                is_allowed_as_vip, deposit, found = self.uid_checker.get_uid_info(uid)
                exchange = self.uid_checker.get_exchange_name()

        except Exception as e:
            logger.error("Could not get uid info", e)

        try:
            already_claimed = sql_db.check_user_exists(uid)
        except Exception as e:
            logger.error("Could not check user exists", e)

        try:
            if is_allowed_as_vip and not already_claimed:
                username = await self.change_role(interaction)
                sql_db.add_user(uid, username, deposit, exchange)
            elif already_claimed:
                logger.info(f"UID {uid} already used")
                await interaction.response.send_message(
                    content=f"UID {uid} already used",
                    ephemeral=True,
                )
            elif not found:
                logger.info(f"UID {uid} hasn't been found")
                await interaction.response.send_message(
                    content=f"UID {uid} hasn't been found in the list",
                    ephemeral=True,
                )
            elif found and not is_allowed_as_vip:
                logger.info(
                    f"UID {uid} hasn't been found or doesn't have enough deposit to claim VIP role"
                )
                await interaction.response.send_message(
                    content=f"UID {uid} doesn't have enough deposit to claim VIP role",
                    ephemeral=True,
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
                    await interaction.response.send_message(
                        content=f"You received {role} role", ephemeral=True
                    )
                    return interaction.user.name


class MyView(discord.ui.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
        emoji=discord.PartialEmoji(name="Fairdesk2", id=1203053186580221952),
    )
    async def fairdesk_callback(self, button, interaction):
        fairdesk = Fairdesk()
        await interaction.response.send_modal(
            MyModal(title="Fairdesk", uid_checker=fairdesk)
        )

    @discord.ui.button(
        label="BingX",
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji(name="BingX", id=1202315672005386321),
    )
    async def bingx_callback(self, button, interaction):
        bingx = BingX()
        await interaction.response.send_modal(MyModal(title="BingX", uid_checker=bingx))

    @discord.ui.button(
        label="Bybit",
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji(name="ByBitEmoji", id=1217198629853462529),
    )
    async def bybit_callback(self, button, interaction):
        bybit = Bybit()
        await interaction.response.send_modal(MyModal(title="Bybit", uid_checker=bybit))

    @discord.ui.button(
        label="Coinbase",
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji(name="coinbase", id=1219723064594403399),
    )
    async def coinbase_callback(self, button, interaction):
        coinbase = CoinbaseImpact()
        await interaction.response.send_modal(
            MyModal(title="Coinbase", uid_checker=coinbase)
        )

    @discord.ui.button(
        label="Blofin",
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji(name="blofin", id=1219723064594403399),
    )
    async def blofin_callback(self, button, interaction):
        blofin = Blofin()
        await interaction.response.send_modal(
            MyModal(title="Blofin", uid_checker=blofin)
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
    await ctx.respond(embed=embed, view=MyView(timeout=None))


@bot.slash_command()
async def stats(ctx):
    users = sql_db.get_users()
    df_users = pd.DataFrame(
        users,
        columns=["id", "uid", "exchange", "deposit", "username", "approval_datetime"],
    )
    df_users = df_users.drop(columns=["id"])
    arr = io.BytesIO()
    df_users.to_csv(arr, index=False)
    arr.seek(0)
    await ctx.respond(
        file=discord.File(arr, filename="users.csv"), content="Here are the stats:"
    )


@bot.event
async def on_ready():
    sql_db.initialize_db()
    if os.getenv("vip_role_id") is None:
        logger.info("set the role id by using vip_role_id")
        exit()
    logger.info("Bot is ready")


bot.run(os.getenv("crown_bot_secret"))
