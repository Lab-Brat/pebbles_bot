# pebbles_bot

## Table of content
- [Introduction](#introduction)
- [Deployment](#deployment)
- [Command Guide](#command-guide)

## Introduction
Pebbles is a bot which allows users to run shell commands on their Linux servers from Telegram.  
It is designed to be self-hosted. To get it up and running clone repository on the server, 
ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot, 
save its API hash to `./pebbles_api`, and just run it!

#### What It Can Do Now
At this stage Pebbles is not very sophisticated, it can:
- Run commands locally.
- Establish a SSH connection to another host and run commands there.

#### What It Will Do In The Future
- Support more built-in commands to do various tasks.
- Support public key authentication for SSH connections.
- Send information from the server to Telegram (upon completion of a script, for example).

#### Is it secure to run a public bot with direct access to a server?
The bot's channel itself is encrypted and secure by default. 
To verify this, run `/setprivacy` on `@BotFather`, then check if privacy settings are enabled.  
However, the bot can still be found by its handle and access to the server could be compromised. 
That is why Pebbles has a built-in whitelisting mechanism to only allow certain users to run 
commands on it.  
Example of `pebbles_whitelist`
```
0123456789
3141592653
0112358132
...
```
There is no limit on how much user IDs can be allowed, but the list cannot be empty. User ID 
can be obtained from a public bot `@userinfobot`, by calling `/start` command on it.  
So yeah, I'd say it is pretty secure :)


## Deployment
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
- Authorize users to use the bot by creating a whitelist file with user IDs.
```bash
echo "<id1>\n<id2>" > pebbles_whitelist
```
- Run Pebbles
```bash
python main.py
```

## Command Guide
- `/start` -> start interacting with Pebbles.
- `/help` -> print all available commands.
- `/mode` -> choose Pebbles mode
  - `local`: run commands on the server it's deployed
  - `remote`: run commands on the remote server. To use this option a connection must be first established by `/login`.
- `/login` -> establish a SSH connection to a remote host. User will be prompted for:  
  - IP address or hostname.  
    If port is not specified (8.8.8.8:22) then port 22 will be used.
  - username
  - password  
    If `~/.ssh/config` has connection information (key and/or user), connection will still be established if a wrond password is entered.
  - confirmation  
    select `Yes` to establish a connection, `No` to cancel.
- `/logout` -> to terminate the SSH connection
- `/run` -> run a shell command, where it runs depends on `/mode`. After command call user will be prompted to enter a command, stdout or stderr will be returned
