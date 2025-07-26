import streamlit as st
import random
import re

# --- Expanded AI-style interpretations by keyword (with fuzzy matching) ---
keyword_responses = [
    (['mountain', 'hill', 'peak'], "Mountains in dreams often symbolize obstacles, aspirations, or a desire for adventure."),
    (['water', 'river', 'lake', 'ocean', 'sea', 'rain'], "Dreams involving water often reflect your emotional state and subconscious feelings."),
    (['animal', 'dog', 'cat', 'bird', 'fish', 'lion', 'tiger', 'elephant'], "Animals in dreams can symbolize instincts, habits, or hidden aspects of yourself."),
    (['flying', 'flight', 'float', 'soar', 'sky', 'cloud', 'air'], "Dreams of flying or being in the sky often represent a desire for freedom and escape from daily pressures."),
    (['teeth', 'tooth', 'mouth'], "Losing teeth in dreams is commonly linked to concerns about self-image or communication."),
    (['celebrity', 'famous', 'star'], "Meeting a celebrity in a dream could reflect aspirations or feelings of inadequacy."),
    (['late', 'delay', 'missed', 'waiting'], "Dreams of being late often point to fear of missing out or not meeting expectations."),
    (['exam', 'test', 'quiz', 'school', 'class'], "Dreams about exams may indicate self-evaluation or fear of being judged."),
    (['clock', 'time', 'watch', 'timer'], "Seeing clocks in your dream may symbolize anxiety about time management or fear of deadlines."),
    (['chase', 'chased', 'run', 'running', 'pursue'], "Being chased in a dream can indicate unresolved stress or avoidance in your waking life."),
    (['fall', 'falling', 'drop', 'slip'], "Dreams about falling may suggest a lack of control or insecurity in some area of your life."),
    (['dream', 'sleep', 'night', 'bed'], "Dreams about dreaming or sleep can reflect your thoughts about rest, escape, or your subconscious mind."),
    (['sun', 'light', 'shine', 'bright'], "Sun or light in dreams often symbolizes hope, clarity, or new beginnings."),
    (['cloud', 'clouds'], "Clouds in dreams can represent confusion, transition, or a sense of drifting.")
]

# --- Fallback random responses (weird, emotional, playful, poetic) ---
ai_responses = [
    "You dreamed of a city made of jellybeans. Maybe your mind is craving sweetness, or just chaos!",
    "A dream of endless stairs could mean you're climbing toward something... or just stuck in a loop!",
    "Dancing with shadows? Sometimes our dreams are just poetry with no translation.",
    "Dreams of losing your shoes might mean you're searching for your path—or just hate shoe shopping!",
    "A dream where you speak in colors, not words, is your brain's way of painting emotions.",
    "You dreamed of rain inside your house. Maybe your feelings are leaking into your safe spaces.",
    "Dreams of being invisible can mean you want to hide, or maybe you want to be seen more than ever.",
    "A dream of laughing with strangers: sometimes joy is just as mysterious as fear.",
    "You dreamed of floating upside down. Maybe your world feels flipped, or maybe you just like the view!",
    "Dreams of doors that never open: sometimes, the mystery is the message.",
    # Classic logical ones for contrast
    "Dreams of flying often represent a desire for freedom and escape from daily pressures.",
    "Seeing clocks in your dream may symbolize anxiety about time management or fear of deadlines.",
    "Dreams involving water often reflect your emotional state and subconscious feelings.",
    "Being chased in a dream can indicate unresolved stress or avoidance in your waking life.",
    "Losing teeth in dreams is commonly linked to concerns about self-image or communication.",
    "Dreams about falling may suggest a lack of control or insecurity in some area of your life.",
    "Meeting a celebrity in a dream could reflect aspirations or feelings of inadequacy.",
    "Dreams of being late often point to fear of missing out or not meeting expectations.",
    "Animals in dreams can symbolize instincts, habits, or hidden aspects of yourself.",
    "Dreams about exams may indicate self-evaluation or fear of being judged."
]

# --- Dream moods/tags ---
dream_tags = [
    "Anxiety 😰", "Adventure 🏞️", "Absurdity 🤪", "Loss 💔", "Hope 🌈", "Freedom 🕊️"
]

# --- Fun dream facts/quotes ---
dream_facts = [
    "Did you know? The average person has 3-5 dreams per night!",
    "Fun fact: Most dreams are forgotten within minutes of waking up.",
    "Quote: 'Dreams are illustrations... from the book your soul is writing about you.' — Marsha Norman",
    "Fact: Blind people also dream, and their dreams involve other senses like sound and touch.",
    "Quote: 'Dreams feel real while we're in them. It's only when we wake up that we realize something was strange.' — Inception",
    "Did you know? You can't read or tell the time in most dreams!"
]

# --- App State ---
if 'dream_history' not in st.session_state:
    st.session_state['dream_history'] = []
if 'soul_score' not in st.session_state:
    st.session_state['soul_score'] = {'yes': 0, 'no': 0}

# --- Welcome & Humanity/Philosophy Banner ---
st.markdown("""
<div style='background: linear-gradient(90deg, #f7cac9 0%, #92a8d1 100%); padding: 1.5em; border-radius: 12px; text-align: center;'>
    <h1>🌙 Dream vs Data: Unmistakably Human Edition 🌙</h1>
    <h3>Share your most surreal, emotional, or weird dream. Our 'AI' will try to interpret it using logic and data.<br>
    <span style='color:#e17055;'>But only you know what it really means.</span></h3>
    <b>Soul Score:</b> After each interpretation, rate if the AI captured the human truth of your dream.<br>
    <i>Does the project radiate humanity, soul, and vibes? Let's find out together!</i>
</div>
""", unsafe_allow_html=True)

# --- App UI ---
st.markdown("""
*This app is a playful, poetic, and sometimes chaotic demo of how AI can miss the soul of human dreams. Sometimes it gets close, sometimes it totally misses the point!*

**Theme:** AI vs Human Meaning | Community Dream Wall | Emotional Truth > Data
""")

def get_ai_interpretation(dream_text):
    dream_text_lower = dream_text.lower()
    best_match = None
    best_keyword = None
    for keywords, response in keyword_responses:
        for kw in keywords:
            if kw in dream_text_lower:
                if not best_match or len(kw) > len(best_keyword):
                    best_match = response
                    best_keyword = kw
    if best_match:
        return best_match
    else:
        return random.choice(ai_responses)

dream = st.text_area("Describe your dream:", "")
tag = st.selectbox("Pick a mood or tag for your dream:", dream_tags)

if st.button("Interpret my dream!") and dream.strip():
    ai_interpretation = get_ai_interpretation(dream)
    st.session_state['dream_history'].append({
        'dream': dream,
        'tag': tag,
        'ai': ai_interpretation,
        'feedback': None
    })
    st.success("AI's Interpretation:")
    st.write(f"<span style='font-size:1.2em;'>{ai_interpretation}</span>", unsafe_allow_html=True)
    feedback = st.radio("Did this make sense? (Soul Score)", ("Yes", "No"), key=f'feedback_{len(st.session_state["dream_history"])}')
    if feedback:
        idx = len(st.session_state['dream_history']) - 1
        st.session_state['dream_history'][idx]['feedback'] = feedback
        st.session_state['soul_score'][feedback.lower()] += 1
        st.balloons() if feedback == "Yes" else st.snow()
        st.info(f"Thanks for your feedback! (Soul Score updated)")
        st.markdown(f"**Dream Fact/Quote:** {random.choice(dream_facts)}")

# --- Display Soul Score ---
st.subheader("Soul Score (Human Truth vs AI Logic)")
st.write(f"✅ Yes: {st.session_state['soul_score']['yes']} | ❌ No: {st.session_state['soul_score']['no']}")

# --- Dream Gallery ---
st.subheader("Dream Gallery (Your Journey)")
for i, entry in enumerate(reversed(st.session_state['dream_history'])):
    st.markdown(f"**Dream {len(st.session_state['dream_history'])-i}:** {entry['dream']}")
    st.markdown(f"*Tag:* {entry['tag']}")
    st.markdown(f"*AI's Interpretation:* {entry['ai']}")
    if entry['feedback']:
        st.markdown(f"*Soul Score:* {entry['feedback']}")
    st.markdown("---")

# --- Dream Wall: Community & Cultural Impact ---
st.subheader("🌐 Dream Wall: Anonymous Community Dreams 🌐")
if st.session_state['dream_history']:
    for entry in reversed(st.session_state['dream_history']):
        st.markdown(f"<div style='background:#f7cac9;padding:0.7em;border-radius:8px;margin-bottom:0.5em;'>"
                    f"<b>Dream:</b> {entry['dream']}<br>"
                    f"<b>Tag:</b> {entry['tag']}<br>"
                    f"<b>Soul Score:</b> {entry['feedback'] if entry['feedback'] else 'Not rated yet'}"
                    f"</div>", unsafe_allow_html=True)
else:
    st.info("No dreams on the wall yet. Be the first to share!")

# --- Philosophical Reflection ---
st.markdown("""
<div style='background: linear-gradient(90deg, #92a8d1 0%, #f7cac9 100%); padding: 1.2em; border-radius: 12px; text-align: center; margin-top:2em;'>
    <h3>🤔 Philosophical Edge</h3>
    <b>Can something as human as a dream ever be decoded by something as mechanical as an algorithm?</b><br>
    <i>This project is a conversation between the subconscious and the synthetic.<br>
    Some things can't be explained by data — that's the point.</i>
</div>
""", unsafe_allow_html=True)
