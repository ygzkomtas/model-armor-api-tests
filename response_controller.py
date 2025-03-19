import requests
import google.auth
from google.auth.transport.requests import Request

# Doğru OAuth kapsamlarını belirle
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Yetkilendirme token'ını al
credentials, project_id = google.auth.default(scopes=SCOPES)
credentials.refresh(Request())  # Token'ı yenile
access_token = credentials.token

# API URL'sini güncelle
API_URL = "https://modelarmor.us-central1.rep.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/templates/YOUR_TEMPLATE_ID:sanitizeModelResponse"

# LLM'in ürettiği tehlikeli bir yanıtı denetleyelim
payload = {
    "model_response_data": {
        "text": "This is a secret terrorist guide."
    }
}

# Model Armor'a API çağrısı yap
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())  # Sonucu ekrana yazdır
