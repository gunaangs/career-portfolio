#!/usr/bin/env python3
"""
Generate a professional, high-impact PDF resume for Gunaseelan N.
Positioned for top roles: Lead Applied GenAI Engineer / Staff Agentic AI Architect.
Finetuned with:
- Target Role: Lead Applied GenAI Engineer | Technical Lead & Enterprise Agentic AI Architect
- Core product: GalaxyONE (Applied GenAI, multi-tier UI JSON generation via agentic workflows)
- Token & Cost Effective Prompt/Skill Engineering (prompt caching, dynamic context budgeting, structured schemas)
- Guardrails & Evaluation for deterministic output quality (Pydantic / JSON schema validators, self-healing reflection loops)
- AI xChange (OCR to Multimodal GenAI migration)
- Enterprise Platform Architecture (Job Scheduler, Sovablu Drive) & Prior MDM + ERP leadership
- PDF document metadata for ATS
- Interactive hyperlinks in PDF header & project cards
- Location: Chennai, India
- Clean, exact 2-page layout
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        text = f"Gunaseelan N — Resume | Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 34, 18, text)
        self.restoreState()

def build_pdf(filename="Gunaseelan_N_Senior_Software_Engineer_Resume.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=32,
        bottomMargin=32,
        title="Gunaseelan N - Lead Applied GenAI Engineer Resume",
        author="Gunaseelan N",
        subject="Lead Applied GenAI Engineer Resume - Agentic Workflows, Multi-Tier UI JSON Generation, Enterprise Platforms",
        keywords="Lead Applied GenAI Engineer, Staff Agentic AI Architect, Technical Lead, GalaxyONE, Agentic Workflows, Multi-Tier UI JSON Generation, LLM Guardrails, Token Cost Optimization, Java, Spring Boot, React Native, Apple MDM"
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0f172a")
    c_accent = colors.HexColor("#1d4ed8")
    c_dark = colors.HexColor("#1e293b")
    c_muted = colors.HexColor("#475569")
    c_light = colors.HexColor("#64748b")
    c_line = colors.HexColor("#cbd5e1")

    name_style = ParagraphStyle(
        'DocName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        textColor=c_primary
    )

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_accent
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_muted
    )

    section_heading = ParagraphStyle(
        'DocSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_primary,
        spaceAfter=1.5,
        textTransform='uppercase'
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=11.3,
        textColor=c_dark
    )

    skill_label_style = ParagraphStyle(
        'DocSkillLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=c_primary
    )

    skill_val_style = ParagraphStyle(
        'DocSkillVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_muted
    )

    role_title_style = ParagraphStyle(
        'DocRoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=11.2,
        textColor=c_primary
    )

    role_meta_style = ParagraphStyle(
        'DocRoleMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_light,
        alignment=2
    )

    role_sub_style = ParagraphStyle(
        'DocRoleSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.6,
        leading=9.8,
        textColor=c_muted
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=c_dark,
        leftIndent=9,
        firstLineIndent=-9,
        spaceAfter=1.8
    )

    card_title_style = ParagraphStyle(
        'DocCardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_primary
    )

    card_desc_style = ParagraphStyle(
        'DocCardDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_muted
    )

    card_link_style = ParagraphStyle(
        'DocCardLink',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_accent
    )

    story = []

    # 1. HEADER WITH INTERACTIVE HYPERLINKS
    header_table_data = [
        [
            Paragraph("GUNASEELAN N", name_style),
            Paragraph("<b>Location:</b> Chennai, India<br/><b>Phone:</b> <a href='tel:+918903857336'><font color='#1d4ed8'>+91 89038 57336</font></a>", contact_style)
        ],
        [
            Paragraph("Lead Applied GenAI Engineer | Technical Lead & Enterprise Agentic AI Architect", title_style),
            Paragraph("<b>Email:</b> <a href='mailto:nguna.mdi@gmail.com'><font color='#1d4ed8'>nguna.mdi@gmail.com</font></a><br/><b>Portfolio:</b> <a href='https://gunaangs.github.io'><font color='#1d4ed8'>gunaangs.github.io</font></a>", contact_style)
        ]
    ]
    header_table = Table(header_table_data, colWidths=[364, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=5))

    def add_section_header(title):
        return [
            Paragraph(f"<b>{title}</b>", section_heading),
            HRFlowable(width="100%", thickness=0.75, color=c_line, spaceBefore=1, spaceAfter=3.5)
        ]

    # 2. EXECUTIVE SUMMARY
    story.extend(add_section_header("Executive Summary"))
    summary_p = Paragraph(
        "<b>Lead Applied GenAI Engineer & Technical Architect with 11+ years of end-to-end engineering excellence</b>, "
        "specializing in Agentic AI systems, LLM orchestration, enterprise platforms, and scalable microservices. "
        "Key architect behind <b>GalaxyONE</b>, an autonomous multi-agent engine generating <b>multi-tier UI JSON and enterprise application code</b> "
        "from natural language prompts via specialized agentic workflows. Proven track record designing <b>token- and cost-effective skills/tools</b>, "
        "rigorous output quality guardrails (grammar-constrained decoding & self-correcting validation loops), and migrating legacy OCR to multimodal GenAI pipelines. "
        "Experienced team leader directing 10+ engineers across system design, security protocols (Apple MDM / Android Management), and high-reliability cloud platforms.",
        body_style
    )
    story.append(summary_p)
    story.append(Spacer(1, 5))

    # 3. CORE TECHNICAL COMPETENCIES
    story.extend(add_section_header("Core Competencies & Technical Stack"))
    skills_data = [
        [Paragraph("Applied GenAI & Agents:", skill_label_style), Paragraph("Agentic Workflows (ReAct, Supervisor/Multi-Agent), GalaxyONE AI Engine, Multi-Tier UI JSON Generation, Custom Agentic Tools, Function Calling, Prompt Engineering & Optimization", skill_val_style)],
        [Paragraph("LLM Ops & Guardrails:", skill_label_style), Paragraph("Token & Cost Optimization (Prompt Caching, Context Pruning), Structured Output Enforcement, Hallucination Guardrails, Self-Healing Code Reflection, Multimodal APIs, OCR to GenAI", skill_val_style)],
        [Paragraph("Enterprise Platform Core:", skill_label_style), Paragraph("Sovablu No-Code Platform Core, Distributed Job Schedulers, Sovablu Drive Architecture, Chunked Multipart File Streaming, Dynamic Configuration Engines", skill_val_style)],
        [Paragraph("Backend & Protocols:", skill_label_style), Paragraph("Java (Core & Advanced), Spring Boot, Microservices, RESTful APIs, Apple MDM Protocol, Android Management API, Kiosk & Lockdown Engines, Mutual TLS", skill_val_style)],
        [Paragraph("Frontend & Mobile:", skill_label_style), Paragraph("React.js, React Native, Android SDK (Java/XML), TypeScript, JavaScript (ES6+), Redux Toolkit, Tailwind CSS, Material 3 Design", skill_val_style)],
        [Paragraph("Data & DevOps:", skill_label_style), Paragraph("MySQL, SQLite, Firebase, Query Optimization, Database Schema Design, Git, Maven, Gradle, Jenkins, Docker, CI/CD Pipelines, JUnit", skill_val_style)],
    ]
    skills_table = Table(skills_data, colWidths=[120, 424])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 5))

    # 4. PROFESSIONAL EXPERIENCE
    story.extend(add_section_header("Professional Experience"))

    # Role 1: Vaken - Sovablu / GalaxyONE
    r1_header = [
        [
            Paragraph("<b>Lead Applied GenAI Engineer & Team Leader</b> | <font color='#1d4ed8'><b>Vaken Technologies Pvt. Ltd.</b></font>", role_title_style),
            Paragraph("May 2022 – Present", role_meta_style)
        ]
    ]
    t_r1 = Table(r1_header, colWidths=[404, 140])
    t_r1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r1)
    story.append(Paragraph("GalaxyONE Autonomous Agentic Engine & Sovablu Enterprise Platform Core", role_sub_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>GalaxyONE Multi-Agent Engine & Multi-Tier UI JSON:</b> Architected the core prompt orchestration and agentic workflows inside <b>GalaxyONE</b>, enabling specialized domain copilots (Layout, Logic, Data) to decompose natural language prompts and synthesize valid, multi-tier UI JSON schemas and full-stack application structures directly consumable by visual designers.", bullet_style))
    story.append(Paragraph("• <b>Cost- & Token-Effective Skill Engineering:</b> Authored modular agentic tools and specialized skills optimized for minimal token consumption via prompt caching, schema pruning, and dynamic context budgeting, slashing average LLM inference costs and latency while boosting complex prompt completion rates.", bullet_style))
    story.append(Paragraph("• <b>Deterministic Guardrails & Output Quality:</b> Built multi-stage verification guardrails and self-healing reflection loops that enforce strict JSON schema compliance, eliminate hallucinated component types, and automatically repair invalid syntax before committing to the visual designer.", bullet_style))
    story.append(Paragraph("• <b>AI xChange (OCR to GenAI Migration):</b> Spearheaded the overhaul of <b>AI xChange</b> document processing, replacing brittle OCR regex pipelines with multimodal LLM APIs; drastically elevated structured extraction accuracy across diverse, complex invoice and receipt formats.", bullet_style))
    story.append(Paragraph("• <b>Sovablu Drive & Distributed Scheduler:</b> Architected <b>Sovablu Drive</b> (enterprise document and asset repository with chunked streaming and validation) and designed high-reliability enterprise Job Scheduler screens and execution backends for recurring background automation.", bullet_style))
    story.append(Spacer(1, 4))

    # Role 2: Vaken - iOS MDM
    r2_header = [
        [
            Paragraph("<b>Software Engineer — Team Leader (iOS MDM Engine)</b> | <font color='#1d4ed8'><b>Vaken Technologies Pvt. Ltd.</b></font>", role_title_style),
            Paragraph("Oct 2020 – May 2022", role_meta_style)
        ]
    ]
    t_r2 = Table(r2_header, colWidths=[404, 140])
    t_r2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r2)
    story.append(Paragraph("iOS Mobile Device Management (MDM) Engine & Concurrency Backend Architecture", role_sub_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Architecture & Protocol Delivery:</b> Architected high-throughput REST APIs for the enterprise iOS MDM Engine using Java and MySQL, strictly implementing Apple MDM Protocol specifications for device enrollment, remote command execution, and configuration profiles.", bullet_style))
    story.append(Paragraph("• <b>Engineering Leadership:</b> Directed and mentored a squad of 10 backend engineers, driving sprint planning, requirement breakdowns, high/low-level design documentation, and peer code reviews with 99%+ sprint milestone adherence.", bullet_style))
    story.append(Paragraph("• <b>Performance Optimization:</b> Refactored mission-critical database schemas and tuned indexing on core device status tables, reducing API response latency and supporting seamless multi-tenant operations.", bullet_style))

    # CLEAN PAGE BREAK: Page 1 ends cleanly after iOS MDM role
    story.append(PageBreak())

    # --- PAGE 2 ---
    story.extend(add_section_header("Professional Experience (Continued)"))

    # Role 3: Works Applications India - Android MDM
    r3_header = [
        [
            Paragraph("<b>Software Engineer (Android MDM & Full-Stack Portal)</b> | <font color='#1d4ed8'><b>Works Applications (India) Pvt. Ltd.</b></font> <font color='#64748b' size='7'>(formerly IVTL Infoview)</font>", role_title_style),
            Paragraph("Sep 2019 – Jul 2020", role_meta_style)
        ]
    ]
    t_r3 = Table(r3_header, colWidths=[404, 140])
    t_r3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r3)
    story.append(Paragraph("Custom Android MDM Kiosk Launcher & Web Administrative Console", role_sub_style))
    story.append(Spacer(1, 2.5))
    story.append(Paragraph("• <b>Autonomous Kiosk Launcher Execution:</b> Independently designed, built, and delivered an Android MDM Custom Launcher application within strict timelines, consuming MDM policy endpoints to enforce granular hardware restrictions and kiosk lock-down.", bullet_style))
    story.append(Paragraph("• <b>Full-Stack Administrative Portal:</b> Engineered a full-stack portal using React.js and Java backend to remotely configure, monitor, and enforce Google Android Management API policies across enterprise device fleets.", bullet_style))
    story.append(Spacer(1, 5))

    # Role 4: Works Applications India - ERP
    r4_header = [
        [
            Paragraph("<b>Junior Software Engineer (ERP Solutions)</b> | <font color='#1d4ed8'><b>Works Applications (India) Pvt. Ltd.</b></font> <font color='#64748b' size='7'>(formerly IVTL Infoview)</font>", role_title_style),
            Paragraph("Apr 2017 – Sep 2019", role_meta_style)
        ]
    ]
    t_r4 = Table(r4_header, colWidths=[404, 140])
    t_r4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r4)
    story.append(Paragraph("Enterprise ERP Suites with AI & Automated Accounting Features for Japanese Market", role_sub_style))
    story.append(Spacer(1, 2.5))
    story.append(Paragraph("• <b>Enterprise Feature Engineering:</b> Developed core transactional accounting and supply chain modules with automated validation rules and business intelligence dashboards for top-tier Japanese enterprises.", bullet_style))
    story.append(Paragraph("• <b>Team Enablement & Mentorship:</b> Guided junior developers on design patterns and module consolidation, standardizing code quality across cross-functional product squads.", bullet_style))
    story.append(Spacer(1, 5))

    # Role 5: Works Applications India - Trainee
    r5_header = [
        [
            Paragraph("<b>Trainee Engineer (Legacy Modernization)</b> | <font color='#1d4ed8'><b>Works Applications (India) Pvt. Ltd.</b></font> <font color='#64748b' size='7'>(formerly IVTL Infoview)</font>", role_title_style),
            Paragraph("Jul 2015 – Mar 2017", role_meta_style)
        ]
    ]
    t_r5 = Table(r5_header, colWidths=[404, 140])
    t_r5.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r5)
    story.append(Paragraph("Desktop Delphi to High-Availability Cloud Web Platform Migration", role_sub_style))
    story.append(Spacer(1, 2.5))
    story.append(Paragraph("• <b>Legacy Modernization:</b> Re-engineered legacy desktop Delphi HR & Payroll software into modern Java web applications, implementing high-precision payroll compliance calculation engines.", bullet_style))
    story.append(Spacer(1, 7))

    # 5. PUBLISHED APPLICATIONS & PRODUCTS
    story.extend(add_section_header("Published Mobile Applications & Independent Products (Angs Corp)"))

    p_secure_notes = [
        Paragraph("<b>Secure Notes</b> <font color='#1d4ed8' size='7.2'>[React Native | Security]</font>", card_title_style),
        Paragraph("Production-grade offline notes app with AES-256 local encryption, biometric lock, dynamic Material 3 theming, and zero network transmission.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/details?id=com.angs.securenotes'><font color='#1d4ed8'><u>Google Play: com.angs.securenotes</u></font></a>", card_link_style)
    ]

    p_moneywise = [
        Paragraph("<b>MoneyWise</b> <font color='#1d4ed8' size='7.2'>[React Native | FinTech]</font>", card_title_style),
        Paragraph("Comprehensive personal finance tracker with multi-account ledgers, interactive budget analytics, multi-currency support, and offline-first SQLite sync.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#1d4ed8'><u>Google Play: Angs Corp Portfolio</u></font></a>", card_link_style)
    ]

    p_appshield = [
        Paragraph("<b>AppShield</b> <font color='#1d4ed8' size='7.2'>[React Native | Privacy]</font>", card_title_style),
        Paragraph("Privacy & permission auditor inspecting third-party apps, background sensor/network access, and system security posture in real time.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#1d4ed8'><u>Google Play: Angs Corp Portfolio</u></font></a>", card_link_style)
    ]

    p_pixelsqueeze = [
        Paragraph("<b>PixelSqueeze</b> <font color='#1d4ed8' size='7.2'>[React Native | Media Utility]</font>", card_title_style),
        Paragraph("High-speed on-device image compression and format converter leveraging native bridge modules for hardware-accelerated processing.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#1d4ed8'><u>Google Play: Angs Corp Portfolio</u></font></a>", card_link_style)
    ]

    col1 = [
        Table([[p] for p in p_secure_notes], colWidths=[266]),
        Spacer(1, 3.5),
        Table([[p] for p in p_appshield], colWidths=[266])
    ]

    col2 = [
        Table([[p] for p in p_moneywise], colWidths=[266]),
        Spacer(1, 3.5),
        Table([[p] for p in p_pixelsqueeze], colWidths=[266])
    ]

    projects_table = Table([[col1, col2]], colWidths=[270, 274])
    projects_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(projects_table)
    story.append(Spacer(1, 7))

    # 6. EDUCATION & HONORS
    story.extend(add_section_header("Education & Academic Distinction"))
    edu_table_data = [
        [
            Paragraph("<b>Bachelor of Technology (B.Tech) — Information Technology</b>", role_title_style),
            Paragraph("<b>CGPA: 8.96 / 10</b> | 2011 – 2015", role_meta_style)
        ],
        [
            Paragraph("Adhiyamaan College of Engineering, Hosur (Anna University)", skill_val_style),
            Paragraph("", role_meta_style)
        ]
    ]
    t_edu = Table(edu_table_data, colWidths=[384, 160])
    t_edu.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_edu)
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "🏆 <b>State Level Winner: 'Student Innovator Award 2015' (ICTACT Tamil Nadu)</b><br/>"
        "Published research & system: <i>'Uzhavan Puthagam: Web Based System of Effective Farm Collaboration'</i> "
        "(ACCCAS-2015 Conference) in Computer Science & IT Applications.",
        bullet_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == '__main__':
    build_pdf()
