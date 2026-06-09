# Zizi — Discord Bot

A feature-rich Discord bot built with **discord.py**, offering moderation tools, fun games, social interactions, an XP leveling system, and community utilities — all through Discord's native slash command interface.

---

## Features at a Glance

| Category      | Features                                                          |
| ------------- | ----------------------------------------------------------------- |
| Moderation    | Kick, Ban, Timeout, Purge, Auto word filter                       |
| Games         | Hangman, Fish mini-game                                           |
| Social        | Kiss, Hug, Cuddle, Love (Milk & Mocha GIFs)                       |
| XP & Leveling | Automatic XP gain, Level-up announcements                         |
| Community     | Anonymous Confessions, Highlights Board, Welcome/Goodbye Messages |
| Utility       | Verification Button, Bump Reminders, Jokes                        |

---

# Commands

## Moderation

> Requires the **Moderator** role unless otherwise noted.

| Command                                | Description                         |
| -------------------------------------- | ----------------------------------- |
| `/kick <member> [reason]`              | Kick a member from the server       |
| `/ban <member> [reason]`               | Permanently ban a member            |
| `/timeout <member> <minutes> [reason]` | Temporarily mute a member           |
| `/purge <amount>`                      | Bulk-delete messages *(Owner Only)* |

### Automatic Moderation

The bot automatically removes and warns users for:

* Hard slurs or hate speech
* Discord invite links (advertising)
* Spam messages containing 10+ repeated characters

Examples:

```text
heyyyyyyyyyyyyyyyyyyyy
aaaaaaaaaaaaaaaaaaaaaa
discord.gg/example
```

---

## Games

### Hangman

| Command           | Description                        |
| ----------------- | ---------------------------------- |
| `/hangman`        | Start a new Hangman game           |
| `/guess <letter>` | Guess a letter in the current game |

### Fish Mini-Game

Every **200 messages**, a fish spawns in the server.

Members compete by clicking the **Catch** button.

The first user to click:

* Catches the fish
* Increases their personal fish count
* Claims the catch before anyone else

---

## Social Commands

Powered by Milk & Mocha GIFs.

| Command            | Description          |
| ------------------ | -------------------- |
| `/kiss <member>`   | Send a kiss 💋       |
| `/hug <member>`    | Send a hug 🤗        |
| `/cuddle <member>` | Send a cuddle 🧸     |
| `/love <member>`   | Express your love ❤️ |

---

## XP & Leveling

Members earn XP automatically while chatting.

### XP Rules

* 5 XP per message
* XP is awarded in the configured XP channel
* Level-up announcements are sent automatically

### Command

| Command  | Description                       |
| -------- | --------------------------------- |
| `/level` | Display your current level and XP |

---

## Community Features

### Anonymous Confessions

| Command              | Description                  |
| -------------------- | ---------------------------- |
| `/confess <message>` | Post an anonymous confession |

Messages are sent anonymously to the configured confessions channel.

---

### Highlights Board

Messages automatically appear in the highlights channel when:

* They receive reactions from **2 or more unique users**

The repost includes:

* Original author
* Message content
* Attached images
* Jump-to-message button

---

### Welcome & Goodbye System

The bot automatically sends embedded messages when:

* A member joins
* A member leaves

Features include:

* Randomized welcome messages
* Randomized goodbye messages
* Current member count

---

## Utility Commands

| Command           | Description                                 |
| ----------------- | ------------------------------------------- |
| `/verifybutton`   | Post the verification button *(Owner Only)* |
| `/joke`           | Get a random joke                           |
| `/bully <member>` | Roast a member *(Owner Only)*               |

---

## Verification System

The bot can create a verification panel.

Users simply:

1. Click **Verify**
2. Receive the configured **Verified** role

This helps protect servers from bots and unverified members.

---

## Bump Reminders

The bot automatically sends reminders every **30 minutes** to encourage server bumping and improve server visibility.

---

# Setup

## Requirements

* Python 3.10+
* Git
* Discord Bot Token

---

## Clone the Repository

```bash
git clone https://github.com/tishxkpr21-tech/Discordbot.git
cd Discordbot
```

---

## Create a Discord Application

1. Open the Discord Developer Portal.
2. Create a new application.
3. Create a bot.
4. Enable the required intents:

   * Server Members Intent
   * Message Content Intent
5. Copy your bot token.

---

## Configuration

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
```

> **Never commit your token or `.env` file.**

---

# Running the Bot

## Linux / macOS

```bash
chmod +x run.sh
./run.sh
```

## Windows

Simply double-click:

```text
windows.bat
```

Or run from Command Prompt:

```cmd
windows.bat
```

---

# Automatic Environment Setup

Both launcher scripts automatically handle setup.

### Linux / macOS (`run.sh`)

* Creates a virtual environment (`venv`) if missing
* Activates the virtual environment
* Checks required dependencies
* Installs missing packages automatically
* Launches the bot

### Windows (`windows.bat`)

* Creates a virtual environment (`venv`) if missing
* Activates the virtual environment
* Checks required dependencies
* Upgrades pip when needed
* Installs missing packages automatically
* Launches the bot

No manual dependency installation is required.

---

## Manual Start (Optional)

If the virtual environment is already active:

```bash
python Services/zizi.py
```

---

# Project Structure

```text
Discordbot/
├── BOT/
│   └── config.py
│
├── Services/
│   ├── zizi.py
│   ├── filter.py
│   ├── hangman.py
│   └── fishgame.py
│
├── .env
├── .gitignore
├── run.sh
├── windows.bat
└── README.md
```

---

## File Overview

| File                   | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| `BOT/config.py`        | Stores channel IDs, role IDs, and configuration   |
| `Services/zizi.py`     | Main bot logic, events, XP system, slash commands |
| `Services/filter.py`   | Auto-moderation system                            |
| `Services/hangman.py`  | Hangman game implementation                       |
| `Services/fishgame.py` | Fish spawning and catch system                    |
| `run.sh`               | Linux/macOS launcher                              |
| `windows.bat`          | Windows launcher                                  |

---

# Tech Stack

* Python
* discord.py
* python-dotenv

---

# Security Notes

* Never share your bot token
* Keep `.env` private
* Restrict owner-only commands
* Regularly review bot permissions
* Use Discord role permissions appropriately

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit your changes

```bash
git commit -m "feat: add new feature"
```

4. Push your branch

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

# License

This project is open source. Contributions and forks are welcome.