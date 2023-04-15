## Table of content
- [Table of content](#table-of-content)
- [Introduction](#introduction)
    - [What It Can Do Now](#what-it-can-do-now)
    - [What It Will Do In The Future](#what-it-will-do-in-the-future)
    - [Is it secure to run a public bot with direct access to a server?](#is-it-secure-to-run-a-public-bot-with-direct-access-to-a-server)
- [Deploy](#deploy)
- [Run Pebbles](#run-pebbles)
- [Command Guide](#command-guide)
- [Prefix](#prefix)
    - [Running Pebbles in a Docker container](#running-pebbles-in-a-docker-container)
    - [Configuration file](#configuration-file)

## Introduction
Pebbles is a bot which allows users to run shell commands on their Linux servers from Telegram.  
There are only 3 steps to get it up and running:
1. Ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot and save its API key.
2. Install the bot on the server where you wish to run commands using Python pip.
3. Configure environment variables and run it!

#### What It Can Do Now
At this stage Pebbles is not very sophisticated, it can:
- Run commands locally.
- Establish a SSH connection to another host and run commands there.
- Send a notification by piping stdout.
- Users whitelist - only whitelisted users can run commands on the bot.

#### What It Will Do In The Future
- More built-in commands to do various tasks without entering long commands.
- Commands whitelist - only whitelisted commands can be run on the bot.
- Log parser that will block users or even shut the bot down if it detects a malicious activity.

#### Is it secure to run a public bot with direct access to a server?
The bot's channel is encrypted via Telegram's proprietary protocol - MTProto, and the API 
also uses appropriate security measures, therefore there are no issues from Telegram's side.
However, the bot is still a public service, and anyone on the internet can attempt to use it 
(if they find bot's handle). That is why Pebbles has a whitelisting mechanism to only allow 
certain users to run commands on it.  
In general I'd say it's pretty safe to use, but don't use it on important production servers 😅


## Deploy
- Ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot, then save it's API key
- Install the bot with pip `python -m pip install pebbles_bot`
  **Note** Alternatively the bot can be ran in a container, see [Prefix](#prefix)
- Define 2 environment variables:
  - `PEBBLES_BOT_TOKEN` - the API key of the bot
  - `PEBBLES_BOT_USERS` - a comma-separated list of Telegram user IDs that will be whitelisted.
    User ID can be obtained from a public bot `@userinfobot`, by calling `/start` command on it.  
- **Optionally** a yaml configuration file can be used to list users and set other options.
  See [Configuration file](#configuration-file) for more details.


## Run Pebbles
Pebbles provides two modes of operation: Proxy and Notification modes. 
In Proxy mode, will run commands that users send from Telegram on the server it's deployed on. 
And in Notification mode it will send a Linux command/service output to the user from the server.  

Run in proxy mode:
```bash
pebot
```

Send notifications with Pebbles:
```bash
echo 'Testing Notifications!' | pebot --notify
```

## Command Guide
- `/start` -> start interacting with Pebbles.
- `/help` -> print all available commands.
- `/mode` -> choose Pebbles mode
  - `local`: run commands on the server it's deployed
  - `remote`: run commands on the remote server. To use this option a connection must be first established by `/login`.
- `/login` -> establish a SSH connection to a remote host using information from `~/.ssh/config`. User will be prompted for:
  - hostname  
    should be the same as in `~/.ssh/config`
  - confirmation  
    select `Yes` to establish a connection, `No` to cancel.
- `/logout` -> to terminate the SSH connection
- `/run` -> run a shell command, where it runs depends on `/mode`. After command call user will be prompted to enter a command, stdout or stderr will be returned


## Prefix
#### Running Pebbles in a Docker container
**Note** This is not the recommended installation method, more like a fun alternative 😉

Create a `$HOME/.pebbles/pebbles.yaml` configuration file first 
(`.pebbles` will be mounted to the container) and run:
```bash
docker run -d --name pebot \
              --volume $HOME/.pebbles:/root/.pebbles \
              labbratnet/pebbles:0.1.1
```

Alternatively, there is a Docker image for this bot in `Docker/Dockerfile` 
which can be customized. To use it, navigrate to `Docker` and run:
```bash
docker build -t pebbles .
docker run -d --name pebot \
              --volume $HOME/.pebbles:/root/.pebbles \
              pebbles
```

#### Configuration file
The default location is `$HOME/pebbles.yaml`, but it can be changed by setting the `PEBBLES_CONFIG` environment variable.  
Example of the configuration file:
```yaml
whitelist_ids:
  - 123456789
  - 987654321
```
**Note** If both environment variables and configuration file are defined, the environment variables will take precedence.
