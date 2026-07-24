from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import CivicReportForm
from .models import Report
from .services.ai_service import analyze_report
from .services.duplicate_service import detect_duplicate


def home(request):

    if request.method == "POST":

        form = CivicReportForm(request.POST, request.FILES)

        if form.is_valid():

            report = form.save(commit=False)

            # AI Analysis
            ai_result = analyze_report(
                report.title,
                report.description,
                report.category,
            )

            report.priority = ai_result["priority"]
            report.severity_score = ai_result["severity_score"]
            report.confidence = ai_result["confidence"]
            report.department = ai_result["department"]
            report.summary = ai_result["summary"]
            report.reason = ai_result["reason"]

            # Duplicate Detection (before saving)
            duplicate_result = detect_duplicate(report)

            if duplicate_result["duplicate"]:
                report.is_duplicate = True
                report.duplicate_of = duplicate_result["report"]

            # Save report
            report.save()

            return render(
                request,
                "success.html",
                {
                    "report": report,
                    "duplicate_result": duplicate_result,
                },
            )

    else:

        form = CivicReportForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
        },
    )


def track_report(request):

    report = None

    if request.method == "POST":

        tracking_code = request.POST.get("tracking_code")

        try:
            report = Report.objects.get(
                tracking_code=tracking_code
            )

        except Report.DoesNotExist:

            report = None

    return render(
        request,
        "tracking.html",
        {
            "report": report,
        },
    )


def dashboard(request):

    search = request.GET.get("search", "")

    reports = Report.objects.all()

    if search:

        reports = reports.filter(
            Q(title__icontains=search)
            | Q(tracking_code__icontains=search)
            | Q(department__icontains=search)
        )

    reports = reports.order_by("-created_at")

    context = {

        "reports": reports,

        "search": search,

        "total_reports": Report.objects.count(),

        "pending_reports":
            Report.objects.filter(status="Pending").count(),

        "progress_reports":
            Report.objects.filter(status="In Progress").count(),

        "resolved_reports":
            Report.objects.filter(status="Resolved").count(),

        "duplicate_reports":
            Report.objects.filter(is_duplicate=True).count(),
    }

    return render(
        request,
        "dashboard.html",
        context,
    )


def update_status(request, report_id):

    report = get_object_or_404(
        Report,
        id=report_id,
    )

    if request.method == "POST":

        report.status = request.POST.get("status")

        report.save()

        return redirect("dashboard")

    return render(
        request,
        "update_status.html",
        {
            "report": report,
        },
    )