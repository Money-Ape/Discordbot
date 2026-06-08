# Zizi — Discord Bot

A feature-rich Discord bot built with **discord.py**, offering moderation tools, fun games, social interactions, an XP leveling system, and community utilities — all via Discord's native slash command interface.

---

## Features at a Glance

| Category | Features |
|---|---|
| Moderation | Kick, Ban, Timeout, Purge, Auto word filter |
| Games | Hangman, Fish mini-game |
| Social | Kiss, Hug, Cuddle, Love (Milk & Mocha GIFs) |
| XP & Leveling | Auto XP gain, level-up announcements |
| Community | Anonymous confessions, Highlights board, Welcome/Goodbye messages |
| Utility | Verification button, Bump reminders, Jokes |

---

## Commands

### Moderation
> Requires the **Moderator** role unless noted.

| Command | Description |
|---|---|
| `/kick <member> [reason]` | Kick a member from the server |
| `/ban <member> [reason]` | Permanently ban a member |
| `/timeout <member> <minutes> [reason]` | Temporarily mute a member |
| `/purge <amount>` | Bulk-delete messages in a channel *(owner only)* |

The bot also **automatically deletes messages** and warns the user for:
- Messages containing hard slurs or hate speech
- Discord server invite links (advertising)
- Spam (10+ repeated characters in a row)

---

### Games

| Command | Description |
|---|---|
| `/hangman` | Start a new Hangman game in the designated game channel |
| `/guess <letter>` | Guess a letter in the active Hangman game |

**Fish Mini-Game** — Every 200 messages sent in the server, a fish spawns with a **Catch** button. The first person to click it catches the fish and increments their personal fish count.

---

### Social (Milk & Mocha)

| Command | Description |
|---|---|
| `/kiss <member>` | Send a kiss GIF to another member 💋 |
| `/hug <member>` | Send a hug GIF to another member 🤗 |
| `/cuddle <member>` | Send a cuddle GIF to another member 🧸 |
| `/love <member>` | Express love for another member ❤️ |

---

### XP & Leveling

| Command | Description |
|---|---|
| `/level` | Check your current level and total XP |

Members earn **5 XP per message** sent in the designated XP channel. The bot automatically announces level-up milestones.

---

### Community

| Command | Description |
|---|---|
| `/confess <message>` | Post an anonymous confession to the confessions channel |

**Highlights Board** — When a message receives reactions from **2 or more unique users**, it is automatically reposted to the highlights channel with a rich embed, including a jump link and any attached images.

**Welcome & Goodbye** — The bot sends randomized, embedded welcome messages when a member joins and goodbye messages when they leave, including the current member count.

---

### Utility

| Command | Description |
|---|---|
| `/verifybutton` | Post the verification button in a channel *(owner only)* |
| `/joke` | Get a random joke |
| `/bully <member>` | Roast a member with a random burn *(owner only)* |

**Verification** — Members click the Verify button to automatically receive the `Verified` role.

**Bump Reminders** — The bot pings the reminder channel every **30 minutes** to prompt the server bump.

---

## Setup

### Prerequisites
- Python 3.10+
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))

### Installation

```bash
# Clone the repository
git clone https://github.com/tishxkpr21-tech/Discordbot.git
cd Discordbot

chmod +x run.sh
./run.sh
```
## bash script will automatically install the required modules for the System, and executes the bot everytime along with checking the dependencies...

### Configuration

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
```

> **Never commit your `.env` file.** It is already listed in `.gitignore`.

### Running the Bot

```bash
python Services/zizi.py
```

---

## Project Structure

```
DC-F/
├── BOT/
│   └── config.py          # All configuration — token, channel IDs, role IDs
├── Services/
│   ├── zizi.py            # Core bot — events, XP system, all slash commands
│   ├── filter.py          # Auto-moderation cog — slurs, invites, spam
│   ├── hangman.py         # Hangman game cog
│   └── fishgame.py        # Fish mini-game cog
├── .env                   # Secret token (not committed)
├── .gitignore
└── README.md
```

---

## Tech Stack

- [discord.py](https://discordpy.readthedocs.io/) — Discord API wrapper
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management

---

## License

This project is open source. Contributions and forks are welcome.
