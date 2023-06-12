from typing import Text
import requests
from shortener.models import Schedules, ShortenedUrls, Users
import json

# ACCESS_TOKEN = json.loads(open("./shrinkers/telegram_access_token.json").read()).get("access_token")
ACCESS_TOKEN = "6242404645:AAGWeIj5_4nNzfbiMq-HaPweVzrk8PHy25w"

def get_chats():
    url = f"https://api.telegram.org/bot{ACCESS_TOKEN}/getUpdates"
    res = requests.get(url).json()
    return res.get("result") if res.get("ok") else []


def chat_handler():
    msgs = get_chats()
    scheduler = Schedules.objects.filter(id=1)
    latest_ts = scheduler.first().value
    final_ts = 0
    chats = {}
    for m in msgs:
        msg = m.get("message")
        chat = msg.get("chat", {})
        chat_ts = msg.get("date", 0)
        if chat_ts > latest_ts:
            chat_id = chat.get("id")
            matched_user = Users.objects.filter(telegram_username=chat_id).first()
            if not matched_user:
                continue
            if chat.get(matched_user.id):
                chat[matched_user.id].append(str(msg.get("text", "")))
            else:
                chats[matched_user.id] = [str(msg.get("text", ""))]

            if chat_ts > latest_ts:
                final_ts = chat_ts
    if final_ts > latest_ts:
        scheduler.update(value=final_ts)
    print(chats)
    return chats


def send_chat(chat_id: str, msg: str):
    url = f"https://api.telegram.org/bot{ACCESS_TOKEN}/sendMessege"
    body = {"chat_id": chat_id, "text": msg}
    res = requests.post(url, data=body)


def get_response(command, url=None):
    c = {
        "start": "shrinkers 서비스를 시작합니다\n (/help로 안내를 받아보세요)",
        "help": "/create [닉네임] [타켓 URL] 형식으로 입력하시면 단축 URL을 생성해드립니다",
        "done": f"완성되었어요{url}",
    }
    return c.get(command, "잘못 입력하셨습니다.\n/help로 안내를 받아보세요")


def command_handler():
    chats = chat_handler()
    for key, val in chats.items():
        user_info = Users.objects.filter(id=key).first()
        for v in val:
            if v == "/start":
                send_chat(user_info.telegram_username, get_response("start"))
            elif v == "/help":
                send_chat(user_info.telegram_username, get_response("help"))
            elif v.startwith("/create"):
                get_text = v.strip().split(" ")
                nick_name = get_text[1]
                target_url = get_text[2]

                url = ShortenedUrls()
                url.nick_name = nick_name
                url.creator = user_info
                url.target_url = target_url
                url.create_via = "telegram"
                url.save()

                send_chat(
                    user_info.telegram_username,
                    get_response("done", url=f"http://localhost:8000/{url.prefix}/{url.shortened_url}"),
                )
