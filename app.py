import streamlit as st
import re
from datetime import datetime

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* {margin: 0; padding: 0; box-sizing: border-box;}
.main {background: #f8f9fa; padding: 2rem;}
.card-preview {width: 800px; max-width: 100%; margin: 0 auto 2rem; background: #ffffff; border-radius: 24px; box-shadow: 0 20px 60px rgba(16,45,105,0.12); overflow: hidden; border: 1px solid rgba(255,255,255,0.2);}
.header {background: linear-gradient(135deg,#102D69 0%,#1e4a8a 100%); padding: 2rem; color: white;}
.logo {font-size: 1.8rem; font-weight: 600; display: flex; align-items: center; gap: 0.75rem;}
.logo-circle {width: 3rem; height: 3rem; background: #DCFF05; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 1.25rem; color: #102D69;}
.title {font-size: 1.5rem; font-weight: 500; margin-top: 0.5rem; opacity: 0.95;}
.content {padding: 2.5rem;}
.section-title {font-size: 1.25rem; font-weight: 600; color: #102D69; margin-bottom: 1rem;}
.text {font-size: 1rem; line-height: 1.6; color: #333; margin-bottom: 1.5rem;}
.stats {display: grid; grid-template-columns: repeat(auto-fit,minmax(12rem,1fr)); gap: 1.25rem; margin: 2rem 0;}
.stat-item {text-align: center; padding: 1.5rem; background: #f8faff; border-radius: 1rem; border: 1px solid #e3f2fd;}
.stat-number {font-size: 2rem; font-weight: 600; color: #102D69; display: block;}
.stat-label {font-size: 0.875rem; color: #666; margin-top: 0.25rem;}
.cta {background: #102D69; color: white; border: none; padding: 1rem 2rem; border-radius: 0.75rem; font-size: 1rem; font-weight: 500; cursor: pointer; width: 100%;}
"""

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

def generate_card_html(title, description, stats):
    stats_html = ""
    for key, value in stats.items():
        stats_html += f'<div class="stat-item"><span class="stat-number">{value}</span><span class="stat-label">{key}</span></div>'
    return f"""
<style>{CSS}</style>
<div class="card-preview">
    <div class="header">
        <div class="logo">
            <div class="logo-circle">HSE</div>
            <div><div>НИУ ВШЭ</div><div class="title">{title}</div></div>
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

st.set_page_config(page_title="Генератор HSE", layout="wide")
st.markdown("<h1 style='text-align:center;color:#102D69;'>🎓 Генератор карточек НИУ ВШЭ</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#666;">Заголовок<br>Описание<br>Ключ1: значение</p>', unsafe_allow_html=True)

text_input = st.text_area("Текст карточки", height=200, placeholder="НИУ ВШЭ: Экономика\n\nПрограмма магистратуры\n\nПродолжительность: 2 года\nКредитов: 120\nТрудоустройство: 95%")
if st.button("🎨 Сгенерировать") and text_input.strip():
    title, desc, stats = parse_text(text_input)
    html = generate_card_html(title, desc, stats)
    st.markdown(html, unsafe_allow_html=True)
    st.download_button("📥 Скачать HTML", html, f"hse-card.html", "text/html")
