# Job Board 

Scrapes job postings from different websites and presents them in one place.

---

### Overview

Job Board allows users to quickly browse job listings aggregated from multiple sources in a single, easy-to-use interface. Service is updated with automated data pipeline every 24 hours.

The backend exposes a full set of CRUD endpoints, allowing for:

- Creating new job entries
- Retrieving jobs (by id or date)
- Updating existing job records
- Deleting jobs

---
### Tech Stack

**Backend:** FastAPI  
**Frontend:** Astro + Svelte  
**Database:** SQLite with SQLAlchemy ORM  
**Web Scraping:** BeautifulSoup  
**Containerization:** Docker  
**Other:** git, uv  

---

### Installation & Setup

Have [Docker](https://www.docker.com/products/docker-desktop/) installed and running

1. Clone the repository:

        git clone https://github.com/antinaho/full-stack-job-board.git  
        cd full-stack-job-board

2. Setup default environment variables:

        cp dev.env .env

3. Build the containers:

        docker compose build

4. Start the containers:

        docker compose up

5. Open your browser and go to: http://localhost:8080/ to see the app

6. Ctrl+C to stop, or in another terminal `docker compose down`


<br>

For local development have [uv](https://docs.astral.sh/uv/) and [node](https://nodejs.org/en/) installed.

Run `docker compose up db` in root folder. Run `uv run fastapi dev` inside backend folder to launch backend dev server  
Run `npm run dev` inside frontend folder to launch frontend dev server

---

### Testing

The project uses Pytest for testing. You need to have [uv](https://docs.astral.sh/uv/) installed.

Run tests with:

        uv run pytest