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