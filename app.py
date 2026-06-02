import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.markdown("""
<style>
.stApp { 
    background-color: #fff0f5; 
    color: #4a1221; 
}
div.stButton > button {
    background-color: #ff8da1; 
    color: white;
    border-radius: 12px;
    padding: 10px 24px;
    border: none;
    font-size: 16px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
div.stButton > button:hover {
    background-color: #ffb7c5; 
    color: #4a1221;
    border: none;
}
div.stButton > button:active {
    background-color: #d81b60; 
    color: white;
}
section[data-testid="stSidebar"] { 
    background-color: #ffe4e1; 
}
h1, h2, h3 { 
    color: #880e4f !important; 
}
.poema {
    background-color: #fff5f7;
    border-left: 5px solid #ff8da1;
    padding: 20px 28px;
    border-radius: 10px;
    font-style: italic;
    font-size: 17px;
    line-height: 1.8;
    color: #4a1221;
    margin: 16px 0;
}
.autor {
    text-align: right;
    font-weight: bold;
    color: #ad1457;
    margin-top: 10px;
}
.stTextArea textarea {
    background-color: #ffffff;
    border-color: #ffb7c5;
}
</style>
""", unsafe_allow_html=True)

st.title("🐱 Conversión de Texto a Audio Miau")

try:
    image = Image.open('TextoaAudio.png')
    st.image(image, width=500)
except:
    st.info("🍥 Imagen de ondas sonoras no encontrada.")

with st.sidebar:
    st.title("🐾 Miau-Audio")
    st.info(
        "1️⃣ Lee el poema 🌸\n\n"
        "2️⃣ Copia el texto o escribe el tuyo 📝\n\n"
        "3️⃣ Selecciona el idioma 🌐\n\n"
        "4️⃣ Presiona **Convertir a Audio** ⚡"
    )
    st.markdown("---")
    st.caption("Con tecnología gTTS 🎀")

try:
    os.mkdir("temp")
except:
    pass

st.markdown("### 🌸 Espero curarme de ti")
st.markdown("""
<div class="poema">
    Con pasos de seda y ojos de Sol, un gato dibuja un dulce rincón.
Su suave ronroneo es música y paz, un tierno latido que cura el hogar.
Pequeño guardián de sueños de amor, nos llena la vida con gracia y primor.
    <div class="autor">— NN</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🍥 ¿Quieres escucharlo?")
st.caption("Copia el poema o escribe tu propio texto:")

text = st.text_area("Ingresa el texto a escuchar", height=160)

idiomas = {"Español": "es", "Italiano": "it", "Francés": "fr"}
col1, col2 = st.columns(2)
with col1:
    option_lang = st.selectbox("🎀 Selecciona el idioma", list(idiomas.keys()))
    lg = idiomas[option_lang]
with col2:
    velocidad = st.radio("🐾 Velocidad", ("Normal", "Lenta"))
    slow = velocidad == "Lenta"

def text_to_speech(text, lg, slow):
    tts = gTTS(text, lang=lg, slow=slow)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

def get_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = (f'<a href="data:application/octet-stream;base64,{bin_str}" '
            f'download="{os.path.basename(file_path)}">'
            f'⬇️ Descargar miau-audio</a>')
    return href

st.markdown("---")
if st.button("🦄 Convertir a Audio"):
    if not text.strip():
        st.warning("⚠️ Por favor escribe o pega algún texto primero.")
    else:
        with st.spinner("Generando audio miau..."):
            result = text_to_speech(text, lg, slow)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()

        st.success("💖 ¡Audio generado con éxito!")
        st.markdown("### 🐾 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(
            get_download_link(f"temp/{result}.mp3"),
            unsafe_allow_html=True
        )

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n * 86400:
                os.remove(f)
remove_files(7)
