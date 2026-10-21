# ProfileCraft — Profile Card Generator

A small Flask app: fill in a form, Flask validates it, and a profile card is rendered from your data. No database, no API keys.

## Features
Responsive UI, live character counter, backend + HTML validation, safe auto-escaped output, default avatar and image-load fallback, optional links hidden when empty.

## Tech stack
Python 3, Flask (Jinja2), HTML5, CSS3, vanilla JavaScript.

## Folder structure
```
profilecraft/
├── app.py                  # Flask routes + validation
├── templates/index.html    # form + placeholder preview
├── templates/profile.html  # generated card
├── static/css/style.css
├── static/js/script.js     # counter, reset, image fallback
├── static/images/default-avatar.svg
├── requirements.txt
└── .gitignore
```

## Setup (Windows PowerShell)
Requires Python 3.9+ (`python --version`).
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open **http://127.0.0.1:5000/**

If PowerShell blocks activation, skip it and call the venv's Python directly:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```
(Or run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.)

## Routes
| URL | Methods | Function | What it does |
|---|---|---|---|
| `/` | GET | `home()` | Renders `index.html` |
| `/generate` | POST (GET redirects home) | `generate_profile()` | Validates form, renders `profile.html` |

## Key concepts
**GET vs POST.** GET asks for a page (typing a URL). POST sends data (submitting a form). The form uses `method="POST"` and `action="/generate"`.

**`request.form`.** A dictionary of submitted fields. Keys are the HTML `name` attributes, so `<input name="name">` is read with `request.form.get("name", "")`. `.get()` with a default avoids crashes when a field is missing.

**`render_template()`.** Loads a file from `templates/` and fills it with values you pass: `render_template("profile.html", profile=profile)`. In the template, `{{ profile.name }}` prints the value, HTML-escaped automatically.

**`redirect()` and `url_for()`.** `url_for("home")` builds the URL for a function (`/`); `redirect()` tells the browser to make a *new* request there. A redirect does **not** carry the form data. This app uses it when someone opens `/generate` with GET. The reference `login` → `user` code uses the Post/Redirect/Get pattern; you could do that here, but you would need to store the data (session or database) or put it in the URL.

**Data flow.**
1. Browser opens `/` → `index.html`.
2. User submits → POST to `/generate`.
3. Flask reads `request.form`, trims, validates.
4. Errors → form re-shown with messages and previous values (HTTP 400).
5. Success → `profile` dictionary passed to `profile.html` → card displayed.

## Troubleshooting
- *`flask` not found*: venv not activated or `pip install` skipped.
- *Port 5000 busy*: change to `app.run(debug=True, port=5001)`.
- *Image not showing*: URL must be a direct http(s) image link; otherwise the default avatar appears.
- *405 Method Not Allowed*: the form must use `method="POST"`.
- Turn `debug=True` **off** for production; use a real WSGI server.

## Manual test checklist
Valid submission; empty/whitespace name or bio; missing optional fields; bad image/GitHub/LinkedIn URLs (e.g. `abc`, `ftp://x.com`); name >60, title >80, bio >250 chars; broken image URL; open `/` directly.
