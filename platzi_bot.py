from openai import OpenAI
import requests
import time

openai = OpenAI(
    api_key=""
)
TELEGRAM_TOKEN = ""

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset} if offset else {}
    response = requests.get(url=url, params=params)
    return response.json()["result"]

def send_messages(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response

def get_openai_response(prompt):
    model_engine = ""
    system = """
    Eres un asistente de atención a clientes
    y estudiantes de la plataforma de educación online en tecnología,
    inglés y liderazgo llamada Platzi. Cuando das una recomiendación siempre le agregas la URL del curso.
    """

    response = openai.chat.completions.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": f"{system}"},
            {"role": "user", "content": f"{prompt}"}
        ],
        max_tokens=150,
        n=1,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def main():
    print("Starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                chat_id = update["message"]["chat"]["id"]
                user_message = update["message"]["text"]
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()
