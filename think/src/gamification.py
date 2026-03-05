"""Gamification engine — XP, levels, badges, streaks for the AI Teaching Assistant."""
import streamlit as st
import random

# ── Level definitions ──
LEVELS = [
    (0, "Curious Learner", "🌱"),
    (100, "Quick Study", "📖"),
    (250, "Rising Star", "⭐"),
    (500, "Knowledge Seeker", "🔍"),
    (750, "Brain Builder", "🧠"),
    (1000, "Knowledge Ninja", "🥷"),
    (1500, "ML Warrior", "⚔️"),
    (2000, "Data Wizard", "🧙"),
    (3000, "AI Sage", "🏛️"),
    (5000, "ML Master", "🏆"),
]

# ── Badge definitions ──
BADGES = {
    "first_spark": {"icon": "🔥", "name": "First Spark", "desc": "Complete your first query analysis"},
    "sharpshooter": {"icon": "🎯", "name": "Sharpshooter", "desc": "Get 5 quiz answers correct in a row"},
    "card_collector": {"icon": "🃏", "name": "Card Collector", "desc": "Review all flashcard decks"},
    "curious_mind": {"icon": "🗣️", "name": "Curious Mind", "desc": "Ask 10 doubts in AI Solver"},
    "overachiever": {"icon": "📈", "name": "Overachiever", "desc": "Score 100% on a quiz"},
    "comeback_kid": {"icon": "🔄", "name": "Comeback Kid", "desc": "Improve from Revision to Next Topic"},
    "speed_demon": {"icon": "⚡", "name": "Speed Demon", "desc": "Complete a quiz in under 3 minutes"},
    "streak_3": {"icon": "🔥", "name": "On Fire", "desc": "Maintain a 3-day streak"},
    "explorer": {"icon": "🧭", "name": "Explorer", "desc": "Use all 7 tabs"},
    "path_finder": {"icon": "🗺️", "name": "Path Finder", "desc": "Generate 5 learning recommendations"},
}

MOTIVATIONAL_QUOTES = [
    "Every problem you solve adds 1% to your mastery! 🚀",
    "The expert in anything was once a beginner. 🌱",
    "Small daily improvements lead to stunning results. ⭐",
    "Your brain is a muscle — keep training it! 🧠",
    "Consistency beats intensity. Show up every day! 🔥",
    "Mistakes are proof you're trying. Keep going! 💪",
    "The more you practice, the luckier you get. 🎯",
    "Learning never exhausts the mind. — Leonardo da Vinci 🎨",
]


def init_gamification():
    """Initialize session state for gamification."""
    defaults = {
        "xp": 0,
        "badges_earned": [],
        "streak_days": 1,
        "queries_count": 0,
        "recommendations_count": 0,
        "quiz_correct_streak": 0,
        "quiz_best_streak": 0,
        "doubts_asked": 0,
        "decks_completed": set(),
        "tabs_visited": set(),
        "quiz_scores": [],
        "last_action": None,
        "show_confetti": False,
        "show_badge_popup": None,
        "total_quizzes": 0,
        "total_cards_flipped": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def add_xp(amount, reason=""):
    """Add XP and check for level-up."""
    old_level = get_level()
    st.session_state.xp += amount
    new_level = get_level()
    if new_level[0] > old_level[0]:
        st.session_state.show_confetti = True
    return amount


def get_level():
    """Get current level info."""
    xp = st.session_state.xp
    current = LEVELS[0]
    for i, (threshold, name, icon) in enumerate(LEVELS):
        if xp >= threshold:
            current = (i + 1, name, icon, threshold)
        else:
            break
    return current


def get_next_level_xp():
    """XP needed for next level."""
    xp = st.session_state.xp
    for threshold, _, _ in LEVELS:
        if xp < threshold:
            return threshold
    return LEVELS[-1][0]


def get_level_progress():
    """Progress to next level as 0-100."""
    xp = st.session_state.xp
    current_threshold = 0
    next_threshold = LEVELS[-1][0]
    for i, (threshold, _, _) in enumerate(LEVELS):
        if xp >= threshold:
            current_threshold = threshold
            if i + 1 < len(LEVELS):
                next_threshold = LEVELS[i + 1][0]
            else:
                return 100
        else:
            next_threshold = threshold
            break
    if next_threshold == current_threshold:
        return 100
    return int(((xp - current_threshold) / (next_threshold - current_threshold)) * 100)


def award_badge(badge_id):
    """Award a badge if not already earned."""
    if badge_id not in st.session_state.badges_earned:
        st.session_state.badges_earned.append(badge_id)
        st.session_state.show_badge_popup = badge_id
        add_xp(50, f"Badge: {badge_id}")


def check_badges():
    """Check and award badges based on current state."""
    s = st.session_state
    if s.queries_count >= 1:
        award_badge("first_spark")
    if s.quiz_best_streak >= 5:
        award_badge("sharpshooter")
    if len(s.decks_completed) >= 7:
        award_badge("card_collector")
    if s.doubts_asked >= 10:
        award_badge("curious_mind")
    if any(score == 100 for score in s.quiz_scores):
        award_badge("overachiever")
    if s.streak_days >= 3:
        award_badge("streak_3")
    if len(s.tabs_visited) >= 7:
        award_badge("explorer")
    if s.recommendations_count >= 5:
        award_badge("path_finder")


def get_random_quote():
    """Get a motivational quote."""
    if "current_quote" not in st.session_state:
        st.session_state.current_quote = random.choice(MOTIVATIONAL_QUOTES)
    return st.session_state.current_quote


def render_sidebar_gamification():
    """Render gamification panel in sidebar."""
    init_gamification()
    check_badges()

    level = get_level()
    progress = get_level_progress()
    next_xp = get_next_level_xp()

    st.markdown(f"""
    <div class="xp-display">
        <div style="font-size:0.7rem; color:#888; text-transform:uppercase; letter-spacing:1px;">Level {level[0]}</div>
        <div class="level-badge">{level[2]} {level[1]}</div>
        <div style="font-size:0.85rem; color:#00d2ff; font-weight:700; margin:0.3rem 0;">{st.session_state.xp} XP</div>
        <div class="xp-bar-container">
            <div class="xp-bar-fill" style="width:{progress}%;"></div>
        </div>
        <div style="font-size:0.65rem; color:#666;">{next_xp - st.session_state.xp} XP to next level</div>
    </div>
    """, unsafe_allow_html=True)

    # Streak
    st.markdown(f"""
    <div style="text-align:center; margin:0.5rem 0;">
        <span class="streak-fire">🔥</span>
        <span style="color:#ff6b35; font-weight:700; font-size:1.1rem;">{st.session_state.streak_days}-Day Streak</span>
    </div>
    """, unsafe_allow_html=True)

    # Badges showcase
    badge_html = ""
    for bid, info in BADGES.items():
        if bid in st.session_state.badges_earned:
            badge_html += f'<span class="badge-earned" title="{info["name"]}: {info["desc"]}">{info["icon"]}</span>'
        else:
            badge_html += f'<span class="badge-locked" title="???">{info["icon"]}</span>'

    st.markdown(f"""
    <div style="text-align:center; margin:0.5rem 0; padding:0.5rem; background:rgba(255,255,255,0.02); border-radius:10px;">
        <div style="font-size:0.7rem; color:#888; margin-bottom:0.3rem;">BADGES</div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

    # Quote
    st.markdown(f"""
    <div style="font-size:0.75rem; color:#9a9ac4; text-align:center; font-style:italic; margin:0.5rem 0; padding:0.5rem;">
        "{get_random_quote()}"
    </div>
    """, unsafe_allow_html=True)


def render_confetti():
    """Render confetti animation if triggered."""
    if st.session_state.get("show_confetti"):
        colors = ["#7b2ff7", "#00d2ff", "#ff6ec7", "#00c853", "#ffc107", "#ff4757"]
        pieces = ""
        for i in range(20):
            c = random.choice(colors)
            x = random.randint(-100, 100)
            d = random.uniform(0.5, 1.5)
            pieces += f'<div class="confetti-piece" style="background:{c}; left:{x}px; animation-delay:{d}s;"></div>'
        st.markdown(f"""
        <div class="confetti-burst">{pieces}</div>
        <div style="text-align:center; padding:1rem;">
            <div style="font-size:2rem;">🎉</div>
            <div style="font-size:1.2rem; font-weight:700; color:#ffc107;">LEVEL UP!</div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_confetti = False


def render_badge_popup():
    """Render badge unlock popup if triggered."""
    badge_id = st.session_state.get("show_badge_popup")
    if badge_id and badge_id in BADGES:
        info = BADGES[badge_id]
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:rgba(123,47,247,0.1); border:1px solid rgba(123,47,247,0.3); border-radius:16px; margin:1rem 0; animation:fadeInUp 0.5s ease;">
            <div style="font-size:2.5rem;" class="badge-earned">{info['icon']}</div>
            <div style="font-size:1rem; font-weight:700; color:#ffc107; margin:0.3rem 0;">Badge Unlocked!</div>
            <div style="font-size:0.9rem; color:#e0e0ff; font-weight:600;">{info['name']}</div>
            <div style="font-size:0.75rem; color:#888;">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_badge_popup = None
