# Five-minute demonstration

Start with `python run.py`, open http://127.0.0.1:8000 and click New conversation.
All inventory and prices are from the official JSON files. Relative dates use
2 November 2026. No payment or real reservation is performed.

1. Ask `Find flights from Baku to Istanbul on Friday`.
   Inspect cards and ask `The cheaper one, is it direct?`.
2. Switch: `What is playing tonight?`.
   Inspect titles, showtimes, cinema names and seat counts.
3. Switch: `Show me laptops`.
   Ask `The second one, is it in stock?`.
4. Return: `The sci-fi one, any seats on Saturday?`.
   Explain that more than one movie matches, then choose a specific showtime.
   Click Reserve, enter quantity and confirm the mock reservation.
5. Switch again: `Headphones under 100 AZN`.
   Click Add to cart. Explain that this sets quantity to one. Refresh the page:
   history, cart and reservations are restored.
6. Ask `Flights to Istanbul on Friday under 500 AZN and backpacks under 100 AZN`.
   Point out separate results and independent budgets.
7. Ask `Show me something good`, then `What is the weather in Ganja?`.
   Explain clarification and scope boundaries.

Use a fresh conversation for each independent test. Reservations consume shared
mock seats across all sessions. Stop the server and remove var/superchat.sqlite3
only when you deliberately want to reset all demo state.

## Installation and validation (PowerShell)

Run from D:\superchat:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run.py
```

No new dependency is required for the reliability updates. Replace app/chat.py
and tests/test_chat.py with their supplied versions. Keep the Stage 4 main.py
and ui.py. Store the supplied Markdown documents in docs/.
