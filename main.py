import threading
import telegram_interface
import brain
from flask import Flask, render_template, request
import config
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api',methods=['GET'])
def api():
    QUERY = str(request.args['query']).strip(config.UNWANTED_CHARS).lower()
    finalQuery = QUERY.replace('addopcode','+')
    userQuery = brain.TelegramQuery(finalQuery)
    try:
        return str(userQuery.action_Router())
    except:
        return 'Something went wrong! 😅'

def fileFinder(fileToFind):
    for r,d,f in os.walk("/"):
        for files in f:
            if files == fileToFind:
                return os.path.join(r,files)

if __name__ == '__main__':
    telegram_thread = threading.Thread(target=telegram_interface.botEngine).start()
    server_thread = threading.Thread(target=app.run).start()
    print('\nInitializing Server...')
    print('Starting Monalisa.AI')