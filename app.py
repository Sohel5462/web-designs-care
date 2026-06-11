import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from database import init_db
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.license_routes import license_bp
from routes.review_routes import review_bp
from routes.wishlist_routes import wishlist_bp
from routes.ticket_routes import ticket_bp
from routes.coupon_routes import coupon_bp
from routes.admin_routes import admin_bp
from routes.settings_routes import settings_bp
from routes.seo_routes import seo_bp
from routes.stripe_routes import stripe_bp
from routes.dropshipping_routes import dropshipping_bp
from routes.ai_routes import ai_bp
from routes.export_routes import export_bp
from routes.misc_routes import misc_bp
from routes.wallet_routes import wallet_bp
from config import Config

app = Flask(__name__, static_folder="static", static_url_path="")
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["DEBUG"] = Config.DEBUG

CORS(app, supports_credentials=True, origins="*", allow_headers=["Content-Type", "Authorization"])

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(license_bp)
app.register_blueprint(review_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(coupon_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(seo_bp)
app.register_blueprint(stripe_bp)
app.register_blueprint(dropshipping_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(export_bp)
app.register_blueprint(misc_bp)
app.register_blueprint(wallet_bp)

# Ensure upload directories exist on startup
os.makedirs(os.path.join(os.path.dirname(__file__), "uploads"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "uploads", "images"), exist_ok=True)


@app.after_request
def after_request(response):
    origin = "*"
    # When credentials are included, wildcard origin is not allowed by browsers.
    # Reflect the actual request origin so cookie-based auth works correctly.
    from flask import request as _req
    req_origin = _req.headers.get("Origin")
    if req_origin:
        origin = req_origin
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,PATCH,OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.route("/api/healthz", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "2.0.0"})


@app.route("/admin")
@app.route("/admin-panel")
def admin_panel_page():
    """Standalone admin management panel."""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    return send_from_directory(static_dir, "admin-panel.html")


@app.route("/my-downloads")
def my_downloads_page():
    """Customer downloads page — view and download purchased products."""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    return send_from_directory(static_dir, "my-downloads.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if path and os.path.exists(os.path.join(static_dir, path)):
        return send_from_directory(static_dir, path)
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return send_from_directory(static_dir, "index.html")
    return jsonify({"message": "Web Designs & Care API is running. Open http://localhost:5000"}), 200


@app.errorhandler(404)
def not_found(e):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(os.path.join(static_dir, "index.html")):
        return send_from_directory(static_dir, "index.html")
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "detail": str(e)}), 500


def seed_demo_data():
    from database import SessionLocal, User, Product, Coupon, SiteSetting, ProductCategory, Notification
    from datetime import datetime, timedelta, timezone

    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            import hashlib as _hl, os as _os
            def _hp(pw):
                salt = _os.urandom(16).hex()
                return "{}:{}".format(salt, _hl.sha256((salt+pw).encode()).hexdigest())
            db.add(User(open_id="demo-admin-001", name="Admin User", email="admin@webdesignscare.com", role="admin", login_method="email", password_hash=_hp("admin123")))
            db.add(User(open_id="demo-user-001", name="John Doe", email="john@example.com", role="user", login_method="email", password_hash=_hp("user123")))
            db.commit()
            print("  [OK] Demo users created (admin: admin123, user: user123)")

        if db.query(Product).count() == 0:
            products = [
                # ── WordPress Themes ─────────────────────────────────────────
                Product(
                    name="Avada | Website Builder For WordPress & WooCommerce", slug="avada-wordpress-website-builder",
                    description="Avada is the #1 selling WordPress theme on ThemeForest of all time. A fully featured, professional WordPress multipurpose theme with the powerful Fusion Builder, Fusion Core plugin and over 90+ pre-built websites.",
                    category="themes", type="theme", price=69.00, original_price=69.00, discount=0,
                    status="published", rating=4.78, rating_count=32105, downloads=1200000, sales=718000,
                    thumbnail_url="https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/avada-responsive-multipurpose-theme/2833226",
                    demo_url="https://avada.theme-fusion.com",
                    tags=["wordpress", "multipurpose", "page-builder", "woocommerce", "elementor"],
                    features=["Fusion Page Builder", "90+ Pre-built Websites", "WooCommerce Ready", "600+ Google Fonts", "Retina Ready", "WPML Compatible"],
                    meta_title="Avada WordPress Theme | Web Designs & Care",
                    meta_description="The world's #1 selling WordPress theme. Feature-rich multipurpose theme with Fusion Builder and 90+ pre-built websites.",
                    keywords="avada, wordpress theme, multipurpose, fusion builder, woocommerce",
                ),
                Product(
                    name="BeTheme | Responsive Multipurpose WordPress & WooCommerce Theme", slug="betheme-responsive-multipurpose-wordpress",
                    description="BeTheme is the largest WordPress theme with more than 700 pre-built websites. A fully responsive, multipurpose WordPress theme with stunning layouts for every industry and purpose.",
                    category="themes", type="theme", price=69.00, original_price=69.00, discount=0,
                    status="published", rating=4.80, rating_count=18943, downloads=985000, sales=328000,
                    thumbnail_url="https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/betheme-responsive-multipurpose-wordpress-html5-theme/7758048",
                    demo_url="https://betheme.net/demo",
                    tags=["wordpress", "multipurpose", "responsive", "woocommerce", "muffin-builder"],
                    features=["700+ Pre-built Websites", "Muffin Page Builder", "WooCommerce Ready", "600+ Google Fonts", "WPML Ready", "Drag & Drop Builder"],
                    meta_title="BeTheme WordPress Theme | Web Designs & Care",
                    meta_description="The largest WordPress theme with 700+ pre-built websites. Stunning responsive layouts for every industry.",
                    keywords="betheme, wordpress theme, multipurpose, 700 demos, muffin builder",
                ),
                Product(
                    name="Flatsome | Multi-Purpose Responsive WooCommerce Theme", slug="flatsome-woocommerce-responsive-theme",
                    description="Flatsome is a super flexible and lightweight WooCommerce theme perfect for any store. Build stunning product pages with the built-in UX Builder and thousands of elements.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.83, rating_count=16723, downloads=820000, sales=185000,
                    thumbnail_url="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/flatsome-multipurpose-responsive-woocommerce-theme/5154388",
                    demo_url="https://flatsome3.uxthemes.com",
                    tags=["woocommerce", "shop", "ecommerce", "ux-builder", "responsive"],
                    features=["UX Builder Included", "WooCommerce Optimized", "Advanced Product Pages", "Lazy Load", "Social Login", "Wishlist & Compare"],
                    meta_title="Flatsome WooCommerce Theme | Web Designs & Care",
                    meta_description="The most popular WooCommerce theme with built-in UX Builder. Fast, flexible, and stunning ecommerce layouts.",
                    keywords="flatsome, woocommerce theme, ecommerce, ux builder, shop",
                ),
                Product(
                    name="Salient | Responsive Multi-Purpose Theme", slug="salient-responsive-multi-purpose-theme",
                    description="Salient is a visually stunning WordPress theme with a large portfolio of award-winning demos. Features the Nectar Page Builder with advanced parallax effects, beautiful UI elements, and a powerful admin.",
                    category="themes", type="theme", price=69.00, original_price=69.00, discount=0,
                    status="published", rating=4.74, rating_count=11892, downloads=567000, sales=161000,
                    thumbnail_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/salient-responsive-multipurpose-theme/4363167",
                    demo_url="https://salient.nectarwpthemes.com",
                    tags=["wordpress", "portfolio", "creative", "parallax", "nectar-builder"],
                    features=["Nectar Page Builder", "Advanced Parallax", "Slider Revolution", "WooCommerce Ready", "WPML Compatible", "One-Click Demo Import"],
                    meta_title="Salient WordPress Theme | Web Designs & Care",
                    meta_description="Visually stunning WordPress theme with award-winning demos and the powerful Nectar Page Builder.",
                    keywords="salient, wordpress theme, creative, parallax, portfolio",
                ),
                Product(
                    name="Bridge | Creative Multipurpose WordPress Theme", slug="bridge-creative-multipurpose-wordpress",
                    description="Bridge is a multi-purpose creative theme built for professionals. With 600+ pre-built demos, the powerful Qode Options panel, and full integration with popular page builders, Bridge is the ultimate creative toolkit.",
                    category="themes", type="theme", price=69.00, original_price=69.00, discount=0,
                    status="published", rating=4.77, rating_count=13421, downloads=638000, sales=172000,
                    thumbnail_url="https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/bridge-creative-multipurpose-wordpress-theme/7315054",
                    demo_url="https://bridge.qodeinteractive.com",
                    tags=["wordpress", "creative", "multipurpose", "elementor", "portfolio"],
                    features=["600+ Pre-built Demos", "Elementor Compatible", "Advanced Portfolio", "WooCommerce Ready", "Qode Options Panel", "Slider Revolution"],
                    meta_title="Bridge WordPress Theme | Web Designs & Care",
                    meta_description="Creative multipurpose WordPress theme with 600+ demos and full Elementor compatibility.",
                    keywords="bridge, wordpress theme, creative, multipurpose, qode",
                ),
                Product(
                    name="Enfold | Responsive Multi-Purpose Theme", slug="enfold-responsive-multi-purpose-theme",
                    description="Enfold is a clean, super flexible and fully responsive WordPress theme with a powerful Avia Layout Builder. It's SEO optimized, has extensive documentation, and is loved by developers and non-developers alike.",
                    category="themes", type="theme", price=69.00, original_price=69.00, discount=0,
                    status="published", rating=4.82, rating_count=20143, downloads=720000, sales=198000,
                    thumbnail_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/enfold-responsive-multi-purpose-theme/4519990",
                    demo_url="https://enfold.kriesi.at",
                    tags=["wordpress", "multipurpose", "avia-builder", "clean", "seo"],
                    features=["Avia Layout Builder", "WooCommerce Ready", "SEO Optimized", "Translation Ready", "Extensive Documentation", "Regular Updates"],
                    meta_title="Enfold WordPress Theme | Web Designs & Care",
                    meta_description="Clean, super flexible WordPress theme loved by developers and non-developers. Includes Avia Layout Builder.",
                    keywords="enfold, wordpress theme, multipurpose, avia builder, responsive",
                ),
                Product(
                    name="WoodMart | Multipurpose WooCommerce WordPress Theme", slug="woodmart-multipurpose-woocommerce-theme",
                    description="WoodMart is a feature-packed WooCommerce theme with 100+ stunning demos for any store type. It includes built-in AJAX filtering, Swatches, Wishlist, Compare, Quick View, Sticky Cart, and much more.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.85, rating_count=9874, downloads=410000, sales=87000,
                    thumbnail_url="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/woodmart-woocommerce-wordpress-theme/20264492",
                    demo_url="https://xtemos.com/demos/woodmart",
                    tags=["woocommerce", "shop", "ecommerce", "ajax", "mega-menu"],
                    features=["100+ Demos", "AJAX Filtering", "Product Swatches", "Wishlist & Compare", "Sticky Cart", "Mega Menu"],
                    meta_title="WoodMart WooCommerce Theme | Web Designs & Care",
                    meta_description="Feature-packed WooCommerce theme with 100+ demos, AJAX filtering, and all essential ecommerce features built-in.",
                    keywords="woodmart, woocommerce theme, ecommerce, ajax filter, product swatches",
                ),
                Product(
                    name="Porto | Multipurpose & WooCommerce Theme", slug="porto-multipurpose-woocommerce-theme",
                    description="Porto is an ultra fast, ultra professional WordPress theme. It features stunning design for every type of website, WooCommerce superstore features, and real-time preview of all customizations.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.79, rating_count=11654, downloads=498000, sales=134000,
                    thumbnail_url="https://images.unsplash.com/photo-1493421419110-74f4e85ba126?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/porto-multipurpose-responsive-wordpress-woocommerce-theme/9207399",
                    demo_url="https://www.portotheme.com",
                    tags=["wordpress", "woocommerce", "multipurpose", "fast", "mega-menu"],
                    features=["Ultra Fast Loading", "WooCommerce Superstore", "Real-Time Preview", "Mega Menu", "AJAX Shop", "One-Click Demo Import"],
                    meta_title="Porto WordPress Theme | Web Designs & Care",
                    meta_description="Ultra fast, ultra professional WordPress theme with WooCommerce superstore features and real-time preview.",
                    keywords="porto, wordpress theme, woocommerce, multipurpose, fast",
                ),
                Product(
                    name="Newspaper | WordPress News & WooCommerce Theme", slug="newspaper-wordpress-news-theme",
                    description="Newspaper is a fully responsive WordPress theme designed for news, magazines, and blogs. It features high-converting ad layouts, lightning-fast performance, and a powerful tagDiv Composer page builder.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.76, rating_count=14532, downloads=620000, sales=167000,
                    thumbnail_url="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/newspaper/5489609",
                    demo_url="https://tagdiv.com/newspaper",
                    tags=["wordpress", "news", "magazine", "blog", "adsense"],
                    features=["tagDiv Composer", "AMP Ready", "AdSense Optimized", "WooCommerce Ready", "100+ Demos", "Speed Optimized"],
                    meta_title="Newspaper WordPress Theme | Web Designs & Care",
                    meta_description="Fully responsive news and magazine theme with lightning-fast performance and high-converting ad layouts.",
                    keywords="newspaper, wordpress theme, news, magazine, blog, adsense",
                ),
                Product(
                    name="Houzez | Real Estate WordPress Theme", slug="houzez-real-estate-wordpress-theme",
                    description="Houzez is the most powerful and feature-rich real estate theme on ThemeForest. Built specifically for real estate agents and agencies, it features advanced property search, agent management, and IDX/MLS integration.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.81, rating_count=8932, downloads=312000, sales=76000,
                    thumbnail_url="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/houzez-real-estate-wordpress-theme/15752549",
                    demo_url="https://houzez.co",
                    tags=["wordpress", "real-estate", "property", "agency", "idx"],
                    features=["Advanced Property Search", "Agent Management", "IDX/MLS Integration", "Google Maps", "Mortgage Calculator", "Email Alerts"],
                    meta_title="Houzez Real Estate Theme | Web Designs & Care",
                    meta_description="The most powerful real estate WordPress theme. Advanced property search, agent management, and IDX/MLS integration.",
                    keywords="houzez, real estate theme, property, agent, wordpress",
                ),
                Product(
                    name="Consulting | Business Finance WordPress Theme", slug="consulting-business-finance-wordpress",
                    description="Consulting is a professional WordPress theme for business, consulting firms, and financial services. It features a clean corporate design with over 40 pre-built demos and an advanced page builder.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.75, rating_count=7621, downloads=289000, sales=68000,
                    thumbnail_url="https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/consulting-finance-business-wordpress-theme/14740561",
                    demo_url="https://consulting.brainstormforce.com",
                    tags=["wordpress", "business", "finance", "corporate", "professional"],
                    features=["40+ Demo Sites", "Elementor Compatible", "Advanced Page Builder", "WooCommerce Ready", "WPML Ready", "SEO Optimized"],
                    meta_title="Consulting Business WordPress Theme | Web Designs & Care",
                    meta_description="Professional WordPress theme for business and consulting firms with 40+ demos and advanced page builder.",
                    keywords="consulting, business theme, finance, corporate, wordpress",
                ),
                # ── Admin Dashboard Templates ────────────────────────────────
                Product(
                    name="Vuexy | Vuejs React Angular Next Laravel & HTML Admin Dashboard Template", slug="vuexy-admin-dashboard-template",
                    description="Vuexy is a beautifully designed admin dashboard template available in Vue.js, React, Angular, Next.js, Laravel, and HTML5. It features 400+ UI components, multiple layouts, and a highly customizable design system.",
                    category="templates", type="template", price=39.00, original_price=79.00, discount=51,
                    status="published", rating=4.88, rating_count=4532, downloads=178000, sales=45000,
                    thumbnail_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/vuexy-vuejs-react-aspnet-html-laravel-admin-dashboard-template/23328599",
                    demo_url="https://demos.pixinvent.com/vuexy-vuejs-admin-template/demo-1",
                    tags=["react", "vue", "angular", "next", "laravel", "dashboard", "admin"],
                    features=["React + Vue + Angular + Next.js + Laravel", "400+ UI Components", "Dark & Light Mode", "RTL Support", "i18n Ready", "TypeScript Support"],
                    meta_title="Vuexy Admin Dashboard Template | Web Designs & Care",
                    meta_description="Premium admin dashboard in Vue.js, React, Angular, Next.js, Laravel & HTML with 400+ components.",
                    keywords="vuexy, admin dashboard, react, vue, angular, admin template",
                ),
                Product(
                    name="Metronic | Bootstrap HTML Sass React Angular Vue & Laravel Admin Dashboard", slug="metronic-bootstrap-admin-dashboard",
                    description="Metronic is the world's most advanced and comprehensive Bootstrap admin dashboard and web application framework. Available in HTML5, React, Angular, Vue.js, and Laravel versions.",
                    category="templates", type="template", price=49.00, original_price=49.00, discount=0,
                    status="published", rating=4.82, rating_count=6234, downloads=234000, sales=87000,
                    thumbnail_url="https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/metronic-responsive-admin-dashboard-template/4021469",
                    demo_url="https://preview.keenthemes.com/metronic8",
                    tags=["bootstrap", "react", "angular", "vue", "laravel", "dashboard", "admin"],
                    features=["All Frameworks Included", "300+ Pages", "CRM Dashboard", "eCommerce Module", "Email App", "Chat App"],
                    meta_title="Metronic Admin Dashboard | Web Designs & Care",
                    meta_description="World's most advanced Bootstrap admin dashboard with HTML5, React, Angular, Vue.js, and Laravel versions.",
                    keywords="metronic, admin dashboard, bootstrap, react, angular, vue",
                ),
                Product(
                    name="Fuse | React Redux Material Design Admin Template", slug="fuse-react-redux-material-admin",
                    description="Fuse is a React material design admin dashboard template built with React, Redux, and Material-UI. It features a complete navigation system, authentication, and hundreds of pages and components.",
                    category="templates", type="template", price=39.00, original_price=79.00, discount=51,
                    status="published", rating=4.80, rating_count=2987, downloads=112000, sales=29000,
                    thumbnail_url="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/fuse-react-react-redux-material-design-admin-template/21769912",
                    demo_url="https://fuse-react.withinpixels.com",
                    tags=["react", "redux", "material-ui", "dashboard", "typescript"],
                    features=["React 18 + TypeScript", "Material-UI", "Redux Toolkit", "Authentication", "RTL Support", "Dark & Light Mode"],
                    meta_title="Fuse React Admin Template | Web Designs & Care",
                    meta_description="Premium React Redux Material Design admin template with comprehensive navigation, auth, and hundreds of components.",
                    keywords="fuse react, admin template, material-ui, redux, dashboard",
                ),
                # ── HTML / Site Templates ──────────────────────────────────
                Product(
                    name="Flatsome | Multi-Purpose Responsive HTML5 Template", slug="flatsome-html5-multipage-template",
                    description="A premium, clean, and modern multi-purpose HTML5 template with pixel-perfect design. Ideal for agencies, corporates, portfolios, and startups. Includes 30+ unique pages.",
                    category="templates", type="template", price=29.00, original_price=49.00, discount=41,
                    status="published", rating=4.72, rating_count=1876, downloads=67000, sales=18000,
                    thumbnail_url="https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/category/site-templates",
                    demo_url="https://themeforest.net/category/site-templates/creative",
                    tags=["html5", "css3", "bootstrap", "multipurpose", "responsive"],
                    features=["30+ Unique Pages", "Bootstrap 5", "CSS3 Animations", "Sass Included", "Cross-Browser", "Well Documented"],
                    meta_title="Multi-Purpose HTML5 Template | Web Designs & Care",
                    meta_description="Premium clean HTML5 template with 30+ unique pages, ideal for agencies, corporates, and startups.",
                    keywords="html5 template, bootstrap, responsive, multipurpose, agency",
                ),
                Product(
                    name="Gostudy | Online Education & LMS HTML5 Template", slug="gostudy-online-education-lms-template",
                    description="Gostudy is a fully responsive HTML5 template designed for online learning platforms, universities, and e-learning websites. Includes course listings, instructor profiles, and a student dashboard.",
                    category="templates", type="template", price=24.00, original_price=49.00, discount=51,
                    status="published", rating=4.68, rating_count=1234, downloads=48000, sales=12000,
                    thumbnail_url="https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/category/site-templates/educational",
                    demo_url="https://themeforest.net/category/site-templates/educational",
                    tags=["education", "lms", "e-learning", "courses", "html5"],
                    features=["Course Listings", "Instructor Profiles", "Student Dashboard", "Quiz Module", "Video Lessons", "Certificate Generator"],
                    meta_title="Gostudy LMS HTML Template | Web Designs & Care",
                    meta_description="Fully responsive HTML5 template for online learning platforms, universities, and e-learning websites.",
                    keywords="education template, lms, e-learning, online courses, html5",
                ),
                # ── React / JavaScript Templates ───────────────────────────
                Product(
                    name="Materially | React Admin & Dashboard Template", slug="materially-react-admin-dashboard",
                    description="Materially is a React admin dashboard template following Material Design principles. It comes with real data integration hooks, multiple dashboard variants, and all the common admin app features.",
                    category="templates", type="template", price=29.00, original_price=59.00, discount=51,
                    status="published", rating=4.75, rating_count=2145, downloads=89000, sales=23000,
                    thumbnail_url="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/materialize-react-react-redux-firebase-admin-template/22197802",
                    demo_url="https://codedthemes.com/demos/admin-templates/materially/react",
                    tags=["react", "material-design", "dashboard", "typescript", "redux"],
                    features=["React 18 + TypeScript", "Material Design", "Firebase Integration", "6 Dashboard Variants", "Dark/Light Mode", "i18n Support"],
                    meta_title="Materially React Admin Template | Web Designs & Care",
                    meta_description="React admin dashboard template following Material Design principles with Firebase integration and 6 dashboard variants.",
                    keywords="react admin, material design, dashboard, typescript, firebase",
                ),
                # ── Plugins ───────────────────────────────────────────────
                Product(
                    name="Essential Grid | WordPress Plugin for Grid & Portfolio", slug="essential-grid-wordpress-plugin",
                    description="Essential Grid is a premium WordPress Grid Plugin that allows you to easily create stunning responsive grids for your posts, pages, WooCommerce products, and custom content types.",
                    category="plugins", type="plugin", price=29.00, original_price=29.00, discount=0,
                    status="published", rating=4.71, rating_count=8923, downloads=380000, sales=126000,
                    thumbnail_url="https://images.unsplash.com/photo-1555421689-d68471e189f2?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/essential-grid-wordpress-plugin/7563340",
                    demo_url="https://www.essential-grid.com",
                    tags=["wordpress", "grid", "portfolio", "gallery", "responsive"],
                    features=["Responsive Grid Layout", "WooCommerce Integration", "Video Support", "Custom Post Types", "Visual Skin Editor", "API Integration"],
                    meta_title="Essential Grid WordPress Plugin | Web Designs & Care",
                    meta_description="Premium WordPress Grid Plugin for posts, pages, WooCommerce products, and custom content with stunning responsive layouts.",
                    keywords="essential grid, wordpress plugin, portfolio grid, gallery, responsive",
                ),
                Product(
                    name="Slider Revolution | Responsive WordPress Plugin", slug="slider-revolution-wordpress-plugin",
                    description="Slider Revolution is the most popular slideshow and content creator plugin for WordPress. Create everything from sliders to full websites with stunning visual effects and animations.",
                    category="plugins", type="plugin", price=29.00, original_price=29.00, discount=0,
                    status="published", rating=4.69, rating_count=22341, downloads=890000, sales=478000,
                    thumbnail_url="https://images.unsplash.com/photo-1534972195531-d756b9bfa9f2?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/slider-revolution-responsive-wordpress-plugin/2751380",
                    demo_url="https://www.sliderrevolution.com",
                    tags=["wordpress", "slider", "animation", "banner", "responsive"],
                    features=["200+ Slider Templates", "Animation Designer", "Video Backgrounds", "Parallax Effects", "Touch Swipe", "Fully Responsive"],
                    meta_title="Slider Revolution WordPress Plugin | Web Designs & Care",
                    meta_description="The most popular WordPress slideshow plugin. Create sliders, hero sections, and full websites with stunning animations.",
                    keywords="slider revolution, wordpress slider, animation, banner plugin",
                ),
                Product(
                    name="WPBakery Page Builder | WordPress Plugin", slug="wpbakery-page-builder-wordpress",
                    description="WPBakery Page Builder (formerly Visual Composer) is the #1 best-selling WordPress page builder plugin on CodeCanyon. Drag and drop any element anywhere on your page without touching code.",
                    category="plugins", type="plugin", price=64.00, original_price=64.00, discount=0,
                    status="published", rating=4.40, rating_count=37821, downloads=1450000, sales=892000,
                    thumbnail_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=500&fit=crop",
                    preview_url="https://codecanyon.net/item/visual-composer-page-builder-for-wordpress/242431",
                    demo_url="https://wpbakery.com",
                    tags=["wordpress", "page-builder", "drag-drop", "visual-composer"],
                    features=["500+ Content Elements", "Frontend & Backend Editor", "Responsive Builder", "Third-Party Plugins Support", "Role Manager", "Template Library"],
                    meta_title="WPBakery Page Builder Plugin | Web Designs & Care",
                    meta_description="The #1 best-selling WordPress page builder. Drag and drop any element without touching code.",
                    keywords="wpbakery, visual composer, page builder, wordpress plugin, drag drop",
                ),
                # ── Bundles ───────────────────────────────────────────────
                Product(
                    name="Ultimate WordPress Bundle | 15 Premium Themes + 20 Plugins", slug="ultimate-wordpress-bundle",
                    description="The Ultimate WordPress Bundle gives you access to 15 premium multipurpose themes and 20 essential plugins at one incredible price. Everything you need to build any type of WordPress website.",
                    category="bundles", type="bundle", price=99.00, original_price=799.00, discount=88,
                    status="published", rating=4.90, rating_count=567, downloads=45000, sales=12000,
                    thumbnail_url="https://images.unsplash.com/photo-1487014679447-9f8336841d58?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/collections",
                    demo_url="https://themeforest.net/collections",
                    tags=["bundle", "wordpress", "themes", "plugins", "value"],
                    features=["15 Premium Themes", "20 Essential Plugins", "Lifetime Updates", "Premium Support", "White Label Option", "Extended License"],
                    meta_title="Ultimate WordPress Bundle | Web Designs & Care",
                    meta_description="Get 15 premium themes and 20 essential plugins in one incredible bundle. Everything for any WordPress website.",
                    keywords="wordpress bundle, premium themes, plugins bundle, ultimate pack",
                ),
                Product(
                    name="React Developer Bundle | 5 Admin Templates + UI Kit", slug="react-developer-bundle",
                    description="The React Developer Bundle includes 5 premium React admin dashboard templates plus a comprehensive UI component library. Build any web application faster with this complete React toolkit.",
                    category="bundles", type="bundle", price=89.00, original_price=249.00, discount=64,
                    status="published", rating=4.85, rating_count=312, downloads=28000, sales=7800,
                    thumbnail_url="https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/collections",
                    demo_url="https://themeforest.net/collections",
                    tags=["react", "bundle", "dashboard", "ui-kit", "typescript"],
                    features=["5 React Admin Templates", "UI Component Library", "TypeScript Support", "Redux & Context Examples", "Figma Files Included", "Lifetime Updates"],
                    meta_title="React Developer Bundle | Web Designs & Care",
                    meta_description="5 premium React admin dashboard templates plus comprehensive UI component library. Complete React development toolkit.",
                    keywords="react bundle, admin templates, ui kit, react developer, typescript",
                ),
                # ── Mobile / UI Kits ──────────────────────────────────────
                Product(
                    name="Kalium | Creative Theme for Professionals", slug="kalium-creative-theme-professionals",
                    description="Kalium is a modern and clean portfolio theme for creative professionals. With the Laborator theme framework, it offers amazing flexibility, beautiful design, and stellar performance.",
                    category="themes", type="theme", price=69.00, original_price=69.00, discount=0,
                    status="published", rating=4.83, rating_count=7234, downloads=298000, sales=72000,
                    thumbnail_url="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/kalium-creative-theme-for-professionals/10860525",
                    demo_url="https://kaliumtheme.com/demos",
                    tags=["wordpress", "portfolio", "creative", "photography", "clean"],
                    features=["Advanced Portfolio Builder", "Photography Gallery", "WooCommerce Ready", "One-Click Demo Import", "Laborator Theme Framework", "Pixel Perfect Design"],
                    meta_title="Kalium Creative WordPress Theme | Web Designs & Care",
                    meta_description="Modern and clean portfolio theme for creative professionals with the powerful Laborator theme framework.",
                    keywords="kalium, creative theme, portfolio, photography, wordpress",
                ),
                Product(
                    name="Rey | Fashion & Clothing WooCommerce Theme", slug="rey-fashion-clothing-woocommerce-theme",
                    description="Rey is an ultra-modern WooCommerce theme designed specifically for fashion, clothing, and lifestyle brands. It features stunning product pages, advanced filtering, and a fast-loading architecture.",
                    category="themes", type="theme", price=59.00, original_price=59.00, discount=0,
                    status="published", rating=4.87, rating_count=3821, downloads=142000, sales=34000,
                    thumbnail_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=500&fit=crop",
                    preview_url="https://themeforest.net/item/rey-fashionclothingwoocommerce-theme/27373434",
                    demo_url="https://reytheme.com",
                    tags=["woocommerce", "fashion", "clothing", "ecommerce", "lifestyle"],
                    features=["Fashion-Forward Layouts", "Advanced AJAX Filter", "Lookbook Feature", "Size Guide Popup", "Wishlist & Compare", "Instagram Shopping"],
                    meta_title="Rey Fashion WooCommerce Theme | Web Designs & Care",
                    meta_description="Ultra-modern WooCommerce theme for fashion, clothing, and lifestyle brands with stunning product pages and AJAX filtering.",
                    keywords="rey theme, fashion woocommerce, clothing store, lifestyle ecommerce",
                ),
            ]
            for p in products:
                db.add(p)
            db.commit()
            print("  [OK] {} ThemeForest products created".format(len(products)))

        if db.query(Coupon).count() == 0:
            now = datetime.now(timezone.utc)
            coupons = [
                Coupon(code="SAVE10", description="10% off any order", type="percentage", value=10, min_order_amount=0, max_uses=1000, is_active=True, expires_at=now + timedelta(days=365)),
                Coupon(code="SAVE20", description="20% off orders over $50", type="percentage", value=20, min_order_amount=50, max_uses=500, is_active=True, expires_at=now + timedelta(days=180)),
                Coupon(code="FLAT5", description="$5 off any order", type="fixed", value=5, min_order_amount=0, max_uses=2000, is_active=True, expires_at=now + timedelta(days=365)),
                Coupon(code="WELCOME", description="15% welcome discount", type="percentage", value=15, min_order_amount=0, max_uses=100, is_active=True, expires_at=now + timedelta(days=90)),
            ]
            for c in coupons:
                db.add(c)
            db.commit()
            print("  [OK] Demo coupons created")

        if db.query(ProductCategory).count() == 0:
            cats = [
                ProductCategory(name="Templates", slug="templates"),
                ProductCategory(name="Themes", slug="themes"),
                ProductCategory(name="Plugins", slug="plugins"),
                ProductCategory(name="Bundles", slug="bundles"),
                ProductCategory(name="UI Kits", slug="ui-kits"),
                ProductCategory(name="Mobile", slug="mobile"),
                ProductCategory(name="Dropshipping", slug="dropshipping"),
            ]
            for c in cats:
                db.add(c)
            db.commit()
            print("  [OK] Default product categories created")

        settings_defaults = [
            ("site_name", "Web Designs & Care"),
            ("site_tagline", "Premium Digital Assets for Modern Developers"),
            ("site_description", "Premium website templates, themes, plugins, and full-site bundles"),
            ("site_url", "http://localhost:5000"),
            ("contact_email", "support@webdesignscare.com"),
            ("currency", "USD"),
            ("language", "en"),
            ("default_theme", "light"),
            ("maintenance_mode", "false"),
            ("demo_mode", "false"),
            ("footer_text", "2025 Web Designs & Care. All rights reserved."),
            ("logo_url", ""),
            ("favicon_url", ""),
            ("primary_color", "#3b82f6"),
            ("secondary_color", "#1e293b"),
            ("accent_color", "#f59e0b"),
            ("custom_css", ""),
            ("custom_header_html", ""),
            ("custom_footer_html", ""),
            ("seo_sitemap_enabled", "true"),
            ("seo_structured_data_enabled", "true"),
            ("seo_robots_txt", "User-agent: *\nAllow: /\nDisallow: /api/admin/\nSitemap: /sitemap.xml"),
            ("seo_default_meta_title_template", "{name} | {site_name}"),
            ("seo_default_meta_description", "Premium digital assets for modern developers and businesses."),
            ("seo_og_image_url", ""),
            ("seo_twitter_handle", ""),
            ("seo_twitter_card_type", "summary_large_image"),
            ("seo_google_analytics_id", ""),
            ("seo_google_site_verification", ""),
            ("seo_bing_site_verification", ""),
            ("seo_canonical_url", ""),
            ("stripe_enabled", "false"),
            ("stripe_publishable_key", ""),
            ("stripe_secret_key", ""),
            ("stripe_webhook_secret", ""),
            ("dropshipping_enabled", "false"),
            ("autods_enabled", "false"),
            ("autods_api_key", ""),
            ("autods_user_id", ""),
            ("autods_auto_fulfill", "false"),
            ("autods_price_markup", "30"),
            ("autods_default_supplier", "amazon"),
            ("autods_stock_monitoring", "true"),
            ("autods_price_monitoring", "true"),
            ("autods_auto_titles", "true"),
            ("dropshipping_processing_days", "3-7"),
            ("dropshipping_return_policy", "30-day returns accepted"),
            ("dropshipping_shipping_note", "Shipped directly from supplier"),
            ("ai_enabled", "false"),
            ("ai_provider", "openai"),
            ("ai_api_key", ""),
            ("ai_model", "gpt-3.5-turbo"),
            ("marketing_email_enabled", "false"),
            ("marketing_smtp_host", ""),
            ("marketing_smtp_port", "587"),
            ("marketing_smtp_user", ""),
            ("marketing_smtp_pass", ""),
            ("marketing_from_email", ""),
            ("marketing_from_name", "Web Designs & Care"),
            ("automarketing_enabled", "false"),
            ("automarketing_facebook", "false"),
            ("automarketing_twitter", "false"),
            ("automarketing_instagram", "false"),
            ("automarketing_schedule", "daily"),
            ("template_types", '["React","Vue.js","Nuxt.js","Angular","Svelte","Laravel (PHP)","Django (Python)","Shopify Liquid","Next.js","SvelteKit","Portfolio","SaaS / App UI"]'),
            ("social_facebook", ""),
            ("social_twitter", ""),
            ("social_instagram", ""),
            ("social_youtube", ""),
            ("social_linkedin", ""),
            ("social_tiktok", ""),
            ("social_github", ""),
            ("social_discord", ""),
            ("social_telegram", ""),
            ("chatbot_enabled", "true"),
            ("chatbot_greeting", "\U0001f44b Hi! How can I help you find something today?"),
            ("chatbot_color", "#3b82f6"),
            ("page_about", ""),
            ("page_faq", ""),
            ("page_terms", ""),
            ("page_privacy", ""),
            ("page_refund", ""),
        ]
        added = 0
        for key, val in settings_defaults:
            if not db.query(SiteSetting).filter(SiteSetting.key == key).first():
                db.add(SiteSetting(key=key, value=val))
                added += 1
        if added:
            db.commit()
            print("  [OK] {} site settings initialized".format(added))

        if db.query(Notification).count() == 0:
            db.add(Notification(
                user_id=None,
                title="Welcome to Web Designs & Care v2.0!",
                message="Admin panel fully fixed. All features are working. Enjoy!",
                type="success",
                icon="check-circle",
                link="/admin",
            ))
            db.add(Notification(
                user_id=None,
                title="CSV Import Ready",
                message="You can now import products from CSV/Excel via Admin > Products > Import.",
                type="info",
                icon="upload",
                link="/admin/products",
            ))
            db.commit()
            print("  [OK] Welcome notifications created")

    except Exception as e:
        db.rollback()
        print("  [WARN] Seed error: {}".format(e))
    finally:
        db.close()


if __name__ == "__main__":
    print("")
    print("=" * 56)
    print("   Web Designs & Care v2.0 — Fixed Edition")
    print("=" * 56)
    print("")
    print("[1/3] Initializing database...")
    init_db()
    print("  [OK] Database ready")
    print("[2/3] Seeding demo data...")
    seed_demo_data()
    print("[3/3] Starting web server...")
    print("")
    print("  >>> Open:         http://localhost:{}".format(Config.PORT))
    print("  >>> Admin Panel:  http://localhost:{}/admin-panel".format(Config.PORT))
    print("  >>> My Downloads: http://localhost:{}/my-downloads".format(Config.PORT))
    print("")
    print("  Admin Login:  admin@webdesignscare.com")
    print("  Customer:     any email")
    print("  Coupons:      SAVE10 | SAVE20 | FLAT5 | WELCOME")
    print("")
    print("  Press Ctrl+C to stop")
    print("=" * 56)
    print("")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, use_reloader=False)
