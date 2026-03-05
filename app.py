import streamlit as st
from poker_engine import PokerEngine

st.set_page_config(page_title="GTO Oracle Pro", layout="wide")
engine = PokerEngine()

# 自定义 CSS 样式（专业暗色调）
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

st.title("♠️ GTO Oracle: 德扑专业分析仪")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 模拟参数")
    players = st.slider("玩家人数", 2, 9, 2)
    precision = st.select_slider("计算精度 (模拟次数)", options=[1000, 5000, 10000], value=5000)
    st.divider()
    pot = st.number_input("底池大小 (BB)", value=10.0)
    call = st.number_input("需跟注额 (BB)", value=2.0)

# 选牌矩阵
card_ranks = "AKQJT98765432"
card_suits = "shdc"
all_cards = [r+s for r in card_ranks for s in card_suits]

col1, col2 = st.columns(2)
with col1:
    my_hand = st.multiselect("🎴 你的底牌 (2张)", options=all_cards, max_selections=2)
with col2:
    board = st.multiselect("🌍 公共牌 (0-5张)", options=[c for c in all_cards if c not in my_hand], max_selections=5)

if st.button("🚀 运行实时模拟", use_container_width=True):
    if len(my_hand) == 2:
        with st.spinner("正在进行高精度蒙特卡洛计算..."):
            equity = engine.run_simulation(my_hand, board, players, precision)
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("胜率 (Equity)", f"{equity:.2%}")
            
            pot_odds = call / (pot + call) if (pot + call) > 0 else 0
            c2.metric("所需胜率 (Pot Odds)", f"{pot_odds:.2%}")
            
            ev = (equity * (pot + call)) - ((1 - equity) * call)
            c3.metric("期望值 (EV)", f"{ev:.2f} BB")

            if ev > 0:
                st.success(f"✅ 正EV决策：建议跟注或加注。你的赢面足以支付当前成本。")
            else:
                st.error(f"❌ 负EV决策：建议弃牌。长期来看这手牌会亏损。")
    else:
        st.warning("请至少选择2张底牌。")
