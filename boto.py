"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

swear_words = ['fuck','fucker','cunt','son of a bitch','motherfucker','holy shit','bastard','bitch','twat','dick','dickhead','you are shit','you piece of shit']
greetings = ['hey','hii','hello','how are you']
questions = ['why','how','where','what','when']
greetings_reply = "I am good. How are you?"
global_variables = {"last_message":"khblksafds","counter":0}


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    reply_message = analyze_message(user_message)
    global_variables["last_message"] = user_message
    global_variables["counter"] += 1
    return json.dumps({"animation": "inlove", "msg": reply_message})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def analyze_message(message):
    words = message.split(" ")
    if global_variables["counter"] == 0:
        return "Hello " + message + ". Nice to meet you!"
    elif global_variables["last_message"] == message:
        return "Dont repeat the same message again."
    elif any(word in swear_words for word in words):
        return "I dont talk with mannerless people."
    elif any(word in greetings for word in words) or message in greetings:
        return greetings_reply
    else:
        return "I dont understand what you want. Note: You can also give me commands. Enter h for help"

def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
