import os
import random
import asyncio
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# MOD CONFIG
# =========================
MOD_ROLE_NAME = "mod"
# =========================

# =========================
# ASK CONFIG
# =========================
ASK_REPLIES = [
    "yeah",
    "nah",
    "maybe...",
    "how should i know..",
    "yes",
    "absolutely not",
    "obviously",
    "idk",
    "fo sure",
    "naur",
    "perhaps",
    "🤔",
    "yeag",
    "no",
    "fuck you",
    "not sure",
    "yeah... i think",
    "i suppose not",
    "true",
    "false",
    "fuh no",
    "hell yeah",
]
# =========================

# =========================
# CONFIG
# =========================
ROLE_EMOJI = "<:_freak:1501983205627269170>"
ROLE_REACTION_REQUIREMENT = 8
ROLE_NAME = "freak"
REWARD_MESSAGES = [
    "certified freak...",
    "shame...",
    "freak detected..."
]

TRIGGER_EMOJI = "<:stupid_neco:1459457937985769474>"
BOT_REACTION = "<:stupid_neco:1459457937985769474>"

GIF_TRIGGER_EMOJI = "<:_saint:1501983273381789727>"
GIF_REACTION_REQUIREMENT = 6
GIFS = [
    "https://tenor.com/view/montgomery-swizzenbocher-iii-gif-15095346273009658011"
]

# =========================
# INACTIVITY CONFIG
# =========================
INACTIVITY_CHANNEL_ID = 1478448506518638745

INACTIVITY_MESSAGES = [
    {"text": "Meowww"},
    {"text": "meows"},
    {"text": "Miau"},
    {"text": "Nya"},
    {"text": "beer?"},
    {"text": "N-Nya!"},
    {"text": "!!!"},
    {"text": "?!"},
    {"text": "woof.."},
    {"text": "ughf..."},
    {"text": "bleh.."},
    {"text": "paws at u"},
    {"text": "😼"},
    {"text": "👀"},
    {"text": "<:letstakealook:1478809260363087983>"},
    {"text": "<:aj_ninja:1291303302310527006>"},
    {"text": "<:chud:1478646737794109591>"},
    {"text": "<:aj_tongue:1291440668035518545>"},
    {"text": "<a:boing:1240335446609887243>"},
    {"text": "<:stupid_neco:1459457937985769474>"},
    {"text": None, "url": "https://cdn.discordapp.com/attachments/1503101647453421778/1503104231173783692/tunabot_blink.gif?ex=6a022267&is=6a00d0e7&hm=a2c4bd7463e046b147efa04359afa6ff60996a42646c6125989c91324e7a771c&"},
    {"text": None, "url": "https://cdn.discordapp.com/attachments/1503101647453421778/1503101700586864750/screaming-gif.gif?ex=6a02200b&is=6a00ce8b&hm=f794849063e48a729f77e19815950c653ba08926217419b9471f3a62f81741a1&"},
    {"text": None, "url": "https://cdn.discordapp.com/attachments/488099837401759747/1448665340040187904/togif.gif?ex=6a01d73b&is=6a0085bb&hm=764f2e20af650628ffc0482c26ccc539fabab60648263aa2339769181431c56a&"},
    {"text": None, "url": "https://media.discordapp.net/attachments/1058472840594214963/1186213255711031356/3dgifmaker63550.gif?ex=6a0189ae&is=6a00382e&hm=90ab66f731c0c3d7cbca9f746d963c0aab3094a6ee03b3a4df896de6c21fb6f9&"},
]

INACTIVITY_MIN_HOURS = 1
INACTIVITY_MAX_HOURS = 6
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

rewarded_messages = set()
gif_replied_messages = set()
gif_locks = {}
last_message_time = {}


async def inactivity_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        channel = bot.get_channel(INACTIVITY_CHANNEL_ID)
        if channel:
            now = asyncio.get_event_loop().time()
            last = last_message_time.get(INACTIVITY_CHANNEL_ID)

            if last is None:
                last_message_time[INACTIVITY_CHANNEL_ID] = now

            threshold = random.uniform(
                INACTIVITY_MIN_HOURS * 1800,
                INACTIVITY_MAX_HOURS * 1800
            )

            if last is not None and (now - last) >= threshold:
                choice = random.choice(INACTIVITY_MESSAGES)
                text = choice.get("text")
                url = choice.get("url")
                msg = f"{text}\n{url}" if text and url else (url or text)
                await channel.send(msg)
                last_message_time[INACTIVITY_CHANNEL_ID] = now

        await asyncio.sleep(300)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(inactivity_loop())


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == INACTIVITY_CHANNEL_ID:
        last_message_time[INACTIVITY_CHANNEL_ID] = asyncio.get_event_loop().time()

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        choice = random.choice(INACTIVITY_MESSAGES)
        text = choice.get("text")
        url = choice.get("url")
        msg = f"{text}\n{url}" if text and url else (url or text)
        await message.reply(msg)

    if TRIGGER_EMOJI in message.content:
        await message.add_reaction(BOT_REACTION)

    await bot.process_commands(message)


# =========================
# COMMANDS
# =========================
@bot.command()
async def ask(ctx, *, question=None):
    if question is None:
        await ctx.send("ask me something!")
        return
    await ctx.reply(random.choice(ASK_REPLIES))


def is_mod():
    async def predicate(ctx):
        return discord.utils.get(ctx.author.roles, name=MOD_ROLE_NAME) is not None
    return commands.check(predicate)


@bot.command()
@is_mod()
async def set_freak(ctx, count: int):
    global ROLE_REACTION_REQUIREMENT
    if count < 1:
        await ctx.send("Must be at least 1.")
        return
    ROLE_REACTION_REQUIREMENT = count
    await ctx.send(f"Freak = **{count}**.")


@bot.command()
@is_mod()
async def set_saint(ctx, count: int):
    global GIF_REACTION_REQUIREMENT
    if count < 1:
        await ctx.send("Must be at least 1.")
        return
    GIF_REACTION_REQUIREMENT = count
    await ctx.send(f"saint = **{count}**.")


@bot.command()
@is_mod()
async def reqs(ctx):
    await ctx.send(
        f"Current requirements:\n"
        f"Freak role: **{ROLE_REACTION_REQUIREMENT}** reactions\n"
        f"GIF trigger: **{GIF_REACTION_REQUIREMENT}** reactions"
    )


@set_freak.error
@set_saint.error
@reqs.error
async def mod_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("ur not mod.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("add a number")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("That's not a valid number.")


# =========================
# REACTION EVENTS
# =========================
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
    message = await channel.fetch_message(payload.message_id)

    # =========================
    # ROLE SYSTEM
    # =========================
    if message.id not in rewarded_messages:
        for reaction in message.reactions:
            if str(reaction.emoji) == ROLE_EMOJI:
                if reaction.count >= ROLE_REACTION_REQUIREMENT:
                    rewarded_messages.add(message.id)
                    member = await guild.fetch_member(message.author.id)
                    role = discord.utils.get(guild.roles, name=ROLE_NAME)
                    if role:
                        await member.add_roles(role)
                        reward_message = random.choice(REWARD_MESSAGES)
                        await message.reply(
                            f"{reward_message}\n"
                            f"{member.mention} got {role.name} role for 24h!\n"
                            f"https://cdn.discordapp.com/attachments/1503101647453421778/1503114422950821950/sound-the-car-alarm-cat.gif?ex=6a022be4&is=6a00da64&hm=f099cb09e387553178ecdeda9c3597b0bcbe397a8d9f3b902a2346477423fe0e&"
                        )
                        await asyncio.sleep(86400)
                        await member.remove_roles(role)
                        await channel.send(f"{member.mention}'s role expired.")
            break

    # =========================
    # GIF SYSTEM
    # =========================
    if str(payload.emoji) == GIF_TRIGGER_EMOJI:
        if payload.message_id in gif_replied_messages:
            return

        if payload.message_id not in gif_locks:
            gif_locks[payload.message_id] = asyncio.Lock()

        async with gif_locks[payload.message_id]:
            if payload.message_id in gif_replied_messages:
                return

            gif_reaction = next(
                (r for r in message.reactions if str(r.emoji) == GIF_TRIGGER_EMOJI),
                None
            )
            if gif_reaction is None or gif_reaction.count < GIF_REACTION_REQUIREMENT:
                return

            gif_replied_messages.add(payload.message_id)
            await message.reply(random.choice(GIFS))


bot.run(TOKEN)
