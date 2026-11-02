# SuperChat Phase 1 — implementation report

## Scope and architecture

SuperChat combines flight search, shopping and cinema in one English chat.
FastAPI serves a self-contained HTML/CSS/JavaScript interface and validated REST
endpoints. Pydantic validates the five official datasets: 17 flights, 12 products,
8 movies, 3 cinemas and 16 showtimes. Repositories keep source data separate from
business services. A deterministic conversation engine routes requests; SQLite
stores session carts, reservations, domain filters, recent result IDs and history.
No external data provider, hosted model, payment or personal data is used.

Repository interfaces allow future service replacements without coupling domain
operations to HTTP provider details. Showtime records join movie and cinema IDs.
Flight duration uses duration_min rather than subtraction of local timestamps.
Money uses Decimal internally; calculated booking/cart totals are decimal strings.

## Routing and context

The engine identifies Flights, Shopping, Cinema, Mixed, Follow-up, Ambiguous and
Out of scope using English keywords, catalog titles and record IDs. Mixed requests
are split at conjunctions introducing explicit domains. Each domain receives its
own date/price constraints. When reliable splitting is impossible, the engine asks
for clarification rather than sharing constraints across domains.

Last-result order resolves ordinal references. Separate domain memory supports
returning after topic changes. Multiple matching movies require an explicit title
or showtime for booking. Relative dates use 2026-11-02. Unknown routes produce no
results. Short references without context trigger clarification. State is persisted
across restarts. No learned classifier or LLM is included; unrestricted natural
language comprehension is not claimed.

## Domain operations and state

REST services support flight search, filtering/sorting, details, comparison and
mock booking; product search/filtering, comparison, stock and cart operations;
movie filters, cinema/showtime search and count-based ticket reservations.
The conversational parser exposes a subset of these filters. Cards provide
additional cart and reservation actions. All catalog information is grounded in
source JSON. Numbered seats are not fabricated because no seat map is supplied.

SQLite BEGIN IMMEDIATE transactions enforce shared seat capacity across sessions.
Reservation request keys prevent duplicate writes through the REST endpoint.
Cart quantities are absolute, checked against stock, and do not reserve inventory.
The web interface asks for explicit confirmation of card-based bookings. Textual
booking commands commit immediately. Separate repeated chat messages remain
separate actions; chat transport deduplication is not implemented.

## Validation and limitations

40 automated checks pass in the development environment, covering repository
integrity, API validation, joins, filters, totals, session isolation, persistence,
concurrency, sold-out inventory, reservation idempotency and all eight brief
conversation scenarios. See test_results_stage_5.txt and ROUTING_RESULTS.md.
A Starlette/httpx deprecation warning is non-failing. Root HTML returns HTTP 200
and embedded JavaScript passes Node syntax validation. Browser interaction and
visual layout could not be verified here because Chromium is unavailable.

Current limits: rule-based English paraphrase coverage, incomplete chat exposure
of REST filters, multiple independent intents in the same domain, and no pending
slot-filling dialogue for every missing field. Session IDs are demo identifiers,
not production authentication. Run one worker: the conversation lock is per process.
No real APIs or production deployment are included. A final competition acceptance
pass is still required; this report does not claim every brief requirement is done.
English-only responses follow the user's explicit instruction and differ from the
brief's language-matching requirement.

## Dependencies and sources

- FastAPI: https://github.com/fastapi/fastapi — MIT.
- Pydantic: https://github.com/pydantic/pydantic — MIT.
- Uvicorn: https://github.com/Kludex/uvicorn — BSD-3-Clause.
- pytest: https://github.com/pytest-dev/pytest — MIT (development).
- HTTPX: https://github.com/encode/httpx — BSD-3-Clause (development).
- Python standard library sqlite3; SQLite is public domain.
- Organizer-supplied SuperChat project brief and five JSON datasets are the
  requirements and catalog sources. Dataset redistribution rights remain with
  their owners. No third-party participant implementation is used.
