import json
import re

from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def analyze_report(title, description, category):

    prompt = f"""
You are an expert civic issue analyst.

Analyze the following citizen report.

Title:
{title}

Category:
{category}

Description:
{description}

Determine:

1. Priority (High, Medium, Low)
2. Severity Score (0-100)
3. Confidence Score (0-100)
4. Responsible Government Department
5. One-sentence summary
6. A short reason explaining your decision

Return ONLY valid JSON.

{{
    "priority": "High",
    "severity_score": 95,
    "confidence": 97,
    "department": "Fire Department",
    "summary": "An active structure fire has been reported inside a building requiring immediate emergency response.",
    "reason": "The report describes an active emergency with immediate risk to life and property."
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    return json.loads(text)