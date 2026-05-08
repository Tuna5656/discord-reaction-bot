import os
import random
import asyncio
import discord

from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# CONFIG
# =========================

ROLE_EMOJI = "<:_freak:1501983205627269170>"
ROLE_REACTION_REQUIREMENT = 5
ROLE_NAME = "<:_freak:1501983205627269170>"

REWARD_MESSAGES = [
    "freak...",
    "shame...",
    "thumbs down emoji..."
]

TRIGGER_EMOJI = "<:stupid_neco:1459457937985769474>"
BOT_REACTION = "<:stupid_neco:1459457937985769474>"

GIF_TRIGGER_EMOJI = "<:_saint:1501983273381789727>"
GIF_REACTION_REQUIREMENT = 3

GIFS = [
    "https://tenor.com/view/montgomery-swizzenbocher-iii-gif-15095346273009658011"
]

# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

rewarded_messages = set()
gif_replied_messages = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if TRIGGER_EMOJI in message.content:
        await message.add_reaction(BOT_REACTION)

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        return

    guild = bot.get_guild(payload.guild_id)

    if guild is None:
        return

    channel = guild.get_channel(payload.channel_id)

    if channel is None:
        return

    message = await channel.fetch_message(
        payload.message_id
    )

    # ROLE SYSTEM

    if message.id not in rewarded_messages:

        for reaction in message.reactions:

            if str(reaction.emoji) == ROLE_EMOJI:

                if reaction.count >= ROLE_REACTION_REQUIREMENT:

                    rewarded_messages.add(message.id)

                    author = message.author

                    role = discord.utils.get(
                        guild.roles,
                        name=ROLE_NAME
                    )

                    if role:

                        await author.add_roles(role)

                        reward_message = random.choice(
                            REWARD_MESSAGES
                        )

                        await message.reply(
                            f"{reward_message}\n"
                            f"{author.mention} got "
                            f"the {role.name} role "
                            f"for 24 hours!"
                        )

                        await asyncio.sleep(86400)

                        await author.remove_roles(role)

                        await channel.send(
                            f"{author.mention}'s "
                            f"{role.name} role expired."
                        )

    # GIF SYSTEM

    if message.id not in gif_replied_messages:

        for reaction in message.reactions:

            if str(reaction.emoji) == GIF_TRIGGER_EMOJI:

                if reaction.count >= GIF_REACTION_REQUIREMENT:

                    gif_replied_messages.add(
                        message.id
                    )

                    gif_url = random.choice(GIFS)

                    await message.reply(gif_url)

bot.run(TOKEN)
