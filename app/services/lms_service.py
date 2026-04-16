import httpx
import logging
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class LMSClient:
    _client = None

    def __init__(self):
        self.base_url = settings.lms_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"{settings.lms_api_key}",
            "X-Tenant-Key": settings.lms_tenant_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def get_client(self):
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers
            )
        return self._client

    async def get_courses(self, search: str = None, page_size: int = 10):
        url = f"{self.base_url}/api/v1/Course"
        params = {"PageSize": page_size}
        if search:
            params["Search"] = search
        
        client = await self.get_client()
        try:
            logger.info(f"Fetching courses from LMS: {url} with params {params}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching courses from LMS: {str(e)}")
            return {"error": "LMS service unavailable", "details": str(e)}

    async def get_course_details(self, course_id: str):
        url = f"{self.base_url}/api/v1/Course/{course_id}"
        client = await self.get_client()
        try:
            logger.info(f"Fetching course details from LMS: {url}")
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching course details from LMS: {str(e)}")
            return {"error": f"Course {course_id} not found or LMS unavailable", "details": str(e)}

    async def get_assessments(self, course_id: str):
        url = f"{self.base_url}/api/v1/Assessment"
        params = {"CourseId": course_id}
        client = await self.get_client()
        try:
            logger.info(f"Fetching assessments from LMS for course: {course_id}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching assessments: {str(e)}")
            return {"error": "Assessments unavailable", "details": str(e)}

    async def get_my_certificates(self):
        url = f"{self.base_url}/api/v1/Certificate"
        client = await self.get_client()
        try:
            logger.info(f"Fetching certificates from LMS")
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching certificates: {str(e)}")
            return {"error": "Certificates unavailable", "details": str(e)}

# Singleton instance for better resource management
_lms_client_instance = LMSClient()

def get_lms_client():
    return _lms_client_instance

