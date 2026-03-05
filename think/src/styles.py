"""Premium CSS styles for the AI Teaching Assistant — Enhanced Edition."""

def get_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141430 0%, #1c1c3a 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] label { color: #c8c8e0 !important; }

/* ══════════════════════════════════════════════════════════════════════════
   ANIMATIONS — Comprehensive library
   ══════════════════════════════════════════════════════════════════════════ */
@keyframes fadeInDown { from { opacity:0; transform:translateY(-15px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeInUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeInLeft { from { opacity:0; transform:translateX(-30px); } to { opacity:1; transform:translateX(0); } }
@keyframes fadeInRight { from { opacity:0; transform:translateX(30px); } to { opacity:1; transform:translateX(0); } }
@keyframes scaleIn { from { opacity:0; transform:scale(0.8); } to { opacity:1; transform:scale(1); } }
@keyframes pulseGlow { 0%,100% { box-shadow:0 0 15px rgba(123,47,247,0.15); } 50% { box-shadow:0 0 30px rgba(123,47,247,0.35); } }
@keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-10px); } }
@keyframes shimmer { 0% { background-position:-200% 0; } 100% { background-position:200% 0; } }
@keyframes badgePop { 0% { transform:scale(0); } 50% { transform:scale(1.3); } 100% { transform:scale(1); } }
@keyframes streak { 0%,100% { text-shadow:0 0 5px #ff6b35; } 50% { text-shadow:0 0 20px #ff6b35,0 0 40px #ff4500; } }
@keyframes particle { 0% { transform:translateY(0) translateX(0); opacity:0; } 10% { opacity:1; } 90% { opacity:1; } 100% { transform:translateY(-100vh) translateX(20px); opacity:0; } }
@keyframes borderGlow {
    0% { border-color: rgba(123,47,247,0.3); }
    33% { border-color: rgba(0,210,255,0.4); }
    66% { border-color: rgba(255,110,199,0.4); }
    100% { border-color: rgba(123,47,247,0.3); }
}
@keyframes correctPulse {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0,200,83,0.4); }
    50% { transform: scale(1.02); box-shadow: 0 0 20px 5px rgba(0,200,83,0.2); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0,200,83,0); }
}
@keyframes wrongShake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
    20%, 40%, 60%, 80% { transform: translateX(4px); }
}
@keyframes countUp {
    from { opacity: 0; transform: translateY(20px) scale(0.5); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes confettiDrop {
    0% { transform: translateY(-20px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(80px) rotate(360deg); opacity: 0; }
}
@keyframes slideInFromRight {
    from { opacity: 0; transform: translateX(60px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInFromLeft {
    from { opacity: 0; transform: translateX(-60px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes orbitalGlow {
    0% { box-shadow: 0 0 20px rgba(123,47,247,0.2), inset 0 0 20px rgba(123,47,247,0.05); }
    25% { box-shadow: 0 0 30px rgba(0,210,255,0.25), inset 0 0 25px rgba(0,210,255,0.05); }
    50% { box-shadow: 0 0 20px rgba(255,110,199,0.2), inset 0 0 20px rgba(255,110,199,0.05); }
    75% { box-shadow: 0 0 30px rgba(0,200,83,0.2), inset 0 0 25px rgba(0,200,83,0.05); }
    100% { box-shadow: 0 0 20px rgba(123,47,247,0.2), inset 0 0 20px rgba(123,47,247,0.05); }
}
@keyframes timerPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
    50% { opacity: 1; transform: scale(1) rotate(180deg); }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Hero ── */
.hero-title {
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #00d2ff, #7b2ff7, #ff6ec7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 0.2rem; letter-spacing: -0.5px; animation: fadeInDown 0.8s ease;
}
.hero-subtitle { color: #9a9ac4; font-size: 1.05rem; font-weight: 400; margin-bottom: 1.5rem; animation: fadeInDown 1s ease; }

/* ── Particles ── */
.particles-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; overflow: hidden; }
.particle { position: absolute; width: 4px; height: 4px; border-radius: 50%; animation: particle linear infinite; }
.particle:nth-child(1) { left:10%; background:#7b2ff7; animation-duration:15s; animation-delay:0s; }
.particle:nth-child(2) { left:25%; background:#00d2ff; animation-duration:20s; animation-delay:2s; }
.particle:nth-child(3) { left:40%; background:#ff6ec7; animation-duration:18s; animation-delay:4s; }
.particle:nth-child(4) { left:60%; background:#00c853; animation-duration:22s; animation-delay:1s; }
.particle:nth-child(5) { left:75%; background:#ffc107; animation-duration:16s; animation-delay:3s; }
.particle:nth-child(6) { left:90%; background:#7b2ff7; animation-duration:19s; animation-delay:5s; }

/* ── Glass Card ── */
.glass-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 2rem; margin: 1rem 0;
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); animation: fadeInUp 0.6s ease;
}
.glass-card:hover { border-color: rgba(123,47,247,0.3); box-shadow: 0 8px 32px rgba(123,47,247,0.1); transition: all 0.3s ease; }

/* ── Result Cards ── */
.result-card {
    background: rgba(255,255,255,0.06); border-radius: 14px; padding: 1.4rem; text-align: center;
    border: 1px solid rgba(255,255,255,0.08); transition: transform 0.2s ease, box-shadow 0.2s ease; animation: fadeInUp 0.5s ease;
}
.result-card:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.3); }
.result-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; color: #888; margin-bottom: 0.5rem; }
.result-value { font-size: 1.5rem; font-weight: 700; color: #fff; }

/* ── Badges ── */
.badge-purple { background: linear-gradient(135deg,#7b2ff7,#9b59b6); color:#fff; padding:6px 16px; border-radius:20px; font-weight:600; font-size:0.85rem; display:inline-block; }
.badge-teal { background: linear-gradient(135deg,#00b4d8,#0077b6); color:#fff; padding:6px 16px; border-radius:20px; font-weight:600; font-size:0.85rem; display:inline-block; }
.badge-pink { background: linear-gradient(135deg,#ff6ec7,#e040a0); color:#fff; padding:6px 16px; border-radius:20px; font-weight:600; font-size:0.85rem; display:inline-block; }
.badge-green { background: linear-gradient(135deg,#00c853,#00e676); color:#fff; padding:6px 16px; border-radius:20px; font-weight:600; font-size:0.85rem; display:inline-block; }
.badge-amber { background: linear-gradient(135deg,#ff9800,#ffc107); color:#1a1a2e; padding:6px 16px; border-radius:20px; font-weight:600; font-size:0.85rem; display:inline-block; }
.badge-red { background: linear-gradient(135deg,#ff4757,#ff6b81); color:#fff; padding:6px 16px; border-radius:20px; font-weight:600; font-size:0.85rem; display:inline-block; }

/* ── Action Cards ── */
.action-revision { border-left: 4px solid #ff4757; background: rgba(255,71,87,0.08); }
.action-practice { border-left: 4px solid #ffc107; background: rgba(255,193,7,0.08); }
.action-next { border-left: 4px solid #00c853; background: rgba(0,200,83,0.08); }

/* ── Stat Box ── */
.stat-box {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 1rem 1.2rem; text-align: center; animation: fadeInUp 0.7s ease;
}
.stat-number { font-size: 2rem; font-weight: 800; background: linear-gradient(135deg,#00d2ff,#7b2ff7); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.stat-label { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }

/* ── Progress Bars ── */
.score-bar-container { background: rgba(255,255,255,0.08); border-radius: 10px; height: 12px; overflow: hidden; margin: 0.5rem 0; }
.score-bar-fill { height: 100%; border-radius: 10px; transition: width 0.8s cubic-bezier(0.4,0,0.2,1); }
.xp-bar-container { background: rgba(255,255,255,0.08); border-radius: 8px; height: 8px; overflow: hidden; margin: 0.3rem 0; }
.xp-bar-fill { height: 100%; border-radius: 8px; background: linear-gradient(90deg,#7b2ff7,#00d2ff); transition: width 0.8s ease; }

/* ── Section Header ── */
.section-header { font-size: 1.6rem; font-weight: 700; color: #e0e0ff; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.6rem; }
.section-desc { color: #8888aa; font-size: 0.95rem; margin-bottom: 1.5rem; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg,#7b2ff7,#00d2ff) !important; color: #fff !important;
    border: none !important; border-radius: 10px !important; padding: 0.6rem 2rem !important;
    font-weight: 600 !important; font-size: 0.95rem !important; letter-spacing: 0.5px;
    transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(123,47,247,0.3) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(123,47,247,0.5) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(255,255,255,0.03); border-radius: 12px; padding: 6px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; color: #9a9ac4; font-weight: 500; padding: 10px 14px; font-size: 0.85rem; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg,rgba(123,47,247,0.25),rgba(0,210,255,0.15)) !important; color: #fff !important; border-bottom-color: transparent !important; }

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #e0e0ff !important; font-family: 'Inter', sans-serif !important; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color: rgba(123,47,247,0.5) !important; box-shadow: 0 0 0 2px rgba(123,47,247,0.15) !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border-color: rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #e0e0ff !important; }
.stSlider > div > div > div > div { background: linear-gradient(90deg,#7b2ff7,#00d2ff) !important; }
.stNumberInput input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #e0e0ff !important; }

/* ── Expander ── */
.streamlit-expanderHeader { background: rgba(255,255,255,0.03) !important; border-radius: 10px !important; color: #c0c0e0 !important; font-weight: 500 !important; }

/* ══════════════════════════════════════════════════════════════════════════
   FLASHCARD — 3D Flip with Perspective
   ══════════════════════════════════════════════════════════════════════════ */
.fc-scene {
    perspective: 1200px;
    width: 100%;
    min-height: 320px;
    margin: 1rem 0;
}
.fc-card {
    width: 100%;
    min-height: 320px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.7s cubic-bezier(0.4, 0.0, 0.2, 1);
}
.fc-card.flipped {
    transform: rotateY(180deg);
}
.fc-face {
    position: absolute;
    width: 100%;
    min-height: 320px;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2.5rem;
    box-sizing: border-box;
}
.fc-front {
    background: linear-gradient(145deg, rgba(123,47,247,0.18), rgba(0,210,255,0.12));
    border: 2px solid rgba(123,47,247,0.25);
    animation: orbitalGlow 6s ease infinite;
}
.fc-front::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px; right: -1px; bottom: -1px;
    border-radius: 24px;
    background: linear-gradient(135deg, #7b2ff7, #00d2ff, #ff6ec7, #7b2ff7);
    background-size: 300% 300%;
    animation: gradientShift 4s ease infinite;
    z-index: -1;
    opacity: 0.15;
}
.fc-back {
    background: linear-gradient(145deg, rgba(0,200,83,0.10), rgba(0,210,255,0.08));
    border: 2px solid rgba(0,200,83,0.25);
    transform: rotateY(180deg);
}
.fc-front .fc-icon { font-size: 3rem; margin-bottom: 1.2rem; animation: float 3s ease infinite; }
.fc-front .fc-question {
    font-size: 1.5rem; font-weight: 700; color: #e0e0ff;
    line-height: 1.4; max-width: 90%;
}
.fc-front .fc-hint {
    font-size: 0.8rem; color: rgba(255,255,255,0.35);
    margin-top: 1.5rem; letter-spacing: 1px; text-transform: uppercase;
}
.fc-back .fc-answer-label {
    font-size: 0.7rem; color: #00c853; text-transform: uppercase;
    letter-spacing: 2px; font-weight: 700; margin-bottom: 1rem;
}
.fc-back .fc-answer {
    font-size: 1rem; color: #c8c8e0; line-height: 1.9;
    text-align: left; max-width: 95%;
}
.fc-back .fc-answer b, .fc-back .fc-answer strong { color: #00d2ff; }

/* Flashcard meta */
.fc-meta {
    position: absolute; top: 1rem; width: calc(100% - 3rem);
    display: flex; justify-content: space-between; align-items: center;
    padding: 0 1.5rem;
}
.fc-topic-badge {
    font-size: 0.65rem; color: #7b2ff7; text-transform: uppercase;
    letter-spacing: 2px; font-weight: 700;
    background: rgba(123,47,247,0.1); padding: 4px 12px; border-radius: 20px;
    border: 1px solid rgba(123,47,247,0.2);
}
.fc-counter {
    font-size: 0.75rem; color: rgba(255,255,255,0.35); font-weight: 600;
}

/* Card dots progress */
.fc-dots {
    display: flex; justify-content: center; gap: 8px; margin: 1rem 0;
}
.fc-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: rgba(255,255,255,0.1); transition: all 0.3s ease;
}
.fc-dot.active { background: #7b2ff7; transform: scale(1.3); box-shadow: 0 0 10px rgba(123,47,247,0.5); }
.fc-dot.done { background: #00c853; }

/* Rating buttons */
.rating-btn-wrap {
    display: flex; gap: 0.8rem; justify-content: center; margin: 1rem 0;
}
.rating-btn {
    padding: 0.7rem 1.5rem; border-radius: 14px; font-weight: 600;
    font-size: 0.9rem; cursor: pointer; transition: all 0.3s ease;
    border: 2px solid transparent; text-align: center;
}
.rating-good { background: rgba(0,200,83,0.1); color: #00c853; border-color: rgba(0,200,83,0.3); }
.rating-good:hover { background: rgba(0,200,83,0.2); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,200,83,0.2); }
.rating-ok { background: rgba(255,193,7,0.1); color: #ffc107; border-color: rgba(255,193,7,0.3); }
.rating-ok:hover { background: rgba(255,193,7,0.2); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,193,7,0.2); }
.rating-bad { background: rgba(255,71,87,0.1); color: #ff4757; border-color: rgba(255,71,87,0.3); }
.rating-bad:hover { background: rgba(255,71,87,0.2); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,71,87,0.2); }

/* Mastery meter */
.mastery-meter {
    background: rgba(255,255,255,0.05); border-radius: 12px; padding: 1rem;
    border: 1px solid rgba(255,255,255,0.08); margin: 1rem 0; animation: fadeInUp 0.5s ease;
}
.mastery-bar-bg { background: rgba(255,255,255,0.08); border-radius: 8px; height: 10px; overflow: hidden; position: relative; }
.mastery-bar-fill { height: 100%; border-radius: 8px; transition: width 1s cubic-bezier(0.4,0,0.2,1); position: relative; }
.mastery-bar-fill::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    background-size: 200% 100%; animation: shimmer 2s infinite;
}

/* ══════════════════════════════════════════════════════════════════════════
   QUIZ — Enhanced Interactive Design
   ══════════════════════════════════════════════════════════════════════════ */

/* Quiz container */
.quiz-container {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px; padding: 2rem; margin: 1rem 0;
    animation: fadeInUp 0.5s ease;
}

/* Question card */
.quiz-q-card {
    background: linear-gradient(135deg, rgba(123,47,247,0.08), rgba(0,210,255,0.05));
    border: 1px solid rgba(123,47,247,0.15); border-radius: 18px;
    padding: 1.8rem; margin: 1rem 0; position: relative;
    animation: slideInFromRight 0.5s ease;
}
.quiz-q-number {
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 10px;
    background: linear-gradient(135deg, #7b2ff7, #00d2ff);
    color: #fff; font-weight: 800; font-size: 0.85rem; margin-bottom: 1rem;
}
.quiz-q-text {
    font-size: 1.15rem; color: #e0e0ff; font-weight: 600;
    line-height: 1.6; margin-bottom: 0.5rem;
}
.quiz-q-progress {
    position: absolute; top: 0; left: 0; height: 3px;
    background: linear-gradient(90deg, #7b2ff7, #00d2ff);
    border-radius: 18px 18px 0 0; transition: width 0.5s ease;
}

/* Quiz timer */
.quiz-timer {
    display: flex; align-items: center; justify-content: center; gap: 0.5rem;
    padding: 0.8rem 1.5rem; border-radius: 14px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    animation: fadeInDown 0.5s ease;
}
.quiz-timer-icon { font-size: 1.3rem; animation: timerPulse 1s ease infinite; }
.quiz-timer-value {
    font-size: 1.4rem; font-weight: 800; font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #00d2ff, #7b2ff7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.quiz-timer-warn .quiz-timer-value {
    background: linear-gradient(135deg, #ff4757, #ff6b81);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.quiz-timer-warn { border-color: rgba(255,71,87,0.3); animation: timerPulse 0.5s ease infinite; }

/* Quiz options — card style */
.quiz-opt-card {
    background: rgba(255,255,255,0.04); border: 2px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 1rem 1.3rem; margin: 0.6rem 0;
    display: flex; align-items: center; gap: 1rem;
    cursor: pointer; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative; overflow: hidden;
}
.quiz-opt-card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 0; height: 100%;
    background: linear-gradient(90deg, rgba(123,47,247,0.08), transparent);
    transition: width 0.3s ease;
}
.quiz-opt-card:hover {
    border-color: rgba(123,47,247,0.4);
    transform: translateX(4px);
    background: rgba(123,47,247,0.06);
}
.quiz-opt-card:hover::before { width: 100%; }
.quiz-opt-letter {
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.9rem; color: #7b2ff7;
    background: rgba(123,47,247,0.1); border: 1px solid rgba(123,47,247,0.2);
    flex-shrink: 0; transition: all 0.3s ease;
}
.quiz-opt-text { font-size: 0.95rem; color: #c8c8e0; font-weight: 500; }
.quiz-opt-selected { border-color: #7b2ff7 !important; background: rgba(123,47,247,0.08) !important; }
.quiz-opt-selected .quiz-opt-letter { background: #7b2ff7; color: #fff; }

/* Correct / Wrong states */
.quiz-opt-correct {
    border-color: #00c853 !important; background: rgba(0,200,83,0.08) !important;
    animation: correctPulse 0.6s ease;
}
.quiz-opt-correct .quiz-opt-letter { background: #00c853; color: #fff; }
.quiz-opt-wrong {
    border-color: #ff4757 !important; background: rgba(255,71,87,0.08) !important;
    animation: wrongShake 0.5s ease;
}
.quiz-opt-wrong .quiz-opt-letter { background: #ff4757; color: #fff; }

/* Quiz score reveal */
.score-reveal {
    text-align: center; padding: 2.5rem; animation: scaleIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.score-circle {
    width: 140px; height: 140px; border-radius: 50%; margin: 0 auto 1.5rem;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative;
}
.score-circle::before {
    content: ''; position: absolute; inset: -3px; border-radius: 50%;
    background: conic-gradient(var(--score-color) var(--score-deg), rgba(255,255,255,0.06) 0);
    z-index: -1;
}
.score-circle::after {
    content: ''; position: absolute; inset: 5px; border-radius: 50%;
    background: linear-gradient(135deg, #1a1a3e, #24243e); z-index: -1;
}
.score-percentage {
    font-size: 2.5rem; font-weight: 800; animation: countUp 0.8s ease;
}
.score-label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }

/* Score stars */
.score-stars { font-size: 2rem; margin: 0.5rem 0; letter-spacing: 0.3rem; }
.score-star { display: inline-block; animation: badgePop 0.4s ease; }
.score-star:nth-child(1) { animation-delay: 0.2s; }
.score-star:nth-child(2) { animation-delay: 0.4s; }
.score-star:nth-child(3) { animation-delay: 0.6s; }
.score-star:nth-child(4) { animation-delay: 0.8s; }
.score-star:nth-child(5) { animation-delay: 1.0s; }

/* Streak indicator in quiz */
.quiz-streak {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.4rem 1rem; border-radius: 20px;
    background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.3);
    font-size: 0.85rem; font-weight: 700; color: #ff6b35;
    animation: badgePop 0.3s ease;
}

/* Explanation card */
.quiz-explain {
    background: rgba(255,255,255,0.03); border-left: 3px solid #00d2ff;
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin: 0.5rem 0;
    font-size: 0.9rem; color: #aaa; animation: fadeInLeft 0.3s ease;
}

/* ── Gamification ── */
.xp-display { text-align: center; padding: 0.8rem; background: rgba(123,47,247,0.1); border-radius: 12px; border: 1px solid rgba(123,47,247,0.2); margin: 0.5rem 0; }
.level-badge { font-size: 1.2rem; font-weight: 800; background: linear-gradient(135deg,#ffc107,#ff9800); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.streak-fire { animation: streak 1.5s ease infinite; font-size: 1.5rem; }
.badge-earned { display: inline-block; font-size: 1.8rem; animation: badgePop 0.5s ease; margin: 0.3rem; }
.badge-locked { display: inline-block; font-size: 1.8rem; opacity: 0.2; filter: grayscale(1); margin: 0.3rem; }
.confetti-burst { position: fixed; top: 50%; left: 50%; z-index: 9999; pointer-events: none; }
.confetti-piece { position: absolute; width: 8px; height: 8px; border-radius: 2px; animation: confettiDrop 1.2s ease forwards; }

/* ── Chat ── */
.chat-container { max-height: 400px; overflow-y: auto; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); }

/* ── Roadmap ── */
.roadmap-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 1.5rem; text-align: center; position: relative; transition: all 0.3s ease;
}
.roadmap-card.completed { border-color: rgba(0,200,83,0.4); background: rgba(0,200,83,0.05); }
.roadmap-card.current { border-color: rgba(123,47,247,0.5); background: rgba(123,47,247,0.08); animation: pulseGlow 2s infinite; }
.roadmap-card.locked { opacity: 0.5; }
.roadmap-connector { height: 30px; display: flex; justify-content: center; align-items: center; color: rgba(255,255,255,0.15); font-size: 1.2rem; }

/* ── Divider / Footer ── */
.custom-divider { height: 1px; background: linear-gradient(90deg,transparent,rgba(123,47,247,0.3),transparent); margin: 2rem 0; }
.footer { text-align: center; color: #555; font-size: 0.8rem; padding: 2rem 0 1rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 3rem; }
</style>
"""
