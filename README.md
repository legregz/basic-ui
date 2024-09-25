# Basic UI
## Description

basic_ui is a project of user interface using pygame and json files. The goal is to simplify the creation of app menus, and interfaces.

To use basic_ui, you need to have a minimal level in usage of pygame.

## Table of contents

1. Preparation
2. Examples

## 1. Preparation

1. Create your project directory
2. In there, create your 'main.py' file where you will going import pygame and basic_ui.

## 2. Examples

> [!IMPORTANT]
> Example of code for elements.json file:
> ```
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