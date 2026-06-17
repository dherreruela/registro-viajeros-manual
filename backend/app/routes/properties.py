from fastapi import APIRouter, HTTPException
from app.database import get_supabase
from app.models import PropertyCreate

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
