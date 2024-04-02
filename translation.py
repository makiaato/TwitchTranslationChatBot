import os
import json
import csv
import re
from twitchio.ext import commands
from twitchio.ext import routines
import deepl 

CLIENT_ID = ''
CLIENT_SECRET = ''
ACCESS_TOKEN = ''
REFRESH_TOKEN = ''
AUTH_KEY = '' # for DeepL
SOURCE_LANGUAGE = '' # the programming code is customized such that only japanese characters are filtered. If you ever want to use other source languages, then you've to remove the filter
TARGET_LANGUAGE = ''
CHANNEL_URL = 'ENTER_CHANNEL_URL_HERE'

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=[CHANNEL_URL])

    async def event_ready(self):
        # Bot says 'None' first, when no routine is set
        print(f'Logged in as | {self.nick}')
        print('Bot is ready!')
        await self.get_channel(CHANNEL_URL).send('Translation-Bot is ready! SeriousSloth')

    # chat messages are incoming from here by the 'message' variable
    async def event_message(self, message):
        if message.echo:
            return
        translation_result = translate(message.content)        
        if translation_result:
            await message.channel.send(f'{message.author.name}: {translation_result}')

    @routines.routine(seconds=900.0)
    async def check_access_token():
        if not is_access_token_valid():    
            refresh_access_token()
    check_access_token.start()

def read_credentials():
    with open('config.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i == 1:
                globals()['CLIENT_ID'] = row[0]
                globals()['CLIENT_SECRET'] = row[1]
                globals()['ACCESS_TOKEN'] = row[2]
                globals()['REFRESH_TOKEN'] = row[3]
                globals()['AUTH_KEY'] = row[4]
                globals()['SOURCE_LANGUAGE'] = row[5]
                globals()['TARGET_LANGUAGE'] = row[6]
    print('CSV-File successfully found.')

def write_credentials():
    with open('config.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['CLIENT_ID', 'CLIENT_SECRET', 'ACCESS_TOKEN', 'REFRESH_TOKEN', 'AUTH_KEY', 'SOURCE_LANGUAGE', 'TARGET_LANGUAGE'])
        writer.writerow([CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN, AUTH_KEY, SOURCE_LANGUAGE, TARGET_LANGUAGE])
    print('Successfully refreshed credentials.')

def is_access_token_valid():
    validation_result = os.popen(f"curl -X GET \"https://id.twitch.tv/oauth2/validate\" -H \"Authorization: OAuth {ACCESS_TOKEN}\"").read()
    parsed_validation_result = json.loads(validation_result)
    if 'expires_in' in parsed_validation_result:
        if parsed_validation_result['expires_in'] > 2400:
            return True
        else:
            return False
    print('Access Token Validation check failed.')

def refresh_access_token():    
    refresh_request_result = os.popen(f"curl -X POST \"https://id.twitch.tv/oauth2/token\" -H \"Content-Type: application/x-www-form-urlencoded\" -d \"grant_type=refresh_token&refresh_token={REFRESH_TOKEN}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}\"").read()
    parsed_refresh_request_result = json.loads(refresh_request_result)
    if 'access_token' in parsed_refresh_request_result:        
        globals()['ACCESS_TOKEN'] = parsed_refresh_request_result['access_token']
    else:
        print('Couldn\'t refresh Access Token. Check Refresh Token.')
    write_credentials()

def translate(source_text):
    source_text_cleaned = re.sub(r'[^\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]', '', source_text)
    if source_text_cleaned:
        result = TRANSLATOR.translate_text(source_text, source_lang=SOURCE_LANGUAGE, target_lang=TARGET_LANGUAGE)
        return result.text

read_credentials()
if not is_access_token_valid():    
    refresh_access_token()
TRANSLATOR = deepl.Translator(AUTH_KEY)
bot = Bot()
bot.run()
