# run_server.py
import os
import uvicorn

def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True, workers=1, log_level="info")

if __name__ == "__main__":
    main()
