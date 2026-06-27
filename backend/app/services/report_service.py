"""
backend/app/services/report_service.py
PDF report generation using ReportLab.
Generates a comprehensive analysis report for a resume.
"""
import os
import tempfile
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Color palette
PURPLE = colors.HexColor("#7C3AED")
DARK_BG = colors.HexColor("#1E1B4B")
LIGHT_BG = colors.HexColor("#F5F3FF")
ACCENT = colors.HexColor("#10B981")
DANGER = colors.HexColor("#EF4444")
TEXT = colors.HexColor("#1F2937")
GRAY = colors.HexColor("#6B7280")
WHITE = colors.white


def _score_color(score: float) -> colors.Color:
    if score >= 75:
        return ACCENT
    elif score >= 50:
        return colors.HexColor("#F59E0B")
    else:
        return DANGER


def generate_pdf_report(resume: dict, analysis: dict, career_pred: dict = None) -> str:
    """Generate a PDF analysis report and return its file path."""
    tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()

    doc = SimpleDocTemplate(
        tmp_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "NexoraTitle",
        fontSize=26,
        fontName="Helvetica-Bold",
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "NexoraSubtitle",
        fontSize=11,
        fontName="Helvetica",
        textColor=colors.HexColor("#DDD6FE"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    section_title_style = ParagraphStyle(
        "SectionTitle",
        fontSize=14,
        fontName="Helvetica-Bold",
        textColor=PURPLE,
        spaceBefore=16,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "Body",
        fontSize=10,
        fontName="Helvetica",
        textColor=TEXT,
        spaceAfter=4,
        leading=14,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        fontSize=10,
        fontName="Helvetica",
        textColor=TEXT,
        leftIndent=12,
        spaceAfter=3,
        leading=14,
    )

    story = []

    # ── Header ─────────────────────────────────────────────────────────────────
    header_data = [
        [Paragraph("NEXORA AI", title_style)],
        [Paragraph("Resume Analysis Report", subtitle_style)],
        [Paragraph(f"Generated: {datetime.utcnow().strftime('%B %d, %Y')}", subtitle_style)],
    ]
    header_table = Table(header_data, colWidths=[17 * cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 16))

    # ── Candidate Info ─────────────────────────────────────────────────────────
    parsed = resume.get("parsed_data", {}) or {}
    name = parsed.get("name") or "Unknown Candidate"
    email = parsed.get("email") or "-"
    phone = parsed.get("phone") or "-"
    original = resume.get("original_name", "-")

    story.append(Paragraph("Candidate Overview", section_title_style))
    info_data = [
        ["Name", name, "File", original],
        ["Email", email, "Phone", phone],
        ["Skills Detected", str(len(parsed.get("skills", []))),
         "Experience Entries", str(len(parsed.get("experience", [])))],
        ["Projects", str(len(parsed.get("projects", []))),
         "Certifications", str(len(parsed.get("certifications", [])))],
    ]
    info_table = Table(info_data, colWidths=[4 * cm, 6 * cm, 4 * cm, 6 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("BACKGROUND", (2, 0), (2, -1), LIGHT_BG),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))

    # ── Score Overview ─────────────────────────────────────────────────────────
    overall = analysis.get("overall_score", 0)
    story.append(Paragraph("ATS Score Overview", section_title_style))

    overall_data = [[
        Paragraph(f"<b>Overall Score</b>", ParagraphStyle("ov", fontSize=12, fontName="Helvetica-Bold", textColor=WHITE)),
        Paragraph(f"<b>{overall}%</b>", ParagraphStyle("ovs", fontSize=22, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_RIGHT)),
    ]]
    overall_table = Table(overall_data, colWidths=[12 * cm, 5 * cm])
    overall_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), _score_color(overall)),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(overall_table)
    story.append(Spacer(1, 8))

    # Score breakdown table
    score_items = [
        ("ATS Compatibility", analysis.get("ats_score", 0)),
        ("Formatting Quality", analysis.get("formatting_score", 0)),
        ("Keyword Optimization", analysis.get("keyword_score", 0)),
        ("Experience Quality", analysis.get("experience_score", 0)),
        ("Education", analysis.get("education_score", 0)),
        ("Projects Portfolio", analysis.get("projects_score", 0)),
    ]
    score_data = [["Category", "Score", "Rating"]]
    for cat, score in score_items:
        rating = "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair" if score >= 40 else "Needs Work"
        score_data.append([cat, f"{score}%", rating])

    score_table = Table(score_data, colWidths=[8 * cm, 4 * cm, 5 * cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), TEXT),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 12))

    # ── Suggestions ────────────────────────────────────────────────────────────
    suggestions = analysis.get("suggestions", [])
    if suggestions:
        story.append(Paragraph("Improvement Suggestions", section_title_style))
        for i, s in enumerate(suggestions[:10], 1):
            story.append(Paragraph(f"<b>{i}.</b> {s}", bullet_style))
        story.append(Spacer(1, 8))

    # ── Career Prediction ──────────────────────────────────────────────────────
    if career_pred:
        story.append(Paragraph("Career Prediction", section_title_style))
        pred_career = career_pred.get("predicted_career", "-")
        confidence = career_pred.get("confidence", 0)
        story.append(Paragraph(
            f"Predicted Career: <b>{pred_career}</b> ({confidence:.1f}% confidence)",
            body_style
        ))

        top_careers = career_pred.get("top_careers", [])
        if top_careers:
            career_data = [["Career Path", "Match Probability"]]
            for c in top_careers[:5]:
                career_data.append([c["career"], f"{c['probability']:.1f}%"])

            career_table = Table(career_data, colWidths=[12 * cm, 5 * cm])
            career_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 1), (-1, -1), TEXT),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ]))
            story.append(career_table)

    # ── Skills ─────────────────────────────────────────────────────────────────
    skills = parsed.get("skills", [])
    if skills:
        story.append(Paragraph("Detected Skills", section_title_style))
        skills_text = " • ".join(skills[:30])
        story.append(Paragraph(skills_text, body_style))

    # ── Footer ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Generated by Nexora AI — AI Resume Analyzer & Career Roadmap | nexora.ai",
        ParagraphStyle("footer", fontSize=8, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    return tmp_path
