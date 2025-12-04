from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from typing import Dict, Any


def generate_prediction_report(
    prediction_data: Dict[str, Any], patient_data: Dict[str, Any]
) -> BytesIO:
    """
    Generate a comprehensive PDF report for diabetes risk prediction

    Args:
        prediction_data: Dictionary containing prediction details (all 29 fields + results)
        patient_data: Dictionary containing patient personal information

    Returns:
        BytesIO: PDF file as bytes stream
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, title="Diabetes Risk Assessment Report"
    )

    # Container for PDF elements
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#2563eb"),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=colors.HexColor("#1e40af"),
        spaceAfter=12,
        spaceBefore=20,
        fontName="Helvetica-Bold",
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=12,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=8,
        fontName="Helvetica-Bold",
    )

    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("🩺 DIABETES RISK ASSESSMENT REPORT", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Report Information
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"<b>Report Generated:</b> {report_date}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # === PATIENT INFORMATION ===
    elements.append(Paragraph("Patient Information", heading_style))

    patient_info = [
        ["Patient Code:", patient_data.get("patient_code", "N/A")],
        ["Date of Birth:", patient_data.get("date_of_birth", "N/A")],
        ["Phone:", patient_data.get("phone", "N/A")],
        ["Address:", patient_data.get("address", "N/A")],
        ["Emergency Contact:", patient_data.get("emergency_contact", "N/A")],
    ]

    patient_table = Table(patient_info, colWidths=[2 * inch, 4 * inch])
    patient_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3 * inch))

    # === PREDICTION RESULTS ===
    elements.append(Paragraph("Prediction Results", heading_style))

    risk_prob = prediction_data.get("risk_probability", 0)
    risk_level = prediction_data.get("risk_level", "Unknown")
    risk_interpretation = prediction_data.get("risk_interpretation", "")

    # Risk level colorColors
    risk_color = (
        colors.HexColor("#10b981")
        if risk_level == "Low"
        else (
            colors.HexColor("#f59e0b")
            if risk_level == "Medium"
            else colors.HexColor("#ef4444")
        )
    )

    results_data = [
        ["Risk Probability:", f"{risk_prob:.1f}%"],
        ["Risk Level:", risk_level],
        ["Assessment:", risk_interpretation],
    ]

    results_table = Table(results_data, colWidths=[2 * inch, 4 * inch])
    results_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
                ("BACKGROUND", (1, 1), (1, 1), risk_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (1, 1), (1, 1), colors.white),
                ("TEXTCOLOR", (0, 2), (-1, 2), colors.black),
                ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
                ("FONTNAME", (1, 1), (1, 1), "Helvetica-Bold"),
                ("FONTNAME", (1, 2), (1, 2), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(results_table)
    elements.append(Spacer(1, 0.3 * inch))

    # === DIAGNOSTIC DATA ===
    elements.append(Paragraph("Diagnostic Data", heading_style))

    # Demographics
    elements.append(Paragraph("Demographics", subheading_style))
    demo_data = [
        ["Age:", f"{prediction_data.get('age', 'N/A')} years"],
        ["Gender:", prediction_data.get("gender", "N/A")],
        ["Ethnicity:", prediction_data.get("ethnicity", "N/A")],
        ["Education:", prediction_data.get("education_level", "N/A")],
        ["Income Level:", prediction_data.get("income_level", "N/A")],
        ["Employment:", prediction_data.get("employment_status", "N/A")],
    ]
    demo_table = Table(demo_data, colWidths=[2.5 * inch, 3.5 * inch])
    demo_table.setStyle(_get_table_style())
    elements.append(demo_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Physical Measurements
    elements.append(Paragraph("Physical Measurements", subheading_style))
    physical_data = [
        ["BMI:", f"{float(prediction_data.get('bmi', 0)):.1f}"],
        [
            "Waist-Hip Ratio:",
            f"{float(prediction_data.get('waist_to_hip_ratio', 0)):.2f}",
        ],
        ["Heart Rate:", f"{prediction_data.get('heart_rate', 'N/A')} bpm"],
        ["Systolic BP:", f"{prediction_data.get('systolic_bp', 'N/A')} mmHg"],
        ["Diastolic BP:", f"{prediction_data.get('diastolic_bp', 'N/A')} mmHg"],
    ]
    physical_table = Table(physical_data, colWidths=[2.5 * inch, 3.5 * inch])
    physical_table.setStyle(_get_table_style())
    elements.append(physical_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Lab Results
    elements.append(Paragraph("Laboratory Results", subheading_style))
    lab_data = [
        [
            "Fasting Glucose:",
            f"{float(prediction_data.get('glucose_fasting', 0)):.1f} mg/dL",
        ],
        [
            "Postprandial Glucose:",
            f"{float(prediction_data.get('glucose_postprandial', 0)):.1f} mg/dL",
        ],
        ["HbA1c:", f"{float(prediction_data.get('hba1c', 0)):.1f}%"],
        [
            "Insulin Level:",
            f"{float(prediction_data.get('insulin_level', 0)):.1f} μU/mL",
        ],
        [
            "Total Cholesterol:",
            f"{float(prediction_data.get('cholesterol_total', 0)):.1f} mg/dL",
        ],
        [
            "HDL Cholesterol:",
            f"{float(prediction_data.get('hdl_cholesterol', 0)):.1f} mg/dL",
        ],
        [
            "LDL Cholesterol:",
            f"{float(prediction_data.get('ldl_cholesterol', 0)):.1f} mg/dL",
        ],
        [
            "Triglycerides:",
            f"{float(prediction_data.get('triglycerides', 0)):.1f} mg/dL",
        ],
    ]
    lab_table = Table(lab_data, colWidths=[2.5 * inch, 3.5 * inch])
    lab_table.setStyle(_get_table_style())
    elements.append(lab_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Lifestyle Factors
    elements.append(Paragraph("Lifestyle Factors", subheading_style))
    lifestyle_data = [
        ["Smoking Status:", prediction_data.get("smoking_status", "N/A")],
        [
            "Alcohol (drinks/week):",
            f"{float(prediction_data.get('alcohol_consumption_per_week', 0)):.1f}",
        ],
        [
            "Physical Activity:",
            f"{prediction_data.get('physical_activity_minutes_per_week', 'N/A')} min/week",
        ],
        ["Diet Score:", f"{float(prediction_data.get('diet_score', 0)):.1f}/10"],
        [
            "Sleep (hours/day):",
            f"{float(prediction_data.get('sleep_hours_per_day', 0)):.1f}",
        ],
        [
            "Screen Time (hours/day):",
            f"{float(prediction_data.get('screen_time_hours_per_day', 0)):.1f}",
        ],
    ]
    lifestyle_table = Table(lifestyle_data, colWidths=[2.5 * inch, 3.5 * inch])
    lifestyle_table.setStyle(_get_table_style())
    elements.append(lifestyle_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Medical History
    elements.append(Paragraph("Medical History", subheading_style))
    medical_data = [
        [
            "Family History of Diabetes:",
            "Yes" if prediction_data.get("family_history_diabetes") else "No",
        ],
        [
            "History of Hypertension:",
            "Yes" if prediction_data.get("hypertension_history") else "No",
        ],
        [
            "Cardiovascular History:",
            "Yes" if prediction_data.get("cardiovascular_history") else "No",
        ],
    ]
    medical_table = Table(medical_data, colWidths=[2.5 * inch, 3.5 * inch])
    medical_table.setStyle(_get_table_style())
    elements.append(medical_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
    )
    elements.append(
        Paragraph("—————————————————————————————————————————", footer_style)
    )
    elements.append(
        Paragraph(
            "This report was generated by an AI-powered diabetes risk assessment system.",
            footer_style,
        )
    )
    elements.append(
        Paragraph(
            "Please consult with a qualified healthcare professional for medical advice.",
            footer_style,
        )
    )
    elements.append(
        Paragraph(
            f"Report ID: PRED-{prediction_data.get('id', 'UNKNOWN')}", footer_style
        )
    )

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def _get_table_style():
    """Helper function to return consistent table styling"""
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f9fafb")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (0, -1), "RIGHT"),
            ("ALIGN", (1, 0), (1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )
