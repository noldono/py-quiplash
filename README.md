# Py-Quiplash

## Background
This is a group project created by [Nolan Donovan](https://github.com/noldono), [Adam Lahouar](https://github.com/adamlahouar), and [EtherealJD](https://github.com/etherealjd) for the class ECE 4564 at Virginia Tech.

## Rules on Running
Before reading further please note that in order to start a game you must have three clients open. Once three clients are open the VIP (first person to join) may start the game. Both the API and the game server must be running as well.

You'll want to start quip_server and the API first.

## Starting the Client
Clone the repository, stay in that current directory where you cloned it, and then paste one of the following scripts into that same terminal window.
### Windows
```cd quiplash; py -m venv venv; venv\Scripts\activate.bat; py -m pip install -r requirements.txt; cd src; py -m quip_client```

### MacOS/Linux
``cd quiplash; python3 -m venv venv; source venv/bin/activate; python3 -m pip install -r requirements.txt; cd src; python3 -m quip_client``

## Starting the API and server UI
Inside the src folder run:

``python3 -m quip_server``

``python3 -m api``


## Starting the API and Server UI in Docker
The running ``docker compose up`` in the root directory will launch the images configured in docker-compose.yml. Read this article to figure out how to get the server UI to run through Docker.

We have had some issues with the UI just being a black screen in some cases. We believe this happens due to some displays trying to automatically upscale the application's resolution. We aren't 100% sure, though.

https://medium.com/@rndonovan1/running-pygame-gui-in-a-docker-container-on-windows-cc587d99f473
