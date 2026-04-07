import os
import re

base_dir = r"c:\Users\LENOVO\IWT-Project-"
assets_css = os.path.join(base_dir, "assets", "css")
modern_css_path = os.path.join(assets_css, "modern.css")
styles_css_path = os.path.join(assets_css, "styles.css")

html_files = ["diet.html", "contact.html", "exercise.html", "assessment.html", "games.html"]

modern_header = """  <header id="top" class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="logo">
        <span class="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path><line x1="6" y1="1" x2="6" y2="4"></line><line x1="10" y1="1" x2="10" y2="4"></line><line x1="14" y1="1" x2="14" y2="4"></line></svg>
        </span>
        FitLife
      </a>
      <nav class="site-nav">
        <a href="index.html">Home</a>
        <a href="diet.html">Diet Plans</a>
        <a href="exercise.html">Exercise</a>
        <a href="contact.html">Contact</a>
      </nav>
      <a href="index.html#assessment" class="btn btn-sm btn-primary">Get Started</a>
    </div>
  </header>"""

modern_footer = """  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <h4>FitLife</h4>
        <p>Dedicated to Your Health & Wellness.</p>
      </div>
      <div class="footer-links">
        <p>© 2025 FitLife | Created by Puneet Kewlani</p>
      </div>
    </div>
  </footer>"""

svg_map = {
    r'🍎': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>',
    r'📞': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>',
    r'💪': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M14.5 10c0-2.8-2.2-5-5-5a5 5 0 000 10h5z"/></svg>',
    r'💡': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M9 21h6m-3-3v3m0-16a5 5 0 00-5 5c0 1.57.8 2.94 2 3.75V17a2 2 0 002 2h2a2 2 0 002-2v-2.25c1.2-.81 2-2.18 2-3.75a5 5 0 00-5-5z"/></svg>',
    r'🔥': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M12 2c-4 5-2 11-2 11 2-3 4-2 4-2 1 2 2 4 4 2 2 7-6 9-6 9s7-1 9-6c2-6-4-10-4-10-1.5-1-5-4-5-4z"/></svg>',
    r'💎': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M6 3h12l4 6-10 12L2 9l4-6z"/></svg>',
    r'🎯': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="text-primary" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    r'🔺': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="text-primary" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    r'✨': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="text-primary" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    r'📊': r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="text-primary" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
}

for file_name in html_files:
    path = os.path.join(base_dir, file_name)
    if os.path.exists(path):
        os.system(f"git checkout -- {path}")

# Delete styles.css completely
if os.path.exists(styles_css_path):
    os.remove(styles_css_path)

for file_name in html_files:
    path = os.path.join(base_dir, file_name)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Step 1: Force stylesheet to modern.css
    html = re.sub(r'<link rel="stylesheet"[^>]*styles\.css[^>]*>', r'<link rel="stylesheet" href="assets/css/modern.css">', html)
    
    # Fonts
    if "Plus+Jakarta+Sans" not in html:
        font_link = '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
        html = html.replace("</head>", f"  {font_link}\n</head>")

    # Step 2: Swap the header tags completely
    html = re.sub(r'<header id="top" class="site-header">.*?</header>', modern_header, html, flags=re.DOTALL)

    # Step 3: Swap the footer tags completely
    html = re.sub(r'<footer class="site-footer">.*?</footer>', modern_footer, html, flags=re.DOTALL)
    
    # Step 4: Swap Emojis safely
    for emoji, svg in svg_map.items():
        html = html.replace(emoji, svg)

    # Clean legacy inline colors but strictly keep the grid styles
    html = re.sub(r'(style=".*?)color:\s*#[a-zA-Z0-9]{3,6};?(.*?")', r'\1\2', html)
    html = re.sub(r'(style=".*?)background:\s*linear-gradient.*?;?(.*?")', r'\1\2', html)
    
    # Active tab fix
    html = html.replace(f'<a href="{file_name}">{file_name.replace(".html", "").capitalize()}', f'<a href="{file_name}" class="active">{file_name.replace(".html", "").capitalize()}')
    if file_name == "diet.html":
        html = html.replace('<a href="diet.html">Diet Plans</a>', '<a href="diet.html" class="active">Diet Plans</a>')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
        
css_append = """
/* ========================================
   Legacy Internal Component Support
   ======================================== */
.card, .card-padding { background: var(--bg-card); border: 1px solid var(--border-color); padding: 32px; border-radius: var(--radius-lg); margin-bottom: 30px;}
.data-table { width: 100%; border-collapse: collapse; background: var(--bg-surface); border-radius: var(--radius-lg); overflow: hidden; border: 1px solid var(--border-color); margin-bottom: 30px;}
.data-table th, .data-table td { padding: 16px 20px; text-align: left; border-bottom: 1px solid var(--border-color); color: var(--text-muted);}
.data-table th { background: rgba(79, 70, 229, 0.15); color: var(--primary-light); font-weight: 700; font-family: var(--font-heading); }
.data-table tr:hover td { background: rgba(255, 255, 255, 0.02); }
.form-input, .form-select, .form-textarea { width: 100%; padding: 14px; background: var(--bg-dark); border: 1px solid var(--border-color); border-radius: var(--radius-md); color: var(--text-main); font-family: var(--font-body); margin-bottom: 20px;}
.assessment-submit, .form-submit { width: 100%; border: none; outline: none; background: var(--primary); color: white; padding: 16px 24px; border-radius: var(--radius-md); font-family: var(--font-heading); font-weight: 700; cursor: pointer; transition: var(--transition); }
.assessment-submit:hover, .form-submit:hover { background: var(--primary-hover); transform: translateY(-2px); }

/* Unified Grids */
.tips-grid, .info-grid, .services-grid, .pricing-grid, .faq-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-bottom: 40px;}
.tip-card, .info-box, .service-card, .faq-item, .info-card { background: var(--bg-card); border: 1px solid var(--border-color); padding: 24px; border-radius: var(--radius-lg); transition: var(--transition); }
.tip-card:hover, .info-box:hover, .service-card:hover, .info-card:hover { transform: translateY(-4px); border-color: rgba(255, 255, 255, 0.2); }
.info-icon, .tip-number { font-size: 2rem; margin-bottom: 16px; color: var(--primary-light); font-family: var(--font-heading); }
.tip-card h5, .info-box h5, .service-card h5, .info-card h4, .faq-item h5 { color: var(--text-main); margin-bottom: 8px; font-size: 1.25rem; font-family: var(--font-heading);}
.tip-card p, .info-box p, .service-card p, .info-card p, .faq-item p { color: var(--text-muted); font-size: 0.95rem; }

/* Pricing Elements */
.pricing-card { background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 32px; text-align: center;}
.pricing-card:hover { transform: translateY(-4px); box-shadow: 0 10px 40px rgba(0,0,0,0.5); border-color: var(--primary-hover); }
.pricing-header h5 { font-size: 1.5rem; color: var(--text-main); margin-bottom: 24px;}
.pricing-price .amount { font-size: 3rem; font-weight: 800; color: var(--primary-light); font-family: var(--font-heading); }
.pricing-features { list-style: none; padding: 0; margin-top: 24px; text-align: left; }
.pricing-features li { padding: 8px 0; color: var(--text-muted); border-bottom: 1px solid rgba(255,255,255,0.05);}
.check { color: #10b981; font-weight: bold; margin-right: 8px;}
.cross { color: #ef4444; font-weight: bold; margin-right: 8px;}

/* BMI Results */
.bmi-result-box { text-align: center; margin-top: 32px; padding: 32px; border: 1px solid var(--border-color); border-radius: var(--radius-lg); background: var(--bg-dark);}
.bmi-value { font-size: 3.5rem; font-family: var(--font-heading); font-weight: 800; margin: 16px 0; }
.bmi-category { font-size: 1.5rem; font-weight: 600; margin-bottom: 8px; }
.bmi-description { color: var(--text-muted); font-size: 1rem;}
.bmi-ranges { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 32px; }
.bmi-range { padding: 16px; border-radius: var(--radius-md); font-size: 0.85rem; background: var(--bg-card); border: 1px solid var(--border-color);}
.bmi-range.underweight { border-left: 4px solid #38bdf8; }
.bmi-range.normal { border-left: 4px solid #10b981; }
.bmi-range.overweight { border-left: 4px solid #f59e0b; }
.bmi-range.obese { border-left: 4px solid #ef4444; }

/* Contact specific */
.welcome-card { background: var(--bg-card); border: 1px solid rgba(79, 70, 229, 0.4); padding: 32px; border-radius: var(--radius-lg); font-size: 1.1rem; max-width: 800px; margin: 0 auto 40px; text-align: center; }
"""

with open(modern_css_path, "r", encoding="utf-8") as f:
    modern_css = f.read()

if "Legacy Internal Component Support" not in modern_css:
    with open(modern_css_path, "a", encoding="utf-8") as f:
        f.write(css_append)
"""
