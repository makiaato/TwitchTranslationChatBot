# TwitchTranslationChatBot v0.3.0-beta
## CURRENTLY WORKING ON
- definitely make thousands of mini-commits for readme changes



## DESCRIPTION
This repository aims to set up and execute a chat bot for [twitch.tv](https://www.twitch.tv/). It's customized for the channel [@blluist](https://www.twitch.tv/blluist). Therefore, the bot will aim to translate japanese messages to English. Rōmaji words are excluded as good as possible for the translation. The bot uses DeepL for translation (**credit card verification** is needed for the free version of DeepL-API, but no cost-subscription will be made). This ReadMe is also written for people with zero knowlege in programming. Those who are more skilled, can quick read the first words of the instructions and skip the rest safely. Additionally, the code is pretty short circuited and written while being hungry. There is still much to be done manually on the human side, so it's more a script than a software (yet?). 

The goal of this script is the following: Execute Bot-Behavior via a registered Twitch-User. The behavior reads messages on a Twitch-Channel, ignore every message that isn't in Japanese (including japanese words written in latin letters), translate it to English with DeepL and post the result in the chat.

Constraints set by the Twitch-API: 
- 20 messages per 30 seconds (unmodded bot)
- 100 messages per 30 seconds (modded bot)
- Refresh Tokens expire 30 days after generation

Constraints set by the DeepL-API:
- maximum of 500k characters per month



## SET UP INSTRUCTIONS
Before you can execute the script in the repository, your own computer needs the required software to even understand the programming language (Python). Furthermore, you obviously need a Twitch-Account and a DeepL-Account. Without those two accounts, you don't have credentials for their respective APIs.

1. Install Python by downloading it from their [website](https://www.python.org/). Generally, accept every default setting the installer throws at you with **one exception**: Let Python add PATH-variables by ticking the check-box at the beginning of the Python-Installation. 

2. Install additional required packages for python by opening your _Shell_. On Windows, you open it by **Windows-Key + R** or search for **cmd** in the Windows search field. Then enter both install-commands. You have to wait a bit after inputting the first command, so that python can install the package. 
```
python -m pip install -U deepl
```
```
python -m pip install -U twitchio
```
You can close the bash then, if you wish. 

3. Register on Twitch and DeepL, if you haven't done yet. Preferably, use a nickname for the Twitch-Account that would fit your chat bot, because that account will be used to chat on your channel. In other words, it becomes the chat bot. 

4. Acquire API-Credentials for Twitch and DeepL. 
   1. For Twitch: Go to the [twitch-developers](https://dev.twitch.tv/) website and log into your Bot-Account. It should recognize your account if you've authorized the log-in once before. Click on the "Your Console"-Button on the right of the purple bar at the top of the page. Click on "Register Your Application" on the Applications-Widget. Name it fittingly and set the "OAuth Redirect URLs" for the time being of this repository to its default value "http://localhost:3000" (without the quotation marks). Select "Chat Bot" as category, check if the "Confidential" Client-Type-Option is selected and then click on "Create". You should be redirected back to your console now and your new app should be listed in the Applications Widget. Click on "Manage" on your app-entry. Scroll down to see your **Client ID**. This value is important and should be kept confidentially. This is metaphorically your username for the Twitch-API-World. Write your Client ID down or save it somewhere save. We'll need that later. Now create a **Client Secret** by just pressing the "New Secret" button. Handle it cautiously like your Client ID. This Client Secret is metaphorically your password in the Twitch-API-Underground-World. Write the Client Secret down, too. Both Client-Credentials are needed in the Initialization Instructions, later on. 

   2. For DeepL: Go to [DeepL](https://www.deepl.com/), register an account and verify as told by entering credit card information. Make sure that you don't accidentally subscribe to their pro-subscription. After that, you should be redirected to your account dashboard. Click on "API-Keys". Then click on "Create Key". Name it fittingly. After that, you can click the copy-to-clipboard-button for the API-Key-value and save the value somewhere safe. This API-Key works metaphorically as a username and as a password at the same time for the DeepL-API-Ghetto-World, so don't lose it. It's your **Authentication Key** for DeepL and has nothing to do with the Twitch-Credentials, because DeepL has their own API.

6. Download the repository if you haven't done it yet! Extract the ZIP-File where you can find it easily.



## INITIALIZATION INSTRUCTIONS
1. Paste your relevant keys into the config_CHANGEME.csv (the file can be opened by Excel or similiar) directly under the respective categories/headers. You should have the following credentials ready now:
   - CLIENT_ID (Twitch)
   - CLIENT_SECRET (Twitch)   
   - AUTH_KEY (DeepL)

2. Set *SOURCE_LANGUAGE* to **JA** and *TARGET_LANGUAGE* to **EN-US**. Also, set your channel by entering the channel name (not the whole URL, so instead of "twitch.tv/your_channel_name" use "your_channel_name" only). Let the other categories empty, the script will collect them for you. 
![Example image of the config.csv file.](/example_images/example_01.png)

3. Make sure to save as CSV-File, so **don't change the file type**!!

4. Rename the file from *config_CHANGEME.csv* to **config.csv** and you're done with the installation! (A real software would've done all that for you.)

5. Start the script by double-clicking the "start_on_windows.bat"-file. The script will give you further instructions that ought to be easy to follow.

6. After finishing the steps in the console window, Python should boot up the script then and if the bot says it's ready, then it's ready! For confirmation, the bot will post a boot-up message in your channel, too.



## STARTING/EXIT INSTRUCTIONS
**Starting/Restarting**: Just double-click the "start_on_windows.bat"-file.
**Closing**: Just close the bash window.



## FEATURES
- bot can translate from English to Japanese by prepending the '!ja' command
- bot is locally hosted and credentials are bound by account. This means that you can execute the script from any computer and as long as you keep the credentials with it, then the same bot will be used



## FUTURE GOALS 
### Waiting/Acquire Feedback
The script freshly came out of its Alpha-Stage! I'll look around and ask people if they notice anything. 



## QUIRKS IN CODE
### Japanese Filter
The code is customized such that only japanese characters are recognized through a filter. If you ever want to use other source languages, then you've to remove the filter in the code itself. The filter uses a regex to recognize a [fixed set of japanese UTF-characters](http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml). So the filter quality is highly dependend on that. Also, mixed languages are also coming through, as long as they have japanese characters. Meaning that a sentence like "遊びましょう please" will be recognized. 

### Error Handling
I currently use simple console outputs to give feedback on what happens and what might have caused an error. So no real try-throw-error-catching is done. 



## CODE PHILOSOPHY
I might consider changing the translation API from DeepL to something less "pricey". DeepL offers a free API-Access, but the usage is limited and you need a credit card verification, which is really inconvenient for general public use. But this involves weighing out the pros and cons and doing comparisions. Currently, DeepL is fine, but I'll think about it. I also prefer minimalistic code and lightweight processes, so a GUI won't be implemented. 
