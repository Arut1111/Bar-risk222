
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Оценка риска осложнений", page_icon="⚠️", layout="centered")
st.title("⚠️ Прогностическая модель риска послеоперационных осложнений")

st.markdown("""Введите параметры пациента для оценки риска осложнений после бариатрической операции.
Модель учитывает клинически значимые предикторы и визуализирует риск по логистической функции.""")

with st.form("risk_form"):
    hb = st.number_input("Гемоглобин (г/л)", min_value=0.0, step=0.1)
    vas = st.slider("Боль по ВАШ (0–10)", 0.0, 10.0, 3.0, step=0.1)
    drain = st.checkbox("Объём дренажа ≥ 70 мл/сут")
    neutro = st.number_input("Палочкоядерные нейтрофилы (%)", min_value=0.0, step=0.1)
    hr = st.number_input("Частота сердечных сокращений (ЧСС)", min_value=0, step=1)
    wbc = st.number_input("Общее количество лейкоцитов (10⁹/л)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Рассчитать риск")

if submitted:
    # Уравнение с новыми факторами: тахикардия и лейкоцитоз
    r = -2.86 - 0.053 * hb + 1.687 * vas + 3.146 * int(drain) + 0.167 * neutro
    if hr > 100:
        r += 0.05
    if wbc > 14:
        r += 0.07

    st.subheader("📊 Результат")
    st.metric(label="Расчётный индекс риска", value=f"{r:.2f}")
    
    if r >= 0.08:
        st.error("🔴 Высокий риск осложнений. Рекомендуется экстренное обследование.")
    else:
        st.success("🟢 Низкий риск осложнений.")

    x = np.linspace(-2, 2, 400)
    y = 1 / (1 + np.exp(-x))
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Вероятность осложнения")
    ax.axvline(r, color='red', linestyle='--', label=f"Текущий риск ({r:.2f})")
    ax.set_xlabel("r - логит-функция")
    ax.set_ylabel("P (осложнение)")
    ax.set_title("Логистическая функция вероятности")
    ax.legend()
    st.pyplot(fig)
