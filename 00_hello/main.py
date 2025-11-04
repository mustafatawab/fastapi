from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get("/")
async def home():
    return {"message" : "Hello World"}