
from flask import (
    Flask,
    request,
    redirect,
    session,
    render_template_string,
    abort
)
from functools import wraps
import os

from theme import page


app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-ctf-development-only"
)

FLAG = os.environ.get(
    "S05_FLAG",
    "SPECTRAL{broken_object_authorization}"
)


# ==========================================
# USERS
# ==========================================

USERS = {
    "analyst": {
        "password": "Analyst2026!",
        "name": "Junior Security Analyst"
    }
}


# ==========================================
# INCIDENT REPORTS
# ==========================================

REPORTS = {
    101: {
        "owner": "analyst",
        "title": "Suspicious Login Activity",
        "content": (
            "Multiple failed authentication attempts "
            "were detected."
        )
    },

    102: {
        "owner": "analyst",
        "title": "Unusual Network Traffic",
        "content": (
            "An unexpected outbound connection "
            "was observed."
        )
    },

    103: {
        "owner": "administrator",
        "title": "Restricted Incident Investigation",
        "content": (
            "CONFIDENTIAL - Ghost Packet investigation.\n"
            f"Evidence flag: {FLAG}"
        )
    }
}


# ==========================================
# AUTHENTICATION DECORATOR
# ==========================================

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "username" not in session:
            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    if "username" in session:
        return redirect("/dashboard")

    return redirect("/login")


# ==========================================
# LOGIN PAGE
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = USERS.get(username)

        if user and user["password"] == password:

            session.clear()
            session["username"] = username

            return redirect("/dashboard")

        error = "Invalid credentials"

    return render_template_string(
        page("Analyst Login", """
        <h1>SECURE INCIDENT PORTAL</h1>

        <p class="subtitle">
            [+] Authentication required
        </p>

        <p>
            Welcome, Analyst. Authenticate to access
            your assigned incident reports.
        </p>

        {% if error %}
            <p class="error">[!] {{ error }}</p>
        {% endif %}

        <form method="post">

            <p>
                <input
                    name="username"
                    placeholder="Username"
                    autocomplete="username"
                    required
                >
            </p>

            <p>
                <input
                    name="password"
                    type="password"
                    placeholder="Password"
                    autocomplete="current-password"
                    required
                >
            </p>

            <button type="submit">
                [ ACCESS SYSTEM ]
            </button>

        </form>

        <hr>

        <p class="subtitle">
            [ STAGE 05 // INTERNAL INVESTIGATION SYSTEM ]
        </p>
        """),
        error=error
    )


# ==========================================
# INCIDENT DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    username = session["username"]

    visible = [
        (report_id, report)
        for report_id, report in REPORTS.items()
        if report["owner"] == username
    ]

    return render_template_string(
        page("Incident Dashboard", """
        <h1>INCIDENT DASHBOARD</h1>

        <p class="subtitle">
            [+] Authentication successful
        </p>

        <p>
            ACTIVE SESSION: {{ username }}
        </p>

        <hr>

        <h2>[ ASSIGNED INCIDENT REPORTS ]</h2>

        <p>
            Review the security incidents assigned
            to your account.
        </p>

        <ul>
        {% for report_id, report in reports %}

            <li>
                <a href="/reports/{{ report_id }}">
                    [REPORT #{{ report_id }}]
                    {{ report.title }}
                </a>
            </li>

        {% endfor %}
        </ul>

        <hr>

        <p class="subtitle">
            [+] Incident management system online
        </p>

        <a href="/logout">[ LOGOUT ]</a>
        """),
        username=username,
        reports=visible
    )


# ==========================================
# INCIDENT REPORT VIEW
# ==========================================

@app.route("/reports/<int:report_id>")
@login_required
def view_report(report_id):

    report = REPORTS.get(report_id)

    if report is None:
        abort(404)

    # ======================================
    # INTENTIONAL CTF VULNERABILITY
    #
    # Missing ownership authorization check.
    #
    # An authenticated user can access
    # another user's report by changing
    # the report ID in the URL.
    # ======================================

    return render_template_string(
        page("Incident Report", """
        <h1>INCIDENT INVESTIGATION REPORT</h1>

        <p class="subtitle">
            [+] Report retrieved successfully
        </p>

        <hr>

        <h2>{{ report.title }}</h2>

        <p>[ EVIDENCE DETAILS ]</p>

        <pre>{{ report.content }}</pre>

        <hr>

        <p class="subtitle">
            [+] End of incident report
        </p>

        <a href="/dashboard">
            [ BACK TO DASHBOARD ]
        </a>
        """),
        report=report
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==========================================
# APPLICATION STARTUP
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
