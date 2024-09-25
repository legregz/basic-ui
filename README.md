basic-ui is a project of user interface using pygame and json files. The goal is to simplify the creation of app menus, and interfaces.

> [!EXAMPLE]
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