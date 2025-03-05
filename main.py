from api import app

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app (use "main:app" if your app is defined in main.py)
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
