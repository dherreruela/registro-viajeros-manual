from fastapi import APIRouter, HTTPException
from app.database import get_supabase
from app.models import PropertyCreate
from app.services.google_calendar import get_calendar_events
from typing import Optional

router = APIRouter(prefix="/api/properties", tags=["properties"])
supabase = get_supabase()

# CREATE - Crear una propiedad
@router.post("/", response_model=dict)
def create_property(property_data: PropertyCreate):
    try:
        data = property_data.dict()
        result = supabase.table("properties").insert(data).execute()

        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            raise HTTPException(status_code=400, detail="Error al crear propiedad")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Obtener todas las propiedades
@router.get("/")
def get_all_properties():
    try:
        result = supabase.table("properties").select("*").execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Obtener una propiedad por ID
@router.get("/{property_id}")
def get_property(property_id: int):
    try:
        result = supabase.table("properties").select("*").eq("id", property_id).execute()

        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# UPDATE - Actualizar una propiedad
@router.put("/{property_id}")
def update_property(property_id: int, property_data: PropertyCreate):
    try:
        data = property_data.dict()
        result = supabase.table("properties").update(data).eq("id", property_id).execute()

        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Obtener eventos del calendario de una propiedad
@router.get("/{property_id}/calendar-events")
def get_property_calendar_events(property_id: int, days_ahead: int = 30):
    try:
        # Obtener la propiedad
        property_result = supabase.table("properties").select("*").eq("id", property_id).execute()

        if not property_result.data:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")

        property_data = property_result.data[0]
        calendar_id = property_data["google_calendar_id"]

        # Obtener eventos del calendario
        events = get_calendar_events(calendar_id, days_ahead)

        return {"success": True, "data": events}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE - Eliminar una propiedad (con cascada)
@router.delete("/{property_id}")
def delete_property(property_id: int):
    try:
        # Primero obtener todas las reservas de esta propiedad
        reservations = supabase.table("reservations").select("id").eq("property_id", property_id).execute()

        # Eliminar huéspedes de esas reservas
        if reservations.data:
            for res in reservations.data:
                supabase.table("guests").delete().eq("reservation_id", res["id"]).execute()

        # Eliminar las reservas
        supabase.table("reservations").delete().eq("property_id", property_id).execute()

        # Finalmente eliminar la propiedad
        result = supabase.table("properties").delete().eq("id", property_id).execute()

        return {"success": True, "message": "Propiedad y sus reservas eliminadas"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error al eliminar: {str(e)}")
