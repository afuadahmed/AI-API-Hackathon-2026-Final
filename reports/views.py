from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import CivicReportForm
from .models import Report, ProgressLog
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

            # Duplicate Detection
            duplicate_result = detect_duplicate(report)

            if duplicate_result["duplicate"]:
                report.is_duplicate = True
                report.duplicate_of = duplicate_result["report"]

            # Save Report
            report.save()

            # Progress History
            ProgressLog.objects.create(
                report=report,
                message="Report submitted by citizen.",
            )

            ProgressLog.objects.create(
                report=report,
                message=f"AI analysis completed. Priority: {report.priority}.",
            )

            ProgressLog.objects.create(
                report=report,
                message=f"Assigned to {report.department}.",
            )

            if report.is_duplicate:

                ProgressLog.objects.create(
                    report=report,
                    message=f"Potential duplicate linked to {report.duplicate_of.tracking_code}.",
                )

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
    logs = []

    if request.method == "POST":

        tracking_code = request.POST.get("tracking_code")

        try:

            report = Report.objects.get(
                tracking_code=tracking_code
            )

            logs = report.progress_logs.all()

        except Report.DoesNotExist:

            report = None

    return render(
        request,
        "tracking.html",
        {
            "report": report,
            "logs": logs,
        },
    )


def dashboard(request):

    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    category = request.GET.get("category", "")
    priority = request.GET.get("priority", "")

    reports = Report.objects.all()

    if search:
        reports = reports.filter(
            Q(title__icontains=search)
            | Q(tracking_code__icontains=search)
            | Q(department__icontains=search)
        )

    if status:
        reports = reports.filter(status=status)

    if category:
        reports = reports.filter(category=category)

    if priority:
        reports = reports.filter(priority=priority)

    reports = reports.order_by("-created_at")

    context = {

        "reports": reports,

        "search": search,
        "status": status,
        "category": category,
        "priority": priority,

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

        new_status = request.POST.get("status")

        if report.status != new_status:

            # Find the master/original report
            master_report = report

            if report.duplicate_of:
                master_report = report.duplicate_of

            # Update the master report
            master_report.status = new_status
            master_report.save()

            ProgressLog.objects.create(
                report=master_report,
                message=f"Status updated to {new_status}.",
            )

            # Update every duplicate linked to the master
            duplicates = master_report.duplicate_reports.all()

            for duplicate in duplicates:

                duplicate.status = new_status
                duplicate.save()

                ProgressLog.objects.create(
                    report=duplicate,
                    message=f"Status synchronized with master incident ({master_report.tracking_code}) to {new_status}.",
                )

        return redirect("dashboard")

    return render(
        request,
        "update_status.html",
        {
            "report": report,
        },
    )