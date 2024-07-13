from .server_api import *

if __name__ == "__main__":
    """
    Auto run server
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
