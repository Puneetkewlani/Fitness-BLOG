import os
import re

base_dir = r"c:\Users\LENOVO\IWT-Project-"
assets_css = os.path.join(base_dir, "assets", "css", "styles.css")
html_files = ["diet.html", "contact.html", "exercise.html", "assessment.html", "games.html"]

# 1. Update completely the :root variables inside styles.css to enforce the modern dark theme globally
with open(assets_css, "r", encoding="utf-8") as f:
    css = f.read()

dark_root = """:root {
  /* Colors */
  --primary: #4f46e5;
  --primary-dark: #3730a3;
  --primary-light: #6366f1;
  --accent: #10b981;
  --accent-green: #10b981;
  --accent-blue: #3b82f6;
  --accent-yellow: #f59e0b;
  --accent-purple: #8b5cf6;

  /* Backgrounds */
  --bg-dark: #09090b;
  --bg-dark-2: #18181b;
  --card-bg: rgba(39, 39, 42, 0.4);
  --card-bg-light: rgba(63, 63, 70, 0.4);

  /* Text */
  --text-dark: #f4f4f5;
  --text-muted: #a1a1aa;
  --text-light: #71717a;

  /* Gradients */
  --gradient-primary: linear-gradient(135deg, var(--primary), var(--primary-light));
  --gradient-accent: linear-gradient(135deg, var(--primary), var(--accent));
  --gradient-hero: linear-gradient(rgba(9, 9, 11, 0.8), rgba(9, 9, 11, 0.8)), linear-gradient(135deg, var(--bg-dark), var(--bg-dark-2));

  /* Shadows */
  --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 8px 25px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.6);
  --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.8);
  --shadow-glow: 0 15px 45px rgba(79, 70, 229, 0.25);
"""

# Replace the existing :root block up to the shadows
css = re.sub(r':root\s*{[\s\S]*?--shadow-glow:[^;]*;', dark_root, css, count=1)

# Add header layout support to styles.css since we are swapping the HTML to be the new header structure
modern_header_css = """
/* Major Overrides for Shared Modern Header/Footer */
.header-inner { display: flex; align-items: center; justify-content: space-between; width: 100%; }
.logo { display: flex; align-items: center; gap: 8px; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 1.25rem; color: var(--text-dark); text-decoration: none;}
.logo-icon { color: var(--primary-light); display: flex; }
.site-footer { padding: 40px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); background: var(--bg-dark); }
.footer-inner { display: flex; justify-content: space-between; align-items: center; }
.footer-brand h4 { font-size: 1.25rem; font-weight: 800; margin-bottom: 4px; font-family: 'Plus Jakarta Sans', sans-serif;}
.footer-brand p { font-size: 0.875rem; color: var(--text-muted);}
.footer-links p { font-size: 0.875rem; color: var(--text-muted); }
.site-header { position: sticky; top: 0; z-index: 50; background-color: rgba(9, 9, 11, 0.7); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding: 16px 0; }
a { color: inherit; text-decoration: none;}
.card, .info-card, .service-card, .pricing-card, .faq-item { backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); }
.data-table th, .data-table td { border-bottom: 1px solid rgba(255,255,255,0.08); }
.data-table th { background: rgba(79, 70, 229, 0.15) !important; color: var(--primary-light); border-bottom: 2px solid var(--primary-light) !important; }
"""
if ".header-inner" not in css:
    css += modern_header_css
    
# Change default styles.css body font
css = css.replace("font-family: 'Poppins', sans-serif;", "font-family: 'Inter', sans-serif;")
css = css.replace("font-family: 'Roboto', sans-serif;", "font-family: 'Inter', sans-serif;")

with open(assets_css, "w", encoding="utf-8") as f:
    f.write(css)

# 2. Iterate HTML files to replace Header, Footer, Fonts, and SVG Emojis safely
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
    r'🍎': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" class="text-primary" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>',
    r'📞': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>',
    r'💪': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><path d="M14.5 10c0-2.8-2.2-5-5-5a5 5 0 000 10h5z"/></svg>',
    r'🏋️‍♂️': r'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#6366f1;vertical-align:middle;margin-right:8px;"><circle cx="12" cy="12" r="10"/><path d="M12 8v8"/><path d="M8 12h8"/></svg>'
}

for file_name in html_files:
    path = os.path.join(base_dir, file_name)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Step 1: Inject font links if needed
    font_link = '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
    if "Plus+Jakarta+Sans" not in html:
        html = html.replace("</head>", f"  {font_link}\n</head>")

    # Step 2: Swap the header tags completely
    html = re.sub(r'<header id="top" class="site-header">.*?</header>', modern_header, html, flags=re.DOTALL)

    # Step 3: Swap the footer tags completely
    html = re.sub(r'<footer class="site-footer">.*?</footer>', modern_footer, html, flags=re.DOTALL)
    
    # Step 4: Swap basic Emojis safely
    for emoji, svg in svg_map.items():
        html = html.replace(emoji, svg)

    # Clean legacy hardcoded colors on inline styles while strictly maintaining the "display: grid" logic
    html = re.sub(r'color:\s*(?:#[0-9a-fA-F]{3,6}|black|teal|red|blue);?', '', html)
    
    # Link to both modern header structure and original grids. We keep the styles.css linked! 
    # Active tab fix
    if file_name == "diet.html":
        html = html.replace('<a href="diet.html">Diet Plans</a>', '<a href="diet.html" class="active">Diet Plans</a>')
    elif file_name == "exercise.html":
        html = html.replace('<a href="exercise.html">Exercise</a>', '<a href="exercise.html" class="active">Exercise</a>')
    elif file_name == "contact.html":
        html = html.replace('<a href="contact.html">Contact</a>', '<a href="contact.html" class="active">Contact</a>')

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Delicate refactor applied safely to {file_name}")
