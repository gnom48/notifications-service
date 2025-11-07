import uvicorn

from app.rest.server import app
from app.configs import SERVER_CONFIG

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",
                port=SERVER_CONFIG.SERVER_PORT, reload=True)
