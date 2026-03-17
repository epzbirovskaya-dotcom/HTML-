import streamlit as st
import re
from datetime import datetime

st.set_page_config(
    page_title="Генератор HSE карточек", 
    layout="wide",
    page_icon="🎓"
)

# CSS в отдельной строке (без минификации)
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.main { background: #f8f9fa; padding: 2rem; }
.card-preview { 
    width: 800px; max-width: 100%; margin: 2rem auto; 
    background: white; border-radius: 24px; 
    box-shadow: 0 20px 60px rgba(16,45,105,0.12); 
    overflow: hidden; border: 1px solid rgba(255,255,255,0.2);
}
.header { 
    background: linear-gradient(135deg,#102D69 0%,#1e4a8a 100%); 
    padding: 2rem; color: white; 
}
.logo { display: flex; align-items: center; gap: 0.75rem; font-size: 1.8rem; font-weight: 600; }
.logo-circle { 
    width: 3rem; height: 3rem; background: #DCFF05; 
    border-radius: 50%; display: flex; align-items: center; 
    justify-content: center; font-weight: 600; font-size: 1.25rem; color: #102D69;
}
.title { font-size: 1.5rem; font-weight: 500; margin-top: 0.5rem; opacity: 0.95; }
.content { padding: 2.5rem; }
.section-title { font-size: 1.25rem; font-weight: 600; color: #102D69; margin-bottom: 1rem; }
.text { font-size: 1rem; line-height: 1.6; color: #333; margin-bottom: 1.5rem; }
.stats { display: grid; grid-template-columns: repeat(auto-fit,minmax(12rem,1fr)); gap: 1.25rem; margin: 2rem 0; }
.stat-item { text-align: center; padding: 1.5rem; background: #f8faff; border-radius: 1rem; border: 1px solid #e3f2fd; }
.stat-number { font-size: 2rem; font-weight: 600; color: #102D69; display: block; }
.stat-label { font-size: 0.875rem; color: #666; margin-top: 0.25rem; }
.cta { background: #102D69; color: white; border: none; padding: 1rem 2rem; border-radius: 0.75rem; font-size: 1rem; font-weight: 500; cursor: pointer; width: 100%; }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

def parse_text(text):
    parts = re.split(r'\n\s*\n', text.strip())
    title = parts[0] if parts else "НИУ ВШЭ"
    description = parts[1] if len(parts) > 1 else ""
    stats = {}
    for line in parts[2:] if len(parts) > 2 else []:
        if ':' in line:
            key, value = line.split(':', 1)
            stats[key.strip()] = value.strip()
    return title, description, stats

def generate_card(title, description, stats):
    stats_html = ""
    for key, value in stats.items():
        stats_html += f'<div class="stat-item"><span class="stat-number">{value}</span><span class="stat-label">{key}</span></div>'
    
    return f"""
    <div class="card-preview">
        <div class="header">
            <div class="logo">
                <div class="logo-circle">HSE</div>
                <div>
                    <div>НИУ ВШЭ</div>
                    <div class="title">{title}</div>
                </div>
            </div>
        </div>
        <div class="content">
            <h2 class="section-title">Программа</h2>
            <p class="text">{description}</p>
            <div class="stats">{stats_html}</div>
            <button class="cta">Подать заявку</button>
        </div>
    </div>
    """

# Заголовок
st.title("🎓 Генератор карточек НИУ ВШЭ")
st.markdown("**Формат:** Заголовок → Описание → Ключ: значение")

# Ввод
col1, col2 = st.columns([3,1])

with col1:
    text_input = st.text_area(
        "Текст карточки", 
        height=250,
        placeholder="""НИУ ВШЭ: Экономика

Программа магистратуры по экономике и финансам.
Фокус на данных и анализе.

Продолжительность: 2 года
Кредитов: 120 ECTS
Трудоустройство: 95%"""
    )

with col2:
    st.markdown("### 📋 Пример")
    st.code("НИУ ВШЭ: Экономика\n\nОписание\n\nКлюч: значение")

# Генерация
if st.button("🎨 Сгенерировать карточку", type="primary"):
    if text_input.strip():
        title, desc, stats = parse_text(text_input)
        html = generate_card(title, desc, stats)
        st.markdown(html, unsafe_allow_html=True)
        
        # Скачать
        st.download_button(
            "📥 Скачать HTML", 
            html, 
            f"hse-card-{datetime.now().strftime('%Y%m%d-%H%M')}.html",
            "text/html"
        )
    else:
        st.error("Введите текст!")

st.markdown("---")
st.markdown("*Разработано в стиле Apple + брендбук НИУ ВШЭ*")
