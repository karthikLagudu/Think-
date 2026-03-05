import streamlit as st
import pandas as pd
import os, sys, time, json, random

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.query_engine import StudentQueryEngine
from src.adaptive_engine import AdaptiveLearningEngine
from src.styles import get_css
from src.gamification import (
    init_gamification, add_xp, get_level, get_level_progress, get_next_level_xp,
    award_badge, check_badges, render_sidebar_gamification, render_confetti,
    render_badge_popup, BADGES
)
from src.flashcards import FLASHCARD_DECKS, get_deck, get_all_topics, get_memory_pairs

# ─── Page Config ──
st.set_page_config(page_title="AI Teaching Assistant", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
st.markdown(get_css(), unsafe_allow_html=True)

# ─── Particles ──
st.markdown("""
<div class="particles-bg">
    <div class="particle"></div><div class="particle"></div><div class="particle"></div>
    <div class="particle"></div><div class="particle"></div><div class="particle"></div>
</div>
""", unsafe_allow_html=True)

# ─── Init ──
init_gamification()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "card_flipped" not in st.session_state:
    st.session_state.card_flipped = False
if "query_history" not in st.session_state:
    st.session_state.query_history = []

@st.cache_resource
def get_engines():
    try:
        return StudentQueryEngine(), AdaptiveLearningEngine()
    except Exception:
        return None, None

query_engine, adaptive_engine = get_engines()

# ─── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <div style="font-size:3rem;">🎓</div>
        <div style="font-size:1.1rem; font-weight:700; color:#e0e0ff;">AI Teaching Assistant</div>
        <div style="font-size:0.7rem; color:#7777aa;">Powered by Llama 3.3 · Groq</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_sidebar_gamification()
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    with st.expander("ℹ️ How it Works"):
        st.markdown("""
        **Query Understanding** classifies questions by intent, topic & difficulty.
        **Adaptive Learning** recommends next steps based on performance.
        **Daily Quiz** tests your knowledge with AI-generated questions.
        **Flashcards** help you master each topic with cue cards.
        **Doubt Solver** answers your questions in real-time.
        **Study Roadmap** tracks your learning journey.
        """)

# ─── Hero ──
render_confetti()
render_badge_popup()

st.markdown("""
<div style="text-align:center; padding:1rem 0 0.5rem;">
    <div class="hero-title">🎓 AI-Powered Teaching Assistant</div>
    <div class="hero-subtitle">Intelligent NLP-driven student support · Adaptive learning · Gamified experience · Real-time AI</div>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4, s5 = st.columns(5)
with s1:
    st.markdown('<div class="stat-box"><div class="stat-number">7</div><div class="stat-label">Topics</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-box"><div class="stat-number">35</div><div class="stat-label">Flashcards</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.xp}</div><div class="stat-label">Your XP</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{len(st.session_state.badges_earned)}</div><div class="stat-label">Badges</div></div>', unsafe_allow_html=True)
with s5:
    st.markdown('<div class="stat-box"><div class="stat-number">70B</div><div class="stat-label">Model Params</div></div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ─── Tabs ──
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🧠 Query Understanding", "🚀 Adaptive Path", "📊 Batch Processing",
    "🎯 Daily Quiz", "💬 Doubt Solver", "🃏 Flashcards", "📚 Study Roadmap"
])

# ━━━ TAB 1 — Query Understanding ━━━
with tab1:
    st.session_state.tabs_visited.add("tab1")
    st.markdown("""
    <div class="section-header">🧠 Student Query Understanding</div>
    <div class="section-desc">Enter a natural language question and the AI will classify its <b style="color:#7b2ff7;">Intent</b>, <b style="color:#00d2ff;">Topic</b>, and <b style="color:#ff6ec7;">Difficulty Level</b>.</div>
    """, unsafe_allow_html=True)

    col_input, col_tips = st.columns([3, 1])

    with col_input:
        example_queries = [
            "I don't understand backpropagation at all. Can you explain how gradients flow?",
            "What is gradient descent?", "Show me a CNN example",
            "I'm confused about loss functions", "How does Adam optimizer work?"
        ]
        selected_example = st.selectbox("💡 Quick examples:", example_queries, label_visibility="collapsed")
        query = st.text_area("Enter your question:", value=selected_example, height=100, label_visibility="collapsed", placeholder="Type a student question here...")
        analyze_btn = st.button("✨ Analyze Query", use_container_width=True, key="analyze_btn")

    with col_tips:
        st.markdown("""
        <div class="glass-card" style="padding:1.2rem;">
            <div style="font-size:0.9rem; font-weight:600; color:#e0e0ff; margin-bottom:0.5rem;">🏆 Rewards</div>
            <div style="font-size:0.8rem; color:#aaa;">
                +10 XP per query analyzed<br/>
                🔥 Badge: "First Spark" for your first query
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.query_history:
            st.markdown("**📜 Recent Queries:**")
            for h in st.session_state.query_history[-3:]:
                st.caption(f"• {h[:50]}...")

    if analyze_btn:
        if not query_engine:
            st.error("⚠️ Engine failed to initialize. Check your API key.")
        elif not query.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner(""):
                pp = st.empty()
                for msg in ["🔍 Parsing query...", "🧠 Analyzing intent...", "📊 Classifying..."]:
                    pp.markdown(f'<div style="text-align:center; color:#9a9ac4; font-size:0.9rem;">{msg}</div>', unsafe_allow_html=True)
                    time.sleep(0.3)
                result = query_engine.analyze_query(query)
                pp.empty()

            xp_gained = add_xp(10, "Query analysis")
            st.session_state.queries_count += 1
            st.session_state.query_history.append(query)
            check_badges()

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.markdown(f'<div style="text-align:center; color:#00c853; font-size:0.9rem; font-weight:600;">✅ Analysis Complete · +{xp_gained} XP</div>', unsafe_allow_html=True)
                intent = result.get("intent", "Unknown")
                topic = result.get("topic", "Unknown")
                difficulty = result.get("difficulty_level", "Unknown")

                r1, r2, r3 = st.columns(3)
                with r1:
                    st.markdown(f'<div class="result-card"><div class="result-label">🎯 Intent</div><div class="result-value">{intent}</div><div style="margin-top:0.6rem;"><span class="badge-purple">{intent}</span></div></div>', unsafe_allow_html=True)
                with r2:
                    st.markdown(f'<div class="result-card"><div class="result-label">📚 Topic</div><div class="result-value">{topic}</div><div style="margin-top:0.6rem;"><span class="badge-teal">{topic}</span></div></div>', unsafe_allow_html=True)
                with r3:
                    db = "badge-green" if difficulty.lower() == "beginner" else ("badge-amber" if difficulty.lower() == "intermediate" else "badge-red")
                    st.markdown(f'<div class="result-card"><div class="result-label">📈 Difficulty</div><div class="result-value">{difficulty}</div><div style="margin-top:0.6rem;"><span class="{db}">{difficulty}</span></div></div>', unsafe_allow_html=True)
                with st.expander("🔗 View Raw JSON"):
                    st.json(result)

# ━━━ TAB 2 — Adaptive Learning Path ━━━
with tab2:
    st.session_state.tabs_visited.add("tab2")
    st.markdown("""
    <div class="section-header">🚀 Adaptive Learning Path</div>
    <div class="section-desc">Configure student performance and get AI-powered recommendations. <b style="color:#ffc107;">+15 XP</b> per recommendation!</div>
    """, unsafe_allow_html=True)

    col_config, col_result = st.columns([1, 1])

    with col_config:
        st.markdown('<div class="glass-card"><div style="font-size:1rem; font-weight:600; color:#e0e0ff; margin-bottom:1rem;">🎛️ Student Performance State</div>', unsafe_allow_html=True)
        topic_sel = st.selectbox("📘 Last Topic Studied", get_all_topics(), index=3)
        score = st.slider("📊 Quiz Score", 0, 100, 45)
        bar_color = "#ff4757" if score < 50 else ("#ffc107" if score < 80 else "#00c853")
        st.markdown(f'<div class="score-bar-container"><div class="score-bar-fill" style="width:{score}%; background:{bar_color};"></div></div><div style="display:flex; justify-content:space-between; font-size:0.7rem; color:#666;"><span>Revision</span><span>Practice</span><span>Advance</span></div>', unsafe_allow_html=True)
        a_col, t_col = st.columns(2)
        with a_col:
            attempts = st.number_input("🔄 Attempts", min_value=1, max_value=10, value=3)
        with t_col:
            time_spent = st.slider("⏱️ Time (min)", 5, 120, 45)
        st.markdown("</div>", unsafe_allow_html=True)
        recommend_btn = st.button("🤖 Generate Recommendation", use_container_width=True)

    with col_result:
        if recommend_btn:
            if not adaptive_engine:
                st.error("⚠️ Engine failed. Check API Keys.")
            else:
                state = {"quiz_score": score, "attempts": attempts, "last_topic": topic_sel, "time_spent_minutes": time_spent}
                with st.spinner(""):
                    pp2 = st.empty()
                    for msg in ["📡 Sending state...", "🤖 Analyzing...", "📋 Generating..."]:
                        pp2.markdown(f'<div style="text-align:center; color:#9a9ac4; font-size:0.9rem;">{msg}</div>', unsafe_allow_html=True)
                        time.sleep(0.3)
                    recommendation = adaptive_engine.recommend_path(state)
                    pp2.empty()

                xp_gained = add_xp(15, "Recommendation")
                st.session_state.recommendations_count += 1
                check_badges()

                if "error" in recommendation:
                    st.error(f"Error: {recommendation['error']}")
                else:
                    action = recommendation.get("action", "Unknown")
                    next_topic = recommendation.get("next_topic", "Unknown")
                    diff_adj = recommendation.get("difficulty_adjustment", "Unknown")

                    if "revision" in action.lower():
                        a_class, a_icon, a_color = "action-revision", "⚠️", "#ff4757"
                    elif "practice" in action.lower():
                        a_class, a_icon, a_color = "action-practice", "📝", "#ffc107"
                    else:
                        a_class, a_icon, a_color = "action-next", "🚀", "#00c853"

                    st.markdown(f'<div style="text-align:center; color:#00c853; font-size:0.9rem; font-weight:600;">✅ Ready · +{xp_gained} XP</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="glass-card" style="animation:pulseGlow 2s infinite;">
                        <div class="result-card {a_class}" style="text-align:left; padding:1.2rem; margin-bottom:1rem;">
                            <div class="result-label">Recommended Action</div>
                            <div style="font-size:1.6rem; font-weight:700; color:{a_color};">{a_icon} {action}</div>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8rem;">
                            <div class="result-card" style="text-align:left; padding:1rem;"><div class="result-label">📘 Next Topic</div><div style="font-size:1.1rem; font-weight:600; color:#e0e0ff;">{next_topic}</div></div>
                            <div class="result-card" style="text-align:left; padding:1rem;"><div class="result-label">📈 Difficulty</div><div style="font-size:1.1rem; font-weight:600; color:#e0e0ff;">{diff_adj}</div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("🔗 View Raw JSON"):
                        st.json(recommendation)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:4rem 2rem;">
                <div style="font-size:3rem;">🤖</div>
                <div style="font-size:1.1rem; font-weight:600; color:#e0e0ff;">Configure & Generate</div>
                <div style="color:#888; font-size:0.9rem; margin-top:0.5rem;">Set performance on the left, then click <b style="color:#7b2ff7;">Generate Recommendation</b></div>
            </div>
            """, unsafe_allow_html=True)

# ━━━ TAB 3 — Batch Processing ━━━
with tab3:
    st.session_state.tabs_visited.add("tab3")
    st.markdown("""
    <div class="section-header">📊 Batch Processing Simulation</div>
    <div class="section-desc">Process synthetic student data to demonstrate scalability.</div>
    """, unsafe_allow_html=True)

    batch_btn = st.button("⚡ Generate & Process Synthetic Data", use_container_width=True)
    if batch_btn:
        data_path = "data/student_interactions.csv"
        if not os.path.exists(data_path):
            st.warning("⚠️ Data file not found. Run `python data/synthetic_data_generator.py` first.")
        else:
            df = pd.read_csv(data_path)
            st.markdown(f'<div style="text-align:center; color:#00d2ff; font-size:0.9rem; margin:1rem 0;">📂 Loaded <b>{len(df)}</b> records</div>', unsafe_allow_html=True)

            sample = df.head(5)
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = []
            for i, (idx, row) in enumerate(sample.iterrows()):
                status_text.markdown(f'<div style="color:#9a9ac4; font-size:0.85rem;">⏳ Student {row.get("student_id", i+1)} ({i+1}/5)</div>', unsafe_allow_html=True)
                state = {"quiz_score": row["quiz_score"], "attempts": row["attempts"], "last_topic": row["topic"]}
                rec = adaptive_engine.recommend_path(state)
                results.append({"Student ID": row.get("student_id", f"S{i+1}"), "Score": row["quiz_score"], "Last Topic": row["topic"], "Action": rec.get("action", "Error"), "Next Topic": rec.get("next_topic", "Error"), "Difficulty": rec.get("difficulty_adjustment", "N/A")})
                progress_bar.progress((i + 1) / 5)
            status_text.empty()

            add_xp(25, "Batch processing")
            st.markdown('<div style="text-align:center; color:#00c853; font-size:1.1rem; font-weight:600;">✅ Batch Complete · +25 XP</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)

            if results:
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                actions = [r["Action"] for r in results]
                sc1, sc2, sc3 = st.columns(3)
                rev = sum(1 for a in actions if "revision" in a.lower())
                pra = sum(1 for a in actions if "practice" in a.lower())
                adv = sum(1 for a in actions if "next" in a.lower() or "advance" in a.lower())
                with sc1:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{rev}</div><div class="stat-label">Need Revision</div></div>', unsafe_allow_html=True)
                with sc2:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{pra}</div><div class="stat-label">Practice Mode</div></div>', unsafe_allow_html=True)
                with sc3:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{adv}</div><div class="stat-label">Ready to Advance</div></div>', unsafe_allow_html=True)

                # Charts
                chart_data = pd.DataFrame({"Action": ["Revision", "Practice", "Advance"], "Count": [rev, pra, adv]})
                st.bar_chart(chart_data.set_index("Action"))

# ━━━ TAB 4 — Daily Practice Quiz ━━━
with tab4:
    st.session_state.tabs_visited.add("tab4")
    st.markdown("""
    <div class="section-header">🎯 Daily Practice Quiz</div>
    <div class="section-desc">AI-generated questions to test your knowledge. Earn XP and climb the leaderboard!</div>
    """, unsafe_allow_html=True)

    # Quiz config row
    qc1, qc2, qc3 = st.columns([2, 2, 1])
    with qc1:
        quiz_topic = st.selectbox("📘 Topic:", get_all_topics(), key="quiz_topic_select")
    with qc2:
        quiz_difficulty = st.selectbox("🎚️ Difficulty:", ["Beginner", "Intermediate", "Advanced"], key="quiz_diff")
    with qc3:
        st.markdown(f"""
        <div class="quiz-timer" style="margin-top:1.7rem;">
            <span class="quiz-timer-icon">🏆</span>
            <span style="font-size:0.85rem; color:#e0e0ff; font-weight:600;">Best: {st.session_state.quiz_best_streak}🔥</span>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🎲 Generate Quiz", use_container_width=True, key="gen_quiz"):
        if not query_engine:
            st.error("⚠️ Engine failed. Check API key.")
        else:
            with st.spinner(""):
                gen_ph = st.empty()
                for msg in ["🧠 Crafting questions...", "🎯 Calibrating difficulty...", "✨ Polishing quiz..."]:
                    gen_ph.markdown(f'<div style="text-align:center; color:#9a9ac4; font-size:0.9rem; padding:0.5rem;">{msg}</div>', unsafe_allow_html=True)
                    time.sleep(0.4)
                prompt = f"""Generate exactly 5 multiple-choice questions about {quiz_topic} at {quiz_difficulty} level for an ML/AI student.
Return as a JSON object with key "questions" containing an array. Each question has:
- "question": the question text
- "options": array of 4 option strings
- "correct": index of correct option (0-3)
- "explanation": brief explanation of the answer
Do not include markdown formatting."""
                try:
                    chat = query_engine.client.chat.completions.create(
                        messages=[{"role": "system", "content": "You are a quiz generator for ML/AI education. Output only valid JSON."},
                                  {"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                        response_format={"type": "json_object"},
                    )
                    quiz_data = json.loads(chat.choices[0].message.content)
                    st.session_state.quiz_questions = quiz_data.get("questions", [])
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    gen_ph.empty()
                except Exception as e:
                    gen_ph.empty()
                    st.error(f"Error generating quiz: {e}")

    if st.session_state.quiz_questions:
        questions = st.session_state.quiz_questions
        total_q = len(questions)

        # Quiz header with question count & streak
        qh1, qh2 = st.columns([3, 1])
        with qh1:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.8rem; margin:0.5rem 0;">
                <div style="color:#e0e0ff; font-weight:600; font-size:1rem;">📝 {total_q} Questions</div>
                <div style="color:#888; font-size:0.85rem;">· {quiz_topic} · {quiz_difficulty}</div>
            </div>
            """, unsafe_allow_html=True)
        with qh2:
            if st.session_state.quiz_correct_streak > 0:
                st.markdown(f'<div class="quiz-streak">🔥 {st.session_state.quiz_correct_streak} streak</div>', unsafe_allow_html=True)

        # Questions
        for i, q in enumerate(questions):
            letters = ["A", "B", "C", "D"]
            progress_w = int(((i + 1) / total_q) * 100)

            st.markdown(f"""
            <div class="quiz-q-card">
                <div class="quiz-q-progress" style="width:{progress_w}%;"></div>
                <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                    <div class="quiz-q-number">{i+1}</div>
                    <div style="font-size:0.75rem; color:#888;">Question {i+1} of {total_q}</div>
                </div>
                <div class="quiz-q-text">{q.get('question', '')}</div>
            </div>
            """, unsafe_allow_html=True)

            options = q.get("options", [])
            answer = st.radio(f"Q{i+1}", options, key=f"quiz_q_{i}", label_visibility="collapsed",
                              format_func=lambda x, opts=options, ltrs=letters: f"{ltrs[opts.index(x)]}. {x}" if x in opts else x)
            st.session_state.quiz_answers[i] = options.index(answer) if answer in options else -1

        # Submit
        if st.button("🚀 Submit Quiz", use_container_width=True, key="submit_quiz"):
            st.session_state.quiz_submitted = True
            correct_count = 0
            streak = 0
            for i, q in enumerate(questions):
                is_correct = st.session_state.quiz_answers.get(i) == q.get("correct", -1)
                if is_correct:
                    correct_count += 1
                    streak += 1
                    add_xp(20, "Correct answer")
                else:
                    add_xp(5, "Attempted")
                    streak = 0

            score_pct = int((correct_count / total_q) * 100) if total_q else 0
            st.session_state.quiz_scores.append(score_pct)
            st.session_state.total_quizzes += 1
            if streak > st.session_state.quiz_best_streak:
                st.session_state.quiz_best_streak = streak
            st.session_state.quiz_correct_streak = streak
            check_badges()

            total_xp = correct_count * 20 + (total_q - correct_count) * 5
            score_color = "#00c853" if score_pct >= 80 else ("#ffc107" if score_pct >= 50 else "#ff4757")
            score_deg = int(score_pct * 3.6)
            stars_count = 5 if score_pct == 100 else (4 if score_pct >= 80 else (3 if score_pct >= 60 else (2 if score_pct >= 40 else 1)))
            stars_html = "".join([f'<span class="score-star">⭐</span>' for _ in range(stars_count)])
            stars_html += "".join([f'<span class="score-star" style="opacity:0.15;">⭐</span>' for _ in range(5 - stars_count)])

            st.markdown(f"""
            <div class="score-reveal">
                <div class="score-circle" style="--score-color:{score_color}; --score-deg:{score_deg}deg;">
                    <div class="score-percentage" style="color:{score_color};">{score_pct}%</div>
                    <div class="score-label">{correct_count}/{total_q} correct</div>
                </div>
                <div class="score-stars">{stars_html}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#e0e0ff; margin:0.5rem 0;">
                    {'🎉 Outstanding!' if score_pct >= 80 else ('👍 Good effort!' if score_pct >= 50 else '💪 Keep practicing!')}
                </div>
                <div style="color:#00d2ff; font-size:0.9rem; font-weight:600;">+{total_xp} XP earned!</div>
                {f'<div class="quiz-streak" style="margin-top:0.8rem;">🔥 {streak} answer streak!</div>' if streak >= 3 else ''}
            </div>
            """, unsafe_allow_html=True)

            # Per-question breakdown
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown("#### 📋 Question Breakdown")
            for i, q in enumerate(questions):
                user_ans = st.session_state.quiz_answers.get(i, -1)
                correct_idx = q.get("correct", -1)
                is_correct = user_ans == correct_idx
                icon = "✅" if is_correct else "❌"
                status_class = "quiz-opt-correct" if is_correct else "quiz-opt-wrong"

                with st.expander(f"{icon} Q{i+1}: {q.get('question', '')[:70]}..."):
                    options = q.get("options", [])
                    for j, opt in enumerate(options):
                        opt_class = ""
                        opt_icon = ""
                        if j == correct_idx:
                            opt_class = "quiz-opt-correct"
                            opt_icon = "✅"
                        elif j == user_ans and not is_correct:
                            opt_class = "quiz-opt-wrong"
                            opt_icon = "❌"
                        letters = ["A", "B", "C", "D"]
                        st.markdown(f"""
                        <div class="quiz-opt-card {opt_class}" style="cursor:default;">
                            <div class="quiz-opt-letter">{letters[j]}</div>
                            <div class="quiz-opt-text">{opt} {opt_icon}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown(f'<div class="quiz-explain">💡 {q.get("explanation", "N/A")}</div>', unsafe_allow_html=True)

# ━━━ TAB 5 — AI Doubt Solver ━━━
with tab5:
    st.session_state.tabs_visited.add("tab5")
    st.markdown("""
    <div class="section-header">💬 AI Doubt Solver</div>
    <div class="section-desc">Chat with the AI to clear your doubts on any ML/AI topic. <b style="color:#ffc107;">+10 XP</b> per question!</div>
    """, unsafe_allow_html=True)

    # Quick question buttons
    st.markdown("**💡 Quick Questions:**")
    quick_qs = ["What is overfitting?", "Explain bias-variance tradeoff", "How does dropout work?", "What is cross-validation?"]
    qcols = st.columns(len(quick_qs))
    for i, qq in enumerate(quick_qs):
        with qcols[i]:
            if st.button(qq, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": qq})
                # Will be processed below

    # Chat display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_doubt = st.chat_input("Ask your doubt here...")
    if user_doubt:
        st.session_state.chat_history.append({"role": "user", "content": user_doubt})
        with st.chat_message("user"):
            st.markdown(user_doubt)

    # Process last message if unanswered
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        last_q = st.session_state.chat_history[-1]["content"]
        if query_engine:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        chat = query_engine.client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a friendly, expert ML/AI tutor. Explain concepts clearly with examples and analogies. Use markdown formatting for readability."},
                                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[-6:]],
                            ],
                            model="llama-3.3-70b-versatile",
                        )
                        response = chat.choices[0].message.content
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        add_xp(10, "Doubt solved")
                        st.session_state.doubts_asked += 1
                        check_badges()
                    except Exception as e:
                        st.error(f"Error: {e}")

# ━━━ TAB 6 — Memory Card Game ━━━
with tab6:
    st.session_state.tabs_visited.add("tab6")
    st.markdown("""
    <div class="section-header">🧠 Memory Match Game</div>
    <div class="section-desc">Match ML/AI concepts with their definitions! Flip two cards at a time — find all 6 pairs to win. Fewer moves = more XP!</div>
    """, unsafe_allow_html=True)

    # Initialize memory game state
    if "mem_cards" not in st.session_state:
        st.session_state.mem_cards = []
        st.session_state.mem_revealed = set()
        st.session_state.mem_matched = set()
        st.session_state.mem_first_pick = None
        st.session_state.mem_second_pick = None
        st.session_state.mem_moves = 0
        st.session_state.mem_topic = ""
        st.session_state.mem_active = False
        st.session_state.mem_checking = False

    # Topic selector and stats
    mc1, mc2, mc3 = st.columns([2, 1, 1])
    with mc1:
        mem_topic = st.selectbox("🎮 Choose Topic:", get_all_topics(), key="mem_topic_sel")
    with mc2:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; margin-top:1.7rem;">
            <div style="font-size:0.7rem; color:#888; text-transform:uppercase; letter-spacing:1px;">Decks Done</div>
            <div style="font-size:1.5rem; font-weight:800; color:#7b2ff7;">{len(st.session_state.decks_completed)}/7</div>
        </div>
        """, unsafe_allow_html=True)
    with mc3:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; margin-top:1.7rem;">
            <div style="font-size:0.7rem; color:#888; text-transform:uppercase; letter-spacing:1px;">Total Cards</div>
            <div style="font-size:1.5rem; font-weight:800; color:#00d2ff;">{st.session_state.total_cards_flipped}</div>
        </div>
        """, unsafe_allow_html=True)

    # Start / Reset game
    if not st.session_state.mem_active or st.session_state.mem_topic != mem_topic:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:3rem 2rem;">
            <div style="font-size:3.5rem; margin-bottom:1rem;">🧠</div>
            <div style="font-size:1.2rem; font-weight:700; color:#e0e0ff; margin-bottom:0.5rem;">How to Play</div>
            <div style="color:#9a9ac4; font-size:0.95rem; line-height:1.8;">
                Flip two cards at a time to find matching pairs.<br/>
                <b style="color:#7b2ff7;">🟣 Concept</b> cards match with <b style="color:#00d2ff;">🔵 Definition</b> cards.<br/>
                Find all <b>6 pairs</b> with the fewest moves to earn max XP!
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Memory Game", use_container_width=True, key="mem_start"):
            pairs = get_memory_pairs(mem_topic)
            if pairs:
                cards = []
                for i, (concept, definition) in enumerate(pairs):
                    cards.append({"id": i * 2, "pair_id": i, "text": concept, "type": "concept"})
                    cards.append({"id": i * 2 + 1, "pair_id": i, "text": definition, "type": "definition"})
                random.shuffle(cards)
                st.session_state.mem_cards = cards
                st.session_state.mem_revealed = set()
                st.session_state.mem_matched = set()
                st.session_state.mem_first_pick = None
                st.session_state.mem_second_pick = None
                st.session_state.mem_moves = 0
                st.session_state.mem_topic = mem_topic
                st.session_state.mem_active = True
                st.session_state.mem_checking = False
                st.rerun()

    # Active game
    if st.session_state.mem_active and st.session_state.mem_topic == mem_topic:
        cards = st.session_state.mem_cards
        total_pairs = len(cards) // 2
        matched_pairs = len(st.session_state.mem_matched) // 2
        moves = st.session_state.mem_moves
        all_matched = matched_pairs >= total_pairs

        # If two cards were picked and not matched, check them
        if st.session_state.mem_checking:
            fp = st.session_state.mem_first_pick
            sp = st.session_state.mem_second_pick
            if fp is not None and sp is not None:
                card1 = cards[fp]
                card2 = cards[sp]
                if card1["pair_id"] == card2["pair_id"] and card1["type"] != card2["type"]:
                    # Match!
                    st.session_state.mem_matched.add(fp)
                    st.session_state.mem_matched.add(sp)
                    add_xp(10, "Memory pair matched")
                    st.session_state.total_cards_flipped += 2
                else:
                    # No match — hide them
                    st.session_state.mem_revealed.discard(fp)
                    st.session_state.mem_revealed.discard(sp)
            st.session_state.mem_first_pick = None
            st.session_state.mem_second_pick = None
            st.session_state.mem_checking = False

        # Game complete check
        if all_matched:
            # Score calculation
            perfect_moves = total_pairs  # minimum possible moves
            score_ratio = max(0, 1 - (moves - perfect_moves) / (total_pairs * 3))
            xp_bonus = int(score_ratio * 50) + 25
            add_xp(xp_bonus, "Memory game complete")
            st.session_state.decks_completed.add(mem_topic)
            check_badges()

            stars_count = 5 if moves <= 8 else (4 if moves <= 10 else (3 if moves <= 13 else (2 if moves <= 16 else 1)))
            stars_html = "".join([f'<span class="score-star">⭐</span>' for _ in range(stars_count)])
            stars_html += "".join([f'<span class="score-star" style="opacity:0.15;">⭐</span>' for _ in range(5 - stars_count)])

            st.markdown(f"""
            <div class="score-reveal">
                <div style="font-size:1rem; color:#888; margin-bottom:0.5rem;">🧠 {mem_topic} — Memory Game Complete!</div>
                <div class="score-circle" style="--score-color:#00c853; --score-deg:360deg;">
                    <div class="score-percentage" style="color:#00c853;">{'🏆' if moves <= 8 else '✅'}</div>
                    <div class="score-label">{moves} moves</div>
                </div>
                <div class="score-stars">{stars_html}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#e0e0ff; margin:0.5rem 0;">
                    {'🏆 PERFECT MEMORY!' if moves <= total_pairs + 2 else ('🎉 Excellent!' if moves <= 10 else ('👍 Well done!' if moves <= 14 else '💪 Keep practicing!'))}
                </div>
                <div style="color:#00d2ff; font-size:0.9rem; font-weight:600;">+{xp_bonus} XP earned!</div>
            </div>
            """, unsafe_allow_html=True)

            # Show all pairs
            st.markdown("#### 📋 Matched Pairs")
            pairs = get_memory_pairs(mem_topic)
            for i, (concept, definition) in enumerate(pairs):
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:0.8rem; padding:0.6rem 1rem; margin:0.3rem 0;
                            background:rgba(0,200,83,0.06); border:1px solid rgba(0,200,83,0.15); border-radius:12px;">
                    <span style="color:#7b2ff7; font-weight:700; font-size:0.9rem;">🟣 {concept}</span>
                    <span style="color:#555;">↔</span>
                    <span style="color:#00d2ff; font-weight:600; font-size:0.9rem;">🔵 {definition}</span>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🔁 Play Again", use_container_width=True, key="mem_again"):
                st.session_state.mem_active = False
                st.rerun()

        else:
            # Stats bar
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin:0.5rem 0 1rem;">
                <div style="display:flex; gap:1.5rem; align-items:center;">
                    <div>
                        <div style="font-size:0.65rem; color:#888; text-transform:uppercase;">Moves</div>
                        <div style="font-size:1.3rem; font-weight:800; color:#e0e0ff;">{moves}</div>
                    </div>
                    <div>
                        <div style="font-size:0.65rem; color:#888; text-transform:uppercase;">Pairs Found</div>
                        <div style="font-size:1.3rem; font-weight:800; color:#00c853;">{matched_pairs}/{total_pairs}</div>
                    </div>
                </div>
                <div style="font-size:0.85rem; color:#9a9ac4;">
                    {'🟣 Pick first card' if st.session_state.mem_first_pick is None else '🔵 Pick second card'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            progress_pct = int((matched_pairs / total_pairs) * 100)
            st.markdown(f"""
            <div class="mastery-bar-bg" style="margin-bottom:1rem;">
                <div class="mastery-bar-fill" style="width:{progress_pct}%; background:linear-gradient(90deg, #7b2ff7, #00d2ff);"></div>
            </div>
            """, unsafe_allow_html=True)

            # Card grid — 4 columns × 3 rows
            for row_start in range(0, len(cards), 4):
                row_cards = cards[row_start:row_start + 4]
                cols = st.columns(len(row_cards))
                for col_idx, card in enumerate(row_cards):
                    card_pos = row_start + col_idx
                    is_revealed = card_pos in st.session_state.mem_revealed
                    is_matched = card_pos in st.session_state.mem_matched

                    with cols[col_idx]:
                        if is_matched:
                            # Matched card — always visible, green
                            badge_color = "#7b2ff7" if card["type"] == "concept" else "#00d2ff"
                            badge_icon = "🟣" if card["type"] == "concept" else "🔵"
                            st.markdown(f"""
                            <div style="background:rgba(0,200,83,0.08); border:2px solid rgba(0,200,83,0.3);
                                        border-radius:16px; padding:1rem 0.8rem; text-align:center; min-height:90px;
                                        display:flex; flex-direction:column; justify-content:center; align-items:center;">
                                <div style="font-size:0.6rem; color:#00c853; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.3rem;">✅ Matched</div>
                                <div style="font-size:0.85rem; font-weight:700; color:{badge_color};">{badge_icon} {card['text']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif is_revealed:
                            # Revealed card — show content
                            bg_color = "rgba(123,47,247,0.12)" if card["type"] == "concept" else "rgba(0,210,255,0.10)"
                            border_color = "rgba(123,47,247,0.4)" if card["type"] == "concept" else "rgba(0,210,255,0.35)"
                            text_color = "#7b2ff7" if card["type"] == "concept" else "#00d2ff"
                            type_label = "CONCEPT" if card["type"] == "concept" else "DEFINITION"
                            type_icon = "🟣" if card["type"] == "concept" else "🔵"
                            st.markdown(f"""
                            <div style="background:{bg_color}; border:2px solid {border_color};
                                        border-radius:16px; padding:1rem 0.8rem; text-align:center; min-height:90px;
                                        display:flex; flex-direction:column; justify-content:center; align-items:center;
                                        animation:scaleIn 0.3s ease;">
                                <div style="font-size:0.55rem; color:{text_color}; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.3rem;">{type_icon} {type_label}</div>
                                <div style="font-size:0.85rem; font-weight:700; color:#e0e0ff; line-height:1.3;">{card['text']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Face-down card — button to flip
                            if st.button("❓", use_container_width=True, key=f"mem_{card_pos}"):
                                if st.session_state.mem_first_pick is None:
                                    st.session_state.mem_first_pick = card_pos
                                    st.session_state.mem_revealed.add(card_pos)
                                    st.rerun()
                                elif st.session_state.mem_second_pick is None and card_pos != st.session_state.mem_first_pick:
                                    st.session_state.mem_second_pick = card_pos
                                    st.session_state.mem_revealed.add(card_pos)
                                    st.session_state.mem_moves += 1
                                    st.session_state.mem_checking = True
                                    st.rerun()

            # Match feedback
            if st.session_state.mem_first_pick is not None and st.session_state.mem_second_pick is not None:
                fp = st.session_state.mem_first_pick
                sp = st.session_state.mem_second_pick
                card1 = cards[fp]
                card2 = cards[sp]
                is_match = card1["pair_id"] == card2["pair_id"] and card1["type"] != card2["type"]

                if is_match:
                    st.markdown(f"""
                    <div style="text-align:center; padding:0.8rem; background:rgba(0,200,83,0.08); border:1px solid rgba(0,200,83,0.2);
                                border-radius:14px; margin:1rem 0; animation:correctPulse 0.6s ease;">
                        <span style="font-size:1.5rem;">🎉</span>
                        <span style="color:#00c853; font-weight:700; font-size:1rem;">It's a match! +10 XP</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align:center; padding:0.8rem; background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.2);
                                border-radius:14px; margin:1rem 0;">
                        <span style="font-size:1.5rem;">🔄</span>
                        <span style="color:#ff4757; font-weight:700; font-size:1rem;">Not a match — try again!</span>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("➡️ Continue", use_container_width=True, key="mem_continue"):
                    st.rerun()

    # Mastery meter (always visible)
    completed_count = len(st.session_state.decks_completed)
    mastery_pct = int((completed_count / 7) * 100)
    mastery_color = "#00c853" if mastery_pct >= 70 else ("#ffc107" if mastery_pct >= 30 else "#7b2ff7")

    # ─── Cue Cards Section ───
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header" style="font-size:1.3rem;">📚 Cue Cards</div>
    <div class="section-desc">Flip through concept-definition cards to study and revise. Click "Flip" to reveal the answer!</div>
    """, unsafe_allow_html=True)

    # Init cue card state
    if "cue_index" not in st.session_state:
        st.session_state.cue_index = 0
        st.session_state.cue_flipped = False

    cue_topic = mem_topic if 'mem_topic' in dir() else get_all_topics()[0]
    cue_pairs = get_memory_pairs(cue_topic)

    if cue_pairs:
        ci = st.session_state.cue_index % len(cue_pairs)
        concept, definition = cue_pairs[ci]
        topic_icons = {"Linear Regression": "📈", "Gradient Descent": "⬇️", "Neural Networks": "🧠", "Backpropagation": "🔄", "Optimization Algorithms": "⚡", "CNNs": "🖼️", "RNNs": "🔁"}
        t_icon = topic_icons.get(cue_topic, "📘")

        if st.session_state.cue_flipped:
            # Back — show definition
            st.markdown(f"""
            <div class="fc-scene">
                <div class="fc-card flipped">
                    <div class="fc-face fc-front"></div>
                    <div class="fc-face fc-back">
                        <div class="fc-meta">
                            <span class="fc-topic-badge" style="border-color:rgba(0,210,255,0.3); color:#00d2ff;">DEFINITION</span>
                            <span class="fc-counter">{ci+1}/{len(cue_pairs)}</span>
                        </div>
                        <div class="fc-answer-label">🔵 Definition</div>
                        <div class="fc-answer">{definition}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Front — show concept
            st.markdown(f"""
            <div class="fc-scene">
                <div class="fc-card">
                    <div class="fc-face fc-front">
                        <div class="fc-meta">
                            <span class="fc-topic-badge">{cue_topic}</span>
                            <span class="fc-counter">{ci+1}/{len(cue_pairs)}</span>
                        </div>
                        <div class="fc-icon">{t_icon}</div>
                        <div class="fc-question">{concept}</div>
                        <div class="fc-hint">tap flip to reveal definition</div>
                    </div>
                    <div class="fc-face fc-back"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Navigation
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            if st.button("⬅️ Previous", use_container_width=True, key="cue_prev"):
                st.session_state.cue_index = max(0, st.session_state.cue_index - 1)
                st.session_state.cue_flipped = False
                st.rerun()
        with cc2:
            flip_lbl = "🔄 Flip to Concept" if st.session_state.cue_flipped else "🔄 Flip to Definition"
            if st.button(flip_lbl, use_container_width=True, key="cue_flip"):
                st.session_state.cue_flipped = not st.session_state.cue_flipped
                if st.session_state.cue_flipped:
                    add_xp(3, "Cue card studied")
                st.rerun()
        with cc3:
            if st.button("➡️ Next", use_container_width=True, key="cue_next"):
                st.session_state.cue_index += 1
                st.session_state.cue_flipped = False
                if st.session_state.cue_index >= len(cue_pairs):
                    st.session_state.cue_index = 0
                st.rerun()

    # Mastery meter (always visible)
    completed_count = len(st.session_state.decks_completed)
    mastery_pct = int((completed_count / 7) * 100)
    mastery_color = "#00c853" if mastery_pct >= 70 else ("#ffc107" if mastery_pct >= 30 else "#7b2ff7")

    st.markdown(f"""
    <div class="mastery-meter">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <div style="font-size:0.85rem; font-weight:600; color:#e0e0ff;">📊 Topic Mastery</div>
            <div style="font-size:0.85rem; font-weight:700; color:{mastery_color};">{mastery_pct}%</div>
        </div>
        <div class="mastery-bar-bg">
            <div class="mastery-bar-fill" style="width:{mastery_pct}%; background:linear-gradient(90deg, {mastery_color}, {mastery_color}88);"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:#666; margin-top:0.3rem;">
            <span>{completed_count}/7 topics completed</span>
            <span>{st.session_state.total_cards_flipped} cards played</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ━━━ TAB 7 — Study Roadmap ━━━
with tab7:
    st.session_state.tabs_visited.add("tab7")
    st.markdown("""
    <div class="section-header">📚 Study Roadmap</div>
    <div class="section-desc">Your learning journey through 7 core ML/AI topics. Complete each milestone to unlock the next!</div>
    """, unsafe_allow_html=True)

    topics_info = [
        {"name": "Linear Regression", "icon": "📈", "time": "3 hrs", "concepts": "MSE, R², Ordinary Least Squares", "prereq": None},
        {"name": "Gradient Descent", "icon": "⬇️", "time": "2 hrs", "concepts": "Learning rate, SGD, Mini-batch", "prereq": "Linear Regression"},
        {"name": "Neural Networks", "icon": "🧠", "time": "4 hrs", "concepts": "Perceptron, Activation functions, Layers", "prereq": "Gradient Descent"},
        {"name": "Backpropagation", "icon": "🔄", "time": "3 hrs", "concepts": "Chain rule, Gradients, Computational graph", "prereq": "Neural Networks"},
        {"name": "Optimization Algorithms", "icon": "⚡", "time": "2 hrs", "concepts": "Adam, Momentum, Learning rate scheduling", "prereq": "Backpropagation"},
        {"name": "CNNs", "icon": "🖼️", "time": "4 hrs", "concepts": "Convolution, Pooling, Feature maps", "prereq": "Optimization Algorithms"},
        {"name": "RNNs", "icon": "🔁", "time": "3 hrs", "concepts": "Sequences, LSTM, GRU, Attention", "prereq": "CNNs"},
    ]

    completed_topics = st.session_state.decks_completed

    for i, t in enumerate(topics_info):
        is_completed = t["name"] in completed_topics
        is_current = (i == 0 and not is_completed) or (i > 0 and topics_info[i-1]["name"] in completed_topics and not is_completed)
        is_locked = not is_completed and not is_current

        card_class = "completed" if is_completed else ("current" if is_current else "locked")
        status_icon = "✅" if is_completed else ("▶️" if is_current else "🔒")
        status_text = "Completed" if is_completed else ("In Progress" if is_current else "Locked")
        status_color = "#00c853" if is_completed else ("#7b2ff7" if is_current else "#555")

        st.markdown(f"""
        <div class="roadmap-card {card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:1rem;">
                    <div style="font-size:2rem;">{t['icon']}</div>
                    <div>
                        <div style="font-size:1.1rem; font-weight:700; color:#e0e0ff;">{t['name']}</div>
                        <div style="font-size:0.75rem; color:#888;">⏱️ {t['time']} · {t['concepts']}</div>
                    </div>
                </div>
                <div>
                    <span style="color:{status_color}; font-weight:600; font-size:0.85rem;">{status_icon} {status_text}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if i < len(topics_info) - 1:
            st.markdown('<div class="roadmap-connector">↓</div>', unsafe_allow_html=True)

    # Progress summary
    total = len(topics_info)
    done = len([t for t in topics_info if t["name"] in completed_topics])
    pct = int((done / total) * 100)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; margin-top:1rem;">
        <div style="font-size:0.85rem; color:#888;">Overall Progress</div>
        <div style="font-size:2rem; font-weight:800; color:#00d2ff;">{pct}%</div>
        <div class="xp-bar-container"><div class="xp-bar-fill" style="width:{pct}%;"></div></div>
        <div style="font-size:0.8rem; color:#888;">{done}/{total} topics completed</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ──
st.markdown("""
<div class="footer">
    Built with ❤️ using <b>Streamlit</b> · <b>Groq</b> · <b>Llama 3.3</b> &nbsp;|&nbsp;
    AI Teaching Assistant — Gamified Learning Experience 🏆
</div>
""", unsafe_allow_html=True)
