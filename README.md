# TwitchTranslationChatBot
_This ReadMe was last reviewed on 2nd April 2024_

# DESCRIPTION
This repository aims to set up and execute a ChatBot for [twitch.tv](https://www.twitch.tv/). It's customized for the channel [@blluist](https://www.twitch.tv/blluist). Therefore, the bot will aim to translate japanese messages to English. Rōmaji words are excluded as good as possible for the translation. The bot uses DeepL for translation (**credit card verification** is needed for free version of DeepL-API, but no cost-subscription will be made). This ReadMe is also written for people with zero knowlege in programming. Those who are more skilled, can quick read the first words of the instructions and skip the rest safely. Additionally, the code is pretty hotwired and written while being hungry. There is still much to be done on the human side, so it's more a script than a software (yet?). 



# SET UP INSTRUCTIONS
Before you can execute the script in the repository, your own computer needs the required software to even understand the programming language (Python). Furthermore, you obviously need a Twitch-Account and a DeepL-Account. Without those two, the script can't access the APIs. 
1. Install Python by downloading it from their [website](https://www.python.org/). It's important to let Python add PATH-variables if it's mentioned. Usually, that setting is checked by default. 

2. Install additional required packages for python by opening your shell. On Windows, you open it by **Windows-Key + R** or search for **cmd** in the windows search field. Then enter both install-commands. You have to wait a bit after inputting the first command, so that python can install the package. 
```
pip install deepl
pip install -U twitchio
```
You can close the bash then, if you wish. 

3. Register on Twitch and DeepL, if you haven't done yet. Preferrably, use a nickname for the Twitch-Account that would fit your chat bot, because that account will be used to chat on your channel. In other words, it becomes the chat bot. 

4. Acquire API-Access to Twitch and DeepL. 
For Twitch: Go to the [twitch-developers](https://dev.twitch.tv/) website and log into your Bot-Account. It should recognize your account if you're logged in on twitch itself already. Click on the "Your Console"-Button on the right of the purple bar at the top of the page. Click on "Register Your Application" on the Applications-Widget. Name it fittingly and set the "OAuth Redirect URLs" for the time being of this repository to its default value "http://localhost:3000" (without the quotation marks). Select "Chat Bot" as category, check if the "Confidential" Client-Type-Option is selected and then click on "create". You should be redirected back to your console now and your new app should be listed in the Applications Widget. Click on "Manage" on your app-entry. Scroll down to see your **Client ID**. This value is important and should be kept confidentially. This is metaphorically your username for the Twitch-API-World. Write your Client ID down or save it somewhere save. We'll need that later. Now create a **Client Secret** by just pressing the "New Secret" button. Handle it cautiously like your Client ID. This secret is metaphorically your personal passphrase in the Twitch-API-Underground-World to get your API-Token. Write the secret down, too. Both Client-Values are needed in the Initialization Instructions. 

5. For DeepL: Go to [DeepL](https://www.deepl.com/), register an account and verify as told by entering credit card information. Make sure that you don't accidentally subscribe to their pro-subscription. After that, you should be redirected to your account dashboard. Click on "API-Keys". Then click on "Create Key". Name it fittingly. After that, you can click the copy-to-clipboard-button for the API-key-value and save the value somewhere safe. This API-Key works metaphorically as a username and as a password for the DeepL-API-Ghetto-World, so don't lose it, it's your **Authentication Key** for DeepL. After that, you can proceed to the next step. 

6. Download the repository if you haven't done it yet! And that's all, you're ready to initialize your chat bot. 



# INITIALIZATION INSTRUCTIONS (FOR TWITCH)
1. We still need an API-Access-Token from the Twitch-API. We get that by having a Client-ID (we have that) and an Authorization-Token (we get that now). According to their [Tutorial](https://dev.twitch.tv/docs/irc/authenticate-bot/) we first use following URL:
```
https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=YOUR_CLIENT_ID_PASTE_HERE&redirect_uri=http://localhost:3000&scope=chat:read+chat:edit&state=GENERATE_THIRTY_TWO_RANDOM_LETTERS_AND_NUMBERS_FOR_SECURITY
```
Just post the URL in your favourite browser and don't forget to replace the template-characters **YOUR_CLIENT_ID_PASTE_HERE** and **GENERATE_THIRTY_TWO_RANDOM_LETTERS_AND_NUMBERS_FOR_SECURITY**. Your browser should either render a blank page or an error-display page, after you've entered that URL in your browser, because the URL doesn't forward you to a webpage, but to an API-Response. You can read your response in the URL of your browser now and it should look like the following example:
```
http://localhost:3000/?code=THE_RELEVANT_AUTHORIZATION_CODE_IS_HERE&scope=chat%3Aread+chat%3Aedit&state=YOUR_RANDOM_VALUE_SHOULD_RETURN_TO_YOU_HERE
```
Make sure that the example-keyword **YOUR_RANDOM_VALUE_SHOULD_RETURN_TO_YOU_HERE** is identical to your random entered value at the beginning. If it's not, then you can't trust that response, else it's a true response from the Twtich-API. Now, copy the value you got for **THE_RELEVANT_AUTHORIZATION_CODE_IS_HERE** and save it somewhere secure, because that's your **Authorization Token**. Metaphorically, the authorization token is the trusted certificate that the Twitch-API recognizes as you being a valid user in the Twitch-API-Underworld. Something like a passport, along the lines. 

2. Following Twitch's [Instructions](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) we now use a so called "cURL". Superficially and in short, it's an URL you can paste into programs, instead of a web browser. First, open your bash again (Windows-Key + R on Windws). And enter the following example:
```
curl -X POST "https://id.twitch.tv/oauth2/token" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=YOUR_CLIENT_ID_PASTE_HERE&client_secret=YOUR_CLIENT_SECRET_PASTE_HERE&code=YOUR_AUTHORIZATION_CODE_PASTE_HERE&grant_type=authorization_code&redirect_uri=http://localhost:3000"
```
Don't forget to replace the keywords **YOUR_CLIENT_ID_PASTE_HERE**, **YOUR_CLIENT_SECRET_PASTE_HERE** and **YOUR_AUTHORIZATION_CODE_PASTE_HERE**. So, with your ID, your passphrase and a passport, we should get the following example response in your bash:
```
{"access_token":"YOUR_ACCESS_TOKEN_IS_HERE","expires_in":13895,"refresh_token":"YOUR_REFRESH_TOKEN_IS_HERE","scope":["chat:edit","chat:read"],"token_type":"bearer"}
```
Write down the two values **YOUR_ACCESS_TOKEN_IS_HERE** and **YOUR_REFRESH_TOKEN_IS_HERE**. I may state the obvious, but still, both values are important, so keep them secretly. And with that, we got our own **Access Token** for the Twitch-API and another one, the **Refresh Token**, if our current one should expire (they expire in about 3-4 hours, but the script handles that). The hardest part is done, congratulations!

3. Paste your relevant keys into the config_CHANGEME.csv (the file can be opened by Excel or similiar). 

4. Set *SOURCE_LANGUAGE* to **JA** and *TARGET_LANGUAGE* to **EN-US**.

5. Make sure to save as CSV-File, so **don't change the file type**!!

6. Rename the file from *config_CHANGEME.csv* to **config.csv** and you're done with the installation! (A real software would've done all that for you.)



# STARTING/EXIT INSTRUCTIONS
**Starting**: Open bash and change the current bash position to the repository folder. For example, if the repository path lies at:
```
C:\Users\YourUsernameIsUsuallyHere\Downloads\gitProjects\TwitchTranslationChatBot
```
then I would enter the following code to change the current directory of the bash to my target directory with the "cd" command:
```
cd C:\Users\YourUsernameIsUsuallyHere\Downloads\gitProjects\TwitchTranslationChatBot
```
Don't forget to replace *YourUsernameIsUsuallyHere* if you intend to copy my example. Now, in the correct directory, enter the following to start the script:
```
py translation.py
```
Python should boot up the script then and if the bot says it's ready, then it's ready! For confirmation, the bot will post a boot-up message in your channel, too. 
**Closing**: Just close the bash window



# GOALS 
todotodotodo
independence
access token acquisition



# QUIRKS IN CODE
todotodotodo
the programming code is customized such that only japanese characters are filtered. If you ever want to use other source languages, then you've to remove the filter
error handling
http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml



# CODE PHILOSOPHY
tododododod
