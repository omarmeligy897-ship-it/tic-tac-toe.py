import streamlit as st

st.set_page_config(page_title="لعبة X-O نيون", page_icon="❌⭕", layout="centered")

# تهيئة حالة اللعبة في الذاكرة المؤقتة
if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "turn" not in st.session_state:
    st.session_state.turn = "X"

if "winner" not in st.session_state:
    st.session_state.winner = None

# حقن الـ CSS الأساسي لخلفية التطبيق والعنوان والعلامة المائية
st.markdown(
    """
    <style>
    /* خلفية داكنة جداً تبرز الإضاءة */
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

    /* إخفاء عناصر أزرار ستريمليت الافتراضية لتبسيط التصميم وتحويلها كلياً */
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        height: auto !important;
    }

    /* ستايل المربع المضيء النيون المخصص */
    .neon-box {
        background-color: #16192b;
        border: 2px solid #1f243d;
        border-radius: 16px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        user-select: none;
        width: 100%;
    }

    /* تأثير تمرير الماوس فوق المربعات */
    .neon-box:hover {
        border-color: #45f3ff;
        box-shadow: 0 0 15px rgba(69, 243, 255, 0.4);
    }

    /* تنسيق حرف X الضخم والمشع باللون الأزرق */
    .char-x {
        color: #00d2ff !important;
        font-size: 70px !important;
        font-weight: 900 !important;
        font-family: 'Arial', sans-serif !important;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff, 0 0 40px #00d2ff !important;
    }

    /* تنسيق حرف O الضخم والمشع باللون الوردي */
    .char-o {
        color: #ff007f !important;
        font-size: 70px !important;
        font-weight: 900 !important;
        font-family: 'Arial', sans-serif !important;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f, 0 0 40px #ff007f !important;
    }
    
    /* العلامة المائية الثابتة لحفظ الحقوق */
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
    b = st.session_state.board
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

# عرض حالة اللعب
if st.session_state.winner:
    if st.session_state.winner == "تعادل":
        st.warning("انتهت اللعبة تعادلاً! 🤝")
    else:
        st.success(f"اللاعب {st.session_state.winner} هو الفائز! 🎉")
    if st.button("إعادة اللعب", use_container_width=True):
        st.session_state.board = [""] * 9
        st.session_state.turn = "X"
        st.session_state.winner = None
        st.rerun()
else:
    st.info(f"دور اللاعب الحالي: {st.session_state.turn}")

st.write("") 

# رسم شبكة اللعبة الـ 3×3 بالستايل النيون الجديد والأزرار الخفية
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        val = st.session_state.board[idx]
        
        # تحديد كود الـ HTML المناسب للحرف بناءً على قيمته لتكبيره بنسبة 100%
        if val == "X":
            cell_html = f'<div class="neon-box"><span class="char-x">X</span></div>'
        elif val == "O":
            cell_html = f'<div class="neon-box"><span class="char-o">O</span></div>'
        else:
            cell_html = f'<div class="neon-box"> </div>'
            
        with cols[col]:
            # نضع الكود المخصص بداخل زر ستريمليت لكن بدون الستايل القديم المزعج
            if st.button(cell_html, key=f"cell_{idx}", use_container_width=True, unsafe_allow_html=True):
                if not st.session_state.board[idx] and not st.session_state.winner:
                    st.session_state.board[idx] = st.session_state.turn
                    winner = check_winner()
                    if winner:
                        st.session_state.winner = winner
                    else:
                        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
                    st.rerun()
