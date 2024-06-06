# Web Scraper with Django Backend

### Overview
This project is a web scraping tool integrated with Django and Celery for fetching real-time data about cryptocurrency coins from various sources. It allows users to submit a list of coin abbreviations, which are then scraped concurrently using Celery tasks. The scraped data includes information such as price, market cap, volume, circulating supply, social media links, and more.

### Features
- Scraping Coin Data: Users can submit a list of coin abbreviations to fetch real-time data about cryptocurrencies.
- Concurrent Scraping: Celery is used for concurrent task execution, ensuring efficient and parallel scraping of multiple coins.
- RESTful API: The project provides RESTful APIs for starting scraping tasks and retrieving scraped data based on job IDs.
- Database Integration: Scraped data is stored in a database for easy access and retrieval.
- Admin Interface: The Django admin panel allows administrators to manage scraping tasks and view scraped data.

### Screenshots
![Screenshot 2024-06-07 033844](https://github.com/Miran-Firdausi/WebScraper-Backend/assets/75238590/169ec647-6773-4353-9544-5d5166e2a715)
![Screenshot 2024-06-07 033909](https://github.com/Miran-Firdausi/WebScraper-Backend/assets/75238590/7623d659-7b04-4c0c-bcd1-9acf5aa5d848)
![Screenshot 2024-06-07 033923](https://github.com/Miran-Firdausi/WebScraper-Backend/assets/75238590/e3034540-0bb5-4f49-aaf9-c048cbfed366)
![Screenshot 2024-06-07 034006](https://github.com/Miran-Firdausi/WebScraper-Backend/assets/75238590/f5016bcd-da5c-4827-9197-7f60dc9f36a6)
![Screenshot 2024-06-07 034024](https://github.com/Miran-Firdausi/WebScraper-Backend/assets/75238590/f57f838b-78ce-4e70-9466-67d4589957f6)

### Usage
1. Access the Django admin panel at http://localhost:8000/admin/ and create a superuser account.
2. Use the provided APIs to start scraping tasks and retrieve scraped data.

### API Endpoints
- *POST /api/taskmanager/start_scraping:* Start a new scraping task by providing a list of coin abbreviations and returns a unique job id.
- *GET /api/taskmanager/scraping_status/<job_id>:* Retrieve scraped data for a specific job ID.

### Technologies Used
Celery: Distributed task queue for asynchronous processing
Selenium: Automating web browsers tool
Beautifulsoup: Web scraping library that allows us to parse web pages
Django: Web framework for backend development
Django REST Framework: Toolkit for building RESTful APIs
SQLite: Database for storing scraped data

