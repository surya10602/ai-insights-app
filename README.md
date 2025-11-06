# AI Insight Generator

This is a full-stack web application built to provide AI-powered insights on meeting transcripts and LinkedIn profiles. It uses an asynchronous task queue to handle long-running AI jobs, with a real-time polling frontend to display results as soon as they are ready.



## Features

* ** Transcript Insight:** Paste a meeting transcript and its metadata. The app analyzes what went well, what could be improved, and provides recommendations for the next meeting.
* ** LinkedIn Icebreaker:** Paste a person's LinkedIn bio and a summary of your pitch deck. The app generates a detailed icebreaker, identifies buying signals, and provides smart discovery questions.
* ** Async Task Queue:** User submissions are instant. Jobs are sent to a background queue, and the frontend shows a "Processing..." status.
* ** Real-time Polling:** The frontend automatically polls the backend and updates the UI from "Processing..." to the final AI-generated text without requiring a page refresh.

## Tech Stack

* **Frontend:** Next.js, React, Tailwind CSS, Shadcn UI
* **Backend:** FastAPI (Python)
* **Database:** Supabase (PostgreSQL)
* **AI:** Groq API
* **Task Queue:** Arq (Python), Upstash (Redis)
* **Deployment:** Vercel (Frontend), Render (Backend Web Service)

## Application Architecture

This project is deployed on a "free-tier-friendly" model, running the entire backend in a single Render Web Service.

1.  The **Next.js Frontend** (on Vercel) makes an API call to the backend.
2.  The **FastAPI Backend** (on Render) receives the request.
3.  FastAPI immediately saves a "Processing..." entry to **Supabase** and enqueues a job in **Upstash (Redis)**.
4.  The **Arq Worker**, which is launched as a background task *in the same Render process*, pulls the job from the queue.
5.  The worker calls the **Groq API** to get the analysis.
6.  The worker updates the "Processing..." entry in **Supabase** with the final text.
7.  The **Next.js Frontend** polls the `/insights` endpoint every 3 seconds (only while a job is processing) and updates the UI live as soon as the change is detected.

## Local Setup & Installation

To run this project locally, you will need two terminals.

### Prerequisites

* [Node.js](https://nodejs.org/en)
* [Python](https://www.python.org/)
* [Git](https://git-scm.com/)
* Accounts for [Supabase](https://supabase.com/), [Groq](https://groq.com/), and [Upstash](https://upstash.com/).

---

### 1. Backend Setup (Terminal 1)

1.  Navigate to the `backend` folder:
    ```bash
    cd backend
    ```
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `backend` folder and add your secret keys:
    ```.env
    # Supabase
    SUPABASE_URL=...
    SUPABASE_KEY=...

    # Groq
    GROQ_API_KEY=...

    # Upstash (Redis)
    UPSTASH_REDIS_HOST=...
    UPSTASH_REDIS_PASSWORD=...
    ```
5.  Run the backend server. The `main.py` file is configured to launch both the API and the worker:
    ```bash
    uvicorn main:app --reload
    ```
    You should see logs for both Uvicorn and the Arq worker starting up.

---

### 2. Frontend Setup (Terminal 2)

1.  Navigate to the `frontend` folder:
    ```bash
    cd frontend
    ```
2.  Install the required packages:
    ```bash
    npm install
    ```
3.  Create a `.env.local` file in the `frontend` folder. This tells your frontend to talk to your local backend.
    ```.env.local
    NEXT_PUBLIC_API_BASE_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
    ```
4.  Run the frontend development server:
    ```bash
    npm run dev
    ```

Your application is now running:
* **Frontend:** `http://localhost:3000`
* **Backend API:** `http://127.0.0.1:8000`