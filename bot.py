import os
import random
import asyncio
import discord

from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# CONFIG
# =========================

processing_gif = set()

TARGET_STICKER_ID = 1476929209363599400
STICKER_GIF_CHANCE = 5  # 1 in 5
CUSTOM_GIF_URL = "https://cdn.discordapp.com/attachments/1402362385108435004/1502317751891398656/screaming-gif.gif?ex=69ff45ef&is=69fdf46f&hm=c60b30677c9a0a54c10a76de6fc04b1ed91ef18da005b0e217881e3ef98fb602&"

ROLE_EMOJI = "<:_freak:1501983205627269170>"
ROLE_REACTION_REQUIREMENT = 10
ROLE_NAME = "freak"

REWARD_MESSAGES = [
    "freak...",
    "shame...",
    "certified freak..."
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

    if message.stickers:

        for sticker in message.stickers:

            if str(sticker.id) == TARGET_STICKER_ID:

                roll = random.randint(1, 5)

                if roll == 1:
                    await message.reply(CUSTOM_GIF_URL)

                break

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
                            f"for 24 hours..."
                        )

                        await asyncio.sleep(86400)

                        await author.remove_roles(role)

                        await channel.send(
                            f"{author.mention}'s "
                            f"{role.name} role expired."
                        )

    # GIF SYSTEM

if message.id in gif_replied_messages:
    return

for reaction in message.reactions:

    if str(reaction.emoji) == GIF_TRIGGER_EMOJI:

        if reaction.count >= GIF_REACTION_REQUIREMENT:

            # 🚨 LOCK immediately (prevents double triggers)
            if message.id in processing_gif:
                return

            processing_gif.add(message.id)

            gif_replied_messages.add(message.id)

            gif_url = random.choice(GIFS)

            try:
                await message.reply(gif_url)
            finally:
                # remove lock after completion
                processing_gif.discard(message.id)

            break

bot.run(TOKEN)
