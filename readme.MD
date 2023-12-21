## Django Project

This application is a Django project which is a ad scraper.

## Installation
1. Clone the repository. `git clone https://github.com/Dylan-YD/scraper.git`
2. Install Python on your machine.
3. Navigate to the project folder. `cd scraper`
4. Install requirements. `pip install -r requirements.txt`
5. Create .env file
6. Put your secret key, domain, aws information in .env file like .env.example
5. Run the server. `python manage.py runserver`


## Usage
1. Go to the home page. `http://127.0.0.1:8000/`
2. Enter the query of the ads you want to scrape.
3. Click the button to scrape the website.
4. The progress will be shown on the page.
5. After the scraping is done, the result will be shown on the page `http://127.0.0.1:8000/crawler/ads`.

## project structure
```
scraper
├── crawler
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
└── scraper
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```
