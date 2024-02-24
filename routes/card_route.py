from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models.cards import Card
from models.update_data import *
import os
router = APIRouter()


@router.get("/update_db", status_code=status.HTTP_200_OK)
async def update_database():
    Card.dropcollection()

    files = os.listdir("data/")
    labeled_files = get_labeled_files(files)
    for file in labeled_files['PICKUP']:
        df = pd.read_csv(os.path.join("data", file))
        df = process_dataframe(df, "PICKUP")

        for i in range(len(df)):
            CARD_ID = df.iloc[i]["CARD_ID"]
            USER_CONTACT = df.iloc[i]["USER_CONTACT"]
            comment = df.iloc[i]["COMMENT"] if "COMMENT" in df.iloc[i].to_dict().keys() else ""
            STATUS_HISTORY = [
                {"STATUS": df.iloc[i]["STATUS"], "COMMENT": comment, "TIMESTAMP": df.iloc[i]["TIMESTAMP"]}]

            card = Card(CARD_ID, USER_CONTACT, STATUS_HISTORY)
            card.save()

    statuses = ["DELIVERED", "RETURNED", "EXCEPTIONS"]
    for status in statuses:
        for file in labeled_files[status]:
            df = pd.read_csv(os.path.join("data", file))
            df = process_dataframe(df, status)
            for i in range(len(df)):
                CARD_ID = df.iloc[i]["CARD_ID"]
                USER_CONTACT = df.iloc[i]["USER_CONTACT"]
                comment = df.iloc[i]["COMMENT"] if "COMMENT" in df.iloc[i].to_dict().keys() else ""
                STATUS_HISTORY = {"STATUS": df.iloc[i]["STATUS"], "COMMENT": comment, "TIMESTAMP": df.iloc[i]["TIMESTAMP"]}

                # Find a card by CARD_ID
                found_card = Card.find_by_card_id(CARD_ID)
                found_card
                if found_card:
                    found_card.update_status(**STATUS_HISTORY)
    return {"msg" : "SUCCESS"}


@router.get("/{identifier}", status_code=status.HTTP_200_OK)
async def get_card_status(identifier : str):
    card = Card.find_by_card_id(identifier)
    if not card:
        card = Card.find_by_contant(identifier)
    if not card:
        return {"msg" : "No Data found"}

    latest_status = max(card.STATUS_HISTORY, key=lambda x: x['TIMESTAMP'])
    data = {"CARD_ID" : card.CARD_ID, "USER_CONTACT" : card.USER_CONTACT, "STATUS" : latest_status}
    return data


