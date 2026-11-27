#!/usr/bin/env python3
"""
Generate a modern, high-end 2026 executive PDF resume for Gunaseelan N.
Features:
- Sleek modern layout: Executive deep navy accent header banner with glowing badges
- Clean typography hierarchy (Plus-Jakarta/Helvetica style)
- Skill chips / badge-styled category pills
- Elegant role cards with timeline dots & soft border accents
- Document metadata for ATS parsing
- Clickable vector links (Email, Phone, Portfolio, Google Play)
- Strictly balanced across exactly 2 pages
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

class ModernNumberedCanvas(canvas.Canvas):
    """Custom canvas that draws a subtle modern top accent bar and bottom running footer."""
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
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = letter

        # Sleek top gradient accent bar (Royal Blue to Slate)
        self.setFillColor(colors.HexColor("#2563eb"))
        self.rect(0, h - 5, w, 5, fill=1, stroke=0)

        # Bottom footer bar
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#0f172a"))
        self.drawString(34, 18, "GUNASEELAN N")

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(108, 18, "|  Lead Applied GenAI Engineer & Enterprise Architect")

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(w - 34, 18, page_str)

        # Subtle bottom line
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(34, 28, w - 34, 28)

        self.restoreState()

def build_pdf(filename="Gunaseelan_N_Senior_Software_Engineer_Resume.pdf"):
    # Letter size: 612 x 792 points
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=32,
        rightMargin=32,
        topMargin=26,
        bottomMargin=36,
        title="Gunaseelan N - Lead Applied GenAI Engineer Resume",
        author="Gunaseelan N",
        subject="Lead Applied GenAI Engineer Resume - Agentic Workflows, Multi-Tier UI JSON Generation, Enterprise Platforms",
        keywords="Lead Applied GenAI Engineer, Staff Agentic AI Architect, Technical Lead, GalaxyONE, Agentic Workflows, Multi-Tier UI JSON Generation, LLM Guardrails, Token Cost Optimization, Java, Spring Boot, React Native, Apple MDM"
    )

    styles = getSampleStyleSheet()

    # Modern 2026 Palette
    c_primary = colors.HexColor("#0f172a")     # Deep rich slate
    c_blue = colors.HexColor("#2563eb")        # Vivid tech blue
    c_blue_light = colors.HexColor("#eff6ff")  # Soft blue fill
    c_blue_border = colors.HexColor("#bfdbfe") # Border for chips
    c_dark = colors.HexColor("#1e293b")        # Text charcoal
    c_muted = colors.HexColor("#475569")       # Slate text
    c_light = colors.HexColor("#64748b")       # Light metadata
    c_card_bg = colors.HexColor("#f8fafc")     # Card background
    c_card_border = colors.HexColor("#e2e8f0") # Subtle card border

    # Typography Styles
    name_style = ParagraphStyle(
        'ModernName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=24,
        textColor=c_primary,
        spaceAfter=2
    )

    title_style = ParagraphStyle(
        'ModernTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_blue
    )

    contact_style = ParagraphStyle(
        'ModernContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_muted
    )

    section_heading = ParagraphStyle(
        'ModernSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_primary,
        spaceAfter=2,
        textTransform='uppercase'
    )

    summary_style = ParagraphStyle(
        'ModernSummary',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=11.6,
        textColor=c_dark
    )

    skill_label_style = ParagraphStyle(
        'ModernSkillLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=c_blue
    )

    skill_val_style = ParagraphStyle(
        'ModernSkillVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_muted
    )

    role_title_style = ParagraphStyle(
        'ModernRoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=c_primary
    )

    role_meta_style = ParagraphStyle(
        'ModernRoleMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=10.5,
        textColor=c_blue,
        alignment=2
    )

    role_sub_style = ParagraphStyle(
        'ModernRoleSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.6,
        leading=9.8,
        textColor=c_muted
    )

    bullet_style = ParagraphStyle(
        'ModernBullet',
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
        'ModernCardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_primary
    )

    card_desc_style = ParagraphStyle(
        'ModernCardDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.2,
        textColor=c_muted
    )

    card_link_style = ParagraphStyle(
        'ModernCardLink',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_blue
    )

    story = []

    # 1. MODERN HEADER HERO BLOCK
    header_left = [
        Paragraph("GUNASEELAN N", name_style),
        Paragraph("Lead Applied GenAI Engineer & Technical Architect", title_style),
    ]

    header_right = [
        Paragraph("📍 <b>Chennai, India</b>  &bull;  📞 <a href='tel:+918903857336'><font color='#2563eb'><b>+91 89038 57336</b></font></a>", contact_style),
        Paragraph("✉️ <a href='mailto:nguna.mdi@gmail.com'><font color='#2563eb'><b>nguna.mdi@gmail.com</b></font></a>  &bull;  🌐 <a href='https://gunaangs.github.io'><font color='#2563eb'><b>gunaangs.github.io</b></font></a>", contact_style),
        Paragraph("📱 Google Play Publisher: <a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#2563eb'><b>Angs Corp</b></font></a>", contact_style),
    ]

    hero_table = Table([[header_left, header_right]], colWidths=[338, 210])
    hero_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_card_border),
        ('LINEBEFORE', (1,0), (1,0), 0.5, c_card_border),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 6))

    def add_section_header(title):
        p = Paragraph(f"<b>{title}</b>", section_heading)
        line = HRFlowable(width="100%", thickness=1, color=c_blue, spaceBefore=2, spaceAfter=4)
        return [p, line]

    # 2. EXECUTIVE SUMMARY (Styled in modern callout box)
    story.extend(add_section_header("Executive Summary"))
    summary_text = (
        "<b>Lead Applied GenAI Engineer & Technical Architect with 11+ years of end-to-end engineering excellence</b>, "
        "specializing in Agentic AI systems, LLM orchestration, enterprise platforms, and scalable microservices. "
        "Key architect behind <b>GalaxyONE</b>, an autonomous multi-agent engine generating <b>multi-tier UI JSON and enterprise application code</b> "
        "from natural language prompts via specialized agentic workflows. Proven track record designing <b>token- and cost-effective skills/tools</b>, "
        "rigorous output quality guardrails (grammar-constrained decoding & self-correcting validation loops), and migrating legacy OCR to multimodal GenAI pipelines. "
        "Experienced team leader directing 10+ engineers across system design, security protocols (Apple MDM / Android Management), and high-reliability cloud platforms."
    )
    summary_table = Table([[Paragraph(summary_text, summary_style)]], colWidths=[548])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_blue_light),
        ('LINELEFT', (0,0), (-1,-1), 2.5, c_blue),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # 3. CORE TECHNICAL COMPETENCIES (Styled Grid with badges)
    story.extend(add_section_header("Core Competencies & Technical Stack"))
    skills_data = [
        [Paragraph("Applied GenAI & Agents", skill_label_style), Paragraph("Agentic Workflows (ReAct, Supervisor/Multi-Agent), GalaxyONE AI Engine, Multi-Tier UI JSON Generation, Custom Agentic Tools, Function Calling, Prompt Engineering & Optimization", skill_val_style)],
        [Paragraph("LLM Ops & Guardrails", skill_label_style), Paragraph("Token & Cost Optimization (Prompt Caching, Context Pruning), Structured Output Enforcement, Hallucination Guardrails, Self-Healing Code Reflection, Multimodal APIs, OCR to GenAI", skill_val_style)],
        [Paragraph("Enterprise Platform Core", skill_label_style), Paragraph("Sovablu No-Code Platform Core, Distributed Job Schedulers, Sovablu Drive Architecture, Chunked Multipart File Streaming, Dynamic Configuration Engines", skill_val_style)],
        [Paragraph("Backend & Protocols", skill_label_style), Paragraph("Java (Core & Advanced), Spring Boot, Microservices, RESTful APIs, Apple MDM Protocol, Android Management API, Kiosk & Lockdown Engines, Mutual TLS", skill_val_style)],
        [Paragraph("Frontend & Mobile", skill_label_style), Paragraph("React.js, React Native, Android SDK (Java/XML), TypeScript, JavaScript (ES6+), Redux Toolkit, Tailwind CSS, Material 3 Design", skill_val_style)],
        [Paragraph("Data & DevOps", skill_label_style), Paragraph("MySQL, SQLite, Firebase, Query Optimization, Database Schema Design, Git, Maven, Gradle, Jenkins, Docker, CI/CD Pipelines, JUnit", skill_val_style)],
    ]
    skills_table = Table(skills_data, colWidths=[124, 424])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 5))

    # 4. PROFESSIONAL EXPERIENCE
    story.extend(add_section_header("Professional Experience"))

    # Role 1: Vaken - Sovablu / GalaxyONE
    r1_header = [
        [
            Paragraph("<b>Lead Applied GenAI Engineer & Team Leader</b> | <font color='#2563eb'><b>Vaken Technologies Pvt. Ltd.</b></font>", role_title_style),
            Paragraph("May 2022 – Present", role_meta_style)
        ]
    ]
    t_r1 = Table(r1_header, colWidths=[408, 140])
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
            Paragraph("<b>Software Engineer — Team Leader (iOS MDM Engine)</b> | <font color='#2563eb'><b>Vaken Technologies Pvt. Ltd.</b></font>", role_title_style),
            Paragraph("Oct 2020 – May 2022", role_meta_style)
        ]
    ]
    t_r2 = Table(r2_header, colWidths=[408, 140])
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

    # Role 3: Works Applications India - MDM
    r3_header = [
        [
            Paragraph("<b>Software Engineer (MDM Engineering & Full-Stack Portal)</b> | <font color='#2563eb'><b>Works Applications (India) Pvt. Ltd.</b></font> <font color='#64748b' size='7'>(formerly IVTL Infoview)</font>", role_title_style),
            Paragraph("Sep 2019 – Sep 2020", role_meta_style)
        ]
    ]
    t_r3 = Table(r3_header, colWidths=[408, 140])
    t_r3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r3)
    story.append(Paragraph("Custom Android MDM Kiosk Launcher & Web Administrative Console", role_sub_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Autonomous Kiosk Launcher Execution:</b> Independently designed, built, and delivered an Android MDM Custom Launcher application within strict timelines, consuming MDM policy endpoints to enforce granular hardware restrictions and kiosk lock-down.", bullet_style))
    story.append(Paragraph("• <b>Full-Stack Administrative Portal:</b> Engineered a full-stack portal using React.js and Java backend to remotely configure, monitor, and enforce Google Android Management API policies across enterprise device fleets.", bullet_style))
    story.append(Spacer(1, 4))

    # Role 4: Works Applications India - ERP
    r4_header = [
        [
            Paragraph("<b>Junior Software Engineer (ERP Solutions)</b> | <font color='#2563eb'><b>Works Applications (India) Pvt. Ltd.</b></font> <font color='#64748b' size='7'>(formerly IVTL Infoview)</font>", role_title_style),
            Paragraph("Apr 2017 – Sep 2019", role_meta_style)
        ]
    ]
    t_r4 = Table(r4_header, colWidths=[408, 140])
    t_r4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r4)
    story.append(Paragraph("Enterprise ERP Suites & Automated Accounting Features for Japanese Market", role_sub_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Enterprise Feature Engineering:</b> Developed core transactional accounting and supply chain modules with automated validation rules and business intelligence dashboards for top-tier Japanese enterprises.", bullet_style))
    story.append(Paragraph("• <b>Team Enablement & Mentorship:</b> Guided junior developers on design patterns and module consolidation, standardizing code quality across cross-functional product squads.", bullet_style))
    story.append(Spacer(1, 4))

    # Role 5: Works Applications India - Trainee
    r5_header = [
        [
            Paragraph("<b>Trainee Engineer (Legacy Modernization)</b> | <font color='#2563eb'><b>Works Applications (India) Pvt. Ltd.</b></font> <font color='#64748b' size='7'>(formerly IVTL Infoview)</font>", role_title_style),
            Paragraph("Jul 2015 – Mar 2017", role_meta_style)
        ]
    ]
    t_r5 = Table(r5_header, colWidths=[408, 140])
    t_r5.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_r5)
    story.append(Paragraph("Desktop Delphi to High-Availability Cloud Web Platform Migration", role_sub_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Legacy Modernization:</b> Re-engineered legacy desktop Delphi HR & Payroll software into modern Java web applications, implementing high-precision payroll compliance calculation engines.", bullet_style))
    story.append(Spacer(1, 6))

    # 5. PUBLISHED APPLICATIONS & PRODUCTS (Styled in modern card boxes)
    story.extend(add_section_header("Published Mobile Applications & Technical Innovations (Angs Corp)"))

    p_secure_notes = [
        Paragraph("<b>Secure Notes</b> <font color='#2563eb' size='7'>[React Native &bull; Security]</font>", card_title_style),
        Paragraph("Production-grade offline notes app with AES-256 local encryption, biometric lock, dynamic Material 3 theming, and zero network transmission.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/details?id=com.angs.securenotes'><font color='#2563eb'><b>Google Play: com.angs.securenotes &rarr;</b></font></a>", card_link_style)
    ]

    p_moneywise = [
        Paragraph("<b>MoneyWise</b> <font color='#2563eb' size='7'>[React Native &bull; FinTech]</font>", card_title_style),
        Paragraph("Comprehensive personal finance tracker with multi-account ledgers, interactive budget analytics, multi-currency support, and offline-first SQLite sync.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#2563eb'><b>Angs Corp Portfolio &rarr;</b></font></a>", card_link_style)
    ]

    p_appshield = [
        Paragraph("<b>AppShield</b> <font color='#2563eb' size='7'>[React Native &bull; Privacy]</font>", card_title_style),
        Paragraph("Privacy & permission auditor inspecting third-party apps, background sensor/network access, and system security posture in real time.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#2563eb'><b>Angs Corp Portfolio &rarr;</b></font></a>", card_link_style)
    ]

    p_pixelsqueeze = [
        Paragraph("<b>PixelSqueeze</b> <font color='#2563eb' size='7'>[React Native &bull; Media Utility]</font>", card_title_style),
        Paragraph("High-speed on-device image compression and format converter leveraging native bridge modules for hardware-accelerated processing.", card_desc_style),
        Paragraph("<a href='https://play.google.com/store/apps/developer?id=Angs+Corp'><font color='#2563eb'><b>Angs Corp Portfolio &rarr;</b></font></a>", card_link_style)
    ]

    c1 = Table([[p] for p in p_secure_notes], colWidths=[266])
    c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_card_border),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    c2 = Table([[p] for p in p_moneywise], colWidths=[266])
    c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_card_border),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    c3 = Table([[p] for p in p_appshield], colWidths=[266])
    c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_card_border),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    c4 = Table([[p] for p in p_pixelsqueeze], colWidths=[266])
    c4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_card_border),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    projects_grid = Table([[c1, c2], [Spacer(1, 3), Spacer(1, 3)], [c3, c4]], colWidths=[271, 271])
    projects_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(projects_grid)
    story.append(Spacer(1, 6))

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
    t_edu = Table(edu_table_data, colWidths=[388, 160])
    t_edu.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_edu)
    story.append(Spacer(1, 2))

    award_p = Paragraph(
        "🏆 <b>State Level Winner: 'Student Innovator Award 2015' (ICTACT Tamil Nadu)</b><br/>"
        "Published research & system: <i>'Uzhavan Puthagam: Web Based System of Effective Farm Collaboration'</i> "
        "(ACCCAS-2015 Conference) in Computer Science & IT Applications.",
        bullet_style
    )
    award_box = Table([[award_p]], colWidths=[548])
    award_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fffbeb")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#fde68a")),
        ('LINELEFT', (0,0), (-1,-1), 2.5, colors.HexColor("#f59e0b")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(award_box)

    doc.build(story, canvasmaker=ModernNumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == '__main__':
    build_pdf()
