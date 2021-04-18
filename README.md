# mango-c2
A Python-based C2.

For educational purposes only.

## Introduction
I initially came up with the idea for mango C2 by brainstorming unorthodox communications methods. Many people use social media sites like Reddit at work, so I planned to build a communications method based off of Reddit's messaging API in order to fly below the radar of firewalls.

Mango is designed to be modular and extensible - it dynamically loads in all communications methods in at runtime. This would allow most any developer to port mango to an additional platform given enough time to research an API at a basic level. All commands are defined separately from the communications methods, so any additional commands or communication methods should be "drop-in" rather than requiring a re-design.

## Installation

Place `server/` on the target machine, and leave `client/` in your controller machine.

Run `python3 -m venv env` and then `pip3 install -r requirements.txt` in both `client/` and `server/`.

Activate the venv via `source env/bin/activate` in either directory.

Start each service by running `python3 main.py`

### Reddit registration
Create 2 reddit accounts and register them with a web service with full permissions. Include the application keys inside `settings.ini`, and the refresh key in `config/reddit.token`. Details on this process can be found [here](https://praw.readthedocs.io/en/latest/getting_started/authentication.html).
