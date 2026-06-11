from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from config import Config

engine = create_engine(
    Config.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in Config.DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Users ────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    open_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    login_method = Column(String(50))
    role = Column(String(50), default="user", nullable=False)
    wallet_balance = Column(Numeric(10, 2), default=0.00)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_signed_in = Column(DateTime, server_default=func.now())


# ─── Wallet Transactions ──────────────────────────────────────────────────────

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)   # topup | payment | refund | admin_add | admin_subtract
    amount = Column(Numeric(10, 2), nullable=False)
    balance_after = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255))
    reference_id = Column(String(255))          # order_id, payment_intent, etc.
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User", backref="wallet_transactions")


# ─── Products ─────────────────────────────────────────────────────────────────

class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    original_price = Column(Numeric(10, 2))
    discount = Column(Integer, default=0)
    thumbnail_url = Column(Text)
    preview_url = Column(Text)
    demo_url = Column(Text)
    file_key = Column(String(255))
    file_name = Column(String(255))
    file_size = Column(Integer)
    status = Column(String(50), default="draft", nullable=False)
    rating = Column(Numeric(3, 2), default=0.00)
    rating_count = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    tags = Column(JSON)
    features = Column(JSON)
    meta_title = Column(String(255))
    meta_description = Column(Text)
    keywords = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Orders ───────────────────────────────────────────────────────────────────

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    coupon_code = Column(String(100))
    discount_amount = Column(Numeric(10, 2), default=0)
    payment_method = Column(String(50), default="demo")
    stripe_payment_intent_id = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    items = relationship("OrderItem", backref="order")
    user = relationship("User", backref="orders")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    product = relationship("Product")


# ─── Cart / Wishlist ──────────────────────────────────────────────────────────

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    product = relationship("Product")


class WishlistItem(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    product = relationship("Product")


# ─── Licenses ─────────────────────────────────────────────────────────────────

class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    license_key = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), default="active", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)
    product = relationship("Product")
    order = relationship("Order")


# ─── Reviews ──────────────────────────────────────────────────────────────────

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    is_approved = Column(Boolean, default=True, nullable=False)
    admin_reply = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    product = relationship("Product")
    user = relationship("User")


# ─── Tickets ──────────────────────────────────────────────────────────────────

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="open", nullable=False)
    priority = Column(String(50), default="medium", nullable=False)
    admin_reply = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("User")


# ─── Coupons ──────────────────────────────────────────────────────────────────

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    type = Column(String(50), default="percentage", nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    min_order_amount = Column(Numeric(10, 2), default=0)
    max_uses = Column(Integer)
    used_count = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Affiliates ───────────────────────────────────────────────────────────────

class AffiliateCode(Base):
    __tablename__ = "affiliate_codes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    commission_rate = Column(Numeric(5, 2), default=10)
    total_clicks = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    total_earnings = Column(Numeric(10, 2), default=0)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User")


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    affiliate_code_id = Column(Integer, ForeignKey("affiliate_codes.id"), nullable=False)
    ip_address = Column(String(100))
    converted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


# ─── Settings ─────────────────────────────────────────────────────────────────

class SiteSetting(Base):
    __tablename__ = "site_settings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Webhooks ─────────────────────────────────────────────────────────────────

class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    secret = Column(String(255))
    events = Column(JSON, default=list)
    is_active = Column(Boolean, default=True, nullable=False)
    last_fired_at = Column(DateTime)
    last_status = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Domains ──────────────────────────────────────────────────────────────────

class Domain(Base):
    __tablename__ = "domains"
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(255), unique=True, nullable=False)
    hosting = Column(String(100), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), default="active", nullable=False)
    ssl_enabled = Column(Boolean, default=True, nullable=False)
    dns_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Apps ─────────────────────────────────────────────────────────────────────

class InstalledApp(Base):
    __tablename__ = "installed_apps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    is_installed = Column(Boolean, default=False, nullable=False)
    config = Column(JSON)
    installed_at = Column(DateTime)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Marketing ────────────────────────────────────────────────────────────────

class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    subject = Column(String(255))
    content = Column(Text)
    status = Column(String(50), default="draft", nullable=False)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    recipients = Column(Integer, default=0)
    opens = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ─── Notifications ────────────────────────────────────────────────────────────

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="info")
    icon = Column(String(50), default="bell")
    link = Column(String(500))
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


# ─── Newsletter ───────────────────────────────────────────────────────────────

class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    subscribed_at = Column(DateTime, server_default=func.now())
    unsubscribed_at = Column(DateTime)


# ─── Contact Messages ─────────────────────────────────────────────────────────

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    admin_reply = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


# ─── Activity Log ─────────────────────────────────────────────────────────────


# ─── Chatbot Leads ────────────────────────────────────────────────────────────

class ChatbotLead(Base):
    __tablename__ = "chatbot_leads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), nullable=False)
    phone = Column(String(100))
    source = Column(String(100), default="chatbot")
    message = Column(Text)
    converted = Column(Boolean, default=False)
    ip_hash = Column(String(64))
    created_at = Column(DateTime, server_default=func.now())


# ─── Page Views (visitor tracking) ───────────────────────────────────────────

class PageView(Base):
    __tablename__ = "page_views"
    id = Column(Integer, primary_key=True, autoincrement=True)
    page = Column(String(500), default="/")
    referrer = Column(String(500))
    ip_hash = Column(String(64))
    created_at = Column(DateTime, server_default=func.now())


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)
    entity = Column(String(100))
    entity_id = Column(Integer)
    detail = Column(Text)
    ip_address = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())


def init_db():
    Base.metadata.create_all(bind=engine)
    _run_migrations()


def _run_migrations():
    """Add new columns to existing tables without dropping data."""
    from sqlalchemy import text
    migrations = [
        ("users", "password_hash", "VARCHAR(255)"),
        ("reviews", "is_approved", "BOOLEAN DEFAULT 1 NOT NULL"),
        ("reviews", "admin_reply", "TEXT"),
        ("orders", "payment_method", "VARCHAR(50) DEFAULT 'demo'"),
        ("wallet_transactions", "reference_id", "VARCHAR(255)"),
    ]
    with engine.connect() as conn:
        for table, column, col_type in migrations:
            try:
                if "sqlite" in str(engine.url):
                    result = conn.execute(text("PRAGMA table_info({})".format(table)))
                    cols = [row[1] for row in result]
                    if column not in cols:
                        conn.execute(text("ALTER TABLE {} ADD COLUMN {} {}".format(table, column, col_type)))
                        conn.commit()
            except Exception:
                pass
