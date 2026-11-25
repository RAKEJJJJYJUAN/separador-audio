import streamlit as st
import subprocess
import sys
import os
import shutil
from pathlib import Path

st.set_page_config(page_title="🎵 Separador de Audio", layout="centered")
st.title("🎧 Separador de Voz y Música con IA")
st.write("Sube una canción y obtén la voz y la música por separado.")

archivo = st.file_uploader("Selecciona un audio", type=["mp3", "wav", "flac", "m4a", "ogg"])
modelo = st.selectbox("Modelo", ["htdemucs", "htdemucs_ft", "htdemucs_6s", "mdx_extra"], index=0)

if archivo and st.button("🚀 Separar"):
    carpeta_tmp = "tmp_audio"
    os.makedirs(carpeta_tmp, exist_ok=True)
    ruta = os.path.join(carpeta_tmp, archivo.name)
    with open(ruta, "wb") as f:
        f.write(archivo.getbuffer())

    with st.spinner("Separando audio... esto puede tardar unos minutos"):
        cmd = [sys.executable, "-m", "demucs", "--two-stems", "vocals",
               "-n", modelo, "-o", "output", ruta]
        proceso = subprocess.run(cmd, capture_output=True, text=True)

    if proceso.returncode == 0:
        nombre_sin_ext = Path(archivo.name).stem
        base = Path("output") / modelo / nombre_sin_ext
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎤 Voz")
            st.audio(str(base / "vocals.wav"))
            with open(base / "vocals.wav", "rb") as f:
                st.download_button("⬇️ Descargar voz", f, file_name="voz.wav")
        with col2:
            st.subheader("🎵 Música")
            st.audio(str(base / "no_vocals.wav"))
            with open(base / "no_vocals.wav", "rb") as f:
                st.download_button("⬇️ Descargar música", f, file_name="musica.wav")
        st.success("✅ ¡Listo!")
    else:
        st.error("❌ Error: " + proceso.stderr)