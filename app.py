from fastapi import FastAPI
from dotenv import load_dotenv
from routes import card_route
from starlette import status


load_dotenv()
app = FastAPI()

app.include_router(card_route.router)

@app.get("/", status_code=status.HTTP_200_OK)
def welcome():
    return {"msg" : "Welcome to Zywa's Backend Engineer Assignment. Go to /docs to get all details"}