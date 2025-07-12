from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "New Learning"}

@app.get('/about')
def read_about():
    return {"message": "This is a basic FastAPI application."}