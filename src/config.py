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

CRITICAL: Check the "Rewrite style" field in the input. If it says "strong_rewrite", you MUST completely rewrite EVERY bullet point from scratch. Do NOT keep the original wording.

Strict rules you MUST follow:
- NEVER invent new work experience, companies, job titles, or dates.
- Keep all company names, job titles, and dates exactly as they appear in the original CV.
- Do not remove real experience just because it is less relevant.
- Be honest and precise. Prefer under-editing over fabricating.
- If reviewer feedback is provided, re-tailor the CV from scratch and explicitly apply that feedback as the primary correction signal.
- Use the company research profile to tailor emphasis in the summary, skills ordering, and experience bullet phrasing so it matches the company's context.
- NEVER DUPLICATE bullets within the same experience entry or across entries. Each bullet must be unique.
- Each experience entry should have its OWN unique bullets based on that specific role.

REWRITE STYLE GUIDE (follow strictly based on the selected style):

### conservative
- Make MINIMAL changes - only reorder skills to put relevant ones first
- Keep summary almost unchanged (only minor keyword additions if absolutely necessary)
- Do NOT rephrase experience bullets - keep them exactly as they are
- Only add confirmed_additions as new bullets, nothing else

### polished
- Rewrite summary to better highlight relevant experience
- Reorder skills and add confirmed skills
- Lightly rephrase experience bullets to include relevant keywords from the job offer
- Add confirmed_additions as new bullets
- Fix obvious grammar/spelling errors

### strong_rewrite
THIS IS A COMPLETE REWRITE. You MUST:
1. COMPLETELY rewrite the professional summary from scratch - make it compelling, professional, and perfectly targeted to this job offer
2. Reorder and optimize skills section
3. REWRITE EVERY SINGLE BULLET POINT from scratch. The new text MUST be significantly different from the original:
   - Start with strong action verbs (Developed, Implemented, Led, Architected, Optimized, etc.)
   - Add quantifiable achievements where possible (percentages, numbers, timeframes)
   - Include relevant technologies/keywords from the job offer
   - Make each bullet concise, impactful, and professional
   - DO NOT just copy the original bullet with minor word changes
4. Add confirmed_additions as polished, professional bullets
5. The result should read like a CV written by a professional CV writer

EXAMPLE of strong_rewrite transformation:
- BEFORE: "Working on multiple clients' projects from various sectors, including banking, HR, and consulting."
- AFTER: "Delivered high-impact Angular applications for enterprise clients across banking, HR, and consulting sectors, consistently meeting tight deadlines and exceeding quality standards."

Interview clarifications rules:
- For strong_rewrite: ALWAYS rewrite ALL bullets regardless of rewrite_permission.
- Use confirmed skill_years to mention specific years of experience in summary or relevant bullets.
- Use confirmed_additions to ADD NEW BULLETS to the specific experience entry indicated by "where" field.
- NEVER add anything from rejected_gaps - the candidate explicitly said they do not have this experience.
- If languages are confirmed (e.g., "Polish - native, English - fluent"), include them in the languages field.

IMPORTANT: 
- Do NOT put everything in the summary. Distribute confirmed_additions as new bullets in the appropriate experience entries.
- Each experience entry must have UNIQUE bullets. Do not copy bullets from one entry to another.
- For strong_rewrite: If a bullet in your output looks similar to the original, REWRITE IT AGAIN.

Return the result strictly matching the given schema."""

CV_TAILORED_NODE_HUMAN_MESSAGE="""Tailor the following CV to better match this job offer.

REWRITE STYLE: {clarifications_style}
(If this is "strong_rewrite", you MUST completely rewrite every bullet point. Do NOT keep original wording.)

### Reviewer feedback (optional)
{tailored_cv_feedback}

### Interview clarifications (from candidate)
Rewrite style: {clarifications_style}
Rewrite permission: {clarifications_rewrite_permission}
Confirmed skill years: {clarifications_skill_years}
Confirmed additions (gaps to add): {clarifications_confirmed_additions}
Rejected gaps (do NOT add): {clarifications_rejected_gaps}
Confirmed languages: {clarifications_languages}

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

### Company profile (from research)
Company name: {company_name}
Company type: {company_type}
Company summary:
{company_summary}

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
{cv.education}

Languages:
{cv.languages}"""

DEFAULT_JOB_OFFER_URL = "https://justjoin.it/job-offer/comarch-angular-developer-warszawa-javascript-d725926d"
DEMO_JOB_OFFER_URL = "https://nofluffjobs.com/job/senior-java-cloud-developer-azure-dahliamatic-warszawa-1"

FETCH_JOB_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

FETCH_JOB_NOISE_KEYWORDS: frozenset[str] = frozenset(
    {
        "cookie",
        "banner",
        "menu",
        "sidebar",
        "related",
        "newsletter",
        "advert",
        "ads",
        "ad-",
        "promo",
        "popup",
        "modal",
        "consent",
        "gdpr",
        "footer",
        "header",
        "nav-",
        "navigation",
        "social",
        "share",
        "subscribe",
        "login",
        "signup",
        "register",
        "breadcrumb",
        "pagination",
        "widget",
        "tracking",
    }
)

FETCH_JOB_REMOVE_TAGS: tuple[str, ...] = (
    "script",
    "style",
    "noscript",
    "iframe",
    "svg",
    "nav",
    "footer",
    "header",
    "aside",
    "form",
)

FETCH_JOB_NOISE_PHRASES: tuple[str, ...] = (
    "accept cookies",
    "cookie policy",
    "all rights reserved",
    "© ",
    "privacy policy",
    "terms of service",
    "terms of use",
)

FETCH_JOB_MIN_CONTENT_LENGTH = 300

APPLY_CV_EDITS_SYSTEM_PROMPT = """
You are an expert at editing existing CVs while preserving their structure.

You will receive:
1. A numbered list of paragraphs extracted from a DOCX file
2. The desired tailored content (TailoredCV)

Your job is to decide which paragraphs should be updated and what their new text should be.

Strict rules:
- Change content related to: professional summary, skills, experience bullets, education, and languages.
- NEVER change company names, job titles, or dates.
- NEVER add new work experience entries.
- NEVER invent skills or achievements that are not present in the TailoredCV.
- Keep bullet point markers (-, •, *) if they exist.
- Return the minimal set of changes necessary.
- If a section header exists but is empty (e.g., "LANGUAGES & EDUCATION" with no content below), you SHOULD fill it with the provided education/languages data.
- Look for empty paragraphs or placeholder paragraphs near section headers and replace them with the appropriate content.

Return only the structured list of changes.
"""

APPLY_CV_EDITS_HUMAN_TEMPLATE = """
Here is the list of paragraphs from the original CV (index: text):

{paragraphs_text}

Here is the tailored content we want to apply:

Summary:
{summary}

Skills:
{skills}

Experience:
{experience}

Education:
{education}

Languages:
{languages}

Return the list of paragraph changes needed.
"""

CV_INTERVIEW_NODE_PROMPT = """
You are a CV intake interviewer.

Ask ONE question at a time.

Cover:
1. Whether the candidate still wants to apply, given the fit score and company type
2. Rewrite style - ask which one they prefer:
   - "conservative" = minimal changes, only reorder skills
   - "polished" = light rephrasing, fix grammar
   - "strong_rewrite" = completely rewrite all bullets professionally
3. Permission to rewrite existing bullets
4. Years of experience for the most important offer skills
5. Each important fit gap: do they have it, where, how to phrase it
6. Language proficiencies (if required by the job offer)

Rules:
- Never invent experience.
- If they do not want to apply, say so in assistant_message and do not fill clarifications.
- If they reject a gap, put it in rejected_gaps.
- confirmed_additions only when they explicitly confirm the experience.
- Set is_complete=true only when the checklist is done and they want to proceed.
- IMPORTANT: When setting clarifications.style, use EXACTLY one of: "conservative", "polished", "strong_rewrite" (with underscore, no spaces).
- If user says "strong rewrite" or "complete rewrite" or similar, set style to "strong_rewrite".
"""

CV_INTERVIEW_CONTEXT = """
Offer: {offer}
CV: {cv}
Fit score: {fit_score}
Fit gaps: {fit_gaps}
Fit rationale: {fit_rationale}
Company: {company_name} ({company_type})
{company_summary}
"""