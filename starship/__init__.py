if __name__ == "__main__":
    from app import app
    from dotenv import load_dotenv

    import os
    import pyruvate

    import admin, api

    load_dotenv()

    SERVER_FALLBACK_PORT = 80
    SERVER_PORT = os.getenv("SERVER_PORT", SERVER_FALLBACK_PORT)
    WORKERS = 2

    pyruvate.serve(app, f"0.0.0.0:{SERVER_PORT}", WORKERS)
