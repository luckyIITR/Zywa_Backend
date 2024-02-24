from fastapi import FastAPI
from dotenv import load_dotenv
from routes import card_route


load_dotenv()
app = FastAPI()

app.include_router(card_route.router)
