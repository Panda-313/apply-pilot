from pathlib import Path

BASE_NODE_MODEL = "gpt-4o-mini"
PARSE_OFFER_PROMPT = """You are an expert job offer parser. Your only task is to extract structured information from the provided job offer text.

Rules (strictly follow them):
- Extract ONLY information that is explicitly present in the text.
- NEVER invent, assume, or hallucinate skills, technologies, company names, requirements, or any other details.
- If a piece of information is missing, use an empty list [] or a short neutral description.
- Keep the "description" field concise (2-5 sentences max).
- Put required skills and experience into "must_have".
- Put preferred / nice-to-have skills into "nice_to_have".
- "tech_stack" should contain all technologies, tools, and frameworks mentioned.
- Always copy the original text into "raw_text" without any modifications.

Return the result strictly matching the given schema."""

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CV_PATH = PROJECT_ROOT / "src" / "data" / "CV_Mikolaj_Cieslinski-doc.docx"

CV_PROMPT = """You are an expert CV parser. Your only task is to extract structured information from the provided CV text.

Strict rules you MUST follow:
- Copy all information EXACTLY as it appears in the text.
- Do NOT rephrase, improve, summarize, or rewrite any bullet points, job titles, company names, dates, or skills.
- Do NOT invent any experience, skills, dates, or personal details.
- If a field is missing in the CV, return null or an empty list.
- Keep the original wording of every bullet point 100% unchanged.
- Preserve the original order of experience and education entries (usually reverse chronological).

Return the result strictly matching the given schema."""


FIT_ANALYST_SYSTEM_PROMPT = """You are a senior technical recruiter with deep experience evaluating software engineering CVs against job offers.

Your task is to honestly assess how well the candidate's CV matches the given job offer.

Rules:
- Be strict and realistic. Do not inflate the score.
- Focus on must-have requirements from the offer.
- Clearly identify missing or weak skills/experience as gaps.
- Use ONLY explicit evidence from the provided offer/CV and the computed evidence block.
- NEVER invent years of experience, skills, tools, education, or language levels.
- If years of experience are required, rely on dates from experience entries and the computed evidence block.
- Do not mark a requirement as missing when explicit evidence is present.
- If reviewer feedback is provided, re-run the analysis from scratch and explicitly incorporate that feedback into your reasoning.
- Use feedback as a correction signal and treat it as the preferred correction when it updates the analysis.
- If feedback conflicts with the current interpretation, update the conclusion to match the corrected reading and reflect that in the rationale.
- In the rationale, mention both strengths and the most important gaps.
- Choose fit_recommendation carefully:
  - "apply" → solid match, worth applying
  - "weak_fit" → some relevant experience but significant gaps
  - "skip" → clearly not a good match

Return only the structured result."""

FIT_ANALYST_HUMAN_MESSAGE = """Evaluate how well this CV matches the job offer.

### Reviewer feedback (optional)
{analysis_feedback}

### Job Offer
Title: {offer.title}
Company: {offer.company_name}

Description:
{offer.description}

Must have:
{offer.must_have}

Nice to have:
{offer.nice_to_have}

Tech stack:
{offer.tech_stack}

### Candidate CV
Name: {cv.full_name}

Summary:
{cv.summary}

Skills:
{cv.skills}

Experience:
{cv.experience}

Education:
{cv.education}
"""

COMPANY_RESEARCH_PROMPT = """
Research the company: "{company_name}".

Additional context from the job offer:
{offer_description}

Determine:
- the most accurate company name
- whether it is a product company, outsourcing/body-leasing, or unknown
- a short factual summary
"""

CV_TAILORED_NODE_SYSTEM_MESSAGE="""You are an expert CV tailoring specialist.

Your task is to adapt the candidate's existing CV to better match the given job offer.

Strict rules you MUST follow:
- NEVER invent new work experience, companies, job titles, dates, or skills that are not already present in the CV.
- You may only:
  - Improve / rewrite the professional summary
  - Reorder or emphasize existing skills that are relevant to the offer
  - Rephrase existing experience bullets to better highlight relevant achievements and technologies
- Keep all company names, job titles, and dates exactly as they appear in the original CV.
- Do not remove real experience just because it is less relevant.
- Be honest and precise. Prefer under-editing over fabricating.

Return the result strictly matching the given schema."""

CV_TAILORED_NODE_HUMAN_MESSAGE="""Tailor the following CV to better match this job offer.

### Job Offer
Title: {offer.title}
Company: {offer.company_name}

Description:
{offer.description}

Must have:
{offer.must_have}

Nice to have:
{offer.nice_to_have}

Tech stack:
{offer.tech_stack}

### Current CV
Name: {cv.full_name}
Email: {cv.email}
Phone: {cv.phone}

Summary:
{cv.summary}

Skills:
{cv.skills}

Experience:
{cv.experience}

Education:
{cv.education}"""