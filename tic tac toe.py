import streamlit as st

st.set_page_config(page_title="لعبة X-O نيون", page_icon="❌⭕", layout="centered")

# --- تحويل التصميم إلى ستايل نيون مضيء بالكامل عبر CSS ---
st.markdown(
    """
    <style>
    /* تغيير خلفية التطبيق بأكمله لتصبح داكنة تناسب النيون */
    .stApp {
        background-color: #0b0c10 !important;
        color: #ffffff;
    }
    
    /* تصميم العنوان الرئيسي */
    h1 {
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff, 0 0 40px #00d2ff;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 30px;
    }
    
    /* تعديل شكل أزرار اللعب (مربعات الـ X-O) */
    div.stButton > button {
        background-color: #1f2833 !important;
        border: 2px solid #45f3ff !important;
        border-radius: 15px !important;
        height: 100px !important;
        font-size: 40px !important;
        font-weight: bold !important;
        margin: 5px 0px !important;
        transition: all 0.3s ease;
        box-shadow: 0 0 5px #45f3ff;
    }
    
    /* تأثير عند تمرير الماوس فوق الأزرار */
    div.stButton > button:hover {
        background-color: #2b3a4a !important;
        box-shadow: 0 0 15px #45f3ff, inset 0 0 10px #45f3ff;
        border-color: #fff !important;
    }

    /* ستايل مخصص للـ X باللون الأزرق المضيء */
    div.stButton > button:has(div:contains("❌")), 
    div.stButton > button:contains("❌") {
        color: #00d2ff !important;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff !important;
        border-color: #00d2ff !important;
        box-shadow: 0 0 15px #00d2ff !important;
    }

    /* ستايل مخصص للـ O باللون الوردي/الأحمر المضيء */
    div.stButton > button:has(div:contains("⭕")), 
    div.stButton > button:contains("⭕") {
        color: #ff007f !important;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f !important;
        border-color: #ff007f !important;
        box-shadow: 0 0 15px #ff007f !important;
    }
    
    /* العلامة المائية الشفافة في الأسفل */
    .watermark {
        position: fixed;
        bottom: 15px;
        right: 15px;
        opacity: 0.25;
        font-size: 20px;
        font-weight: bold;
        color: #45f3ff;
        text-shadow: 0 0 5px #45f3ff;
        z-index: 9999;
        pointer-events: none;
        user-select: none;
    }
    </style>
    
    <div class="watermark">© Developed by Py</div>
    """,
    unsafe_allow_html=True
)

st.title("TIC TAC TOE • NEON")

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

# عرض الدور الحالي أو النتيجة بستايل متناسق
if st.session_state.winner:
    if st.session_state.winner == "تعادل":
        st.warning("انتهت اللعبة تعادلاً! 🤝")
    else:
        st.success(f"اللاعب {st.session_state.winner} هو الفائز! 🎉")
    if st.button("إعادة اللعب", use_container_width=True):
        st.session_state.board = [""] * 9
        st.session_state.turn = "❌"
        st.session_state.winner = None
        st.rerun()
else:
    st.info(f"دور اللاعب الحالي: {st.session_state.turn}")

# رسم مربعات اللعبة (3 أعمدة × 3 صفوف) داخل حاوية منسقة
st.write("") # مسافة جمالية
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
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
