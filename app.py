from collections import Counter
import random
import string
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Mini-Apps Hub", page_icon="🚀", layout="centered"
)

# App Header
st.title("🚀 Python Mini-Apps Hub")
st.write(
    "Explore the Number Guessing Game and Word Counter built completely in"
    " Python!"
)
st.markdown("---")

# Navigation Tabs
tab1, tab2 = st.tabs(["🎮 Number Guessing Game", "📊 Word Counter Tool"])

# --- TAB 1: NUMBER GUESSING GAME ---
with tab1:
  st.subheader("🎯 Guess the Secret Number")
  st.write("I have picked a number between 1 and 100. You have 7 attempts!")

  # Initialize game session state
  if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts_left = 7
    st.session_state.game_over = False

  # Metric display for attempts
  st.metric("Attempts Remaining", st.session_state.attempts_left)

  guess = st.number_input(
      "Enter your guess (1-100):",
      min_value=1,
      max_value=100,
      step=1,
      key="guess_input",
  )

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Submit Guess") and not st.session_state.game_over:
      st.session_state.attempts_left -= 1

      if guess == st.session_state.secret_number:
        score = (st.session_state.attempts_left + 1) * 15
        st.success(
            f"🎉 Congratulations! You found the number"
            f" {st.session_state.secret_number}!\nYour Score: {score} Points"
        )
        st.session_state.game_over = True
      elif st.session_state.attempts_left == 0:
        st.error(
            f"❌ Game Over! The secret number was"
            f" {st.session_state.secret_number}."
        )
        st.session_state.game_over = True
      elif guess < st.session_state.secret_number:
        st.info("📈 Too low! Try a higher number.")
      else:
        st.info("📉 Too high! Try a lower number.")

      st.rerun()

  with col2:
    if st.button("Reset Game"):
      st.session_state.secret_number = random.randint(1, 100)
      st.session_state.attempts_left = 7
      st.session_state.game_over = False
      st.rerun()

# --- TAB 2: WORD COUNTER TOOL ---
with tab2:
  st.subheader("📝 Live Text & Word Analyzer")
  st.write("Type or paste your text below to instantly analyze stats.")

  text_input = st.text_area(
      "Your Text:",
      placeholder="Start typing or paste your text here...",
      height=150,
  )

  if text_input:
    chars = len(text_input)
    words = (
        text_input.lower().translate(str.maketrans("", "", string.punctuation)).split()
    )
    total_words = len(words)
    sentences = (
        text_input.count(".") + text_input.count("!") + text_input.count("?")
    )
    read_time = max(1, round((total_words / 200) * 60))

    # Stats Grid
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Words", total_words)
    m2.metric("Characters", chars)
    m3.metric("Sentences", sentences)
    m4.metric("Read Time", f"{read_time}s")

    # Frequent Words
    st.markdown("### Top Frequent Words")
    if total_words > 0:
      word_counts = Counter(words)
      top_common = word_counts.most_common(5)

      for w, count in top_common:
        st.write(f"- **'{w}'**: {count} times")
    else:
      st.write("No words detected yet.")
