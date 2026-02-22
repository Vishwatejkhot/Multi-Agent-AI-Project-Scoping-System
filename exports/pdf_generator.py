from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
import os



def add_page_number(canvas_obj, doc):
    page_num = canvas_obj.getPageNumber()
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawRightString(7.8 * inch, 0.5 * inch, f"Page {page_num}")


def add_watermark(canvas_obj, doc, logo_path):
    if logo_path and os.path.exists(logo_path):
        canvas_obj.saveState()
        canvas_obj.setFillAlpha(0.05)
        canvas_obj.drawImage(
            logo_path,
            100,
            200,
            width=400,
            height=400,
            preserveAspectRatio=True,
            mask='auto'
        )
        canvas_obj.restoreState()


def generate_pdf(
    data,
    filename="project_scope.pdf",
    logo_path=None,
    company_name="Project Scoping Assistant",
    primary_color=colors.darkblue
):

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    section_style = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        textColor=primary_color,
        spaceAfter=10
    )

    normal_style = styles["Normal"]

    analysis = data.get("analysis", {})
    report = data.get("investor_report", {})

   
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch
        logo.drawWidth = 3 * inch
        logo.hAlign = "CENTER"
        elements.append(Spacer(1, 2 * inch))
        elements.append(logo)
        elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(company_name, styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("Startup Project Report", section_style))
    elements.append(PageBreak())

  
    elements.append(Paragraph("Executive Summary", section_style))
    elements.append(Paragraph(report.get("executive_summary", ""), normal_style))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("Problem Statement", section_style))
    elements.append(Paragraph(report.get("problem_statement", ""), normal_style))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("Solution Overview", section_style))
    elements.append(Paragraph(report.get("solution_overview", ""), normal_style))
    elements.append(PageBreak())

    elements.append(Paragraph("Project Overview", section_style))

    complexity = analysis.get("complexity", {})
    cost = analysis.get("estimated_cost", {})

    cost_currency = cost.get("display_currency", "USD")
    cost_low = cost.get("display_low", cost.get("low_usd", 0))
    cost_high = cost.get("display_high", cost.get("high_usd", 0))

    overview_data = [
        ["Idea", analysis.get("idea", "")],
        ["Complexity Level", complexity.get("level", "")],
        ["Complexity Score", complexity.get("score", "")],
        ["Timeline", analysis.get("timeline", "")],
        ["Estimated Cost", f"{cost_currency} {cost_low:,} - {cost_high:,}"],
    ]

    overview_table = Table(overview_data, colWidths=[2 * inch, 4 * inch])
    overview_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
    ]))

    elements.append(overview_table)
    elements.append(Spacer(1, 0.5 * inch))

   
    elements.append(Paragraph("Timeline Estimation", section_style))

    drawing = Drawing(400, 200)
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 125
    chart.width = 300

   
    timeline_map = {"Low": 2, "Medium": 4, "High": 8}
    timeline_value = timeline_map.get(complexity.get("level", "Medium"), 4)

    chart.data = [[timeline_value]]
    chart.categoryAxis.categoryNames = ["Development"]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 12
    chart.valueAxis.valueStep = 2

    drawing.add(chart)
    elements.append(drawing)
    elements.append(Spacer(1, 0.5 * inch))

  
    elements.append(Paragraph("Cost Breakdown", section_style))

    cost_drawing = Drawing(400, 200)
    cost_chart = VerticalBarChart()
    cost_chart.x = 50
    cost_chart.y = 50
    cost_chart.height = 125
    cost_chart.width = 300

    cost_chart.data = [[cost_low / 1000, cost_high / 1000]]
    cost_chart.categoryAxis.categoryNames = ["Min (K)", "Max (K)"]
    cost_chart.valueAxis.valueMin = 0
    cost_chart.valueAxis.valueMax = max(cost_high / 1000 * 1.2, 50)

    cost_drawing.add(cost_chart)
    elements.append(cost_drawing)
    elements.append(PageBreak())

    
    elements.append(Paragraph("Key Risks", section_style))
    risks = analysis.get("risks", {})

    elements.append(Paragraph("<b>Technical Risks</b>", normal_style))
    for risk in risks.get("technical_risks", []):
        elements.append(Paragraph(f"• {risk}", normal_style))

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Business Risks</b>", normal_style))
    for risk in risks.get("business_risks", []):
        elements.append(Paragraph(f"• {risk}", normal_style))

    elements.append(Spacer(1, 0.5 * inch))

    
    elements.append(Paragraph("Investor Readiness", section_style))
    readiness_score = report.get("investor_readiness_score", 0)

    score_style = ParagraphStyle(
        name="ScoreStyle",
        parent=styles["Heading1"],
        textColor=colors.green if readiness_score >= 7 else colors.red
    )

    elements.append(Paragraph(f"{readiness_score}/10", score_style))

    doc.build(
        elements,
        onFirstPage=lambda c, d: (add_page_number(c, d), add_watermark(c, d, logo_path)),
        onLaterPages=lambda c, d: (add_page_number(c, d), add_watermark(c, d, logo_path)),
    )