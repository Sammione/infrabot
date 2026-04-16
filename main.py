from app.main import app

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use the PORT environment variable if it's set (usual for cloud deployments)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
