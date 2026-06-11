import os

# Load .env file if it exists (requires python-dotenv: pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("SESSION_SECRET", "web-designs-care-secret-key-change-in-production")

    # Database: SQLite by default (works offline on PC and Pydroid3)
    # For MySQL:     mysql+pymysql://user:password@localhost/dbname
    # For PostgreSQL: postgresql://user:password@localhost/dbname
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///web_designs_care.db")

    # Stripe (optional, leave empty to use demo checkout)
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    # Server settings
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "5000"))

    # JWT expiry
    JWT_EXPIRY_HOURS = 24 * 7  # 7 days
