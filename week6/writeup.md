# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Feiyang Zhou** \
SUNet ID: **TODO** \
Citations: **Claude Code (Opus 4.6) for code fixes and documentation**

This assignment took me about **2** hours to do.


## Brief findings overview
Semgrep identified 6 code findings and 17 supply chain findings in the week6 application:

**Code Findings (SAST):**
1. Wildcard CORS policy (`allow_origins=["*"]`) - Medium severity
2. SQL injection via f-string in `text()` query - High severity
3. `eval()` arbitrary code execution - Critical severity
4. `subprocess.run(shell=True)` command injection - High severity
5. SSRF via `urlopen()` with user-controlled URL - High severity
6. XSS via `innerHTML` in frontend JavaScript - High severity

**Supply Chain Findings (SCA):**
- 1 Reachable finding: Werkzeug CVE-2024-34069 (CSRF vulnerability)
- 16 Undetermined findings in pydantic, requests, and jinja2 dependencies

**False positives:** The intentional debug endpoints (`/debug/run`, `/debug/fetch`, `/debug/read`) are designed for educational purposes and would be removed in production. The wildcard CORS is acceptable for a demo but should be restricted in production.

## Fix #1
a. File and line(s)
> `week6/backend/app/routers/notes.py`, lines 69-82

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text` - SQL Injection

c. Brief risk description
> The original code used f-string interpolation to construct a SQL query: `WHERE title LIKE '%{q}%'`. This allows attackers to inject arbitrary SQL commands by crafting malicious search queries. For example, a query like `%' OR 1=1 --` could return all records or potentially access other tables.

d. Your change (short code diff or explanation, AI coding tool usage)
> Changed from f-string interpolation to parameterized query:
> ```python
> # Before (vulnerable):
> sql = text(f"WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'")
>
> # After (secure):
> sql = text("WHERE title LIKE :search_pattern OR content LIKE :search_pattern")
> rows = db.execute(sql, {"search_pattern": f"%{q}%"})
> ```
> Used Claude Code to identify the vulnerability and apply the fix.

e. Why this mitigates the issue
> Parameterized queries separate the SQL code from user input. The database driver properly escapes the `search_pattern` parameter, preventing any SQL characters in the input from being interpreted as SQL commands. This is the standard defense against SQL injection.

## Fix #2
a. File and line(s)
> `week6/backend/app/routers/notes.py`, lines 104-109

b. Rule/category Semgrep flagged
> `python.lang.security.audit.eval-detected` - Code Injection

c. Brief risk description
> The `eval()` function executes arbitrary Python code passed as a string. An attacker could pass malicious Python code (e.g., `__import__('os').system('rm -rf /')`) to execute any command on the server. This is a critical remote code execution vulnerability.

d. Your change (short code diff or explanation, AI coding tool usage)
> Disabled the endpoint entirely:
> ```python
> # Before (vulnerable):
> def debug_eval(expr: str) -> dict[str, str]:
>     result = str(eval(expr))
>     return {"result": result}
>
> # After (secure):
> def debug_eval(expr: str) -> dict[str, str]:
>     raise HTTPException(
>         status_code=403,
>         detail="eval() endpoint disabled for security."
>     )
> ```
> Used Claude Code to implement the fix.

e. Why this mitigates the issue
> By removing the `eval()` call entirely and returning a 403 Forbidden error, no user input can be executed as Python code. If expression evaluation is genuinely needed, alternatives include `ast.literal_eval()` for safe literal evaluation, or a sandboxed execution environment with strict resource limits.

## Fix #3
a. File and line(s)
> `week6/frontend/app.js`, lines 14-18

b. Rule/category Semgrep flagged
> `javascript.browser.security.insecure-document-method` - Cross-Site Scripting (XSS)

c. Brief risk description
> Using `innerHTML` with user-controlled data (`${n.title}` and `${n.content}`) allows attackers to inject malicious HTML/JavaScript. If note content contains `<script>alert('XSS')</script>`, the script executes in the victim's browser, potentially stealing cookies, session tokens, or performing actions on behalf of the user.

d. Your change (short code diff or explanation, AI coding tool usage)
> Changed from `innerHTML` to safe DOM manipulation with `textContent`:
> ```javascript
> // Before (vulnerable):
> li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
>
> // After (secure):
> const strong = document.createElement('strong');
> strong.textContent = n.title;
> li.appendChild(strong);
> li.append(': ', n.content);
> ```
> Used Claude Code to implement the fix.

e. Why this mitigates the issue
> `textContent` and `createTextNode()` automatically escape any HTML characters in the input. If a note contains `<script>`, it will be displayed as literal text rather than being executed as HTML. This is the standard defense against DOM-based XSS when displaying user content.
