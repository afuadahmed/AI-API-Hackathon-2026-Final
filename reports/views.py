from django.shortcuts import render, redirect

from .forms import CivicReportForm
from .services.ai_service import analyze_report


def home(request):

    ai_result = None

    if request.method == "POST":

        form = CivicReportForm(request.POST, request.FILES)

        if form.is_valid():

            report = form.save(commit=False)

            ai_result = analyze_report(
                report.title,
                report.description,
                report.category,
            )

            report.ai_priority = ai_result["priority"]

            report.save()

            return render(
                request,
                "home.html",
                {
                    "form": CivicReportForm(),
                    "result": ai_result,
                },
            )

    else:

        form = CivicReportForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "result": ai_result,
        },
    )