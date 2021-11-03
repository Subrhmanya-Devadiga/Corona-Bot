from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests
import bs4

app = Flask(__name__)
chatbot = ChatBot('ChatBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("brain_files/")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if userText.startswith("#"):
        userText = userText[1:]
        cases = get_covid_detail_bd(userText)
        return(str(cases))
    else:
        answ = str(chatbot.get_response(userText))
        return(str(answ))
        

def get_html_data(url):
    data = requests.get(url).text
    return data


def get_covid_detail_bd(country):
    url = "https://worldometers.info/coronavirus/country/"+country+"/"
    print(url)
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data, 'lxml')
    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")
    all_detail =""
    for block in info_div[:3]:
        if block != None:
            text = block.find("h1", class_=None).text
            count = block.find("span", class_=None).text
            all_detail = all_detail + text + " " + count +"\n"
    return all_detail



if __name__ == "__main__":
    app.run()
