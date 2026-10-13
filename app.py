import streamlit as st

st.set_page_config(page_title="لعبة X-O نيون", page_icon="❌⭕", layout="centered")

# تهيئة حالة اللعبة في الذاكرة المؤقتة بأبعاد جديدة تماماً
if "game_board_neon" not in st.session_state:
    st.session_state.game_board_neon = [""] * 9

if "player_turn_neon" not in st.session_state:
    st.session_state.player_turn_neon = "X"

if "game_winner_neon" not in st.session_state:
    st.session_state.game_winner_neon = None

# حقن الـ CSS لتغيير مظهر التطبيق بالكامل وتكبير الحروف بدون أخطاء برمجة
st.markdown(
    """
    <style>
    /* خلفية داكنة لتناسب ألوان النيون */
    .stApp {
        background-color: #0d0f1d !important;
        color: #ffffff;
    }
    
    /* تصميم العنوان العلوي */
    h1 {
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff;
        font-family: 'Arial Black', Gadget, sans-serif;
        margin-bottom: 20px;
    }
    
    /* ستايل المربعات (الأزرار) القياسية */
    div.stButton > button {
        background-color: #16192b !important;
        border: 2px solid #1f243d !important;
        border-radius: 16px !important;
        height: 120px !important;
        margin: 8px 0px !important;
        transition: all 0.2s ease;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    /* تكبير وتوسيط الحرف الداخلي بشكل إجباري وقوي */
    div.stButton > button p {
        font-size: 55px !important;
        font-weight: 900 !important;
        font-family: 'Arial', sans-serif !important;
    }
    
    /* تأثير مضيء عند تمرير الماوس فوق المربع الفارق */
    div.stButton > button:hover {
        border-color: #45f3ff !important;
        box-shadow: 0 0 15px rgba(69, 243, 255, 0.4) !important;
    }

    /* التوهج النيوني الأزرق الخاص بحرف X */
    div.stButton > button:has(p:contains("X")), div.stButton > button:contains("X") {
        color: #00d2ff !important;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff, 0 0 40px #00d2ff !important;
        border-color: #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
    }

    /* التوهج النيوني الوردي الخاص بحرف O */
    div.stButton > button:has(p:contains("O")), div.stButton > button:contains("O") {
        color: #ff007f !important;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f, 0 0 40px #ff007f !important;
        border-color: #ff007f !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.3) !important;
    }
    
    /* العلامة المائية */
    .watermark {
        position: fixed;
        bottom: 15px;
        right: 15px;
        opacity: 0.2;
        font-size: 18px;
        font-weight: bold;
        color: #00d2ff;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    <div class="watermark">© Developed by Py</div>
    """,
    unsafe_allow_html=True
)

st.title("TIC TAC TOE • NEON")

# دالة لفحص الفائز
def check_winner():
    b = st.session_state.game_board_neon
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combo in winning_combinations:
        if b[combo[0]] and b[combo[0]] == b[combo[1]] == b[combo[2]]:
            return b[combo[0]]
    if "" not in b:
        return "تعادل"
    return None

# عرض حالة ومجريات اللعبة
if st.session_state.game_winner_neon:
    if st.session_state.game_winner_neon == "تعادل":
        st.warning("انتهت اللعبة تعادلاً! 🤝")
    else:
        st.success(f"اللاعب {st.session_state.game_winner_neon} هو الفائز! 🎉")
    if st.button("إعادة اللعب الجديد", use_container_width=True):
        st.session_state.game_board_neon = [""] * 9
        st.session_state.player_turn_neon = "X"
        st.session_state.game_winner_neon = None
        st.rerun()
else:
    st.info(f"دور اللاعب الحالي: {st.session_state.player_turn_neon}")

st.write("") 

# رسم شبكة المربعات الـ 3×3 بأزرار آمنة وجديدة كلياً لتفادي الكاش القديم
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
            button_label = st.session_state.game_board_neon[idx] if st.session_state.game_board_neon[idx] else " "
            # استخدام متغيرات ومفاتيح جديدة تماماً (neon_grid_btn_) لتخطي الأخطاء السابقة
            if st.button(button_label, key=f"neon_grid_btn_{idx}", use_container_width=True):
                if not st.session_state.game_board_neon[idx] and not st.session_state.game_winner_neon:
                    st.session_state.game_board_neon[idx] = st.session_state.player_turn_neon
                    winner = check_winner()
                    if winner:
                        st.session_state.game_winner_neon = winner
                    else:
                        st.session_state.player_turn_neon = "O" if st.session_state.player_turn_neon == "X" else "X"
                    st.rerun()
