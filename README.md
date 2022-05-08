# pebbles_bot

## Table of contet
- [Introduction](#introduction)
- [How-To](#how-to)

## Introduction
Pebbles is a telegram bot, which is designed to allow Linux users to have access to their VMs by just using their phones.  
You can find Pebbles by searching for [@Pebbles_LinuxHelper_bot](https://t.me/Pebbles_LinuxHelper_bot) in Telegram global search.  
Alternatively, it is possible to clone the repo and run it locally. For that you need to ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot for you.

**What It Can Do Now**  
At this stage Pebbles is not very sophisticated, it can only do one thing: run a command with Paramiko library and return output to the user.  
\
**What It Will Do In The Future**
- Run commands with Ansible
- Run playbooks
- Support public key authentication
- Save credentials in a safe way (to reduce amount of IP/password entries)
- Logging
- Pass output from a VM to the user (upon completion of a task, for exemple)
- And much more!

## How-To
#### Using Pebbles
- find [@Pebbles_LinuxHelper_bot](https://t.me/Pebbles_LinuxHelper_bot) in Telegram search, and initiate a conversation
- type ```/help``` to see available commands
- type ```/login``` function to establish an SSH connection with your host. User will be promted for following information:
  - IP address or hostname in the form \<IP\>:\<port\>, for example 8.8.8.8:22
  - username 
  - password
  - after that a confirmation message is displayed with a Yes/No question
- after connection is established, commands can be run by first calling ```/run```, and then typing the command in the next message.
- ```/logout``` is used to break the SSH connection

#### Install and run locally
- Install dependencies
```
python -m pip install pytelegrambotapi paramiko fabric
```
- Clone the repository
```
git clone https://github.com/Lab-Brat/pebbles_bot.git && cd pebbles_bot
```
- Ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot for you, then store the bot hash at ```/home/$USER/bot_api.txt```
- Run the bot's main script
```
python main.py
```

