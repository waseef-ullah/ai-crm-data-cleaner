import pandas as pd
from email_validator import validate_email, EmailNotValidError
from rapidfuzz import fuzz
from app.ai_utils import (
    categorize_lead_stage,
    clean_phone_number,
    detect_buyer_persona,
    detect_churn_risk,
    detect_industry,
    detect_product_interest,
    detect_sentiment,
    email_type,
    estimate_hiring_intent,
    extract_domain_category,
    extract_location_from_note,
    extract_meeting_date,
    extract_seniority_level,
    extract_skills_from_note,
    guess_company_size,
    infer_timezone_from_city,
    is_valid_name,
    normalize_job_title,
    normalize_name,
    normalize_company_name,
    guess_department,
    classify_note_intent,
    score_lead_quality,
    suggest_next_action,
    summarize_note,
    detect_language,
    translate_to_english,
    verify_company_location,
)
from app.ai_utils import OPENAI_ENABLED

def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def deduplicate_records(records, key_fields=('email', 'phone', 'name')):
    seen = {}
    keep = []
    for r in records:
        email = (r.get('email') or "").strip().lower()
        if email:
            if email in seen:
                continue
            seen[email] = True
            keep.append(r)
        else:
            duplicate = False
            for s in keep:
                if fuzz.token_sort_ratio((s.get('name') or ""), (r.get('name') or "")) > 90:
                    duplicate = True
                    break
            if not duplicate:
                keep.append(r)
    return keep

def process_dataframe(df: pd.DataFrame):
    records = df.fillna("").to_dict(orient="records")
    deduped = deduplicate_records(records)

    for r in deduped:
        r['email_valid'] = validate_email_address(r.get('email', ''))
        r['name_normalized'] = normalize_name(r.get('name', ''))

        if OPENAI_ENABLED:
            r['job_title_normalized'] = normalize_job_title(r.get('job_title', ''))
            r['company_normalized'] = normalize_company_name(r.get('company', ''))
            r['department'] = guess_department(r.get('name', ''), r.get('job_title', ''))
            r['intent'] = classify_note_intent(r.get('note', ''))
            r['name_valid'] = is_valid_name(r.get('name', ''))
            r['note_summary'] = summarize_note(r.get('note', ''))
            r['note_language'] = detect_language(r.get('note', ''))
            r['note_translated'] = translate_to_english(r.get('note', ''))
            r['seniority'] = extract_seniority_level(r.get('job_title', ''))
            r['industry'] = detect_industry(r.get('company', ''), r.get('job_title', ''))
            r['phone_cleaned'] = clean_phone_number(r.get('phone', ''))
            r['location'] = extract_location_from_note(r.get('note', ''))
            r['next_action'] = suggest_next_action(r.get('note', ''))
            r['lead_stage'] = categorize_lead_stage(r.get('note', ''), r.get('job_title', ''))
            r['persona'] = detect_buyer_persona(r.get('job_title', ''), r.get('department', ''), '')
            r['lead_quality'] = score_lead_quality(r.get('job_title', ''), r.get('company', ''), r.get('note', ''))
            r['meeting_date'] = extract_meeting_date(r.get('note', ''))
            r['sentiment'] = detect_sentiment(r.get('note', ''))
            r['interest'] = detect_product_interest(r.get('note', ''))
            r['skills'] = extract_skills_from_note(r.get('note', ''))
            r['email_type'] = email_type(r.get('email', ''))
            r['company_size_guess'] = guess_company_size(r.get('company', ''))
            r['hiring_intent'] = estimate_hiring_intent(r.get('job_title', ''), r.get('note', ''))
            r['churn_risk'] = detect_churn_risk(r.get('note', ''))
            r['geo_match'] = verify_company_location(r.get('company', ''), r.get('city', ''))
            r['domain_category'] = extract_domain_category(r.get('website', ''))
            r['timezone'] = infer_timezone_from_city(r.get('city', ''))

    return deduped