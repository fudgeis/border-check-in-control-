Border Check In Simulator 

Features:
- interactive UI: built with Python's `rich` library to render a live status bar, official rulebook, digital passport, and Embassy database lookup side-by-side.
  
- documents Verification: inspect passport expiration dates, `U0` Slack ID prefixes, valid Embassy stamps (`EMBASSY-2026`, `ORPHEUS-OK`, `YSWS-VERIFIED`), and GitHub commit counts.
  
- interrogation (`I`): question up to 2 suspicious hackers per shift (especially travelers with low `1–4` commit counts) to catch lies between their passport destination and their story.

- system date & shift progression: Syncs with your real system date (`datetime.now()`) and advances across multi-day shifts every 4 hackers processed.

- citation & firing system:every wrong approval or denial issues an official embassy citation—survive as many days as possible before hitting 3 strikes.

Setup and run!:

install the required library using 'pip'
```bash
   pip install -r requirements.txt
   ```
   run the game:
  ```bash
      python main.py
   ```

  The sreenshot is uploaded to the repo as a seperate file 