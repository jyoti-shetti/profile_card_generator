from urllib.parse import urlparse

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Limits are kept in one place so the HTML form and Python checks agree.
MAX_NAME, MAX_TITLE, MAX_BIO = 60, 80, 250


def is_valid_url(value):
    """Return True only for http/https URLs that have a host name."""
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def validate(form):
    """Check the form data. Returns (errors, cleaned_values)."""
    errors = []
    # .get(key, "") never crashes if a field is missing; .strip() trims spaces.
    data = {
        "name": form.get("name", "").strip(),
        "title": form.get("title", "").strip(),
        "bio": form.get("bio", "").strip(),
        "image_url": form.get("image_url", "").strip(),
        "github": form.get("github", "").strip(),
        "linkedin": form.get("linkedin", "").strip(),
    }

    if not data["name"]:
        errors.append("Please enter your full name.")
    elif len(data["name"]) > MAX_NAME:
        errors.append(f"Name must be {MAX_NAME} characters or fewer.")

    if len(data["title"]) > MAX_TITLE:
        errors.append(f"Title must be {MAX_TITLE} characters or fewer.")

    if not data["bio"]:
        errors.append("Please write a short biography.")
    elif len(data["bio"]) > MAX_BIO:
        errors.append(f"Biography must be {MAX_BIO} characters or fewer.")

    labels = {"image_url": "Profile image", "github": "GitHub", "linkedin": "LinkedIn"}
    for key, label in labels.items():
        if data[key] and not is_valid_url(data[key]):
            errors.append(f"{label} URL must start with http:// or https://")

    return errors, data


@app.route("/")
def home():
    return render_template("index.html", errors=[], values={})


@app.route("/generate", methods=["POST", "GET"])
def generate_profile():
    # Someone typed /generate in the address bar (GET): send them home.
    if request.method != "POST":
        return redirect(url_for("home"))

    errors, profile = validate(request.form)

    if errors:
        # Show the form again with messages and the user's earlier input.
        return render_template("index.html", errors=errors, values=profile), 400

    return render_template("profile.html", profile=profile)


if __name__ == "__main__":
    app.run(debug=True)  # Turn debug OFF in production.
