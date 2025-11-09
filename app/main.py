if __name__ == "__main__":
    import uvicorn

    from .rest.server import app as asgi_application
    from .configs import SERVER_CONFIG

    uvicorn.run(asgi_application, host="0.0.0.0",
                port=int(SERVER_CONFIG.SERVER_PORT))
