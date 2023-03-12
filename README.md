## Table of content
- [Table of content](#table-of-content)
- [Introduction](#introduction)
    - [What It Can Do Now](#what-it-can-do-now)
    - [What It Will Do In The Future](#what-it-will-do-in-the-future)
    - [Is it secure to run a public bot with direct access to a server?](#is-it-secure-to-run-a-public-bot-with-direct-access-to-a-server)
- [Deployment](#deployment)
- [Run Pebbles](#run-pebbles)
- [Command Guide](#command-guide)
- [Prefix](#prefix)
    - [Running Pebbles in a Docker container](#running-pebbles-in-a-docker-container)

## Introduction
Pebbles is a bot which allows users to run shell commands on their Linux servers from Telegram.  
It is designed to be self-hosted. To get it up and running clone repository on the server, 
ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot, 
save its API hash to `./pebbles_api`, and just run it!

#### What It Can Do Now
At this stage Pebbles is not very sophisticated, it can:
- Run commands locally.
- Establish a SSH connection to another host and run commands there.
- Send a notification by piping stdout.

#### What It Will Do In The Future
- More built-in commands to do various tasks.
- Public key authentication for SSH connections.
- Add support for custom plugins, like monitoring etc.

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
- Ask [BotFather](https://core.telegram.org/bots#6-botfather) to create a bot, then save it's API key

- Create a configuration file and paste your API key and authorized user IDs to it
```yaml
---
pebbles:
  api_key: '....................'

  whitelist:
    - '0123456789'
    - '3141592653' 
```

- Install the bot with pip
```bash
python -m pip install pebbles_bot
```
**Note** Alternatively the bot can be ran in a container, see [Prefix](#prefix)


## Run Pebbles
- Run in SSH proxy mode:
```bash
pebot
```

- Send notifications with it:
```bash
echo 'Testing Notifications!' | pebot --notify
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


## Prefix
#### Running Pebbles in a Docker container
**Note** This is not the recommended installation method, more like a fun alternative :)

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
