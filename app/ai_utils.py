import os
from openai import OpenAI
from openai._exceptions import APIError, AuthenticationError, RateLimitError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENABLED = bool(OPENAI_API_KEY)

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_ENABLED else None

def call_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    global OPENAI_ENABLED

    if not OPENAI_ENABLED:
        return ""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for CRM data cleaning."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    except (AuthenticationError, RateLimitError, APIError) as e:
        print(f"[OpenAI Disabled] {e}")
        OPENAI_ENABLED = False
        return ""

    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return ""


def normalize_job_title(title: str) -> str:
    if not title:
        return ""
    return call_openai(f"Normalize this job title: '{title}'. Only return the cleaned job title.")


def normalize_name(name: str) -> str:
    if not name:
        return ""
    parts = name.strip().split()
    return " ".join(p.capitalize() for p in parts)


def normalize_company_name(company: str) -> str:
    if not company:
        return ""
    return call_openai(f"Clean and standardize this company name: '{company}'. Only return the corrected name.")


def guess_department(name: str, title: str) -> str:
    if not title:
        return ""
    return call_openai(f"Guess the department of a person named '{name}' with the title '{title}'. Only return the department.")


def classify_note_intent(note: str) -> str:
    if not note:
        return "Other"
    return call_openai(f"What is the intent of this CRM note: '{note}'? Return only one of: Inquiry, Complaint, Follow-up, Unsubscribe, Other.")


def is_valid_name(name: str):
    if not name:
        return ""
    
    response = call_openai(f"Is '{name}' a valid full name? Reply only with 'yes' or 'no'.")
    if not response:
        return ""
    
    response = response.lower().strip()
    if response.startswith("y"):
        return True
    elif response.startswith("n"):
        return False
    else:
        return ""
    

def summarize_note(note: str) -> str:
    if not note:
        return ""
    return call_openai(f"Rephrase this CRM note professionally: '{note}'")


def detect_language(text: str) -> str:
    if not text:
        return ""
    return call_openai(f"What language is this text written in: '{text}'? Return only the language name.")


def translate_to_english(text: str) -> str:
    if not text:
        return ""
    return call_openai(f"Translate this to English: '{text}'")


def extract_seniority_level(title: str) -> str:
    if not title:
        return ""
    return call_openai(f"What is the seniority level in this job title: '{title}'? Reply with one of: Entry-level, Mid, Senior, Executive, Unknown.")


def detect_industry(company: str, job_title: str = "") -> str:
    if not company:
        return ""
    return call_openai(f"Based on the company name '{company}' and job title '{job_title}', what is the likely industry? Return a single industry name like 'Healthcare', 'Tech', 'Finance', etc.")


def clean_phone_number(phone: str) -> str:
    if not phone:
        return ""
    return call_openai(f"Standardize this phone number: '{phone}'. Use international E.164 format if possible. Only return the cleaned number.")


def extract_location_from_note(note: str) -> str:
    if not note:
        return ""
    return call_openai(f"Extract the geographic location (e.g., city or country) mentioned in this CRM note: '{note}'. Return only the location or 'Unknown'.")


def suggest_next_action(note: str) -> str:
    if not note:
        return ""
    return call_openai(f"Based on this CRM note: '{note}', suggest a follow-up action (e.g., Call, Email, Close, Escalate). Return only the suggested action.")


def categorize_lead_stage(note: str, job_title: str = "") -> str:
    if not note:
        return ""
    prompt = f"Given the note: '{note}', and job title: '{job_title}', classify the lead stage. Reply with one of: Cold, Warm, Hot, Closed, Nurturing."
    return call_openai(prompt)


def detect_buyer_persona(job_title: str, department: str = "", company_size: str = "") -> str:
    if not job_title:
        return ""
    prompt = f"What buyer persona does this describe? Title: '{job_title}', Department: '{department}', Company size: '{company_size}'. Return one persona like 'Decision Maker', 'Influencer', 'Champion', 'Gatekeeper', 'User', or 'Unknown'."
    return call_openai(prompt)


def score_lead_quality(job_title: str, company: str, note: str) -> str:
    if not job_title:
        return ""
    prompt = f"Based on job title '{job_title}', company '{company}', and CRM note '{note}', how would you rate the lead quality? Reply with: High, Medium, or Low."
    return call_openai(prompt)


def extract_meeting_date(note: str) -> str:
    if not note:
        return ""
    prompt = f"Does this note contain a meeting or call date? If yes, extract the date in ISO format (YYYY-MM-DD), otherwise return 'None'. Note: '{note}'"
    return call_openai(prompt)


def detect_sentiment(note: str) -> str:
    if not note:
        return ""
    prompt = f"What is the sentiment of this CRM note: '{note}'? Return: Positive, Neutral, or Negative."
    return call_openai(prompt)


def detect_product_interest(note: str) -> str:
    if not note:
        return ""
    prompt = f"Based on this CRM note: '{note}', what product or service is the person showing interest in? Return a short answer like 'CRM software', 'Pricing plan', 'Training', or 'Unknown'."
    return call_openai(prompt)


def extract_domain_category(website: str) -> str:
    if not website:
        return "Unknown"
    return call_openai(f"What is the category or industry of this website: '{website}'? Return a single word like 'Tech', 'Retail', 'Education', etc.")


def infer_timezone_from_city(city: str) -> str:
    if not city:
        return "Unknown"
    return call_openai(f"What is the time zone for the city '{city}'? Return only the time zone name like 'PST', 'EST', 'CET', etc.")


def extract_skills_from_note(note: str) -> str:
    if not note:
        return ""
    return call_openai(f"What job-related skills or keywords are mentioned or implied in this note: '{note}'? Return a comma-separated list of 1-5 concise skills.")


def guess_company_size(company: str) -> str:
    if not company:
        return "Unknown"
    return call_openai(f"Based on the company name '{company}', what is the most likely size? Reply with: Small (1-50), Medium (51-500), Large (500+), or Unknown.")


def email_type(email: str) -> str:
    if not email:
        return "Unknown"
    return call_openai(f"Is this email address '{email}' corporate or personal? Reply with: Corporate or Personal.")


def estimate_hiring_intent(job_title: str, note: str) -> str:
    if not note:
        return "Unknown"
    return call_openai(f"Does this CRM note and job title indicate a potential hiring or recruitment need? Note: '{note}', Title: '{job_title}'. Reply with: Yes, No, or Unclear.")


def detect_churn_risk(note: str) -> str:
    if not note:
        return "Unknown"
    return call_openai(f"Based on this note, how likely is this contact to stop engaging with us or churn? Note: '{note}'. Reply with: High, Medium, Low.")


def verify_company_location(company: str, city: str) -> str:
    if not company or not city:
        return "Unknown"
    return call_openai(f"Is it common or expected for the company '{company}' to operate in the city '{city}'? Reply with: Likely, Unlikely, or Unknown.")

