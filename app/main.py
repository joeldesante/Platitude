from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/plates")
def create_plate():
    return {"hello": "world"}
