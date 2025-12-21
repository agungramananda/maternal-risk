import subprocess
import sys
import os

def run_migrations():
    print("Running database migrations...")
    try:
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
        print("Migrations completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
        return False

def run_streamlit():
    print("Starting Streamlit app...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    if run_migrations():
        run_streamlit()
    else:
        print("Failed to run migrations. Please check your database configuration.")
        sys.exit(1)
