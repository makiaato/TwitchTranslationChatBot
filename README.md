# TwitchTranslationChatBot v1.0.0
## CURRENTLY WORKING ON
- definitely make thousands of mini-commits for readme changes



## DESCRIPTION
This repository aims to set up and execute a chat bot for [twitch.tv](https://www.twitch.tv/). It's customized for the channel [@blluist](https://www.twitch.tv/blluist). Therefore, the following tutorial will set up the bot with the aim to translate japanese messages to English. Rōmaji words are excluded as good as possible for the translation. But you can change the translation languages of course. The bot uses DeepL for translation (**credit card verification** is needed for the free version of DeepL-API, but no cost-subscription will be made). This ReadMe is also written for people with zero knowlege in programming. Those who are more skilled, can quick read the first words of the instructions and skip the rest safely. Additionally, the code is pretty short circuited and written while being hungry. 

The goal of this script is the following: Execute Bot-Behavior via a registered Twitch-User. The behavior reads messages on a Twitch-Channel, ignore every message that isn't your set Source Language, translate it to your Target Language with DeepL and post the result in the chat.

Constraints set by the Twitch-API: 
- 20 messages per 30 seconds (unmodded bot)
- 100 messages per 30 seconds (modded bot)
- Refresh Tokens expire 30 days after generation

Constraints set by the DeepL-API:
- maximum of 500k characters per month
   <details>
   
   <summary>Supported DeepL languages and their tags</summary>
   
   | Source Tag | Target Tag | Language |
   | --- | --- | --- |
   | BG | BG | Bulgarian |
   | CS | CS | Czech |
   | DA | DA | Danish |
   | DE | DE | German |
   | EL | EL | Greek |
   | EN | EN-GB and EN-US | English |
   | ES | ES | Spanish |
   | ET | ET | Estonian |
   | FI | FI | Finnish |
   | FR | FR | French |
   | HU | HU | Hungarian |
   | ID | ID | Indonesian |
   | IT | IT | Italian |
   | JA | JA | Japanese |
   | KO | KO | Korean |
   | LT | LT | Lithuanian |
   | LV | LV | Latvian |
   | NB | NB | Norwegian (Bokmål) |
   | NL | NL | Dutch |
   | PL | PL | Polish |
   | PT | PT-BR and PT-PT | Portuguese (Brazilian & all other Portuguese varieties) |
   | RO | RO | Romanian |
   | RU | RU | Russian |
   | SK | SK | Slovak |
   | SL | SL | Slovenian |
   | SV | SV | Swedish |
   | TR | TR | Turkish |
   | UK | UK | Ukrainian |
   | ZH | ZH | Chinese (simplified) |
   </details>



## SET UP INSTRUCTIONS
1. Register on Twitch and DeepL, if you haven't done yet. Preferably, use a nickname for the Twitch-Account that would fit your chat bot, because that account will be used to chat on your channel. In other words, it becomes the chat bot. 

2. Acquire API-Credentials for Twitch and DeepL. 
   1. For Twitch: Go to the [twitch-developers](https://dev.twitch.tv/) website and log into your Bot-Account. It should recognize your account if you've authorized the log-in once before. Click on the "Your Console"-Button on the right of the purple bar at the top of the page. Click on "Register Your Application" on the Applications-Widget. Name it fittingly (you'll read it later on again) and set the "OAuth Redirect URLs" for the time being of this repository to its default value "http://localhost:3000" (without the quotation marks). Select "Chat Bot" as category, check if the "Confidential" Client-Type-Option is selected and then click on "Create". You should be redirected back to your console now and your new app should be listed in the Applications Widget. Click on "Manage" on your app-entry. Scroll down to see your **Client ID**. This value is important and should be kept confidentially. This is metaphorically your username for the Twitch-API-World. Write your Client ID down or save it somewhere save. We'll need that later. Now create a **Client Secret** by just pressing the "New Secret" button. Handle it cautiously like your Client ID. This Client Secret is metaphorically your password in the Twitch-API-Underground-World. Write the Client Secret down, too. Both Client-Credentials are needed in the Initialization Instructions, later on. 

   2. For DeepL: Go to [DeepL](https://www.deepl.com/), register an account and verify as told by entering credit card information. Make sure that you don't accidentally subscribe to their pro-subscription. After that, you should be redirected to your account dashboard. Click on "API-Keys". Then click on "Create Key". Name it fittingly. After that, you can click the copy-to-clipboard-button for the API-Key-value and save the value somewhere safe. This API-Key works metaphorically as a username and as a password at the same time for the DeepL-API-Ghetto-World, so don't lose it. It's your **Authentication Key** for DeepL and has nothing to do with the Twitch-Credentials, because DeepL has their own API.

3. Download the Release-ZIP-file [here](https://github.com/makiaato/TwitchTranslationChatBot/releases) if you haven't done it yet! Extract the ZIP-File where you can find it easily.



## INITIALIZATION INSTRUCTIONS
1. Paste your relevant keys into the config_CHANGEME.csv (the file can be opened by Excel or similiar) directly under the respective categories/headers. You should have the following credentials ready now:
   - CLIENT_ID (Twitch)
   - CLIENT_SECRET (Twitch)   
   - AUTH_KEY (DeepL)

2. Set *SOURCE_LANGUAGE* to **JA** and *TARGET_LANGUAGE* to **EN-US** -- if you want to set other languages, you can change them there respectively. Also, set your channel by entering the channel name (not the whole URL, so instead of "twitch.tv/your_channel_name" use "your_channel_name" only). Let the other categories empty, the script will collect them for you. 
![Example image of the config.csv file.](/example_images/example_01.png)

3. Make sure to save as CSV-File, so **don't change the file type**!!

4. Rename the file from *config_CHANGEME.csv* to **config.csv** and you're done with the installation!

5. Start the bot by double-clicking the EXE-file. The console will give you further instructions that ought to be easy to follow.

6. After finishing the steps in the console window, if the bot says it's ready, then it's ready! For confirmation, the bot will post a boot-up message in your channel, too.



## STARTING/EXIT INSTRUCTIONS
**Starting/Restarting**: Just double-click the EXE-file (for Windows).

**Closing**: Just close the bash window.



## FEATURES
- bot can reverse translate from Source Langauge to Japanese by prepending the '!ja' command
- bot is locally hosted and credentials are bound by account. This means that you can execute the script from any computer and as long as you keep the credentials with it, then the same bot will be used



## FUTURE GOALS 
### Waiting/Acquire Feedback
Nothing big planned so far, just casually looking out for bugs. 



## QUIRKS IN CODE
### Japanese Filter
The code is customized such that only japanese characters are recognized through a filter, when you set the Source Language to Japanese. The filter uses a regex to recognize a [fixed set of japanese UTF-characters](http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml). So the filter quality is highly dependend on that. Also, mixed languages in a sentence are also coming through with Japanese as Source Language, as long as they have japanese characters. Meaning that a sentence like "遊びましょう please" will be recognized and used as translation target. 

### Error Handling
I currently use simple console outputs to give feedback on what happens and what might have caused an error. So no real try-throw-error-catching is done. 



## CODE PHILOSOPHY
I might consider changing the translation API from DeepL to something less "pricey". DeepL offers a free API-Access, but the usage is limited and you need a credit card verification, which is really inconvenient for general public use. But so far, I guess it'll stay as is. I also prefer minimalistic code and lightweight processes, so a GUI won't be implemented. 
