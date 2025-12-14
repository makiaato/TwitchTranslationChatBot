import secrets
import requests
import csv
import re
import sys
import deepl 
import asyncio
from datetime import timedelta
from twitchio import eventsub
from twitchio.ext import commands
from twitchio.ext import routines

CLIENT_ID = ''
CLIENT_SECRET = ''
ACCESS_TOKEN = ''
REFRESH_TOKEN = ''
CHANNEL_URL = ''
BOT_USERNAME = ''
CHANNEL_USER_ID = ''
BOT_USER_ID = ''

AUTH_KEY = ''
TRANSLATOR = 0
SOURCE_LANGUAGE = ''
TARGET_LANGUAGE = ''

IGNORE_LIST = []

class Bot(commands.Bot):
    channel_partial_user = 0

    def __init__(self):
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_USER_ID,
            prefix="!"
        )

    async def setup_hook(self):
        print('setup_hook got called')
        await self.add_component(GeneralCommands())
        self.check_access_token.start()
        chat = eventsub.ChatMessageSubscription(broadcaster_user_id=CHANNEL_USER_ID, user_id=BOT_USER_ID)
        await self.subscribe_websocket(chat, as_bot=True)

    async def event_ready(self):        
        print(f'Trying to post test message in channel: {CHANNEL_URL} as {self.user}')
        self.channel_partial_user = self.create_partialuser(user_id=CHANNEL_USER_ID)
        await self.channel_partial_user.send_message(sender=BOT_USER_ID, message="Translation-Bot is awake! CoolStoryBob (v1.1.0)")

    async def event_message(self, message):
        """
        if message.chatter.id == BOT_USER_ID:            
            return
        """
        if message.chatter.name.lower() in IGNORE_LIST:            
            return        
        if message.text[:3] == '!ja':            
            return
        translation_result = translate(message.text, SOURCE_LANGUAGE, TARGET_LANGUAGE)        
        if translation_result:            
            await message.channel.send(f'{message.author.name}: {translation_result}')
        
    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        print(error)

    @routines.routine(delta=timedelta(minutes=15))
    async def check_access_token(self):
        if not is_access_token_valid():    
            refresh_access_token()

class GeneralCommands(commands.Component):
    @commands.command()
    async def ja(self, ctx: commands.Context[Bot], *, message: str):
        # todo
        print('entered !ja command')
        translation_result = reverse_translate(message, TARGET_LANGUAGE, 'JA')
        if translation_result:            
            await ctx.send(f'{ctx.chatter}: {translation_result}')

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

def read_credentials():
    found_config = False
    while not found_config:
        try:
            f = open('config.csv')
        except FileNotFoundError:
            input('Your config.csv couldn\'t be found. Press enter to let the script try again.')
        else:
            with f:
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
                        globals()['BOT_USERNAME'] = row[8]
            print('config-File successfully read.')
            found_config = True

def write_credentials():
    with open('config.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['CLIENT_ID', 'CLIENT_SECRET', 'ACCESS_TOKEN', 'REFRESH_TOKEN', 'AUTH_KEY', 'SOURCE_LANGUAGE', 'TARGET_LANGUAGE', 'CHANNEL_URL', 'BOT_USERNAME'])
        writer.writerow([CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN, AUTH_KEY, SOURCE_LANGUAGE, TARGET_LANGUAGE, CHANNEL_URL, BOT_USERNAME])
    print('Successfully refreshed credentials.')

def read_ignore_list():
        global IGNORE_LIST
        try:
            f = open('ignore_list.csv')
        except FileNotFoundError:
            print('Your ignore_list.csv couldn\'t be found. No users will be ignored.')
        else:
            with f:
                csv_reader = csv.reader(f, delimiter=',')
                for row in csv_reader:
                    for cell in row:
                        IGNORE_LIST.append(cell.lower())
            IGNORE_LIST = [name for name in IGNORE_LIST if name]
            print('ignore-File successfully read.')

def fetch_user_ids():
    print('Attempting to fetch User-IDs ...')
    url = f"https://api.twitch.tv/helix/users?login={CHANNEL_URL}&login={BOT_USERNAME}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Client-Id": CLIENT_ID
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    parsed_get_users_result = response.json()
    if 'data' in parsed_get_users_result:        
        globals()['CHANNEL_USER_ID'] = parsed_get_users_result['data'][0]['id']
        # to do, revert to index 1
        globals()['BOT_USER_ID'] = parsed_get_users_result['data'][0]['id']
        print('User-IDs fetched!')
    else:
        input('Couldn\'t fetch User-IDs. Check Channel_Url and Bot_Username. Pressing enter will close the script.')
        sys.exit()

def is_access_token_valid():
    url = "https://id.twitch.tv/oauth2/validate"
    headers = {
        "Authorization": f"OAuth {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    parsed_validation_result = response.json()    
    if 'expires_in' in parsed_validation_result:
        if parsed_validation_result['expires_in'] > 2400:
            return True
        else:
            return False
    else:        
        print('Access Token has expired (or has no expiration value).')
        return False
    
def generate_access_token_request():
    request_success = False
    while not request_success:
        print('Requesting Access Token for Twitch: Copy the following URL and paste it in your favourite browser.\n')
        xref_hash = secrets.token_hex(16)
        print(f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://localhost:3000&scope=user:read:chat+user:write:chat+user:bot&state={xref_hash}")
        response = input("\nAfter authorizing, you'll land on an error page/forward page, but also get a response from Twitch back in your URL-bar after a bit. Copy-Paste the whole url-response in this console and press enter: ")
        response_state_hash = response.split('state=')[-1]
        if xref_hash != response_state_hash:
            print('XRef-check failed! Try again.')
            continue
        response_url = re.search(r'code=(.*?)&', response)
        if response_url == None:
            print('An invalid response URL was entered or authorization was denied. Try again.')
            continue
        # the re.search method retrieves every matching string and returns groups. So we just want the first and only group
        authorization_code = response_url.group(1)
        url = f"https://id.twitch.tv/oauth2/token"
        data = {            
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        parsed_request_token_response = response.json()                
        if 'access_token' in parsed_request_token_response:
            globals()['ACCESS_TOKEN'] = parsed_request_token_response['access_token']
            globals()['REFRESH_TOKEN'] = parsed_request_token_response['refresh_token']
        else:
            print('Couldn\'t read Access Token from Twitch-API response. Access Token request failed. Script will start anew.')
            continue
        write_credentials()
        print('Successfully added Access Token and Refresh Token to credentials.')
        request_success = True

def refresh_access_token():
    print('Attempting to request new tokens ...')
    url = "https://id.twitch.tv/oauth2/token"
    data = {                    
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,        
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN        
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    parsed_refresh_request_result = response.json()    
    if 'access_token' in parsed_refresh_request_result:
        globals()['ACCESS_TOKEN'] = parsed_refresh_request_result['access_token']
        globals()['REFRESH_TOKEN'] = parsed_refresh_request_result['refresh_token']
        write_credentials()
    else:
        input('Couldn\'t refresh Access Token. Check Refresh Token. Pressing enter will close the script.')
        sys.exit()

def main():
    read_credentials()
    read_ignore_list()
    if ACCESS_TOKEN == '':
        generate_access_token_request()
    if not is_access_token_valid():
        refresh_access_token()
    fetch_user_ids()

    globals()['TRANSLATOR'] = deepl.DeepLClient(AUTH_KEY)

    async def runner():
            bot = Bot()
            await bot.add_token(ACCESS_TOKEN, REFRESH_TOKEN)
            await bot.start(load_tokens=False)
    asyncio.run(runner())

if __name__ == "__main__":
    main()
