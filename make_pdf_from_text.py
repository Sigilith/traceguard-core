import os
import subprocess
import sys

# Ensure reportlab is available
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "--quiet", "--no-build-isolation"])
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

download_dirs = [
    "/storage/emulated/0/Download",
    "/sdcard/Download",
    os.path.expanduser("~/storage/downloads"),
    os.path.expanduser("~/downloads")
]

target_dir = next((d for d in download_dirs if os.path.exists(d) or os.access(os.path.dirname(d), os.W_OK)), ".")
os.makedirs(target_dir, exist_ok=True)
pdf_path = os.path.join(target_dir, "lineage_test.pdf")

doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=12, leading=16, spaceAfter=8, fontName='Helvetica-Bold')
body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, leading=12, fontName='Courier', spaceAfter=4)

if os.path.exists("lineage_test.txt"):
    with open("lineage_test.txt", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    story.append(Paragraph("System Snapshot & Environment Report", title_style))
    story.append(Spacer(1, 6))
    
    for line in content.split("\n"):
        if not line.strip():
            story.append(Spacer(1, 4))
            continue
        # Escape XML entities for ReportLab
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(safe_line, body_style))
    
    doc.build(story)
    print(f"[+] Successfully generated PDF from lineage_test.txt at: {pdf_path}")
else:
    print("[-] Error: lineage_test.txt not found in the current directory.")
