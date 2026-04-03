import time
import logging
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import router
from app.core.config import settings

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=settings.PROJECT_NAME)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 1. CORS for Mobile Clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In strict production, lock this down or keep open for native mobile
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Simple API Key Authentication
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(api_key_header: str = Depends(api_key_header)):
    if not api_key_header or api_key_header.replace("Bearer ", "") != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization header",
        )
    return api_key_header

# 3. Rate-Limits & 7. Logging Middlewares applied at router dependencies or directly
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"path={request.url.path} method={request.method} status_code={response.status_code} process_time={formatted_process_time}ms")
    return response

# Hook up Unified Router securely
app.include_router(router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])

@app.get("/health")
async def health():
    return {"status": "Evidexus backend running"}
