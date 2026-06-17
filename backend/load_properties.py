"""
Script para cargar las viviendas iniciales en la base de datos
"""
import requests
import json

API_URL = "http://localhost:8000/api/properties/"

properties = [
    {
        "name": "Fithouse",
        "google_calendar_id": "294cf36f654227907ca7bea093abc9e6ba92e5dff9cc4286768bcf3712e49285@group.calendar.google.com",
        "address": ""
    },
    {
        "name": "Caleta Paraiso",
        "google_calendar_id": "961f0ccc911d33fb3d03f5eb37c4a7e6367d59aa24f5091e61564c8358eb86e5@group.calendar.google.com",
        "address": ""
    },
    {
        "name": "Puerta del Sol",
        "google_calendar_id": "1e4ffe3be5ca18a0b836eb0f6fb92b3c3648689e16041d8ace6efff562bbb084@group.calendar.google.com",
        "address": ""
    },
    {
        "name": "Eurocaleta",
        "google_calendar_id": "043a81c26ed4fa700bc3b30793f66ca373f9e4be33f40b00e139e379862a3f63@group.calendar.google.com",
        "address": ""
    },
]

print("🏠 Cargando viviendas en el sistema...\n")

for prop in properties:
    try:
        response = requests.post(
            API_URL,
            json=prop,
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ {prop['name']} - Cargada correctamente")
            else:
                print(f"❌ {prop['name']} - Error: {data.get('detail')}")
        else:
            print(f"❌ {prop['name']} - Error HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ {prop['name']} - Error de conexión: {e}")

print("\n✅ Proceso completado")
