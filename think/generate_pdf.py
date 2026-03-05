"""
Technical Documentation PDF Generator
AI-Powered Teaching Assistant
"""

from fpdf import FPDF
import os


class TechnicalDocPDF(FPDF):
    """Custom PDF class with headers, footers, and styled sections."""

    # ── Colours ──
    PRIMARY = (26, 58, 114)       # Deep blue
    ACCENT = (0, 150, 136)        # Teal
    DARK = (33, 37, 41)           # Near-black
    LIGHT_BG = (245, 247, 250)    # Light grey bg
    WHITE = (255, 255, 255)

    def header(self):
        if self.page_no() == 1:
            return  # Skip header on cover page
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*self.PRIMARY)
        self.cell(0, 8, "AI-Powered Teaching Assistant - Technical Documentation", align="L")
        self.cell(0, 8, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "AU Campus Recruitment 2026 | Problem Statement 1", align="C")

    # ── Helper methods ──
    def cover_page(self):
        """Draw a styled cover page."""
        self.add_page()
        self.ln(50)

        # Title
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*self.PRIMARY)
        self.cell(0, 14, "AI-Powered Teaching Assistant", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        # Subtitle
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 10, "Technical Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

        # Divider line
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.8)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(12)

        # Meta info
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*self.DARK)
        meta = [
            ("Submitted by", "Karthik Lagudu"),
            ("Problem Statement", "1 - AI-Powered Teaching Assistant"),
            ("Program", "AU Campus Recruitment 2026"),
            ("Tech Stack", "Python | Streamlit | Groq API | Llama 3.3-70b"),
            ("Date", "February 2026"),
        ]
        for label, value in meta:
            self.set_font("Helvetica", "B", 11)
            self.cell(55, 8, f"{label}:", align="R")
            self.set_font("Helvetica", "", 11)
            self.cell(0, 8, f"  {value}", align="L", new_x="LMARGIN", new_y="NEXT")
        self.ln(20)

        # Decorative box at bottom
        self.set_fill_color(*self.LIGHT_BG)
        self.rect(15, 210, 180, 40, style="F")
        self.set_y(215)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 5,
            "This document describes the approach, dataset, model architecture, assumptions, "
            "limitations, and sample outputs of the AI-Powered Teaching Assistant system.",
            align="C")

    def section_title(self, number, title):
        """Draw a numbered section heading."""
        self.ln(6)
        self.set_fill_color(*self.PRIMARY)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"  {number}. {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_text_color(*self.DARK)

    def sub_heading(self, text):
        """Draw a sub-heading."""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.DARK)

    def body_text(self, text):
        """Draw body text with word-wrap."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        """Draw a bullet point."""
        self.set_font("Helvetica", "", 10)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(5, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def code_block(self, code, title=None):
        """Draw a styled code block."""
        if title:
            self.set_font("Helvetica", "BI", 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")

        self.set_fill_color(40, 44, 52)
        self.set_text_color(220, 220, 220)
        self.set_font("Courier", "", 8.5)

        x, y = self.get_x(), self.get_y()
        lines = code.strip().split("\n")
        block_h = len(lines) * 5 + 8

        # Check if block fits on page, else add page
        if y + block_h > 275:
            self.add_page()
            y = self.get_y()

        self.rect(x, y, 190, block_h, style="F")
        self.set_y(y + 4)
        for line in lines:
            self.set_x(x + 4)
            self.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_text_color(*self.DARK)

    def table(self, headers, rows, col_widths=None):
        """Draw a simple styled table."""
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)

        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*self.PRIMARY)
        self.set_text_color(*self.WHITE)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C")
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(*self.LIGHT_BG)
            else:
                self.set_fill_color(*self.WHITE)
            for i, val in enumerate(row):
                self.cell(col_widths[i], 7, str(val), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(4)

    def info_box(self, text, box_type="info"):
        """Draw a coloured info/warning box."""
        colors = {
            "info": (232, 244, 253),
            "warning": (255, 249, 230),
            "success": (232, 252, 237),
        }
        border_colors = {
            "info": (66, 133, 244),
            "warning": (251, 188, 4),
            "success": (52, 168, 83),
        }
        bg = colors.get(box_type, colors["info"])
        bd = border_colors.get(box_type, border_colors["info"])

        y = self.get_y()
        self.set_fill_color(*bg)
        self.set_draw_color(*bd)
        self.set_line_width(0.6)

        # Calculate height
        self.set_font("Helvetica", "", 9)
        lines = self.multi_cell(180, 5, text, dry_run=True, output="LINES")
        h = len(lines) * 5 + 8

        if y + h > 275:
            self.add_page()
            y = self.get_y()

        self.rect(10, y, 190, h, style="DF")
        self.set_xy(15, y + 4)
        self.set_text_color(*self.DARK)
        self.multi_cell(180, 5, text)
        self.ln(4)


def build_pdf():
    pdf = TechnicalDocPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ─────────────────────────── COVER PAGE ───────────────────────────────
    pdf.cover_page()

    # ─────────────────────────── TABLE OF CONTENTS ────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*TechnicalDocPDF.PRIMARY)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    toc = [
        ("1", "Approach Explanation", "3"),
        ("2", "Dataset Source & Generation", "4"),
        ("3", "Model Architecture", "5"),
        ("4", "Gamification & Interactive Features", "7"),
        ("5", "Assumptions and Limitations", "9"),
        ("6", "Sample Outputs", "10"),
        ("7", "System Design & Project Structure", "11"),
    ]
    for num, title, page in toc:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*TechnicalDocPDF.DARK)
        pdf.cell(10, 8, num + ".")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(140, 8, title)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*TechnicalDocPDF.ACCENT)
        pdf.cell(0, 8, page, align="R", new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 1: APPROACH EXPLANATION
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1", "Approach Explanation")

    pdf.body_text(
        "The AI-Powered Teaching Assistant is designed as a modular, production-ready system "
        "with two primary intelligence engines. The architecture separates concerns between "
        "Natural Language Processing (understanding what the student needs) and Adaptive "
        "Learning (recommending what to do next)."
    )

    pdf.sub_heading("1.1  Student Query Understanding (Q1)")
    pdf.body_text(
        "Goal: Interpret natural language questions from students and extract structured "
        "metadata including intent, topic, and difficulty level."
    )
    pdf.body_text(
        "Method: We utilize a Large Language Model (Llama-3.3-70b-versatile) via the Groq API, "
        "with carefully engineered system and user prompts. The LLM acts as an educational "
        "classifier, providing deep contextual understanding that goes beyond simple keyword "
        "matching. It can differentiate between a student asking for an 'Explanation' versus "
        "requesting an 'Example', even when the phrasing is ambiguous."
    )
    pdf.body_text(
        "The system prompt establishes the AI persona as an EdTech assistant and constrains "
        "output to structured JSON format. The user prompt wraps the student's question with "
        "explicit classification instructions for three dimensions: Intent (Explanation, "
        "Example, Doubt clarification, Revision), Topic (e.g., Neural Networks, Optimization), "
        "and Difficulty Level (Beginner, Intermediate, Advanced)."
    )

    pdf.sub_heading("1.2  Adaptive Learning Path Recommendation (Q2)")
    pdf.body_text(
        "Goal: Recommend the next logical learning step based on student performance metrics."
    )
    pdf.body_text(
        "Method: A hybrid approach combining rule-based pedagogical logic with LLM reasoning. "
        "The system evaluates a student's state (quiz score, number of attempts, time spent, "
        "last topic studied) against curriculum-aware rules:"
    )
    pdf.bullet("Score < 50: Action = Revision, Difficulty = Decrease, Stay on same topic")
    pdf.bullet("50 <= Score < 80: Action = Practice, Difficulty = Same, Reinforce current topic")
    pdf.bullet("Score >= 80: Action = Next Topic, Difficulty = Increase, Advance in curriculum")
    pdf.body_text(
        "These rules are embedded within the LLM prompt along with the full curriculum order, "
        "allowing the model to make contextually intelligent recommendations that follow a "
        "research-backed spaced-repetition and mastery-learning pedagogy."
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 2: DATASET SOURCE
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("2", "Dataset Source & Generation")

    pdf.sub_heading("2.1  Source: Synthetic Data (Self-Generated)")
    pdf.body_text(
        "No publicly available dataset perfectly matched the multi-turn interaction model "
        "required for adaptive learning path recommendations. Therefore, we built a custom "
        "synthetic data generator to simulate realistic student interactions."
    )

    pdf.sub_heading("2.2  Generation Logic")
    pdf.body_text(
        "The generator script (data/synthetic_data_generator.py) creates a configurable "
        "dataset of student interactions with the following characteristics:"
    )

    pdf.table(
        ["Field", "Type", "Description"],
        [
            ["student_id", "Integer", "Unique student identifier (1 to N)"],
            ["topic", "String", "Randomly selected from 7 ML topics"],
            ["quiz_score", "Float", "Normal distribution (mean=70, SD=15), clipped 0-100"],
            ["attempts", "Integer", "Inversely correlated with score (1-4)"],
            ["time_spent_minutes", "Integer", "Random, 5-60 minutes"],
            ["last_asked_intent", "String", "Random: Explanation/Example/Doubt/Revision"],
        ],
        col_widths=[35, 20, 135],
    )

    pdf.sub_heading("2.3  Dataset Statistics")
    pdf.body_text(
        "Default configuration: 100 students, each with 5-20 interactions, producing "
        "approximately 1,250 records. The current generated file contains 1,282 records."
    )
    pdf.info_box(
        "Privacy Note: The dataset is entirely synthetic and contains no Personally "
        "Identifiable Information (PII). All student IDs are arbitrary integers."
    )

    pdf.sub_heading("2.4  Sample Data")
    pdf.table(
        ["Student", "Topic", "Score", "Attempts", "Time (min)", "Intent"],
        [
            ["1", "Linear Regression", "68.66", "1", "15", "Doubt clarification"],
            ["1", "Backpropagation", "56.24", "1", "39", "Revision"],
            ["1", "Neural Networks", "57.51", "3", "9", "Revision"],
            ["1", "Optimization", "84.52", "1", "50", "Revision"],
            ["2", "CNNs", "94.46", "1", "39", "Example"],
            ["2", "Gradient Descent", "100.0", "1", "43", "Revision"],
        ],
        col_widths=[20, 40, 20, 22, 25, 45],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 3: MODEL ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("3", "Model Architecture")

    pdf.sub_heading("3.1  Core Model")
    pdf.body_text(
        "Model: Llama-3.3-70b-versatile (70 billion parameters)\n"
        "Provider: Groq API (cloud-hosted inference)\n"
        "Response Format: Structured JSON via json_object mode"
    )

    pdf.sub_heading("3.2  Architecture Overview")
    pdf.body_text(
        "The system follows a prompt-engineering-first architecture where the LLM serves as "
        "the core reasoning engine. Rather than fine-tuning a model or training from scratch, "
        "we leverage the pre-trained capabilities of Llama-3.3-70b through carefully designed "
        "prompts that encode domain knowledge and pedagogical rules."
    )

    pdf.info_box(
        "Why Prompt Engineering? For an EdTech assistant with a well-defined scope, prompt "
        "engineering provides: (1) Zero training cost, (2) Instant iteration on logic, "
        "(3) Transparent reasoning that can be audited and improved, (4) Consistent JSON "
        "output via Groq's json_object mode.", "success"
    )

    pdf.sub_heading("3.3  Processing Pipeline")
    pdf.body_text("Query Understanding Pipeline:")
    pdf.code_block(
        'User Question (string)\n'
        '    |\n'
        '    v\n'
        'StudentQueryEngine.analyze_query(query)\n'
        '    |\n'
        '    v\n'
        'System Prompt: "You are an AI assistant that classifies\n'
        '                student queries in an EdTech context."\n'
        'User Prompt:   "Analyze: <query>. Classify into intent,\n'
        '                topic, difficulty_level."\n'
        '    |\n'
        '    v\n'
        'Groq API -> Llama-3.3-70b (json_object mode)\n'
        '    |\n'
        '    v\n'
        'Structured JSON: { intent, topic, difficulty_level }',
        "Pipeline: Student Query Understanding"
    )

    pdf.ln(4)

    pdf.body_text("Adaptive Learning Pipeline:")
    pdf.code_block(
        'Student State (dict: score, attempts, topic, time)\n'
        '    |\n'
        '    v\n'
        'AdaptiveLearningEngine.recommend_path(state)\n'
        '    |\n'
        '    v\n'
        'System Prompt: "You are an AI academic advisor."\n'
        'User Prompt:   "State: <metrics>. Rules: <pedagogical\n'
        '                rules>. Curriculum: <ordered topics>."\n'
        '    |\n'
        '    v\n'
        'Groq API -> Llama-3.3-70b (json_object mode)\n'
        '    |\n'
        '    v\n'
        'Structured JSON: { next_topic, action, difficulty_adjustment }',
        "Pipeline: Adaptive Learning Recommendation"
    )

    pdf.sub_heading("3.4  Key Design Decisions")
    pdf.bullet("JSON-only output mode eliminates parsing errors and guarantees structured responses")
    pdf.bullet("System prompts define persona boundaries, preventing off-topic responses")
    pdf.bullet("Curriculum sequence is embedded in the prompt, enabling context-aware topic progression")
    pdf.bullet("Class-based engine design allows easy swap of the underlying model or API provider")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 4: GAMIFICATION & INTERACTIVE FEATURES
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("4", "Gamification & Interactive Features")

    pdf.body_text(
        "The application transforms passive learning into active engagement through multiple "
        "game-based learning modes, XP rewards, and achievement systems."
    )

    pdf.sub_heading("4.1  XP & Level System")
    pdf.body_text(
        "Students earn XP through all interactions. Level progression spans 10 tiers from "
        "'Curious Learner' (Level 1) to 'AI Grandmaster' (Level 10), requiring increasing XP "
        "thresholds (100, 250, 500, 1000, ... XP)."
    )
    pdf.table(
        ["Action", "XP Reward"],
        [
            ["Correct quiz answer", "+15 XP"],
            ["Attempted quiz answer", "+3 XP"],
            ["Memory pair matched", "+10 XP"],
            ["Cue card studied", "+3 XP"],
            ["Game completion bonus", "+25 to 75 XP"],
            ["Perfect score bonus", "+25 XP"],
        ],
        col_widths=[95, 95],
    )

    pdf.sub_heading("4.2  Memory Match Game")
    pdf.body_text(
        "A card-matching game with a 4x3 grid of 12 face-down cards (6 concept-definition "
        "pairs per topic). Students flip two cards at a time; matching concept-definition "
        "pairs stay revealed. The game tracks moves and awards a 1-5 star rating based on "
        "efficiency. 42 unique pairs across 7 ML/AI topics."
    )
    pdf.bullet("Match: Concept card (purple) + Definition card (blue)")
    pdf.bullet("+10 XP per match, +25-75 XP on completion based on move count")
    pdf.bullet("5 stars for <= 8 moves, 1 star for 16+ moves")

    pdf.sub_heading("4.3  Cue Cards (Flip Cards)")
    pdf.body_text(
        "Traditional flip-style study cards for active recall. Front shows the concept name, "
        "back reveals the definition. Students navigate with Previous/Flip/Next buttons. "
        "Each flip earns +3 XP. Uses the same topic and pairs as the Memory Game."
    )

    pdf.sub_heading("4.4  Daily Quiz")
    pdf.body_text(
        "5-question adaptive quizzes generated by the LLM. Features animated correct/wrong "
        "feedback, streak tracking, and a score reveal screen with stars and XP breakdown."
    )

    pdf.sub_heading("4.5  Badges & Study Roadmap")
    pdf.bullet("Achievement badges: First Steps, Quiz Master, Knowledge Explorer, etc.")
    pdf.bullet("Daily streak tracking with fire icon indicator")
    pdf.bullet("Visual learning roadmap through 7 ML/AI topics with sequential unlocking")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 5: ASSUMPTIONS AND LIMITATIONS
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("5", "Assumptions and Limitations")

    pdf.sub_heading("4.1  Assumptions")
    pdf.bullet("The student follows a fixed Machine Learning curriculum in a predefined order: "
               "Linear Regression -> Gradient Descent -> Neural Networks -> Backpropagation -> "
               "Optimization Algorithms -> CNNs -> RNNs.")
    pdf.bullet("Quiz scores are the primary metric for gauging student understanding and "
               "determining the appropriate next step.")
    pdf.bullet("The Groq API is available with consistent uptime and acceptable latency for "
               "real-time interactions.")
    pdf.bullet("Students interact with one topic at a time, and each interaction is "
               "independent (stateless per request).")
    pdf.bullet("The LLM consistently follows the structured output format specified in the "
               "system/user prompts.")

    pdf.sub_heading("4.2  Limitations")

    pdf.info_box(
        "LLM Dependency: The system requires an active internet connection to query the "
        "Groq API. Offline usage is not supported. Any API downtime directly impacts "
        "availability.", "warning"
    )

    pdf.bullet("Statelessness: Each request is processed independently. The system does not "
               "maintain a persistent student profile across sessions. A production deployment "
               "would require a database layer (e.g., PostgreSQL, MongoDB) to track learning "
               "history over time.")
    pdf.bullet("Fixed Curriculum: The topic list is hardcoded in the prompt for this demo. "
               "A production system would need a dynamic curriculum management module.")
    pdf.bullet("No Fine-Tuning: The model is used as-is via prompt engineering. Domain-specific "
               "fine-tuning could improve accuracy for edge cases but would increase cost and "
               "complexity.")
    pdf.bullet("Single Language: Currently supports English-language queries only.")
    pdf.bullet("No Authentication: The Streamlit demo does not implement user authentication "
               "or session management.")

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 6: SAMPLE OUTPUTS
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("6", "Sample Outputs")

    pdf.sub_heading("5.1  Student Query Understanding (Q1)")

    pdf.body_text('Sample Input: "I don\'t understand backpropagation."')
    pdf.code_block(
        '{\n'
        '  "intent": "Explanation",\n'
        '  "topic": "Backpropagation",\n'
        '  "difficulty_level": "Intermediate"\n'
        '}',
        "Output JSON"
    )

    pdf.body_text('Sample Input: "Can you show me an example of gradient descent with code?"')
    pdf.code_block(
        '{\n'
        '  "intent": "Example",\n'
        '  "topic": "Gradient Descent",\n'
        '  "difficulty_level": "Intermediate"\n'
        '}',
        "Output JSON"
    )

    pdf.body_text('Sample Input: "What is linear regression?"')
    pdf.code_block(
        '{\n'
        '  "intent": "Explanation",\n'
        '  "topic": "Linear Regression",\n'
        '  "difficulty_level": "Beginner"\n'
        '}',
        "Output JSON"
    )

    pdf.sub_heading("5.2  Adaptive Learning Path Recommendation (Q2)")

    pdf.body_text("Case 1 - Low Score (Needs Revision):")
    pdf.table(
        ["Parameter", "Value"],
        [
            ["Quiz Score", "45"],
            ["Attempts", "3"],
            ["Last Topic", "Backpropagation"],
            ["Time Spent", "45 minutes"],
        ],
        col_widths=[60, 130],
    )
    pdf.code_block(
        '{\n'
        '  "next_topic": "Backpropagation",\n'
        '  "action": "Revision",\n'
        '  "difficulty_adjustment": "Decrease"\n'
        '}',
        "Recommendation Output"
    )

    pdf.body_text("Case 2 - High Score (Ready to Advance):")
    pdf.table(
        ["Parameter", "Value"],
        [
            ["Quiz Score", "92"],
            ["Attempts", "1"],
            ["Last Topic", "Neural Networks"],
            ["Time Spent", "30 minutes"],
        ],
        col_widths=[60, 130],
    )
    pdf.code_block(
        '{\n'
        '  "next_topic": "Backpropagation",\n'
        '  "action": "Next Topic",\n'
        '  "difficulty_adjustment": "Increase"\n'
        '}',
        "Recommendation Output"
    )

    pdf.body_text("Case 3 - Medium Score (Practice):")
    pdf.table(
        ["Parameter", "Value"],
        [
            ["Quiz Score", "65"],
            ["Attempts", "2"],
            ["Last Topic", "Gradient Descent"],
            ["Time Spent", "50 minutes"],
        ],
        col_widths=[60, 130],
    )
    pdf.code_block(
        '{\n'
        '  "next_topic": "Gradient Descent",\n'
        '  "action": "Practice",\n'
        '  "difficulty_adjustment": "Same"\n'
        '}',
        "Recommendation Output"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 7: SYSTEM DESIGN
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("7", "System Design & Project Structure")

    pdf.sub_heading("7.1  Project Structure")
    pdf.code_block(
        'think/\n'
        '  |\n'
        '  +-- app.py                     # Streamlit web interface (7 tabs)\n'
        '  +-- main.py                    # CLI interface\n'
        '  +-- generate_pdf.py            # PDF documentation generator\n'
        '  +-- requirements.txt           # Python dependencies\n'
        '  +-- .env                       # API key (GROQ_API_KEY)\n'
        '  +-- technical_documentation.md # Source documentation\n'
        '  |\n'
        '  +-- src/\n'
        '  |   +-- __init__.py\n'
        '  |   +-- query_engine.py        # Student Query Understanding engine\n'
        '  |   +-- adaptive_engine.py     # Adaptive Learning Path engine\n'
        '  |   +-- gamification.py        # XP, levels, badges, streaks\n'
        '  |   +-- flashcards.py          # MCQ data + Memory pairs\n'
        '  |   +-- styles.py              # CSS styling for web UI\n'
        '  |\n'
        '  +-- data/\n'
        '  |   +-- synthetic_data_generator.py   # Data generation script\n'
        '  |   +-- student_interactions.csv       # Generated dataset\n'
        '  |\n'
        '  +-- tests/\n'
        '  |   +-- verify.py              # Verification / integration tests\n'
        '  |\n'
        '  +-- presentation/\n'
        '      +-- index.html             # Presentation slides',
        "Project Tree"
    )

    pdf.sub_heading("7.2  Module Responsibilities")
    pdf.table(
        ["Module", "Purpose", "Key Class/Function"],
        [
            ["query_engine.py", "NLP intent/topic/difficulty classification", "StudentQueryEngine"],
            ["adaptive_engine.py", "Learning path recommendation", "AdaptiveLearningEngine"],
            ["gamification.py", "XP, levels, badges, streaks", "add_xp(), check_badges()"],
            ["flashcards.py", "MCQ + Memory pairs + Cue cards", "get_deck(), get_memory_pairs()"],
            ["styles.py", "CSS styling for all UI components", "get_css()"],
            ["app.py", "Interactive web dashboard (7 tabs)", "get_engines()"],
            ["main.py", "Command-line demo interface", "main()"],
            ["generate_pdf.py", "PDF documentation generator", "build_pdf()"],
        ],
        col_widths=[40, 80, 70],
    )

    pdf.sub_heading("7.3  Technology Stack")
    pdf.table(
        ["Component", "Technology", "Purpose"],
        [
            ["LLM", "Llama-3.3-70b-versatile", "Core AI reasoning"],
            ["API Provider", "Groq", "Fast LLM inference (cloud)"],
            ["Web Framework", "Streamlit", "Interactive UI dashboard"],
            ["Language", "Python 3.x", "Primary programming language"],
            ["Data Processing", "Pandas + NumPy", "Dataset handling"],
            ["Config", "python-dotenv", "Environment variable management"],
            ["PDF Generation", "fpdf2", "Technical documentation output"],
        ],
        col_widths=[40, 60, 90],
    )

    pdf.sub_heading("7.4  Scalability Considerations")
    pdf.body_text(
        "The modular class-based architecture supports straightforward scaling:"
    )
    pdf.bullet("Engine classes can be imported into any Python web framework (Flask, FastAPI, Django)")
    pdf.bullet("The Groq API handles model hosting and GPU infrastructure")
    pdf.bullet("Batch processing demonstrates multi-student throughput capability")
    pdf.bullet("Adding new topics or intents requires only prompt modifications, not code changes")
    pdf.bullet("Flashcard data is decoupled from UI logic, enabling easy content expansion")

    # ─────────────────────────── SAVE ─────────────────────────────────────
    output_path = os.path.join(os.path.dirname(__file__), "Technical_Documentation.pdf")
    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    path = build_pdf()
    print(f"PDF generated successfully: {path}")
