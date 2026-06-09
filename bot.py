import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import os
import threading
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web).start()

TOKEN = os.environ.get("VK_TOKEN")
GROUP_ID = int(os.environ.get("VK_GROUP_ID", "236632318"))

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# Путь к PDF-файлам
pdf_files = {
    "МТС Линк": "mts_link.pdf",
    "Сферум": "sferum.pdf",
    "Яндекс 360": "yandex360.pdf",
    "СберКласс": "sberklass.pdf",
    "Битрикс24": "bitrix24.pdf"
}

def keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button("МТС Линк", VkKeyboardColor.PRIMARY)
    kb.add_button("Сферум", VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("Яндекс 360", VkKeyboardColor.PRIMARY)
    kb.add_button("СберКласс", VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("Битрикс24", VkKeyboardColor.PRIMARY)
    return kb.get_keyboard()

def send_pdf(user_id, file_path):
    upload = vk_api.VkUpload(vk)
    doc = upload.document_message(peer_id=user_id, doc=file_path, title=file_path)
    vk.messages.send(
        user_id=user_id,
        random_id=random.randint(1,100000),
        attachment=f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}",
        keyboard=keyboard()
    )

def send_message(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1,100000),
        keyboard=keyboard()
    )

print("Бот запущен")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_id = event.obj.message['from_id']
        text = event.obj.message['text']

        if text.lower() == "начать":
            send_message(user_id, "Выберите платформу для получения методических рекомендаций")

        elif text in pdf_files:
            send_message(user_id, f"Отправляю PDF с рекомендациями по {text}")
            send_pdf(user_id, pdf_files[text])
