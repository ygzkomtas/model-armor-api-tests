from openai import OpenAI
import requests
import google.auth
from google.auth.transport.requests import Request
import json

# OpenAI API Key
OPENAI_API_KEY = ""

client = OpenAI(api_key=OPENAI_API_KEY)

# Google Cloud Model Armor API Yetkilendirme
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
credentials, project_id = google.auth.default(scopes=SCOPES)
credentials.refresh(Request())
access_token = credentials.token

# Model Armor API URL'leri
PROJECT_ID = "yagiz"
LOCATION = "us-central1"
TEMPLATE_ID = ""
MODEL_ARMOR_PROMPT_URL = f"https://modelarmor.{LOCATION}.rep.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/templates/{TEMPLATE_ID}:sanitizeUserPrompt"
MODEL_ARMOR_RESPONSE_URL = f"https://modelarmor.{LOCATION}.rep.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/templates/{TEMPLATE_ID}:sanitizeModelResponse"

# Model Armor'a API çağrısı yapacak fonksiyon
def check_with_model_armor(text, url):
    payload = {"user_prompt_data": {"text": text}} if "sanitizeUserPrompt" in url else {"model_response_data": {"text": text}}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# OpenAI API çağrısı yapacak fonksiyon
def chat_with_openai(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content.strip()

# Kullanıcıdan input al
user_input = input("Soru sor: ")

# 1️⃣ Model Armor ile prompt'u kontrol et
prompt_check = check_with_model_armor(user_input, MODEL_ARMOR_PROMPT_URL)

if prompt_check["sanitizationResult"]["filterMatchState"] == "MATCH_FOUND":
    print("🚨 Tehlikeli prompt tespit edildi! OpenAI API'ye gönderilmeyecek.")
    print("📋 Model Armor yanıtı:", json.dumps(prompt_check, indent=2, ensure_ascii=False))
else:
    # 2️⃣ OpenAI API'ye güvenli prompt'u gönder
    ai_response = chat_with_openai(user_input)

    # 3️⃣ Model Armor ile OpenAI yanıtını kontrol et
    response_check = check_with_model_armor(ai_response, MODEL_ARMOR_RESPONSE_URL)

    if response_check["sanitizationResult"]["filterMatchState"] == "MATCH_FOUND":
        print("🚨 OpenAI modelinin yanıtı güvenli değil, gösterilmeyecek!")
    else:
        print("✅ AI Yanıtı:", ai_response)
