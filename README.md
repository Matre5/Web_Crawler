# Web Crawling project
A web crawler and API for scraping book data built with python and its libraries.
This project used MongoDb to store the database; specifically MongoDb Atlas so as to have it on the cloud.  
The data retrieved is served using FastAPI with API key aunthentication for security purposes and controlled access.

## Features
- Asynchronous web crawler application
- Stores data in MonogDb
- FastApi endpoints to:
  -  List books ( with pagination)
  -  Search books with certain filers
  -  Retrieve specific books by their ID
  -  View changes
  -  See statistics of data
- Swagger UI documentation (/docs)

## Folder Structure
<img width="692" height="303" alt="image" src="https://github.com/user-attachments/assets/fd7c73eb-222e-4592-b318-c205865a7486" />


# Setup Instructions
1. Clone the repository
2. Create and activate a virtual environment
 <br>  <img width="308" height="222" alt="image" src="https://github.com/user-attachments/assets/f8bf7f76-48cb-46ea-9d77-f0efc3635dd9" />

3. Install dependencies
 <br>  <img width="346" height="62" alt="image" src="https://github.com/user-attachments/assets/2f17dff8-962b-469c-a9c8-08605a9f4240" />
4. Create a .env file in the root directory this will hold the authentication keys.

# Running the Project
1. Start the FastAPI server
  <br> <img width="302" height="52" alt="image" src="https://github.com/user-attachments/assets/7d3cfea1-d2f1-4ffb-ac7e-78e216b51f47" />

2. Access the API <br>
Swagger UI: http://127.0.0.1:8000/docs
<br>
ReDoc: http://127.0.0.1:8000/redoc
<br>
4. Endpoints
 <br>  <img width="576" height="217" alt="image" src="https://github.com/user-attachments/assets/b01b60ad-1356-4897-b594-ef6fa74f7a83" />

Example MongoDB Document: <br>
{
  "_id": "64b9e5f9e5a4b1234567890a", <br>
  "title": "A Light in the Attic", <br>
  "price_including_tax": 51.77, <br>
  "availability": "In stock", <br>
  "rating": 3, <br>
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", <br>
  "category": "Poetry" <br>
}

# Testing
All tests are in the Tests/ folder and run using pytest
<img width="547" height="42" alt="image" src="https://github.com/user-attachments/assets/15d8e5f0-c6cb-40f0-bd74-91922f835a4b" /> <br>
Test include:
1. Endpoints status check
2. Valid and invalid id checks
3. Search and filter checks
4. Categories, stats and health checks

# Screenshots
Pytest test
<br>
<img width="1914" height="844" alt="image" src="https://github.com/user-attachments/assets/bbee4fb8-46b2-49ef-9e82-82123c2d7098" />
<br>
Page Crawling (Page 51 does not exist hence the error message and after 3 tries it moves on)
<img width="1682" height="1008" alt="image" src="https://github.com/user-attachments/assets/fbc9bef5-1eef-4564-a842-33122ac1a8d2" />
<img width="1912" height="395" alt="image" src="https://github.com/user-attachments/assets/03872a1a-1836-4306-8988-869edcbf525d" />
Crawler successfully found 1000 books from 50 pages <br>
Each book and their details crawled and stored to the database successfully
<img width="1905" height="727" alt="image" src="https://github.com/user-attachments/assets/53d13168-091f-40a0-98ca-dc9eac82b860" />





