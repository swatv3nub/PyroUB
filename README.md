# PyroUB

Just another Pyrogram based Telegram User(bot)

# Deployment

Host this Bot Anywhere you want (except Railways, might get the app/account suspended)
- [Heroku](#Heroku)
- [Qovery](#Qovery)
- [GNU Linux](#GNU-Linux)
- [Windows](#Windows)
- [Others](#Other-Platform)
- [Generate String Session](#String-Session)

## String Session

[![Run in Repl.it](https://img.shields.io/badge/Repl%20It-Run%20Online-blue.svg)](https://replit.com/@swatv3nub/PyroSession)

**or**

Run [stringsession.py](https://github.com/swatv3nub/PyroUB/blob/Alpha/stringsession.py) in a Terminal

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/swatv3nub/PyroUB)

## Qovery

- Fork the Repo: [here](https://github.com/swatv3nub/PyroUB/fork)
- Go to Qovery official site: [here](https://qovery.com)
- sign-in using GitHub
- Deploy the Application connecting the Forked Repo
- Configure the Environmental Variables
- Done

## GNU Linux

- Open Terminal
- Install Python Version >= 3.9.0
- `pkg install git`
- `git clone https://github.com/swatv3nub/PyroUB`
- Install Screen:
    - `sudo apt-get install screen` (debian based)
    -    or
    - `sudo pacman -S screen` (arch based)
- `screen -S pyroub`
- `cd PyroUB`
- Create a VENV `python3.9 -m venv venv`
- `. ./venv/bin/activate`
- `pip3 install -U -r requirements.txt`
- `cp sample_config.py config.py`
- Generate Session by Running `python3 stringsession.py`
- run `CTRL+Z` after the String Session gets saved in your Saved Messages in telegram
- Fill the config.py properly
- Install FFMPEG:
    - `sudo apt-get install ffmpeg-python` (debian based)
    -   or
    - `sudo pacman -S ffmpeg-python` (arch based)
- `python3 -m pyroub` (for turning on userbot)
- `python3 pyrovc.py` (for turning on the VC Bot)

**NOTE:** You need two Different Screen for running two apps (userbot and vcbot)

## Windows

Are you Fucking Dumb?
Use Linux!

## Other Platform

If You use or Know amy other good(free or cheap) Hosting provider to host Telegram Bots/Userbots
Drop in my PM [@MaskedVirus](https://t.me/MaskedVirus)

# License
PyroUB is Licensed under [GNU Affero General Public License V3](https://gnu.org/licenses/agpl-3.0.en.html) which can be found [here](LICENSE)

[![License](https://gnu.org/graphics/agplv3-155x51.png)](LICENSE)

# Special Thanks
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/Pyrogram)
- [HamkerPussy](https://github.com/TheHamkerCat) for [python-arq](https://github.com/TheHamkerCat/Python_ARQ)
- [Roj](https://github.com/rojserbest) for [pytgcalls-wrapper](https://github/callsmusic/pytgcalls-wrapper)
- [Me](https://maskedvirus.me) for writng this messy code
- [Aditya](https://xditya.me)
- [Satwik](https://github/okay-retard)
- [Blankie](https://t.me/TheKneesocks) and [Justin](https://github.com/Justasic) for Sukuinote and Shadowhawk Respectively