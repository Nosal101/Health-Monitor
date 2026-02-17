from app.repositories.service_repo import ServiceRepository
from app.models.service import Service

class ServiceService:
    def __init__(self, repo: ServiceRepository):
        self.repo = repo

    def create_service(self, name: str, url: str, expected_status: int = 200) -> Service:
        if not name or not url:
            raise ValueError("Name and URL must not be empty")
        
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        
        existing_service = self.repo.get_by_url(url)
        if existing_service:
            raise ValueError(f"Service with URL '{url}' already exists (id: {existing_service.id})")
        
        service = Service(name=name, url=url, expected_status=expected_status)
        return self.repo.create(service)

    def list_services(self) -> list[Service]:
        return self.repo.get_all()

    def get_service(self, service_id: int) -> Service | None:
        return self.repo.get_by_id(service_id)

    def delete_service(self, service_id: int) -> bool:
        return self.repo.delete(service_id)
