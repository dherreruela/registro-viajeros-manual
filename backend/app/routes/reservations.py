from fastapi import APIRouter, HTTPException
from app.database import get_supabase
from app.models import ReservationCreate, ReservationUpdate, Reservation

router = APIRouter(prefix="/api/reservations", tags=["reservations"])
supabase = get_supabase()

# CREATE - Crear una nueva reserva
@router.post("/", response_model=dict)
def create_reservation(reservation: ReservationCreate):
    try:
        data = reservation.dict()
        data["check_in"] = str(data["check_in"])
        data["check_out"] = str(data["check_out"])
        result = supabase.table("reservations").insert(data).execute()

        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            raise HTTPException(status_code=400, detail="Error al crear reserva")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Obtener todas las reservas
@router.get("/")
def get_all_reservations(property_id: int = None):
    try:
        query = supabase.table("reservations").select("*")

        if property_id:
            query = query.eq("property_id", property_id)

        result = query.execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Obtener una reserva por ID
@router.get("/{reservation_id}")
def get_reservation(reservation_id: int):
    try:
        result = supabase.table("reservations").select("*").eq("id", reservation_id).execute()

        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# UPDATE - Actualizar una reserva
@router.put("/{reservation_id}")
def update_reservation(reservation_id: int, reservation: ReservationUpdate):
    try:
        # Solo actualizar campos que no son None
        data = {k: v for k, v in reservation.dict().items() if v is not None}

        if not data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")

        result = supabase.table("reservations").update(data).eq("id", reservation_id).execute()

        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE - Eliminar una reserva
@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int):
    try:
        result = supabase.table("reservations").delete().eq("id", reservation_id).execute()
        return {"success": True, "message": "Reserva eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
