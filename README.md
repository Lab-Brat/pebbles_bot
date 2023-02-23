# pebbles_bot

## Table of content
- [Introduction](#introduction)
- [How-To](#how-to)

## Introduction
Pebbles is a bot which allows users to run shell commands on their Linux servers from Telegram.  
It is designed to be self-hosted. To get it up and running clone repository on the server, 
ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot, 
save its API hash to `./pebbles_api`, and just run it!

**What It Can Do Now**  
At this stage Pebbles is not very sophisticated, it can:
- Run commands locally.
- Establish a SSH connection to another host and run commands there.

**What It Will Do In The Future**
- Support more built-in commands to do various tasks.
- Support public key authentication for SSH connections.
- Send information from the server to Telegram (upon completion of a script, for example).

## How-To
#### Installing
- Clone the repository and navigate to it
```bash
git clone https://github.com/Lab-Brat/pebbles_bot.git && cd pebbles_bot
cd pebbles_bot
```
- Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate
python -m pip install pytelegrambotapi paramiko
```
- Ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot, then save it's API hash
```bash
bot_api=<API_HASH>
echo $bot_api >> pebbles_api
```
- Run Pebbles
```
python main.py
```

#### Using Pebbles
- find Pebbles bot in Telegram search, and initiate a conversation
- type `/help` to see available commands
- type `/login` to establish a SSH connection to a remote host. User will be prompted for:
  - IP address or hostname. If port is not specified (8.8.8.8:22) then port 22 is used
  - username
  - password. If `~/.ssh/config` has connection information, connection will still be established if password is wrong
- after that a confirmation message will be displayed, to confirm user must press on `Yes`
- after connection is established, commands can be run by first calling `/run`, and then typing the command in the next message
- type `/logout` to break the SSH connection
