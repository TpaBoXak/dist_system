import uvicorn
from app import app
from config import settings

import time
if __name__ == "__main__":
    uvicorn.run(app="app:app", reload=True,
            host=settings.run.host,
            port=settings.run.port)