from difflib import SequenceMatcher

from reports.models import Report


LOCATION_WEIGHT = 0.25
CATEGORY_WEIGHT = 0.25
DESCRIPTION_WEIGHT = 0.50

DUPLICATE_THRESHOLD = 80


def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower(),
    ).ratio()


def detect_duplicate(new_report):

    reports = Report.objects.all()

    best_report = None
    best_score = 0

    for report in reports:

        location_score = similarity(
            new_report.location,
            report.location,
        )

        category_score = (
            1.0
            if new_report.category == report.category
            else 0
        )

        description_score = similarity(
            new_report.description,
            report.description,
        )

        final_score = (
            location_score * LOCATION_WEIGHT
            + category_score * CATEGORY_WEIGHT
            + description_score * DESCRIPTION_WEIGHT
        )

        final_score *= 100

        if final_score > best_score:

            best_score = final_score
            best_report = report

    if best_score >= DUPLICATE_THRESHOLD:

        return {
            "duplicate": True,
            "score": round(best_score),
            "report": best_report,
        }

    return {
        "duplicate": False,
        "score": round(best_score),
        "report": None,
    }