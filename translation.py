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
AUTH_KEY = ''
SOURCE_LANGUAGE = ''
TARGET_LANGUAGE = ''
CHANNEL_URL = ''

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=[CHANNEL_URL])

    async def event_ready(self):
        # Bot says 'None' first, when no routine is set
        print(f'Logged in as: {self.nick}')
        print(f'Now trying to post test message in channel: {self.nick}')
        await self.get_channel(CHANNEL_URL).send('Translation-Bot is ready! SeriousSloth')
    
    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)
        if message.content[:3] == '!ja':
            return
        translation_result = translate(message.content, SOURCE_LANGUAGE, TARGET_LANGUAGE)        
        if translation_result:
            await message.channel.send(f'{message.author.name}: {translation_result}')
        
    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        print(error)

    @commands.command()
    async def ja(self, ctx: commands.Context, *, phrase: str):
        translation_result = reverse_translate(phrase, TARGET_LANGUAGE, 'JA')
        if translation_result:
            await ctx.send(f'{ctx.author.name}: {translation_result}')

    @routines.routine(seconds=900.0)
    async def check_access_token():
        if not is_access_token_valid():    
            refresh_access_token()    

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
                globals()['CHANNEL_URL'] = row[7]
    print('CSV-File successfully found.')

def write_credentials():
    with open('config.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['CLIENT_ID', 'CLIENT_SECRET', 'ACCESS_TOKEN', 'REFRESH_TOKEN', 'AUTH_KEY', 'SOURCE_LANGUAGE', 'TARGET_LANGUAGE', 'CHANNEL_URL'])
        writer.writerow([CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN, AUTH_KEY, SOURCE_LANGUAGE, TARGET_LANGUAGE, CHANNEL_URL])
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
        globals()['REFRESH_TOKEN'] = parsed_refresh_request_result['refresh_token']
    else:
        print('Couldn\'t refresh Access Token. Check Refresh Token. Your Access Token might expire soon.')
        return        
    write_credentials()

def translate(source_text, source_l, target_l):
    if source_l == 'JA':
        source_text_cleaned = re.sub(r'[^\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]', '', source_text)
    else:
        source_text_cleaned = source_text
    if source_text_cleaned:
        # DeepL-API recognizes only EN as source-value, no EN-US or EN-GB
        result = TRANSLATOR.translate_text(source_text, source_lang=source_l[:2], target_lang=target_l)
        return result.text
    
def reverse_translate(source_text, source_l, target_l):
    if TRANSLATOR.translate_text(source_text, target_lang='EN-US').detected_source_lang == source_l[:2]:        
        source_text_cleaned = source_text
    else:
        return ''
    if source_text_cleaned:        
        result = TRANSLATOR.translate_text(source_text, source_lang=source_l[:2], target_lang=target_l)
        return result.text
    
def generate_access_token_request():
    request_success = False
    while not request_success:
        print('Requesting Access Token for Twitch: Copy the following URL and paste it in your favourite browser.\n')
        xref_hash = os.urandom(16).hex()
        print(f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://localhost:3000&scope=chat:read+chat:edit&state={xref_hash}")
        response = input("\nAfter authorizing, you'll land on an error page, but also get a response from Twitch back in your URL-bar. Paste the whole response in this console and press enter: ")
        response_state_hash = response.split('state=')[-1]
        if xref_hash != response_state_hash:
            print('XRef-check failed! Try again.\n')
            continue
        response_url = re.search(r'code=(.*?)&', response)
        if response_url == None:
            print('An invalid response URL was entered or authorization was denied. Try again.\n')
            continue
        authorization_code = response_url.group(1)
        request_token_response = os.popen(f"curl -X POST \"https://id.twitch.tv/oauth2/token\" -H \"Content-Type: application/x-www-form-urlencoded\" -d \"client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={authorization_code}&grant_type=authorization_code&redirect_uri=http://localhost:3000\"").read()
        parsed_request_token_response = json.loads(request_token_response)
        if 'access_token' in parsed_request_token_response:
            globals()['ACCESS_TOKEN'] = parsed_request_token_response['access_token']
            globals()['REFRESH_TOKEN'] = parsed_request_token_response['refresh_token']
        else:
            print('Couldn\'t read Access Token from Twitch-API response. Access Token request failed. Script will start anew.\n')
        write_credentials()
        print('Successfully added Access Token and Refresh Token to credentials.')
        request_success = True

read_credentials()
if ACCESS_TOKEN == '':
    generate_access_token_request()
if not is_access_token_valid():    
    refresh_access_token()
TRANSLATOR = deepl.Translator(AUTH_KEY)

bot = Bot()
bot.run()
