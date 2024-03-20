# Telegram_Notifier_Bot
This bot uses Python/Flask and the Telegram API to connect to a repository and notify the reviewer of a PR through Telegram. First, the user should add the pair of GithubID - TelegramChatId to the bot by writing "setGithubIdChatIdPair <GitHubID> <ChatID>". Then, whenever a PR opens in the repository, the reviewer will be notified if he/she is saved in the program. Currently, this bot does not allow public use since it is hardcoded for a specific repository webhook, but it is created to showcase the possibilities of a Telegram Bot in a simple way..
