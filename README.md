# 🤖 AI CRM Data Cleaner

AI CRM Data Cleaner is a powerful, lightweight, and extensible tool for cleaning, deduplicating, validating, and enriching CRM contact data using OpenAI and traditional logic. It supports CSV file uploads and processes large datasets in the background using Celery and Redis.

---

## 🚀 Features

- 🔍 **Email validation** using `email-validator`
- 🧠 **AI-powered enrichment** with OpenAI GPT (optional)
- 🧹 **Name, job title, and company normalization**
- 🏢 **Department guessing & seniority detection**
- 🌎 **Language detection & translation**
- 📞 **Phone number standardization (E.164 format)**
- 🧠 **Intent detection & note summarization**
- 📊 **Lead scoring, buyer persona classification**
- 😐 **Sentiment analysis & interest extraction**
- ❌ **Duplicate detection based on email and name similarity**
- ⏳ **Background job processing with status tracking**
- ⚡ **Built with FastAPI, SQLAlchemy, Celery, and Docker**

---

## 🛠 Tech Stack

- **FastAPI** – API Framework  
- **Celery + Redis** – Task queue and broker  
- **PostgreSQL** – Data persistence  
- **Pandas** – Data processing  
- **OpenAI** – AI enrichment (optional)  
- **Docker** – Containerization  

---

## 📦 Directory Structure

```
.
├── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── models.py             # Database models
│   ├── tasks.py              # Celery tasks for background jobs
│   ├── cleaning.py           # Data cleaning/enrichment logic
│   ├── ai_utils.py           # OpenAI API wrapper with failover handling
│   ├── database.py           # SQLAlchemy engine and session setup
│   ├── celery_worker.py      # Celery app and queue config
│   └── routers/
│       ├── job.py            # Job submission, tracking APIs
│       └── upload.py         # File upload and validation endpoints
├── scripts/
│   └── generate_fake_contacts.py # Generate demo CRM CSV
├── init_db.py                # Initialize database tables
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your-openai-key
REDIS_URL=redis://redis:6379/0
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

You can leave `OPENAI_API_KEY` blank to disable enrichment.

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```

Your API will be available at:

```
http://localhost:8000
```

You can access the interactive docs at:

```
http://localhost:8000/docs
```

---

## 📄 Sample API Usage

### 📤 Upload a File

```http
POST /upload/
```

**Form Data**:
- `file`: CSV file with columns like `name`, `email`, `phone`, `job_title`, `company`, `note`, etc.

Returns a job ID to check status later.

---

### 📥 Check Job Status

```http
GET /jobs/{job_id}
```

Returns job details including status and cleaned row count.

---

### 📥 Download Cleaned Data

```http
GET /jobs/{job_id}/download
```

Returns the cleaned CSV file for the given job as an attachment.

---

## 🧪 Generate Demo Contacts

```bash
python scripts/generate_fake_contacts.py
```

Generates a realistic CSV of fake CRM contacts at `/data/demo_contacts.csv`.

---

## ✨ Enrichment Fields (AI-powered)

If OpenAI is enabled, each row can be enriched with:

- `email_valid`
- `name_normalized`
- `job_title_normalized`
- `company_normalized`
- `department`
- `seniority`
- `industry`
- `note_summary`
- `note_language`
- `note_translated`
- `sentiment`
- `intent`
- `lead_quality`
- `lead_stage`
- `persona`
- `interest`
- `skills`
- `company_size_guess`
- `hiring_intent`
- `churn_risk`
- `geo_match`
- `timezone`
- `domain_category`
- `email_type`
- `phone_cleaned`
- `meeting_date`
- `next_action`

If OpenAI credits are exhausted or invalid, AI-based enrichment is automatically skipped.

---

## 🧾 License

MIT License — free for personal and commercial use.

---

## 👨‍💻 Author

Made with ❤️ by [Waseef Ullah](https://www.linkedin.com/in/waseef-ullah)

---

## ⭐️ Support

If you find this project useful, feel free to ⭐️ the repository or contribute via pull requests!