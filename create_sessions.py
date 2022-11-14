import json
from pyrogram import Client
config = json.load(open("config.json", "r", encoding="utf-8"))


def main():
    for username, info in config["users"].items():
        print(username)
        with Client(username, info["id"], info["hash"], proxy=info["proxy"]) as app:
            continue
    print("Сессии созданы!")


if __name__ == '__main__':
    main()
