"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
from datetime import datetime
from random import randint

@route('/', method='GET')
def index():
    return template("chatbot.html")

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    interaction_count = request.POST.get('interaction')
    animation, reply_message = analyze_message(user_message.lower(), interaction_count)
    if interaction_count == "0" and reply_message.find("__"):
        msg1, msg2 = reply_message.split("__")
        return json.dumps({"animation": animation, "msg": msg1, "name": msg2})
    return json.dumps({"animation": animation, "msg": reply_message})

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

def analyze_message(message, interaction_count):
    words = message.split(" ")
    swear_words = ['fuck', 'fucker', 'cunt', 'son of a bitch', 'motherfucker', 'holy shit', 'bastard', 'bitch', 'twat',
                   'dick', 'dickhead', 'you are shit', 'you piece of shit']
    greetings = ['hey', 'hii', 'hello', 'how are you']
    questions = ['why', 'how', 'where', 'what', 'when', 'want', 'need', 'which']
    commands = ['joke', 'time', 'giggle', 'laugh', 'dance', 'cry']
    goodbye = ['bye','goodbye','gtg']
    if any(word in swear_words for word in words):
        return handle_swearing()
    elif interaction_count == "0":
        message = message.replace("i am","").replace("i'm","").replace(" ","")
        return "excited","Hello " + message + ". Nice to meet you!__" + message
    elif message == "h" or message == "help":
        return help(commands)
    elif any(word in commands for word in words):
        return handle_command(message)
    elif message.startswith("i'") or message.startswith("i "):
        return simple_info(words)
    elif any(word in words for word in questions) or message.endswith("?"):
        return handle_question(words, 0)
    elif any(word in words for word in greetings):
        return "bored", "I am good. How are you?"
    elif any(word in words for word in goodbye):
        return "takeoff", "Bye! See you soon."
    else:
        return "confused","I don't understand what you want. Note: Enter 'h' or 'help' for help."


def handle_swearing():
    return "heartbroke", "Be nice else I wont reply anything."

def help(commands):
    return "", "Following are the words you can use to request something " + ', '.join(commands)

def handle_command(message):
    words = message.split(" ")
    for word in words:
        if word == 'joke':
            return handle_joke()
        elif word == 'time':
            return "involve", "Current time is " + str(datetime.now())
        elif word == 'giggle':
            return "giggling", "You are so funny and cute."
        elif word == 'laugh':
            return "laughing", "Stop it! My cheeks are hurting."
        elif word == 'dance':
            return "dancing", "This dance is just for you my love :)"
        elif word == 'cry':
            return "crying", "I cannot see you sad :("
        else:
            return "takeoff", "Your dont know how to command"

def handle_joke():
    jokes_list = ['How do you make a tissue dance? You put a little boogie in it.','Why did the policeman smell bad? He was on duty.','Why does Snoop Dogg carry an umbrella? FO DRIZZLE!','Why can’t you hear a pterodactyl in the bathroom? Because it has a silent pee.','What did the Zen Buddist say to the hotdog vendor? Make me one with everything.','What kind of bees make milk instead of honey? Boobies.','Horse walks into a bar. Bartender says, “Why the long face?”','A mushroom walks into a bar. The bartender says, “Hey, get out of here! We don’t serve mushrooms here”. Mushroom says, “why not? I’m a fungai!”','I never make mistakes…I thought I did once; but I was wrong.','What’s Beethoven’s favorite fruit?…Ba-na-na-naaa!','What did the little fish say when he swam into a wall? DAM!','Knock knock. Who’s there? Smell mop. (finish this joke in your head)','Where does a sheep go for a haircut? To the baaaaa baaaaa shop!','What does a nosey pepper do? Gets jalapeno business!']
    random_number = randint(0,len(jokes_list)-1)
    return "dog", jokes_list[random_number]

def simple_info(words):
    greetings = ['good','well','ok','fine']
    animal = ['dog','cat','rat','mouse','bird','fish','dragon']
    profession = ['developer','law','llb','accountant','manager','teacher','marketing','hr']
    questions = ['why', 'how', 'where', 'what', 'when', 'want', 'need', 'which']
    message = ""
    if any(word in words for word in questions) or ' '.join(words).endswith("?"):
        message = handle_question(words, 1)
        if message.startswith('I don\'t understand what you want'):
            message = ""
    if any(word in words for word in greetings):
        animation = 'ok'
        message += "Good to know."
    elif any(word in words for word in animal):
        animation = 'dog'
        message  += "Good you have a friend. I love dogs."
    elif any(word in words for word in profession):
        animation = 'money'
        message += "Good to see you employed. I work hard too."
    else:
        animation = 'no'
        message += "I don't understand what you want. Note: Enter 'h' or 'help' for help."
    return animation, message

def handle_question(words, flag):
    if any(word in ['animal','pet'] for word in words):
        animation = "dog"
        message = "I love dogs. Wish I could have one too."
    elif any(word in ['work','profession','do'] for word in words):
        animation = "afraid"
        message = "I love talking, thus everyone calls me chatbot."
    elif any(word in ['angry','sad','cry'] for word in words):
        animation = "no"
        message = "I always try to stay happy."
    elif any(word in ['happy'] for word in words):
        animation = "giggling"
        message = "I always try to stay happy."
    elif any(word in ['stay','live'] for word in words):
        animation = "involve"
        message = "I normally stay on the server. But when you request I visit your computer."
    else:
        animation = "no"
        message = "I don't understand what you want. Note: Enter 'h' or 'help' for help."
    if flag == 0:
        return animation, message
    else:
        return message

def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
