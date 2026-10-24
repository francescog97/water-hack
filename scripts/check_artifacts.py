"""Check only application build assets; never read or print confidential inputs."""
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
dist=ROOT/"app/frontend/dist"
assert (dist/"index.html").is_file(), "Frontend build required first"
# React DOM contains the harmless property `password:!0`; that is not a credential.
# Check confidential source markers and value-bearing credential patterns instead.
forbidden=[b"gofile.me",b"EIT Water Hackathon Sofia 2026 v7.pdf",b"hackathonhost.com/teambuilding",b"BEGIN PRIVATE KEY",b"BEGIN RSA PRIVATE KEY"]
errors=[]
for path in dist.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix not in {".html",".js",".css",".svg",".png",".woff2"}:
        errors.append(f"Unexpected build artifact type: {path.name}")
    content=path.read_bytes()
    if any(token.lower() in content.lower() for token in forbidden):
        errors.append(f"Forbidden sensitive-input marker in {path.name}; value withheld")
    if re.search(rb"(?:sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{30,})",content):
        errors.append(f"Potential secret token in {path.name}; value withheld")
    if re.search(rb'''(?i)(?:password|api_key|access_token)\s*[:=]\s*["'][^"'\s]{12,}["']''',content):
        errors.append(f"Potential embedded credential value in {path.name}; value withheld")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("PASS: built artifacts contain only application assets; no confidential-input markers or credential patterns found. This is a bounded scan, not a guarantee against all possible secrets.")
