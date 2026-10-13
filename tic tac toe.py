import streamlit as st

st.set_page_config(page_title="لعبة X-O", page_icon="❌⭕")

# --- إضافة العلامة المائية في الخلفية باستخدام CSS ---
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.2; /* درجة الشفافية */
        font-size: 24px;
        font-weight: bold;
        color: #888888;
        z-index: 9999;
        pointer-events: none; /* تمنع حجب الأزرار */
        user-select: none;
    }
    </style>
    <!-- يمكنك تغيير النص المكتوب هنا باسمك أو اسم موقعك -->
    <div class="watermark">© PY/OMAR MELIGY</div>
    """,
    unsafe_allow_html=True
)

st.title("❌ لعبة X-O (Tic-Tac-Toe) ⭕")

# تهيئة حالة اللعبة في الذاكرة المؤقتة
if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "turn" not in st.session_state:
    st.session_state.turn = "❌"

if "winner" not in st.session_state:
    st.session_state.winner = None

# دالة لفحص الفائز
def check_winner():
    b = st.session_state.board
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # صفوف
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # أعمدة
        (0, 4, 8), (2, 4, 6)              # أقطار
    ]
    for combo in winning_combinations:
        if b[combo[0]] and b[combo[0]] == b[combo[1]] == b[combo[2]]:
            return b[combo[0]]
    if "" not in b:
        return "تعادل"
    return None

# عرض الدور الحالي أو النتيجة
if st.session_state.winner:
    if st.session_state.winner == "تعادل":
        st.warning("انتهت اللعبة تعادلاً! 🤝")
    else:
        st.success(f"اللاعب {st.session_state.winner} هو الفائز! 🎉")
    if st.button("إعادة اللعب"):
        st.session_state.board = [""] * 9
        st.session_state.turn = "❌"
        st.session_state.winner = None
        st.rerun()
else:
    st.info(f"دور اللاعب: {st.session_state.turn}")

# رسم مربعات اللعبة (3 أعمدة × 3 صفوف)
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
            # زر لكل خانة
            button_label = st.session_state.board[idx] if st.session_state.board[idx] else " "
            if st.button(button_label, key=f"cell_{idx}", use_container_width=True):
                if not st.session_state.board[idx] and not st.session_state.winner:
                    st.session_state.board[idx] = st.session_state.turn
                    winner = check_winner()
                    if winner:
                        st.session_state.winner = winner
                    else:
                        st.session_state.turn = "⭕" if st.session_state.turn == "❌" else "❌"
                    st.rerun()
