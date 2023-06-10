import uvicorn
from app.config.config import PORT_SERVER

if __name__ == "__main__":
    config = uvicorn.Config("app.app:app", host="127.0.0.1",
                            port=PORT_SERVER, reload=True)
    server = uvicorn.Server(config)
    server.run()
