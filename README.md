# mango-c2
A Python-based C2.

For educational purposes only.

## Introduction
I initially came up with the idea for mango C2 by brainstorming unorthodox communications methods. Many people use social media sites like Reddit at work, so I planned to build a communications method based off of Reddit's messaging API in order to fly below the radar of firewalls.

Mango is designed to be modular and extensible - it dynamically loads in all communications methods in at runtime. This would allow most any developer to port mango to an additional platform given enough time to research an API at a basic level. All commands are defined separately from the communications methods, so any additional commands or communication methods should be "drop-in" rather than requiring a re-design.

