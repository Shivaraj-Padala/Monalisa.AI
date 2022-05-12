import wikipedia
import config
import wolframalpha
import automation
from transformers import pipeline, Conversation
from googletrans import Translator, LANGUAGES
import requests

actions = {"hi" : "hi there !",
"who created you" : "I was created by shivaraj padala and his team",
"bye" : "bye bye", "good bye" : "don't say good bye, just say bye"} 

print('Starting Core Services...')
translator = Translator()
conversational_pipeline = pipeline("conversational")

def coreBrain(req):
    reqdata = Conversation(req)
    ans = (str(conversational_pipeline(reqdata)).splitlines())
    return ans[2].replace('bot >> ','')

def wolframeAlphaFun(req):
    try:
        bot_client = wolframalpha.Client(config.WOLFRAM_ALPHA_KEY)
        res = bot_client.query(req)
        answer = next(res.results).text.replace('Wolfram|Alpha','Monalisa.AI').replace('Stephen Wolfram','Shivaraj Padala')
        return answer
    except:
        return coreBrain(req)


def contextRouter(req):
    try:
        return eval(req)
    except:
        return wolframeAlphaFun(req)
        

def wikiData(req):
    wikiReq = req.replace('info','')
    try:
        return wikipedia.summary(wikiReq, sentences=3)
    except wikipedia.exceptions.PageError:
        return 'No information available'
    except wikipedia.exceptions.WikipediaException:
        return 'Something went wrong! 😅'

def textTranslator(req):
    extractedStr = ''
    transRequest = req.replace('translate text','').split(' ')
    lang = transRequest[1]
    for i in transRequest[2:]:
        extractedStr += f' {i}'
    try:
        translation = translator.translate(extractedStr,lang)
        tempTransStr = translation.text
        try:
            finTransStr = tempTransStr[:tempTransStr.index('&')]
            return 'translatedText ' + finTransStr
        except ValueError:
            return 'translatedText ' + translation.text
    except ValueError:
        return 'Invalid text translation query'

def detectText(req):
    detectReq = req.replace('detect text', '')
    detectLang = translator.translate(detectReq)
    return LANGUAGES[detectLang.src]


def getNews():
    news = ''
    try:
        newsResponse = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=5c34a419a9fe48c3a9b42a8223e76bbb')
        newsData = newsResponse.json()
        articlesData = newsData['articles']
        articleTitles = [i['title'] for i in articlesData]
        articleDescription = [j['description'] for j in articlesData]
        for fetch in range(10):
            news += f"news-Data {articleTitles[fetch]}  {articleDescription[fetch]} \n\n "#test <br>
        return news
    except:
        return 'Something went wrong! 😅'


class TelegramQuery():
    def __init__(self, req):
        self.req = req
    def action_Router(self):
        if 'press' or 'click' or 'move up' or 'move down' 'click' or 'scroll down' or 'scroll up' or 'move right' or 'move left' or 'type' in self.req:
            return automation.automateAction(self.req)
        try:
            return actions[self.req]
        except KeyError:
            if 'info' in self.req:
                return wikiData(self.req)
            elif 'translate text' in self.req:
                return textTranslator(self.req)
            elif 'detect text' in self.req:
                return detectText(self.req)
            elif 'news headlines' in self.req:
                return getNews()
            else:
                return contextRouter(self.req)