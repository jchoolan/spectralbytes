
from flask import Flask, request, redirect, session, render_template_string, abort
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-ctf-development-only")

FLAG = os.environ.get("S05_FLAG", "SPECTRAL{broken_object_authorization}")

USERS = {
    "analyst": {
        "password": "Analyst2026!",
        "name": "Junior Security Analyst"
    }
}

REPORTS = {
    101: {
        "owner": "analyst",
        "title": "Suspicious Login Activity",
        "content": "Multiple failed authentication attempts were detected."
    },
    102: {
        "owner": "analyst",
        "title": "Unusual Network Traffic",
        "content": "An unexpected outbound connection was observed."
    },
    103: {
        "owner": "administrator",
        "title": "Restricted Incident Investigation",
        "content": f"CONFIDENTIAL - Ghost Packet investigation.\nEvidence flag: {FLAG}"
    }
}

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return redirect("/dashboard" if "username" in session else "/login")

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

    return render_template_string("""
    <h1>SpectralBytes Internal Incident Portal</h1>
    <h2>Analyst Login</h2>
    <p style="color:red">{{ error }}</p>
    <form method="post">
        <input name="username" placeholder="Username" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    """, error=error)

@app.route("/dashboard")
@login_required
def dashboard():
    username = session["username"]
    visible = [
        (report_id, report)
        for report_id, report in REPORTS.items()
        if report["owner"] == username
    ]

    return render_template_string("""
    <h1>Incident Dashboard</h1>
    <p>Logged in as {{ username }}</p>
    <h2>My Reports</h2>
    <ul>
    {% for report_id, report in reports %}
        <li>
            <a href="/reports/{{ report_id }}">
                {{ report.title }}
            </a>
        </li>
    {% endfor %}
    </ul>
    <a href="/logout">Logout</a>
    """, username=username, reports=visible)

@app.route("/reports/<int:report_id>")
@login_required
def view_report(report_id):
    report = REPORTS.get(report_id)
    if report is None:
        abort(404)

    # INTENTIONAL CTF VULNERABILITY:
    # Missing ownership authorization check.
    return render_template_string("""
    <h1>{{ report.title }}</h1>
    <pre>{{ report.content }}</pre>
    <a href="/dashboard">Back to Dashboard</a>
    """, report=report)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
