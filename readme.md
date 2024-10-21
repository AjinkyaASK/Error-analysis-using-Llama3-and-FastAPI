# Setup Steps

## Run followings commands in sequence:
1. python -m venv .venv
2. source .venv/bin/activate
3. which python <!-- Ensure this shows output path from this project's directory  -->
4. python -m pip install --upgrade pip
5. pip install -r requirements.txt
6. pip install "fastapi[standard]" <!-- for FastAPI CLI  -->
7. fastapi dev api/main.py <!-- This runs the API app  -->
8. streamlit run view/app.py <!-- This runs the UI app  -->