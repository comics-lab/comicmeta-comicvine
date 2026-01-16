# comicmeta-comicvine

## Agent and Logs

- Agent profile: `AGENTS.md`
- Logs (local-only): `CONVERSATION.md`, `BOOKMARKS.md`, `Action-Log.md` (when present)


Connector for ComicVine: search & normalize to shared models.

## Setup

1. Get API Key
   - Visit https://comicvine.gamespot.com/api/
   - Sign up/login and get your API key
   - Set up the key (choose one):
     ```bash
     # Option 1: Environment variable
     export COMICVINE_API_KEY='your-key-here'
     
     # Option 2: Config file
     mkdir -p ~/.config/comicvine
     echo 'your-key-here' > ~/.config/comicvine/api_key
     
     # Option 3: .env file in project
     echo 'COMICVINE_API_KEY=your-key-here' > .env
     ```

2. Create virtualenv
    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    ```

## Action Log
- 2025-10-19 — Initialized repository skeleton (MIT, Python 3 only).

## Appendix: Directory Structure — comicmeta-comicvine

<!-- BEGIN DIR TREE -->
```
comicmeta-comicvine
├── comicmeta_comicvine
│   ├── __init__.py
│   └── cli.py
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```
<!-- END DIR TREE -->
