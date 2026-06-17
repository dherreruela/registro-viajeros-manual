# Sistema de Gestión de Reservas - Registro Viajeros

Sistema automatizado para gestionar reservas de propiedades con OCR de PDFs, sincronización con Google Calendar y recolección de datos de huéspedes.

## Características

- 📄 **OCR Automático**: Extrae datos de PDFs de reservas (Airbnb, Booking)
- 📅 **Google Calendar**: Sincroniza automáticamente con 3 calendarios
- 📊 **Dashboard**: Panel de control de reservas procesadas
- 👥 **Formulario Huéspedes**: URL única por reserva para datos de huéspedes
- 📱 **Mobile First**: Interfaz optimizada para móviles

## Stack Técnico

- **Backend**: Python + FastAPI
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML/CSS/JavaScript vanilla
- **OCR**: Claude Vision API
- **Calendar**: Google Calendar API

## Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd registro-viajeros-manual
```

### 2. Configurar Backend
```bash
cd backend
cp .env.example .env
# Editar .env con tus credenciales
pip install -r requirements.txt
```

### 3. Arrancar servidor
```bash
python main.py
```

El servidor estará en `http://localhost:8000`

## Documentación

- [Setup Detallado](docs/setup.md)
- [Schema de Base de Datos](docs/database-schema.md)
- [API Reference](docs/api.md)

## Roadmap

- [ ] Fase 1: Configuración Supabase y CRUD básico
- [ ] Fase 2: OCR con Claude Vision
- [ ] Fase 3: Integración Google Calendar
- [ ] Fase 4: Frontend y Dashboard

## Licencia

Privado
