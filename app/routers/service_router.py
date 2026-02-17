from fastapi import APIRouter, Depends, HTTPException
from app.services.service_service import ServiceService
from app.dependencies import get_service_service
from app.schemas import ServiceCreate, ServiceResponse

router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=ServiceResponse, status_code=201)
def create_service(
    req: ServiceCreate,
    service: ServiceService = Depends(get_service_service)
):
    try:
        return service.create_service(req.name, req.url, req.expected_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ServiceResponse])
def get_services(
    service: ServiceService = Depends(get_service_service)
):
    return service.list_services()


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: int,
    service: ServiceService = Depends(get_service_service)
):
    obj = service.get_service(service_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")
    return obj


@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    service: ServiceService = Depends(get_service_service)
):
    success = service.delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"ok": True}
