## VinnyBot
[![Discord](https://img.shields.io/badge/Discord-Support-blue.svg)](https://discord.gg/XMwyzxZ)
[![Build Status](https://travis-ci.org/JessWalters/VinnyBot.svg?branch=master)](https://travis-ci.org/bwmarrin/discordgo)
[![Documentation Status](https://readthedocs.org/projects/vinnybot/badge/?version=latest)](http://vinnybot.readthedocs.io/en/latest/?badge=latest)

A side project I have been working on for about 5 months now. In these 5 months Vinny has accumulated over 153,000 users across over 7,000 servers. The codebase is currently undergoing a major redesign and refactor. This is to increase readability for other devs and maintainability. This started as a small hackathon project and the core was not written for a bot of this scale. 

## Usage
### To add Vinny to your own server go to: https://goo.gl/g1vWxS  
[Full list of commands](docs/commands.md)

## Support
The best way to get help with Vinny is to go to his support Discord server: https://discord.gg/XMwyzxZ

## Usage of code
Vinny is completly open-source under the MIT License. Feel free to use and modify any code as you see fit. Just make sure to mention where you got it from. ;)

## Contributing
If you want to help by suggesting a feature or update to Vinny the best way is to reach out to me. Either on Vinny's support sever or by making an issue on this repo.

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request :D

## Want to try to run Vinny locally?
Right now this guide is only for the text module. If you have any problems feel free to reach out to me.

1. Have Pip and python 3.5.2+ installed
2. Clone repo
3. cd into repo
4. pip install -r requirements.txt
5. Make a file Core/config/tokens.txt
6. Make tokens.txt like so:  
\*\*\*Discord\*\*\*   
\<Discord bot Oauth2 Token\>  (You need to register a bot on https://discordapp.com/developers/applications/me)  
\*\*\*Bot API\*\*\*  
\<bots.discord.pw Token\>   
\*\*\*Bot ID\*\*\*  
\<BotID\>  (This also comes from https://discordapp.com/developers/applications/me)  
\*\*\*Reddit\*\*\*  
\<Reddit client secret token\> (Retrieved from registering a bot with reddits API)
7. Run Core/Main.py  
