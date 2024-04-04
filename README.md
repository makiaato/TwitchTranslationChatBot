# TwitchTranslationChatBot v0.2.0
## CURRENTLY WORKING ON
- Reviewing Code and Instructions
- Add example images to the instructions



## DESCRIPTION
This repository aims to set up and execute a chat bot for [twitch.tv](https://www.twitch.tv/). It's customized for the channel [@blluist](https://www.twitch.tv/blluist). Therefore, the bot will aim to translate japanese messages to English. Rōmaji words are excluded as good as possible for the translation. The bot uses DeepL for translation (**credit card verification** is needed for the free version of DeepL-API, but no cost-subscription will be made). This ReadMe is also written for people with zero knowlege in programming. Those who are more skilled, can quick read the first words of the instructions and skip the rest safely. Additionally, the code is pretty short circuited and written while being hungry. There is still much to be done manually on the human side, so it's more a script than a software (yet?). 

The goal of this script is the following: Execute Bot-Behavior via a registered Twitch-User. The behavior reads messages on a Twitch-Channel, ignore every message that isn't in Japanese (including japanese words written in latin letters), translate it to English with DeepL and post the result in the chat.

The current state on how to use the repository is this: Enter personal credentials in a CSV-File, then open a bash terminal and execute the python script



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



## INITIALIZATION INSTRUCTIONS (FOR TWITCH)
1. My script gets access to the Twitch-API by having an API-Access-Token. We can request one by having a Client-ID (we have that) and an **Authorization-Token** (we generate that now and don't confuse it with the Authentication Key from DeepL). According to Twitch's [Tutorial](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#authorization-code-grant-flow), to generate an Authorization-Token, we first use following URL:
```
https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=YOUR_CLIENT_ID_PASTE_HERE&redirect_uri=http://localhost:3000&scope=chat:read+chat:edit&state=GENERATE_THIRTY_TWO_RANDOM_LETTERS_AND_NUMBERS_FOR_SECURITY
```
Copy the URL and replace the template-words **YOUR_CLIENT_ID_PASTE_HERE** with your Client-ID and **GENERATE_THIRTY_TWO_RANDOM_LETTERS_AND_NUMBERS_FOR_SECURITY** with a random series of 32 characters, consisting of numbers and letters and write it down, too (it can look for example like this: a1b2c3d4e5f6g7h8i9j8k7l6). 

2. After replacing the template-words, paste it in the URL-bar of your favourite browser. 

3. When you have entered your modified URL, you will land on an Authorization Page you might be familiar with. The same name of your registered App in your Twitch-Developer Account should be found there, too. Authorize it, after you've verified the correct name and you'll land on a blank page or an error page after that, because we set that in the Twitch-App-Settings at the beginning (remember the "http://localhost:3000"). 

4. You should be able to read your API-Response from the Twitch-API in the URL of your browser now, while being on that error-page. It should look like the following example:
```
http://localhost:3000/?code=THE_RELEVANT_AUTHORIZATION_CODE_IS_HERE&scope=chat%3Aread+chat%3Aedit&state=YOUR_RANDOM_VALUE_SHOULD_RETURN_TO_YOU_HERE
```
Make sure that the template-word **YOUR_RANDOM_VALUE_SHOULD_RETURN_TO_YOU_HERE** is identical to your random entered value from before. If it's not, then you can't trust that response, else it's a true response from the Twtich-API. Now, copy the value you got for **THE_RELEVANT_AUTHORIZATION_CODE_IS_HERE** and save it somewhere secure, because that's your Authorization Token. Metaphorically, the authorization token is the trusted certificate that the Twitch-API recognizes as you being a valid user in the Twitch-API-Underworld. Something like a passport, along the lines. 

5. Following Twitch's Instructions we now use a so called "cURL" to get our Access Token. Superficially and in short, it's an URL you can paste into programs, instead of a web browser. First, open your bash again (Windows-Key + R on Windws), copy the following example:
```
curl -X POST "https://id.twitch.tv/oauth2/token" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=YOUR_CLIENT_ID_PASTE_HERE&client_secret=YOUR_CLIENT_SECRET_PASTE_HERE&code=YOUR_AUTHORIZATION_CODE_PASTE_HERE&grant_type=authorization_code&redirect_uri=http://localhost:3000"
```
and replace the keywords **YOUR_CLIENT_ID_PASTE_HERE**, **YOUR_CLIENT_SECRET_PASTE_HERE** and **YOUR_AUTHORIZATION_CODE_PASTE_HERE**. 

6. After modifiying the example, enter it in your shell. You'll get the following example response in your bash:
```
{"access_token":"YOUR_ACCESS_TOKEN_IS_HERE","expires_in":13895,"refresh_token":"YOUR_REFRESH_TOKEN_IS_HERE","scope":["chat:edit","chat:read"],"token_type":"bearer"}
```
Write down the two values that are in my example-words **YOUR_ACCESS_TOKEN_IS_HERE** and **YOUR_REFRESH_TOKEN_IS_HERE**. I may state the obvious, but still, both values are important, so keep them secretly. And with that, we got our own **Access Token** for the Twitch-API and another one, the **Refresh Token**, if our current one should expire (they expire in about 3-4 hours, but the script handles that). The hardest part is done, congratulations!

7. Paste your relevant keys into the config_CHANGEME.csv (the file can be opened by Excel or similiar) directly under the respective categories/headers. You should have the following credentials ready now:
   - CLIENT_ID (Twitch)
   - CLIENT_SECRET (Twitch)
   - ACCESS_TOKEN (Twitch)
   - REFRESH_TOKEN (Twitch)
   - AUTH_KEY (DeepL)

8. Set *SOURCE_LANGUAGE* to **JA** and *TARGET_LANGUAGE* to **EN-US**. Also, set your channel by entering the channel name (not the whole URL, so instead of "twitch.tv/your_channel_name" use "your_channel_name" only). 

9. Make sure to save as CSV-File, so **don't change the file type**!!

10. Rename the file from *config_CHANGEME.csv* to **config.csv** and you're done with the installation! (A real software would've done all that for you.)



## STARTING/EXIT INSTRUCTIONS
### Starting/Restarting
Open bash and change the current bash position to the repository folder. For example, if the repository path lies at:
```
C:\Users\YourUsernameIsUsuallyHere\Downloads\gitProjects\TwitchTranslationChatBot
```
then I would enter the following code to change the current directory of the bash to my target directory with the "cd" command:
```
cd C:\Users\YourUsernameIsUsuallyHere\Downloads\gitProjects\TwitchTranslationChatBot
```
Don't forget to replace *YourUsernameIsUsuallyHere* if you intend to copy my example. Now, in the correct directory, enter the following to start the script:
```
python translation.py
```
Python should boot up the script then and if the bot says it's ready, then it's ready! For confirmation, the bot will post a boot-up message in your channel, too. 

### Closing
Just close the bash window



## FEATURES
- bot can translate from English to Japanese by prepending the '!ja' command



## FUTURE GOALS 
### Simplify API-Credential-Acquisition
To state the obvious, it's a real pain to acquire the necessary API-Credentials. I wish it to be more convenient. For me and for those, who will use it, too. 



## QUIRKS IN CODE
### Japanese Filter
The code is customized such that only japanese characters are recognized through a filter. If you ever want to use other source languages, then you've to remove the filter in the code itself. The filter uses a regex to recognize a [fixed set of japanese UTF-characters](http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml). So the filter quality is highly dependend on that. Also, mixed languages are also coming through, as long as they have japanese characters. Meaning that a sentence like "遊びましょう please" will be recognized. 

### Error Handling
I currently use simple console outputs to give feedback on what happens and what might have caused an error. So no real try-throw-error-catching is done. 



## CODE PHILOSOPHY
I might consider changing the translation API from DeepL to something less "pricey". DeepL offers a free API-Access, but the usage is limited and you need a credit card verification, which is really inconvenient for general public use. But this involves weighing out the pros and cons and doing comparisions. Currently, DeepL is fine, but I'll think about it. 
