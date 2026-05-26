import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
import random
import math
from collections import defaultdict
import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1439993397963395122
GUILD_ID = 1505844271855435826
MOD_ROLE_ID = 1359384902847565846
CONFESSION_CHANNEL_ID = 1359194169964237104
ALLOWED_CHANNEL_ID = 1359386224539729967
REMINDER_CHANNEL_ID = 1359386488546263221
VERIFICATION_CHANNEL_ID = 1359384372062453892
WELCOME_CHANNEL_ID = 1359399333421912104
GOODBYE_CHANNEL_ID = 1359399374660304906
LEVELUP_CHANNEL_ID = 1360201583802978365
VERIFIED_ROLE_NAME = "Verified"
HIGHLIGHTS_CHANNEL_ID = 1360164383250190415
fish_active = False
fish_lock = asyncio.Lock()
fish_counts = defaultdict(int)
message_counter = 0
xp_data = defaultdict(lambda: {"xp": 0, "level": 1})
banned_words = ["fuck", "dick", "nigger", "nigga", "sex"]

words = ["discord", "python", "hangman", "bot", "server"]
hangman_games = {}
class HangmanGame:
    STAGES = [
        "```\n\n\n\n\n=====\n```",
        "```\n |\n |\n |\n |\n=====\n```",
        "```\n +---+\n |\n |\n |\n |\n=====\n```",
        "```\n +---+\n |   O\n |\n |\n |\n=====\n```",
        "```\n +---+\n |   O\n |   |\n |   |\n |\n=====\n```",
        "```\n +---+\n |   O\n |  /|\\\n |   |\n |\n=====\n```",
        "```\n +---+\n |   O\n |  /|\\\n |   |\n |  / \\\n=====\n```"
    ]

    def __init__(self, word):
        self.word = word
        self.guessed_letters = set()
        self.remaining_tries = 6

    def display(self):
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def guess(self, letter):
        letter = letter.lower()
        if letter in self.guessed_letters:
            return False, "You've already guessed that letter."
        self.guessed_letters.add(letter)
        if letter not in self.word:
            self.remaining_tries -= 1
            return False, f"Incorrect guess. {self.remaining_tries} tries left."
        return True, "Correct!"

    def is_won(self):
        return all(letter in self.guessed_letters for letter in self.word)

    def is_lost(self):
        return self.remaining_tries <= 0

    def art(self):
        return self.STAGES[6 - self.remaining_tries]

milk_mocha_urls = {
    "kiss": "https://media.tenor.com/Tt72qF0Uk8sAAAAC/milk-and-mocha-bear.gif",
    "hug": "https://media.tenor.com/vYg4u4xPIScAAAAC/milk-and-mocha.gif",
    "cuddle": "https://media.tenor.com/wCRu3cqJAgcAAAAC/milk-and-mocha-bear-love.gif",
    "love": "https://media.tenor.com/_4YgA77ExHEAAAAC/milk-and-mocha-love.gif"
}

jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet."
]

bully_sentences = [
    "You're the reason the gene pool needs a lifeguard.",
    "You're as useless as the 'ueue' in 'queue'.",
    "You're not stupid; you just have bad luck thinking."
]


# Fish Button
class FishButton(View):
    def __init__(self, author):
        super().__init__(timeout=30)
        self.author = author
        self.fish_caught = False

    @discord.ui.button(label="Catch 🐟", style=discord.ButtonStyle.green)
    async def catch(self, interaction: discord.Interaction, button: Button):
        if self.fish_caught:
            await interaction.response.send_message("The fish is already caught!", ephemeral=True)
            return
        self.fish_caught = True
        fish_counts[interaction.user.id] += 1
        await interaction.response.edit_message(content=f"{interaction.user.mention} caught the fish! 🎉 Total: {fish_counts[interaction.user.id]}", view=None)


class VerificationView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=VERIFIED_ROLE_NAME)
        if not role:
            await interaction.response.send_message("Verification role not found.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.response.send_message("You're already verified!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("You have been verified!", ephemeral=True)


# Fish game logic
async def spawn_fish(channel):
    global fish_active
    async with fish_lock:
        if not fish_active:
            fish_active = True
            view = FishButton(author=None)
            await channel.send("🐟 A wild fish has appeared!", view=view)
            await asyncio.sleep(50)
            if not view.fish_caught:
                await channel.send("The fish got away... 🐟💨")
            fish_active = False



def calculate_level(xp):
    return int(math.sqrt(xp) // 10) + 1



@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    bot.add_view(VerificationView())
    print(f"Logged in as {bot.user}")
    if not bump_reminder.is_running():
        bump_reminder.start()


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if not reaction.message.guild:
        return

    # Get the highlights channel by ID
    highlights_channel = bot.get_channel(HIGHLIGHTS_CHANNEL_ID)
    if not highlights_channel:
        print("Highlights channel not found!")
        return

    # Count non-bot users who reacted with this emoji
    reaction_users = [u async for u in reaction.users() if not u.bot]
    if len(reaction_users) == 2:
        # Check if already highlighted
        for r in reaction.message.reactions:
            if str(r.emoji) == "📸":
                return

        # Add 📸 emoji to the message
        await reaction.message.add_reaction("📸")

        # Create and send embed
        embed = discord.Embed(
            title="Message Highlighted!",
            description=reaction.message.content or "No text content",
            color=discord.Color.gold()
        )
        embed.set_author(
            name=reaction.message.author.display_name,
            icon_url=reaction.message.author.avatar.url if reaction.message.author.avatar else None
        )
        embed.add_field(name="Channel", value=reaction.message.channel.mention)
        embed.add_field(name="Jump to Message", value=f"[Click here]({reaction.message.jump_url})", inline=False)

        # Add image if message has attachments
        if reaction.message.attachments:
            image_url = reaction.message.attachments[0].url
            embed.set_image(url=image_url)

        # Add footer
        embed.set_footer(text="⭐ Highlighted by the community")

        await highlights_channel.send(embed=embed)


@bot.event
async def on_message(message):
    global message_counter
    if message.author.bot:
        return

    if any(word in message.content.lower() for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, watch your language!", delete_after=3)

    message_counter += 1
    if message_counter >= 200:
        message_counter = 0
        await spawn_fish(message.channel)

    if message.channel.id == LEVELUP_CHANNEL_ID:
        user_data = xp_data[message.author.id]
        user_data["xp"] += 5
        new_level = calculate_level(user_data["xp"])
        if new_level > user_data["level"]:
            user_data["level"] = new_level
            await message.channel.send(f"🎉 {message.author.mention} leveled up to **Level {new_level}**!")

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    print(f"[DEBUG] {member} joined the server.")
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        print("[DEBUG] Welcome channel not found.")
        return

    welcome_messages = [
        f"Hey {member.mention}, welcome to **{member.guild.name}**! 🎉",
        f"{member.mention} just arrived! Let's give them a warm welcome 💕",
        f"A new star has joined us! 🌟 Say hi to {member.mention}!",
    ]

    embed = discord.Embed(
        title="🌸 Welcome Aboard!",
        description=random.choice(welcome_messages),
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="📥 Joined At", value=discord.utils.format_dt(member.joined_at, style='F'), inline=True)
    embed.add_field(name="👥 Member Count", value=f"{len([m for m in member.guild.members if not m.bot])}", inline=True)
    embed.set_footer(text=f"We're glad you're here, {member.name}! 💐")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    print(f"[DEBUG] {member} left the server.")
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if not channel:
        print("[DEBUG] Goodbye channel not found.")
        return

    goodbye_messages = [
        f"{member.mention} has left the server... 💔",
        f"We just lost a star. Bye {member.name}! 🌙",
        f"{member.name} said goodbye. We’ll miss you 😢"
    ]

    embed = discord.Embed(
        title="💨 Someone Left...",
        description=random.choice(goodbye_messages),
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 User", value=f"{member}", inline=True)
    embed.add_field(name="🧮 Remaining Members", value=f"{len([m for m in member.guild.members if not m.bot])}", inline=True)
    embed.set_footer(text="Hope they come back someday 💭")
    await channel.send(embed=embed)



@tasks.loop(minutes=30)
async def bump_reminder():
    channel = bot.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        await channel.send("Don't forget to `/bump` the server! 🔔")

@bot.tree.command(name="confess")
async def confess(interaction: discord.Interaction, message: str):
    channel = bot.get_channel(CONFESSION_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="Anonymous Confession", description=message, color=discord.Color.purple())
        await channel.send(embed=embed)
        await interaction.response.send_message("Confession sent anonymously!", ephemeral=True)


@bot.tree.command(name="verifybutton", description="Send the verification button")
async def verifybutton(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the owner can use this.", ephemeral=True)
        return

    view = VerificationView()
    await interaction.channel.send("Click the button to verify yourself!", view=view)
    await interaction.response.send_message("Verification button sent.", ephemeral=True)


@bot.tree.command(name="joke")
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(jokes))

@bot.tree.command(name="bully")
@app_commands.describe(member="The member to roast")
async def bully(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the owner can use this.", ephemeral=True)
        return
    await interaction.response.send_message(f"{member.mention} {random.choice(bully_sentences)}")

@bot.tree.command(name="purge")
async def purge(interaction: discord.Interaction, amount: int):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the owner can use this.", ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)

@bot.tree.command(name="level")
async def level(interaction: discord.Interaction):
    if interaction.channel.id != LEVELUP_CHANNEL_ID:
        await interaction.response.send_message("Check your level in the XP channel only!", ephemeral=True)
        return
    user_data = xp_data[interaction.user.id]
    await interaction.response.send_message(f"You are Level {user_data['level']} with {user_data['xp']} XP!")

@bot.tree.command(name="kiss")
async def kiss(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.mention} kissed {member.mention}! 💋", embed=discord.Embed().set_image(url=milk_mocha_urls["kiss"]))

@bot.tree.command(name="hug")
async def hug(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.mention} hugged {member.mention}! 🤗", embed=discord.Embed().set_image(url=milk_mocha_urls["hug"]))

@bot.tree.command(name="cuddle")
async def cuddle(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.mention} cuddled {member.mention}! 🧸", embed=discord.Embed().set_image(url=milk_mocha_urls["cuddle"]))

@bot.tree.command(name="love")
async def love(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.mention} loves {member.mention}! ❤️", embed=discord.Embed().set_image(url=milk_mocha_urls["love"]))

@bot.tree.command(name="kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if not discord.utils.get(interaction.user.roles, id=MOD_ROLE_ID):
        await interaction.response.send_message("You don't have permission to kick.", ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member} was kicked. Reason: {reason}")

@bot.tree.command(name="ban")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if not discord.utils.get(interaction.user.roles, id=MOD_ROLE_ID):
        await interaction.response.send_message("You don't have permission to ban.", ephemeral=True)
        return
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member} was banned. Reason: {reason}")

@bot.tree.command(name="timeout")
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason"):
    if not discord.utils.get(interaction.user.roles, id=MOD_ROLE_ID):
        await interaction.response.send_message("You don't have permission to timeout.", ephemeral=True)
        return
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(f"{member} timed out for {minutes} minutes. Reason: {reason}")

# Moved OUTSIDE and fixed indentation
@bot.tree.command(name="hangman", description="Start a new game of Hangman")
async def hangman(interaction: discord.Interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("You can only use this command in the game channel!", ephemeral=True)
        return

    word = random.choice(words).lower()
    game = HangmanGame(word)
    hangman_games[interaction.channel.id] = game

    embed = discord.Embed(title="🎯 Hangman Game Started!", color=discord.Color.blurple())
    embed.description = f"{game.art()}\nWord: `{game.display()}`\nTries Left: {game.remaining_tries}\nUse `/guess <letter>` to guess!"
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="guess", description="Guess a letter in Hangman")
@app_commands.describe(letter="The letter you want to guess")
async def guess(interaction: discord.Interaction, letter: str):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("You can only play in the game channel!", ephemeral=True)
        return

    if interaction.channel.id not in hangman_games:
        await interaction.response.send_message("No Hangman game is active in this channel. Start one with `/hangman`!", ephemeral=True)
        return

    game = hangman_games[interaction.channel.id]

    if len(letter) != 1 or not letter.isalpha():
        await interaction.response.send_message("Please enter a single valid letter.", ephemeral=True)
        return

    correct, message = game.guess(letter)

    embed = discord.Embed(title="🎯 Hangman", color=discord.Color.orange())
    embed.description = f"{game.art()}\n{message}\n\nWord: `{game.display()}`\nTries Left: {game.remaining_tries}"

    if game.is_won():
        embed.title = "🎉 You Won!"
        embed.color = discord.Color.green()
        embed.description = f"Word: `{game.word}`\nYou guessed it right!"
        del hangman_games[interaction.channel.id]
    elif game.is_lost():
        embed.title = "💀 Game Over"
        embed.color = discord.Color.red()
        embed.description = f"{game.art()}\nNo more tries left.\nThe word was: `{game.word}`"
        del hangman_games[interaction.channel.id]

    await interaction.response.send_message(embed=embed)

bot.run(config.DISCORD_TOKEN)