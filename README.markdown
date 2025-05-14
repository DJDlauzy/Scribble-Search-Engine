# Scribble Search

A basic search engine! built with Flask, indexing Wikipedia pages.

## Setup on Glitch

1. Import the repository into Glitch:
   - Go to [glitch.com](https://glitch.com) and click "New Project" > "Import from GitHub."
   - Enter `https://github.com/DJDlauzy/Scribble-Search-Engine`.
2. Wait for Glitch to install dependencies (via `requirements.txt`).
3. Click "Show" to view the app.
4. Search for terms like "python" or "html".

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/DJDlauzy/Scribble-Search-Engine
   cd scribble-search
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python search_engine.py
   ```

## Notes
- Indexes three Wikipedia pages (Python, JavaScript, HTML).
- Uses TF-IDF for ranking.
- Features Scribble branding with a playful, handwritten aesthetic.
- Hosted on Glitch for easy access.
