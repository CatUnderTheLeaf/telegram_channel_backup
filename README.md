# telegram_channel_backup

The idea is very simple: you have a Telegram channel and just want to automatically backup your posts to GitHub.

Sounds easy. But how to do this with less hassle and without registering of additional Telegram and GitHub Apps IDs? Just follow these steps.

### 1. Create a Telegram bot and get its token

- In Telegram find `@BotFather`, Telegram’s tool for creating and managing bots.
- Use the `/newbot` command to create a new bot.
- `@BotFather` will ask you for a name and username, then generate an authentication token for your new bot.

   > The 'name' of your bot is displayed in contact details and elsewhere.

   > The 'username' is a short name, used in search, mentions and t.me links. Usernames are 5-32 characters long and not case sensitive – but may only include Latin characters, numbers, and underscores. Your bot's username must end in 'bot', like 'tetris_bot' or 'TetrisBot'.

   > The 'token' is a string, like `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`, which is required to authorize the bot and send requests to the Bot API. Keep your token secure and store it safely, it can be used by anyone to control your bot.

   > Unlike the bot’s name, the username cannot be changed later – so choose it carefully.

- Add newly created bot to your channel as subscriber or administrator.

### 2. Create a (private) repository for channel backup

### 3. Create a personal access token (lets call it AUTH)

Just follow the [instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token). Be sure to grant repository read-and-write permissions for `actions` and `contents`. You can also restrict permissions to only this repository.

### 4. Add BOT and AUTH tokens to your channel backup repository as secrets

Follow the [instructions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository) and add `AUTH_TOKEN` and `BOT_TOKEN` secrets

### 5. Create an action workflow

- Copy code from [action_workflow_example](action_workflow_example.yml)
- Replace `CHANNEL_REPO` and `BRANCH` placeholders with your names (13-14 lines)
- Action is triggered on schedule at 23:30 UTC every day (line 7). Look [here](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) if you want to change it.

 
