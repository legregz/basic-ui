# Basic UI
## Description

basic_ui is a project of user interface using pygame and json files. The goal is to simplify the creation of app menus, and interfaces.

> [!IMPORTANT]
> To use basic_ui, you need to have a minimal level in usage of pygame.

## Table of contents

1. Preparation
2. Examples

## 1. Preparation

1. Create your project directory

2. In there, create your 'main.py' file where you will going import pygame and basic_ui.
>```python
>import basic_ui, pygame
>pygame.init()
>
>screen = pygame.display.set_mode(flags = pygame.RESIZABLE)
>```

3. The following line create a new directory called 'config' in your project directory and add in the 'aliases.json' and 'defaults.json' config files. If there is already these files and directory, they don't be changed.
>```python
>basic_ui.importConfigFiles()
>```

> [!NOTE]
>The 'aliases.json' file contain that:
>```json
>{
>    "red": "f00",
>    "green": "0f0",
>    "blue": "00f",
>    "yellow": "f00",
>    "cyan": "0ff",
>    "pink": "f0f",
>}
>```

> [!NOTE]
>The 'default.json' file contain that:
>```json
>{
>    "color": "f",
>    "text": "text",
>    "font-size": 12,
>    "font-color": "0",
>    "font": "Liberation Sans",
>    "border-radius": 1,
>    "border-width": 1,
>    "border-color": "0",
>    "size": "auto",
>    "position": ["50%", "50%"],
>    "margin": 3
>}
>```

## 2. Examples

Example of code for elements.json file:
> ```json
> {
>    "homeButton": {
>        "Button": {
>            "border-width": 1,
>            "font-size": 30,
>            "margin": 5,
>            "size": ["20px", "100px"]
>        }
>    },
>
>    "homeTitle": {
>        "Text": {
>            "text": "Hello World!",
>            "font-size": 40
>        }
>    },
>
>    "homeHeaderSection": {
>        "homeButton": {},
>        "homeTitle": {}
>    }
> }
> ```