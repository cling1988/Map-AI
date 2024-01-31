
# Outlet Map And SQL Agent

This project is sample using web scraping list of outlet information and display it in google map.
The data will store into SQL database and create a SQL Agent by using LLM OpenAI

## Prerequisite
- Python 3.10 above
- nodejs
- OpenAI API key
- Google API key

## Setup
### Frontend
1. Go to folder frontend
2. Install js library with execute 'npm install'
3. Create .env from .env.example with include Google API key
4. Build js library with execute 'npm run build --production'

### App
1. Create .env from .env.example with include OpenAI API key, database url and data csv file path.
2. Edit docker-compose.yaml for the volumns
3. Build the docker with execute 'docker compose build'
4. Start the docker with execute 'docker compose up -d'

### After
- If first time, go to url /api/create/outlet to trigger DB insert
- Go to the url wiht port 60001 to view the page.


## Tool
1. collect_postcode.py
    - use for collect kl postcode and will store in /data/kl_postcode.txt
2. collect_subway_info.py
    - use for collect subway infor and will store in /data/all_shop_info.csv
3. process_data.py
    - use for clean/transform/filter collected subway data and will store in /data/final.csv
    - this result will use to store in DB

## API
1. GET /api/outlets
   - to query all outlet info from DB
2. GET /api/create/outlet
   - to insert processed csv data into DB
3. POST /api/auery
   - to query by using LLM model
   - this will using OpenAI model will have cost