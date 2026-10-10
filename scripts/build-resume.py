from pathlib import Path
from shutil import copy2

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FINAL_PDF = OUTPUT_DIR / "Mohith_Dharshan_Resume_One_Page.pdf"
SITE_PDF = ROOT / "assets" / "Mohith_Dharshan_Resume.pdf"

PAGE_W, PAGE_H = A4
MARGIN = 11 * mm
INK = colors.HexColor("#151014")
MUTED = colors.HexColor("#554C51")
ACCENT = colors.HexColor("#EF3D46")
LINE = colors.HexColor("#D8D2D5")
PAPER = colors.HexColor("#FFFFFF")


class OnePageResume(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=MARGIN,
            rightMargin=MARGIN,
            topMargin=MARGIN,
            bottomMargin=MARGIN,
            title="",
            author="",
            subject="",
        )
        frame = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN, id="resume")
        self.addPageTemplates(PageTemplate(id="one-page", frames=[frame], onPage=self._decorate))

    @staticmethod
    def _decorate(canvas, _doc):
        canvas.saveState()
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canvas.setFillColor(ACCENT)
        canvas.rect(0, PAGE_H - 4 * mm, PAGE_W, 4 * mm, fill=1, stroke=0)
        canvas.setFillColor(INK)
        canvas.rect(0, 0, PAGE_W, 5 * mm, fill=1, stroke=0)
        canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ResumeName",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=23,
    leading=24,
    textColor=INK,
    spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="ResumeRole",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.7,
    leading=10.5,
    textColor=ACCENT,
    tracking=0.8,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="ResumeContact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.8,
    leading=10.2,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=11,
    textColor=ACCENT,
    tracking=0.9,
    spaceBefore=5,
    spaceAfter=3.5,
    borderWidth=0,
    borderPadding=0,
))
styles.add(ParagraphStyle(
    name="Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.35,
    leading=11.2,
    textColor=MUTED,
    spaceAfter=2.4,
    alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="BodyTight",
    parent=styles["Body"],
    fontSize=8.05,
    leading=10.5,
    spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="ItemTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9.1,
    leading=11,
    textColor=INK,
    spaceAfter=1,
))
styles.add(ParagraphStyle(
    name="Meta",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=7.4,
    leading=9,
    textColor=ACCENT,
    spaceAfter=1.2,
))
styles.add(ParagraphStyle(
    name="SkillLabel",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.0,
    leading=9.6,
    textColor=INK,
    spaceAfter=0.6,
))
styles.add(ParagraphStyle(
    name="SkillValue",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.9,
    leading=10,
    textColor=MUTED,
    spaceAfter=3.8,
))


def section(title: str):
    return [
        Spacer(1, 1.5 * mm),
        Paragraph(title.upper(), styles["Section"]),
        Table([[""]], colWidths=[None], rowHeights=[0.45], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LINE),
        ])),
        Spacer(1, 1.5 * mm),
    ]


def bullets(items):
    return [Paragraph(f"- {item}", styles["BodyTight"]) for item in items]


def experience(title, organisation, date, items):
    return [
        Paragraph(title, styles["ItemTitle"]),
        Paragraph(f"{organisation}  |  {date}", styles["Meta"]),
        *bullets(items),
        Spacer(1, 1.2 * mm),
    ]


def project(title, stack, description):
    return [
        Paragraph(title, styles["ItemTitle"]),
        Paragraph(stack, styles["Meta"]),
        Paragraph(description, styles["BodyTight"]),
        Spacer(1, 1.1 * mm),
    ]


def skill(label, value):
    return [
        Paragraph(label, styles["SkillLabel"]),
        Paragraph(value, styles["SkillValue"]),
    ]


pdf = canvas.Canvas(str(FINAL_PDF), pagesize=A4)
pdf.setTitle("")
pdf.setAuthor("")
pdf.setSubject("")
pdf.setCreator("")
pdf._doc.info.producer = ""
pdf._doc.info.keywords = ""
pdf.setFillColor(PAPER)
pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
pdf.setFillColor(ACCENT)
pdf.rect(0, PAGE_H - 4 * mm, PAGE_W, 4 * mm, fill=1, stroke=0)
pdf.setFillColor(INK)
pdf.rect(0, 0, PAGE_W, 5 * mm, fill=1, stroke=0)

left_x = MARGIN
left_w = 112 * mm
right_x = left_x + left_w + 5 * mm
right_w = PAGE_W - MARGIN - right_x
content_top = PAGE_H - 36 * mm


def draw_paragraph(text, style, x, y, width, gap=0):
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(pdf, x, y - height)
    return y - height - gap


def draw_section(title, x, y, width):
    y -= 3.1 * mm
    y = draw_paragraph(title.upper(), styles["Section"], x, y, width, 1.1 * mm)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.55)
    pdf.line(x, y, x + width, y)
    return y - 1.8 * mm


def draw_bullets(items, x, y, width):
    for item in items:
        y = draw_paragraph(f"- {item}", styles["BodyTight"], x, y, width, 0.35 * mm)
    return y


def draw_experience(title, organisation, date, items, x, y, width):
    y = draw_paragraph(title, styles["ItemTitle"], x, y, width, 0.2 * mm)
    y = draw_paragraph(f"{organisation}  |  {date}", styles["Meta"], x, y, width, 0.45 * mm)
    y = draw_bullets(items, x, y, width)
    return y - 1.2 * mm


def draw_project(title, stack, description, x, y, width):
    y = draw_paragraph(title, styles["ItemTitle"], x, y, width, 0.1 * mm)
    y = draw_paragraph(stack, styles["Meta"], x, y, width, 0.35 * mm)
    y = draw_paragraph(description, styles["BodyTight"], x, y, width)
    return y - 1.15 * mm


def draw_skill(label, value, x, y, width):
    y = draw_paragraph(label, styles["SkillLabel"], x, y, width, 0.2 * mm)
    y = draw_paragraph(value, styles["SkillValue"], x, y, width)
    return y - 0.8 * mm


# Header
pdf.setFillColor(INK)
pdf.setFont("Helvetica-Bold", 23)
pdf.drawString(left_x, PAGE_H - 23 * mm, "MOHITH DHARSHAN J")
pdf.setFillColor(ACCENT)
pdf.setFont("Helvetica-Bold", 8.7)
pdf.drawString(left_x, PAGE_H - 31 * mm, "SOFTWARE ENGINEERING / AI / FULL-STACK DEVELOPMENT")
pdf.setStrokeColor(LINE)
pdf.setLineWidth(0.7)
pdf.line(right_x - 3 * mm, PAGE_H - 34 * mm, right_x - 3 * mm, PAGE_H - 14 * mm)

contact_y = PAGE_H - 15 * mm
contact_y = draw_paragraph("Chennai, Tamil Nadu, India", styles["ResumeContact"], right_x, contact_y, right_w, 0.45 * mm)
contact_y = draw_paragraph("+91 78451 22655  |  jmohith2912@gmail.com", styles["ResumeContact"], right_x, contact_y, right_w, 0.45 * mm)
contact_y = draw_paragraph('<link href="https://github.com/Mohith2912" color="#554C51">github.com/Mohith2912</link>', styles["ResumeContact"], right_x, contact_y, right_w, 0.45 * mm)
draw_paragraph('<link href="https://www.linkedin.com/in/mohith-dharshan-994357381/" color="#554C51">linkedin.com/in/mohith-dharshan-994357381</link>', styles["ResumeContact"], right_x, contact_y, right_w)

pdf.setStrokeColor(LINE)
pdf.line(right_x - 3 * mm, 20 * mm, right_x - 3 * mm, content_top + 3 * mm)

# Left column
y_left = content_top
y_left = draw_section("Profile", left_x, y_left, left_w)
y_left = draw_paragraph(
    "B.E. Computer Science and Engineering student building production-minded full-stack products, AI workflows, and computer-vision systems. Hackathon experience across healthcare and logistics, with a focus on clear architecture, dependable workflows, and practical delivery.",
    styles["Body"], left_x, y_left, left_w,
)
y_left = draw_section("Experience", left_x, y_left, left_w)
y_left = draw_experience(
    "Backend Developer & AI Trainer", "Codeathon Hackathon", "Feb 2026",
    [
        "Built Node.js REST APIs and workflow services for structured data exchange.",
        "Integrated Firebase Realtime Database for synchronized application state.",
        "Contributed to a Random Forest classification workflow, testing, and debugging.",
    ], left_x, y_left, left_w,
)
y_left = draw_experience(
    "Frontend Developer", "UniHealth - CMR Hackfest 3.0", "Jan 2026",
    [
        "Built responsive React interfaces for hospital and pharmacy workflows.",
        "Integrated authentication and real-time Firebase data with backend coordination.",
        "Improved usability, tested critical flows, and supported the product demonstration.",
    ], left_x, y_left, left_w,
)
y_left = draw_section("Selected Projects", left_x, y_left, left_w)
project_rows = [
    ("Beyond Syllabus", "Next.js  |  TypeScript  |  Prisma  |  MySQL", "Interactive engineering learning platform with structured notes, visual modules, practice modes, podcasts, authentication, and AI-assisted study tools."),
    ("Urban Furniture OS", "Next.js  |  Flask  |  PostgreSQL  |  GST", "Furniture business operating system connecting inventory, purchasing, sales, GST invoices, payments, double-entry accounting, and reports."),
    ("PeoplePay360", "Next.js  |  Prisma  |  MySQL  |  RBAC", "Role-aware HR and payroll platform that turns contracts, schedules, attendance, leave, and salary rules into auditable payslips."),
    ("EXtendQuality", "OpenCV  |  YOLOv11  |  VLM  |  Next.js", "Confidence-aware industrial inspection concept combining deterministic defect detection, selective VLM review, recommendations, history, and quality KPIs."),
    ("UniHealth", "React  |  Node.js  |  MySQL  |  Security", "Hospital operations workspace for doctors, beds, wards, patient queues, analytics, recovery, and server-generated audit history."),
    ("FairDispatch", "Express  |  JavaScript  |  Firebase  |  Random Forest", "Delivery-dispatch prototype exploring workload-aware assignment, live fleet visibility, stop progress, ETA estimates, disputes, and support workflows."),
]
for row in project_rows:
    y_left = draw_project(*row, left_x, y_left, left_w)

# Right column
y_right = content_top
y_right = draw_section("Education", right_x, y_right, right_w)
y_right = draw_paragraph("B.E. Computer Science and Engineering", styles["ItemTitle"], right_x, y_right, right_w, 0.5 * mm)
y_right = draw_paragraph("SRM Easwari Engineering College", styles["BodyTight"], right_x, y_right, right_w, 0.5 * mm)
y_right = draw_paragraph("2025 - 2029", styles["Meta"], right_x, y_right, right_w, 0.6 * mm)
y_right = draw_paragraph("Semester 1: 8.53 / 10<br/>Semester 2: 9.16 / 10<br/><b>First-year average: 8.85 / 10</b>", styles["BodyTight"], right_x, y_right, right_w)
y_right = draw_section("Technical Skills", right_x, y_right, right_w)
skill_rows = [
    ("Languages", "Java, JavaScript, TypeScript, Python, C++"),
    ("Frontend", "React, Next.js, HTML, CSS, responsive UI"),
    ("Backend", "Node.js, Express, Flask, REST APIs, Prisma"),
    ("Data", "MySQL, PostgreSQL, Firebase, SQLite"),
    ("AI / Computer Vision", "OpenCV, YOLOv11, VLM workflows, classification"),
    ("Tools", "Git, GitHub, testing, debugging, Figma"),
]
for row in skill_rows:
    y_right = draw_skill(*row, right_x, y_right, right_w)
y_right = draw_section("Core Strengths", right_x, y_right, right_w)
y_right = draw_bullets([
    "System and API design",
    "Rapid product prototyping",
    "Problem solving and OOP",
    "Cross-functional teamwork",
    "Technical demonstrations",
], right_x, y_right, right_w)
y_right = draw_section("Additional Work", right_x, y_right, right_w)
y_right = draw_paragraph("VOE Web, student finance tools, drowsiness detection, QR scanning, and Java/C++ problem-solving repositories.", styles["BodyTight"], right_x, y_right, right_w)
y_right = draw_section("Languages", right_x, y_right, right_w)
y_right = draw_paragraph("English - Fluent<br/>Tamil - Fluent", styles["BodyTight"], right_x, y_right, right_w)

minimum_y = 18 * mm
if y_left < minimum_y or y_right < minimum_y:
    raise RuntimeError(f"Resume content overflow: left={y_left:.1f}, right={y_right:.1f}")

pdf.showPage()
pdf.save()
copy2(FINAL_PDF, SITE_PDF)
print(FINAL_PDF)
print(SITE_PDF)
print(f"column_bottoms left={y_left:.1f} right={y_right:.1f}")
