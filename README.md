# TwitchTranslationChatBot
DESCRIPTION
todododododdo

SET UP INSTRUCTIONS
1) Install Python
2) Install packages for python
pip install deepl
pip install -U twitchio
3) register on Twitch and DeepL
4) acquire API-Token for Twitch and DeepL



INITIALIZATION INSTRUCTIONS
1) enter in browser https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=YOUR_CLIENT_ID_PASTE_HERE&redirect_uri=http://localhost:3000&scope=chat:read+chat:edit&state=c3ab8aa609ea11e793ae92361f002671
example response http://localhost:3000/?code=THE_RELEVANT_AUTHORIZATION_CODE_IS_HERE&scope=chat%3Aread+chat%3Aedit&state=c3ab8aa609ea11e793ae92361f002671

2) curl -X POST "https://id.twitch.tv/oauth2/token" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=YOUR_CLIENT_ID_PASTE_HERE&client_secret=YOUR_CLIENT_SECRET_PASTE_HERE&code=YOUR_AUTHORIZATION_CODE_PASTE_HERE&grant_type=authorization_code&redirect_uri=http://localhost:3000"
example response {"access_token":"YOUR_ACCESS_TOKEN_IS_HERE","expires_in":13895,"refresh_token":"YOUR_REFRESH_TOKEN_IS_HERE","scope":["chat:edit","chat:read"],"token_type":"bearer"}

3) Paste relevant keys into the config.csv



STARTING/EXIT INSTRUCTIONS
1) TODO TODO TODO



GOALS 
todotodotodo
independence
access token acquisition



QUIRKS IN CODE
todotodotodo
the programming code is customized such that only japanese characters are filtered. If you ever want to use other source languages, then you've to remove the filter
error handling
http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml