# SuperChat — Phase 1

One English chat for flights, shopping and cinema, backed by the five official
mock JSON datasets. Python 3.11+ is required. No API key is needed.

## Install and run

Run from the project directory in Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run.py
```

If the environment is already installed, use only the final two commands.
Open http://127.0.0.1:8000 for chat, /health for readiness and /docs for REST API.
Stop with Ctrl+C. Dependencies need internet at installation; the running
application uses local datasets and SQLite, with no external service calls.
On macOS/Linux use python3, .venv/bin/python and the same arguments.

## Features

- Flights: route/date, airline, price, stops and departure-time filters; sorting,
  details, comparison, quantity-based mock reservation and current availability.
- Shopping: keyword/category/brand/color/price filters, rating/price/name sorting,
  stock, comparisons, session cart and totals.
- Cinema: title/genre/language/rating/date filters, cinema listing, venue/time/price
  showtime search, availability and mock ticket reservations.
- Conversation: seven routing categories, cross-domain switches, independent
  mixed-request constraints, ordinal references, per-domain state and persistent
  history. Missing flight destination/date is collected through follow-up turns.
- UI: unified chat, cards, booking confirmation, cart removal, reservations,
  local session restoration and a responsive layout.

See docs/CHAT_COMMANDS.md for supported English phrasing, docs/DEMO.md for the
five-minute walkthrough, and docs/TECHNICAL_REPORT.md for architecture and limits.
Older STAGE documents describe historical versions, not current delivery status.

## Project layout

| Path | Responsibility |
|---|---|
| app/main.py | FastAPI startup, routes, error handling and health |
| app/ui.py | Self-contained web page, no frontend build step |
| app/chat.py | Offline intent routing, context and conversation persistence |
| app/api.py | Validated domain and session REST endpoints |
| app/config.py | Data/database paths and fixed reference date |
| app/models.py | Validated official dataset models |
| app/repositories/ | Read-only dataset loading and repository contracts |
| app/services/ | Catalog operations, SQLite carts and atomic bookings |
| data/ | Unmodified official JSON files |
| tests/ | Foundation, API, domain and multi-turn tests |
| docs/ | Reports, command reference and demonstration |
| var/ | Local runtime database, not source data |

## Data and state

Reference date: 2026-11-02. Currency: AZN. Airport timestamps are local;
flight duration_min is authoritative. Showtimes link movie_id and cinema_id.
No seat numbers, real payment or real booking are generated.

Runtime state lives in var/superchat.sqlite3. To reset the entire demo, stop the
server and deliberately remove that file. This removes every saved session,
cart, conversation and mock reservation. New conversation creates an independent
session but does not reset globally consumed seats.

Reservation transactions prevent overselling; REST request_key retries are
idempotent. Chat commands are separate actions and do not support automatic
transport retry deduplication. Cart PUT/add sets an absolute quantity. Carts
check stock but do not reserve it. Stored source seat counts are immutable;
availability endpoints and chat search expose adjusted inventory.

## Verification and remaining limits

49 automated tests pass in the development environment. One non-failing
Starlette/httpx deprecation warning remains. Tests include all eight official
conversation scenarios; these are not a held-out routing accuracy benchmark.

The router is deterministic English pattern matching, with a documented command
vocabulary. Unrestricted paraphrase coverage, multiple independent requests in
one domain, and every possible missing-field dialogue are not claimed. Phase 2
provider integrations and optional voice/image features are excluded. English
responses follow the user's instruction and differ from the brief's language
matching preference. Session IDs are demo identifiers, not authentication.
Use one Uvicorn worker; conversation turn locking is process-local.

## Dependency sources

- FastAPI: https://github.com/fastapi/fastapi (MIT)
- Pydantic: https://github.com/pydantic/pydantic (MIT)
- Uvicorn: https://github.com/Kludex/uvicorn (BSD-3-Clause)
- pytest: https://github.com/pytest-dev/pytest (MIT, development)
- HTTPX: https://github.com/encode/httpx (BSD-3-Clause, development)

Official organizer files supply requirements and catalog records. SQLite is used
through Python's standard library. No model or external provider is invoked.
