import re, discord
from discord.ext import commands

banned_words = {
    "nigger", "nigga",
    "chink", "kike", "gook", "wetback", "beaner", "towelhead", "raghead",
    "faggot", "tranny",
    "retard",
    "kys", "kill yourself", "kill ur self", "neck yourself",
    "heil hitler", "white power",
}

BANNED_PATTERN = re.compile("|".join(re.escape(w) for w in banned_words), re.IGNORECASE)
INVITE_PATTERN = re.compile(r"discord\.gg/|discord\.com/invite/", re.IGNORECASE)
SPAM_PATTERN   = re.compile(r"(.)\1{9,}")


class FilterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _warn_and_delete(self, message, warning):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, {warning}", delete_after=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        if BANNED_PATTERN.search(content):
            await self._warn_and_delete(message, "that language isn't welcome here.")
            return

        if INVITE_PATTERN.search(message.content):
            await self._warn_and_delete(message, "advertising other servers isn't allowed.")
            return

        if SPAM_PATTERN.search(content):
            await self._warn_and_delete(message, "please don't spam.")
            return


async def setup(bot):
    await bot.add_cog(FilterCog(bot))