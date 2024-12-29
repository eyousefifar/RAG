from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="RAG", version="0.1.0")


# # Startup event for connecting to MongoDB
# @app.on_event("startup")
# async def startup_event():
#     print(f"Connecting to MongoDB at {MONGO_URI}...")
#     await connect_to_mongo()
#     print("Successfully connected to MongoDB.")


# # Shutdown event for closing MongoDB connection
# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Closing MongoDB connection...")
#     await close_mongo_connection()
#     print("MongoDB connection closed.")


app.include_router(router, prefix="/api", tags=["API Endpoints"])
