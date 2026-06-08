import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BOT'))

import discord
from discord.ext import commands, tasks
from discord.ui import View
from datetime import timedelta
import asyncio
import random
from config import (
    DISCORD_TOKEN,
    OWNER_ID,
    GUILD_ID,
    MOD_ROLE_ID,
    VERIFIED_ROLE_NAME,
    CONFESSION_CHANNEL_ID,
    REMINDER_CHANNEL_ID,
    WELCOME_CHANNEL_ID,
    GOODBYE_CHANNEL_ID,
    HIGHLIGHTS_CHANNEL_ID,
)
from filter import FilterCog, banned_words
from hangman import HangmanCog
from fishgame import FishCog
from xpsystem import XPCog

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

HIGHLIGHTS_REACTION_THRESHOLD = 2

roleplay_gifs = {
    "kiss":   "https://media.tenor.com/Tt72qF0Uk8sAAAAC/milk-and-mocha-bear.gif",
    "hug":    "https://media.tenor.com/vYg4u4xPIScAAAAC/milk-and-mocha.gif",
    "cuddle": "https://media.tenor.com/wCRu3cqJAgcAAAAC/milk-and-mocha-bear-love.gif",
    "love":   "https://media.tenor.com/_4YgA77ExHEAAAAC/milk-and-mocha-love.gif",
}

joke_list = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
]

roast_lines = [
    "You're the reason the gene pool needs a lifeguard.",
    "You're as useless as the 'ueue' in 'queue'.",
    "You're not stupid; you just have bad luck thinking.",
]

welcome_templates = [
    "Hey {mention}, welcome to **{guild}**!",
    "{mention} just arrived! Let's give them a warm welcome.",
    "A new star has joined us! Say hi to {mention}!",
]

goodbye_templates = [
    "{mention} has left the server...",
    "We just lost a star. Bye {name}!",
    "{name} said goodbye. We'll miss you.",
]


class VerificationView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def handle_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        verified_role = discord.utils.get(interaction.guild.roles, name=VERIFIED_ROLE_NAME)
        if not verified_role:
            await interaction.response.send_message("Verification role not found.", ephemeral=True)
            return
        if verified_role in interaction.user.roles:
            await interaction.response.send_message("You are already verified!", ephemeral=True)
        else:
            await interaction.user.add_roles(verified_role)
            await interaction.response.send_message("You have been verified!", ephemeral=True)


def is_moderator(ctx: commands.Context) -> bool:
    return (
        ctx.author.id == OWNER_ID
        or discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is not None
    )


@bot.event
async def on_ready():
    bot.add_view(VerificationView())
    print(f"Logged in as {bot.user}")
    if not bump_reminder.is_running():
        bump_reminder.start()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if any(word in message.content.lower() for word in banned_words):
        return

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot or not reaction.message.guild:
        return

    highlights_channel = bot.get_channel(HIGHLIGHTS_CHANNEL_ID)
    if not highlights_channel:
        return

    non_bot_reactors = [u async for u in reaction.users() if not u.bot]
    if len(non_bot_reactors) < HIGHLIGHTS_REACTION_THRESHOLD:
        return

    for existing_reaction in reaction.message.reactions:
        if str(existing_reaction.emoji) == "📸":
            return

    await reaction.message.add_reaction("📸")

    highlight_embed = discord.Embed(
        title="Message Highlighted!",
        description=reaction.message.content or "No text content",
        color=discord.Color.gold(),
    )
    highlight_embed.set_author(
        name=reaction.message.author.display_name,
        icon_url=reaction.message.author.avatar.url if reaction.message.author.avatar else None,
    )
    highlight_embed.add_field(name="Channel", value=reaction.message.channel.mention)
    highlight_embed.add_field(
        name="Jump to Message",
        value=f"[Click here]({reaction.message.jump_url})",
        inline=False,
    )
    if reaction.message.attachments:
        highlight_embed.set_image(url=reaction.message.attachments[0].url)
    highlight_embed.set_footer(text="Highlighted by the community")
    await highlights_channel.send(embed=highlight_embed)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    welcome_text = random.choice(welcome_templates).format(
        mention=member.mention,
        guild=member.guild.name,
    )
    human_member_count = len([m for m in member.guild.members if not m.bot])

    embed = discord.Embed(title="Welcome!", description=welcome_text, color=discord.Color.blurple())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Joined At", value=discord.utils.format_dt(member.joined_at, style="F"), inline=True)
    embed.add_field(name="Member Count", value=str(human_member_count), inline=True)
    embed.set_footer(text=f"We're glad you're here, {member.name}!")
    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if not channel:
        return

    goodbye_text = random.choice(goodbye_templates).format(
        mention=member.mention,
        name=member.name,
    )
    human_member_count = len([m for m in member.guild.members if not m.bot])

    embed = discord.Embed(title="Someone Left...", description=goodbye_text, color=discord.Color.red())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="User", value=str(member), inline=True)
    embed.add_field(name="Remaining Members", value=str(human_member_count), inline=True)
    embed.set_footer(text="Hope they come back someday.")
    await channel.send(embed=embed)


@tasks.loop(minutes=30)
async def bump_reminder():
    channel = bot.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        await channel.send("Don't forget to `/bump` the server!")


@bot.command(name="confess")
async def confess(ctx: commands.Context, *, message: str):
    confession_channel = bot.get_channel(CONFESSION_CHANNEL_ID)
    if confession_channel:
        embed = discord.Embed(title="Anonymous Confession", description=message, color=discord.Color.purple())
        await confession_channel.send(embed=embed)
    await ctx.message.delete()
    await ctx.send("Your confession was sent anonymously.", delete_after=3)


@bot.command(name="verifybutton")
async def verifybutton(ctx: commands.Context):
    if ctx.author.id != OWNER_ID:
        await ctx.send("Only the server owner can use this.")
        return
    await ctx.channel.send("Click the button below to verify yourself!", view=VerificationView())
    await ctx.send("Verification button posted.")


@bot.command(name="joke")
async def joke(ctx: commands.Context):
    await ctx.send(random.choice(joke_list))


@bot.command(name="bully")
async def bully(ctx: commands.Context, member: discord.Member):
    if ctx.author.id != OWNER_ID:
        await ctx.send("Only the server owner can use this.")
        return
    await ctx.send(f"{member.mention} {random.choice(roast_lines)}")


@bot.command(name="purge")
async def purge(ctx: commands.Context, amount: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("Only the server owner can use this.")
        return
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=3)


ROLEPLAY_ACTIONS = {
    "kiss":   ("kissed",         "💋"),
    "hug":    ("hugged",         "🤗"),
    "cuddle": ("cuddled",        "🧸"),
    "love":   ("showed love to", "❤️"),
}


@bot.command(name="roleplay")
async def roleplay(ctx: commands.Context, action: str, member: discord.Member):
    action = action.lower()
    if action not in ROLEPLAY_ACTIONS:
        await ctx.send("Invalid action. Choose from: kiss, hug, cuddle, love")
        return
    verb, emoji = ROLEPLAY_ACTIONS[action]
    embed = discord.Embed().set_image(url=roleplay_gifs[action])
    await ctx.send(
        f"{ctx.author.mention} {verb} {member.mention}! {emoji}",
        embed=embed,
    )


@bot.command(name="kick")
async def kick(ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
    if not is_moderator(ctx):
        await ctx.send("You don't have permission to kick members.")
        return
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked. Reason: {reason}")


@bot.command(name="ban")
async def ban(ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
    if not is_moderator(ctx):
        await ctx.send("You don't have permission to ban members.")
        return
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned. Reason: {reason}")


@bot.command(name="timeout")
async def timeout_cmd(ctx: commands.Context, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
    if not is_moderator(ctx):
        await ctx.send("You don't have permission to timeout members.")
        return
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"{member} was timed out for {minutes} minutes. Reason: {reason}")


@bot.command(name="help")
async def help_command(ctx: commands.Context):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blurple())
    embed.add_field(name="?confess <message>", value="Send an anonymous confession", inline=False)
    embed.add_field(name="?verifybutton", value="Post the verification button (owner only)", inline=False)
    embed.add_field(name="?joke", value="Get a random joke", inline=False)
    embed.add_field(name="?bully <@member>", value="Roast a member (owner only)", inline=False)
    embed.add_field(name="?purge <amount>", value="Delete messages in bulk (owner only)", inline=False)
    embed.add_field(name="?roleplay <action> <@member>", value="Roleplay action — kiss, hug, cuddle, love", inline=False)
    embed.add_field(name="?kick <@member> [reason]", value="Kick a member from the server", inline=False)
    embed.add_field(name="?ban <@member> [reason]", value="Permanently ban a member", inline=False)
    embed.add_field(name="?timeout <@member> <minutes> [reason]", value="Temporarily mute a member", inline=False)
    embed.add_field(name="?hangman", value="Start a Hangman game in the game channel", inline=False)
    embed.add_field(name="?guess <letter>", value="Guess a letter in the active Hangman game", inline=False)
    embed.add_field(name="?xp", value="Check your XP and level progress", inline=False)
    embed.add_field(name="?xpleaderboard", value="View the top XP earners", inline=False)
    await ctx.send(embed=embed)


async def main():
    async with bot:
        await bot.add_cog(FilterCog(bot))
        await bot.add_cog(FishCog(bot))
        await bot.add_cog(HangmanCog(bot))
        await bot.add_cog(XPCog(bot))
        await bot.start(DISCORD_TOKEN)


asyncio.run(main())