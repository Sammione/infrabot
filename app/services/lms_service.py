import httpx
from app.core.config import get_settings

settings = get_settings()

class LMSClient:
    def __init__(self):
        self.base_url = settings.lms_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"{settings.lms_api_key}",
            "X-Tenant-Key": settings.lms_tenant_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def get_courses(self, search: str = None, page_size: int = 10):
        url = f"{self.base_url}/api/v1/Course"
        params = {"PageSize": page_size}
        if search:
            params["Search"] = search
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def get_course_details(self, course_id: str):
        url = f"{self.base_url}/api/v1/Course/{course_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_faqs(self):
        # Placeholder: If the LMS has an FAQ endpoint, we'd call it here
        # For now, let's assume there's a Knowledge endpoint or logic
        url = f"{self.base_url}/api/v1/Knowledge/faqs" # Hypothetical
    async def get_assessments(self, course_id: str):
        url = f"{self.base_url}/api/v1/Assessment"
        params = {"CourseId": course_id}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def get_my_certificates(self):
        url = f"{self.base_url}/api/v1/Certificate"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

def get_lms_client():
    return LMSClient()
