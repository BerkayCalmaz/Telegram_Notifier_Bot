import threading
import telebot
import os
from flask import Flask, request

API_KEY = os.environ.get("BOT_API_KEY")
bot = telebot.TeleBot(API_KEY)

CHAT_ID = {}  #The user should add the possible reviewers' GithubID and their ChatId to this dictionary.
username_chatId_dict = {}


@bot.message_handler(commands=['getMyChatId'])
def getChatId(message):
    chatId = message.json["from"]["id"]
    bot.reply_to(message, chatId)

def validateGithubIdChatIdPair(message):
    request = message.text.split()
    if len(request) != 3 or request[0][0] == '/' or request[0] != "setGithubIdChatIdPair":
        return False
    else:
        return True

@bot.message_handler(func=validateGithubIdChatIdPair)
def setGithubIdChatIdPair(message):
        request = message.text.split()
        githubId = str(request[1])
        chatId = request[2]
        CHAT_ID[githubId] = chatId
        bot.reply_to(message, "The Github ID: " + githubId + " is set with the chat ID: " + CHAT_ID[githubId])

app = Flask(__name__)

# When an action happens in the repository, the payload is redirected here by ngrok.
@app.route('/payload', methods=['POST'])
def github_payload():
    data = request.json
    if data["action"] == "review_requested":
        #Only gets the latest reviewer to not spam previous reviewers
        latestReviewer = data["pull_request"]["requested_reviewers"][-1]

        if CHAT_ID[latestReviewer["login"]] is None:
            raise ValueError("The reviewer's chat id is not saved!")

        repository = data["repository"]["name"]
        requester = data["sender"]["login"]
        bot.send_message(chat_id=CHAT_ID[latestReviewer["login"]],
                         text="Dear: " + latestReviewer["login"] + " you have been assigned to a new pull request on the repository: " +
                         repository + " by: " + requester)
    else:
        print("The action is not a request of a review")
    return request.data, 200


if __name__ == "__main__":
    # Create another thread since bot.polling() and flask cannot run at the same thread
    threading.Thread(target=lambda: app.run(port=5000)).start()
    bot.polling()
