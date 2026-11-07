import csv
import threading
from src.core.run_context import get_run_id, get_report_dir, get_log_dir
from datetime import datetime
import html
# _name private variable
# __name strict private variable oops(class and objects)
# _function private function ( local to this specific python module file)

_lock = threading.Lock()


HEADERS = [
    "run_id",
    "timestamp",
    "validation",
    "status",
    "duration_seconds",
    "details"
]

REPORT_DIR = get_report_dir()

CSV_REPORT = REPORT_DIR / "validation_report.csv"
HTML_REPORT = REPORT_DIR / "validation_report.html"
SUMMARY_REPORT = REPORT_DIR / "summary.txt"

def _create_report():

    if CSV_REPORT.exists():
        return

    with CSV_REPORT.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(HEADERS)

def write_output(validation_type,
        status,
        duration_seconds,
        details):
    with _lock:
        _create_report()

        with CSV_REPORT.open(
                mode="a",
                newline="",
                encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                get_run_id(),
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                validation_type,
                status,
                duration_seconds,
                details
            ])

def _read_validation_results():

    if not CSV_REPORT.exists():
        return []

    with CSV_REPORT.open(
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(
            csv.DictReader(file)
        )

def generate_summary(test_stats):

    results = _read_validation_results()

    total_validations = len(results)

    passed_validations = sum(
        1
        for row in results
        if row["status"].upper() == "PASS"
    )

    failed_validations = sum(
        1
        for row in results
        if row["status"].upper() == "FAIL"
    )

    validation_percentage = (
        round(
            (passed_validations / total_validations) * 100,
            2
        )
        if total_validations
        else 0
    )

    execution_status = (
        "PASSED"
        if test_stats["failed"] == 0
        else "FAILED"
    )

    summary = f"""
======================================================================
ETL AUTOMATION EXECUTION SUMMARY
======================================================================

Run ID                 : {get_run_id()}

PYTEST EXECUTION
----------------------------------------------------------------------
Total Tests            : {test_stats["total"]}
Passed Tests           : {test_stats["passed"]}
Failed Tests           : {test_stats["failed"]}
Skipped Tests          : {test_stats["skipped"]}

VALIDATION EXECUTION
----------------------------------------------------------------------
Total Validations      : {total_validations}
Passed Validations     : {passed_validations}
Failed Validations     : {failed_validations}
Pass Percentage        : {validation_percentage}%

Overall Status         : {execution_status}

======================================================================
"""

    SUMMARY_REPORT.write_text(
        summary.strip(),
        encoding="utf-8"
    )


def generate_html_report(test_stats):

    results = _read_validation_results()

    total = len(results)

    passed = sum(
        1
        for row in results
        if row["status"].upper() == "PASS"
    )

    failed = sum(
        1
        for row in results
        if row["status"].upper() == "FAIL"
    )

    pass_percentage = (
        round((passed / total) * 100, 2)
        if total
        else 0
    )

    overall_status = (
        "PASSED"
        if test_stats["failed"] == 0
        else "FAILED"
    )

    rows = []

    for row in results:

        status = row["status"].upper()

        status_class = (
            "pass"
            if status == "PASS"
            else "fail"
        )

        details = html.escape(
            row.get("details", "")
        )

        rows.append(
            f"""
            <tr>
                <td>{html.escape(row["validation"])}</td>

                <td>
                    <span class="status {status_class}">
                        {status}
                    </span>
                </td>

                <td>
                    {html.escape(str(row["duration_seconds"]))}
                </td>

                <td class="details">
                    {details}
                </td>
            </tr>
            """
        )

    validation_rows = "\n".join(rows)

    report_html = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="UTF-8">

    <title>ETL Automation Labs | Data Quality Report</title>

    <style>

    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        padding: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: #f5f5f5;
        color: #1a1a1a;
    }}

    /* =========================================================
       HEADER
       ========================================================= */

    .header {{
        background: #111111;
        border-bottom: 6px solid #FFD400;
        padding: 28px 45px;
         text-align: center;
    }}

    .brand {{
        color: #FFD400;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 1px;
    }}

    .report-name {{
        color: #ffffff;
        font-size: 18px;
        font-weight: 500;
        margin-top: 7px;
    }}

    .run-info {{
        color: #cfcfcf;
        font-size: 13px;
        margin-top: 10px;
    }}


    /* =========================================================
       MAIN CONTAINER
       ========================================================= */

    .container {{
        max-width: 1450px;
        margin: auto;
        padding: 32px 40px;
    }}


    /* =========================================================
       SECTION TITLE
       ========================================================= */

    .section-title {{
        font-size: 20px;
        font-weight: 700;
        margin: 28px 0 15px 0;
        border-left: 6px solid #FFD400;
        padding-left: 12px;
    }}


    /* =========================================================
       SUMMARY CARDS
       ========================================================= */

    .cards {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }}

    .card {{
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        border-top: 4px solid #FFD400;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}

    .card-title {{
        color: #666666;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}

    .card-value {{
        margin-top: 8px;
        font-size: 30px;
        font-weight: 800;
        color: #111111;
    }}

    .card-pass {{
        border-top-color: #16a34a;
    }}

    .card-pass .card-value {{
        color: #15803d;
    }}

    .card-fail {{
        border-top-color: #dc2626;
    }}

    .card-fail .card-value {{
        color: #dc2626;
    }}


    /* =========================================================
       OVERALL STATUS
       ========================================================= */

    .overall-container {{
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 30px;
    }}

    .overall-label {{
        font-size: 13px;
        color: #666666;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}

    .overall {{
        display: inline-block;
        padding: 9px 20px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 800;
    }}

    .overall-pass {{
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #16a34a;
    }}

    .overall-fail {{
        background: #fee2e2;
        color: #b91c1c;
        border: 1px solid #dc2626;
    }}


    /* =========================================================
       TABLE
       ========================================================= */

    .table-wrapper {{
        background: #ffffff;
        border-radius: 8px;
        overflow-x: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
    }}

    thead {{
        background: #111111;
    }}

    th {{
        color: #FFD400;
        text-align: left;
        padding: 14px 16px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}

    td {{
        padding: 14px 16px;
        border-bottom: 1px solid #eeeeee;
        font-size: 13px;
        vertical-align: top;
    }}

    tbody tr:hover {{
        background: #fffbea;
    }}


    /* =========================================================
       PASS / FAIL BADGES
       ========================================================= */

    .status {{
        display: inline-block;
        min-width: 70px;
        text-align: center;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: 800;
    }}

    .status.pass {{
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
    }}

    .status.fail {{
        background: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fca5a5;
    }}


    /* =========================================================
       DETAILS
       ========================================================= */

    .details {{
        max-width: 750px;
        word-break: break-word;
        line-height: 1.5;
        color: #444444;
    }}


    /* =========================================================
       PYTEST SUMMARY
       ========================================================= */

    .pytest-table th {{
        width: 220px;
        background: #111111;
        color: #FFD400;
    }}

    .pytest-table td {{
        font-weight: 600;
    }}


    /* =========================================================
       FOOTER
       ========================================================= */

    .footer {{
        background: #111111;
        color: #aaaaaa;
        margin-top: 35px;
        padding: 20px 30px;
        border-top: 4px solid #FFD400;
        text-align: center;
        font-size: 12px;
    }}

    .footer-brand {{
        color: #FFD400;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 5px;
    }}


    /* =========================================================
       RESPONSIVE
       ========================================================= */

    @media (max-width: 900px) {{

        .cards {{
            grid-template-columns: repeat(2, 1fr);
        }}

        .container {{
            padding: 20px;
        }}

    }}

    </style>

    </head>


    <body>

    <!-- =====================================================
         HEADER
         ===================================================== -->

    <div class="header">

        <div class="brand">
            ETL AUTOMATION LABS
        </div>

        <div class="report-name">
            Data Quality Automation Execution Report
        </div>

        <div class="run-info">
            Run ID: {get_run_id()}
            &nbsp;&nbsp; | &nbsp;&nbsp;
            Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>

    </div>


    <div class="container">


    <!-- =====================================================
         EXECUTION SUMMARY
         ===================================================== -->

    <div class="section-title">
        Execution Summary
    </div>


    <div class="cards">

        <div class="card">

            <div class="card-title">
                Total Validations
            </div>

            <div class="card-value">
                {total}
            </div>

        </div>


        <div class="card card-pass">

            <div class="card-title">
                Passed
            </div>

            <div class="card-value">
                {passed}
            </div>

        </div>


        <div class="card card-fail">

            <div class="card-title">
                Failed
            </div>

            <div class="card-value">
                {failed}
            </div>

        </div>


        <div class="card">

            <div class="card-title">
                Pass Percentage
            </div>

            <div class="card-value">
                {pass_percentage}%
            </div>

        </div>


        <div class="card">

            <div class="card-title">
                Pytest Tests
            </div>

            <div class="card-value">
                {test_stats["total"]}
            </div>

        </div>

    </div>


    <!-- =====================================================
         OVERALL STATUS
         ===================================================== -->

    <div class="overall-container">

        <div class="overall-label">
            Overall Execution Status
        </div>

        <span class="
            overall
            {'overall-pass'
    if overall_status == 'PASSED'
    else 'overall-fail'}
        ">

            {overall_status}

        </span>

    </div>


    <!-- =====================================================
         VALIDATION RESULTS
         ===================================================== -->

    <div class="section-title">
        Validation Results
    </div>


    <div class="table-wrapper">

    <table>

    <thead>

    <tr>

        <th>
            Validation
        </th>

        <th>
            Status
        </th>

        <th>
            Duration (Sec)
        </th>

        <th>
            Details
        </th>

    </tr>

    </thead>


    <tbody>

    {validation_rows}

    </tbody>

    </table>

    </div>


    <!-- =====================================================
         PYTEST SUMMARY
         ===================================================== -->

    <div class="section-title">
        Pytest Execution Summary
    </div>


    <div class="table-wrapper">

    <table class="pytest-table">

    <tr>

        <th>
            Total Tests
        </th>

        <td>
            {test_stats["total"]}
        </td>

    </tr>


    <tr>

        <th>
            Passed
        </th>

        <td style="color:#15803d;">
            {test_stats["passed"]}
        </td>

    </tr>


    <tr>

        <th>
            Failed
        </th>

        <td style="color:#dc2626;">
            {test_stats["failed"]}
        </td>

    </tr>


    <tr>

        <th>
            Skipped
        </th>

        <td>
            {test_stats["skipped"]}
        </td>

    </tr>

    </table>

    </div>


    </div>


    <!-- =====================================================
         FOOTER
         ===================================================== -->

    <div class="footer">

        <div class="footer-brand">
            ETL AUTOMATION LABS
        </div>

        Advanced ETL Automation & Data Quality Framework

        <br>

        Report generated automatically by the
        ETL Automation Framework

    </div>


    </body>

    </html>
    """

    HTML_REPORT.write_text(
        report_html,
        encoding="utf-8"
    )