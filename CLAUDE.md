# Sistema de Gestión de Reservas - Registro Viajeros

## Descripción
Sistema para gestionar reservas de propiedades (Airbnb/Booking) con OCR automático de PDFs, sincronización con Google Calendar, y recolección de datos de huéspedes.

## Flujo principal
1. Usuario sube PDF de reserva (Airbnb/Booking)
2. OCR automático extrae: código reserva, nombre, personas, fechas, extras
3. Se crea registro en BD
4. Se sincroniza automáticamente con Google Calendar (3 calendarios disponibles)
5. Dashboard visualiza todas las reservas procesadas
6. URL única por reserva para que huéspedes completen sus datos (1-4 personas)

## Tech Stack
- **Backend**: Python + FastAPI
- **Frontend**: HTML/CSS/JavaScript vanilla, Mobile-first
- **Database**: Supabase (PostgreSQL hosted)
- **OCR**: Claude Vision API (automático)
- **Google Calendar**: Google Calendar API
- **Hosting**: (pendiente decidir)

## Estructura del Proyecto
```
registro-viajeros-manual/
├── backend/
│   ├── main.py              # Entrada principal FastAPI
│   ├── requirements.txt      # Dependencias Python
│   ├── .env.example          # Variables de entorno
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py         # Modelos de datos (Pydantic)
│   │   ├── database.py       # Conexión Supabase
│   │   ├── routes/
│   │   │   ├── reservations.py
│   │   │   ├── guests.py
│   │   │   └── ocr.py
│   │   └── services/
│   │       ├── claude_ocr.py
│   │       └── google_calendar.py
│   └── tests/
├── frontend/
│   ├── index.html            # Página principal
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   ├── pages/
│   │   ├── dashboard.html    # Panel de reservas
│   │   ├── upload.html       # Subida de PDF
│   │   └── guest-form.html   # Formulario huéspedes (URL única)
│   └── assets/
├── docs/
│   ├── setup.md              # Guía de configuración
│   ├── database-schema.md    # Schema de BD
│   └── api.md                # Documentación API
├── .gitignore
└── README.md
```

## Variables de Entorno (copiar a .env)
```
# Supabase
SUPABASE_URL=
SUPABASE_KEY=

# Claude API
CLAUDE_API_KEY=

# Google Calendar
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# App
DEBUG=True
PORT=8000
```

## Fases de Desarrollo

### Fase 1: Fundación (Esta semana)
- [x] Crear estructura Git
- [ ] Configurar Supabase (schema BD)
- [ ] Setup FastAPI básico
- [ ] Crear CRUD reservas

### Fase 2: OCR e Ingesta
- [ ] Endpoint subida PDF
- [ ] Integración Claude Vision
- [ ] Validación datos

### Fase 3: Google Calendar
- [ ] Autenticación OAuth
- [ ] Sincronización calendarios

### Fase 4: Frontend
- [ ] Dashboard reservas
- [ ] Formulario huéspedes

## Notas de desarrollo
- El usuario está aprendiendo Python, explicar conceptos conforme se avanza
- Mobile-first en el frontend
- OCR automático (confiar en Claude)
- URL de huéspedes es pública (sin autenticación)
