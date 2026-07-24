import json
import re
from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def analyze_report(title, description, category):

    prompt = f"""
You are an expert civic issue analyst.

Analyze this civic report.

Title:
{title}

Category:
{category}

Description:
{description}

Return ONLY valid JSON.

{{
    "priority":"High",
    "department":"Department Name",
    "summary":"One sentence summary"
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