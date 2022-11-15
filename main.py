import json
import random
import asyncio
from pyrogram import Client
from pyrogram.types import Chat
from pyrogram.errors.exceptions import UsernameInvalid, InviteHashExpired, UsernameNotOccupied, BadRequest


def optimize_array(arr):
    new_arr = []
    for i in arr:
        if i != "":
            new_arr.append(i)
    return new_arr


chats = optimize_array(list(set(open("chats.txt", "r", encoding="utf-8").read().split("\n"))))
config = json.load(open("config.json", "r", encoding="utf-8"))
errors = open("errors.txt", "w", encoding="utf-8")


async def start_user(name: str, api_id: int, api_hash: str, proxy: dict):
    async with Client(name, api_id, api_hash, proxy=proxy) as app:
        for chat in chats:
            await asyncio.sleep(random.randint(10, 65))
            try:
                response = await app.join_chat(chat)
            except UsernameInvalid:
                try:
                    response = await app.join_chat(chat.split("/")[-1])
                except Exception as err:
                    if err.__class__.__name__ == "FloodWait":
                        count = 1
                        while True:
                            if count > 20:
                                errors.write(f"Chat {chat} wait so long")
                            await asyncio.sleep(random.randint(120 * count, 200 * count))
                            count += 1
                            try:
                                response = await app.join_chat(chat.split("/")[-1])
                                break
                            except Exception as err:
                                errors.write(f"Error '{err.__class__.__name__}' at {chat}\n")
                                continue
                    else:
                        errors.write(f"Error '{err.__class__.__name__}' at {chat}\n")
                        continue
            except InviteHashExpired:
                print(f"Ссылка {chat} устарела ({name})")
                continue
            except UsernameNotOccupied:
                print(f"Ссылка {chat} некорректна или такого канала не существует ({name})")
                continue
            except BadRequest:
                print(f"Ссылка на канал {chat} либо некорректна, либо заявка на вступление рассматривается ({name})")
                continue
            except Exception as err:
                errors.write(f"Error '{err.__class__.__name__}' at {chat}\n")
                continue

            if isinstance(response, Chat):
                print(f"Успешно добавлен в канал: {response.title} ({name})")
            else:
                print(f"Ссылка на канал {chat} либо некорректна, либо заявка на вступление рассматривается ({name})")

        print(f"Клиент {name} добавлен во все каналы")


def main():
    loop = asyncio.get_event_loop()
    tasks = []
    for username, info in config["users"].items():
        tasks.append(loop.create_task(start_user(username, info["id"], info["hash"], proxy=info["proxy"])))
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main()
