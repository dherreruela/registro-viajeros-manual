from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pathlib import Path
from datetime import datetime, timedelta
import json

# Credenciales de la Service Account
SERVICE_ACCOUNT_FILE = Path(__file__).parent.parent.parent / "sensibles" / "google_service_account.json"

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """Obtiene el servicio de Google Calendar autenticado"""
    if not SERVICE_ACCOUNT_FILE.exists():
        raise FileNotFoundError(f"Archivo de credenciales no encontrado: {SERVICE_ACCOUNT_FILE}")

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)
    return service

def get_calendar_events(calendar_id: str, days_ahead: int = 30):
    """
    Obtiene los eventos de un calendario para los próximos días

    Args:
        calendar_id: ID del calendario de Google
        days_ahead: Cantidad de días a futuro para obtener eventos

    Returns:
        Lista de eventos
    """
    try:
        service = get_calendar_service()

        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events

    except Exception as e:
        print(f"Error obteniendo eventos del calendario {calendar_id}: {e}")
        return []

def create_calendar_event(calendar_id: str, event: dict):
    """
    Crea un evento en Google Calendar

    Args:
        calendar_id: ID del calendario
        event: Diccionario con los datos del evento

    Returns:
        El evento creado
    """
    try:
        service = get_calendar_service()
        created_event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        return created_event
    except Exception as e:
        print(f"Error creando evento: {e}")
        return None
