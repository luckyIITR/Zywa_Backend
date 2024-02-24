**Project Title:** Zywa Card Status API

**Problem Statement**

Zywa's support agents need a centralized way to quickly determine the current status of a user's card. This API combines data from multiple CSV files provided by partner companies to present a single, consolidated view of card statuses.

**Project Overview**

This project provides a RESTful API endpoint to fetch card statuses based on either a user's phone number or a unique card ID. The solution includes:

* **Database Integration:** A MongoDB to store and query data from CSV files, ensuring persistence beyond in-memory solutions.
* **API Endpoint:**  A `/get_card_status` endpoint that handles requests, performs data retrieval, and returns the current card status.
* **Flexible Design:**  Well-structured request and response payloads. 
* **Dockerization:** A Dockerfile for containerized deployment.

* **Data Description**  The project assumes a `data` folder containing CSV files with relevant card information. 

**API Endpoint 1.**

* **Method:** GET
* **Path:**  `/get_card_status/{identifier}`
* **identifier can be:**
   * `phone_number` **or**
   * `card_id` 
* **Sample Request** `/get_card_status/ZYW8827`
* **Sample Response:**

   ```json
   {
      "CARD_ID": "ZYW8827",
      "USER_CONTACT": "585949014",
      "STATUS_HISTORY": [
         {
            "STATUS": "PICKUP",
            "COMMENT": "",
            "TIMESTAMP": "2023-11-12T23:59:00"
         },
         {
            "STATUS": "DELIVERED",
            "COMMENT": "DELIVERED",
            "TIMESTAMP": "2023-11-13T09:34:56"
         }
      ]
   }
   ```

**API Endpoint 2.**
After uploading the csv file one can manually update the application
* **Method:** GET
* **Path:**  `/update_db`
* **Sample Request** `/update_db`
* **Sample Response:**

   ```json
   {
      "msg": "SUCCESS"
   }
   ```


**Getting Started**

1. **Unzip File:** Unzip all the files 
2. **Set up Environment(optional):** 
   * Create Python Virtual Environment
   ```
   python -m venv zywa
   ```
   * activate the env
   ```
   source zywa/bin/activate
   ```
3. **Install the requirements**
   ```
   pip install -r requirements.txt
   ```
4. **Import CSV Data:**  Copy all the CSV files in data folder
5. **Run the Application:**  
   ```
   uvicorn app:app --reload 
   ```

8. **Test the API:** 
   * go to `http://127.0.0.1:8000/docs`
   * You can test all the APIs from the above url

**Deployment**

* **Build Docker Image:**  `docker build -t card-status-api .`
* **Run Docker Container:** `docker run -p 8000:8000 card-status-api`

**Technologies Used**

* Python
* fastAPI
* MongoDB

**Contact**

* Project Maintainer: Lucky Kushwaha (lucky_k@ph.iitr.ac.in)
