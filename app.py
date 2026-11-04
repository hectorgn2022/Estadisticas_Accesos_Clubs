import streamlit as st
import pandas as pd
from google import genai
import os
import json
import re
import matplotlib.pyplot as plt

# CONFIGURACIÓN: Reemplaza esta URL con la ruta real de tu logo en el bucket de Amazon S3
S3_LOGO_URL = "https://egonsolutionscloudtrailbucket.s3-us-west-2.amazonaws.com/Recursos/cs_51/Imagenes/logo.png"

# Configuración de la página
st.set_page_config(page_title="Club Demo - Estadísticas de Acceso", layout="wide")

# Estilos personalizados para el historial y diseño
st.markdown(
    """
    <style>
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-bubble {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .bot-bubble {
        background-color: #f5f5f5;
        border-left: 5px solid #4caf50;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Archivo donde se persistirán las consultas guardadas
ARCHIVO_CONSULTAS = "consultas_guardadas.txt"

def cargar_consultas_guardadas():
    if os.path.exists(ARCHIVO_CONSULTAS):
        with open(ARCHIVO_CONSULTAS, "r", encoding="utf-8") as f:
            return [linea.strip() for linea in f if linea.strip()]
    return []

def guardar_consulta_en_archivo(consulta):
    consultas = cargar_consultas_guardadas()
    if consulta not in consultas:
        with open(ARCHIVO_CONSULTAS, "a", encoding="utf-8") as f:
            f.write(consulta + "\n")

def guardar_todas_las_consultas(lista_consultas):
    with open(ARCHIVO_CONSULTAS, "w", encoding="utf-8") as f:
        for c in lista_consultas:
            f.write(c + "\n")

# Inicializar estados de la aplicación en Streamlit
if "historial" not in st.session_state:
    st.session_state.historial = []

if "consultas_guardadas" not in st.session_state:
    st.session_state.consultas_guardadas = cargar_consultas_guardadas()

if "query_to_run" not in st.session_state:
    st.session_state.query_to_run = ""

# Obtener API Key de manera segura sin exponerla en la UI
api_key = ""
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY", "")

# Encabezado Superior con Título y Logo desde S3
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    try:
        # Intentar cargar la imagen desde la URL de Amazon S3
        st.image(S3_LOGO_URL, width=120)
    except Exception:
        # Caída de respaldo amigable en caso de error de conexión o URL incorrecta
        st.markdown("## ⛳")
with col_titulo:
    st.title("Club Demo")
    st.markdown("#### Sistema de Estadísticas de Acceso al Club")

st.markdown("##### **Captura tu consulta y oprime &lt;Enviar&gt;**")

# Estructura de diseño: Parte izquierda (Operación e Historial), Parte derecha (Menú de opciones)
col_izquierda, col_derecha = st.columns([3, 1])

# Verificación preventiva del estado del archivo CSV
ruta_archivo = "accesos_club.csv"
csv_cargado_exito = False
num_registros = 0

try:
    if os.path.exists(ruta_archivo):
        df_check = pd.read_csv(ruta_archivo)
        num_registros = len(df_check)
        if num_registros > 0:
            csv_cargado_exito = True
except Exception as e:
    pass

with col_derecha:
    st.markdown("### Opciones")

    # Indicador visual del estado del archivo CSV
    st.markdown("**Estado de los Datos:**")
    if csv_cargado_exito:
        st.success(f"🟢 CSV Activo ({num_registros} registros)")
    else:
        st.error("🔴 Sin datos activos o CSV vacío")

    # Opción 1: Cargar Archivo CSV
    archivo_cargado = st.file_uploader("Cargar Archivo CSV", type=["csv"])
    if archivo_cargado is not None:
        with open("accesos_club.csv", "wb") as f:
            f.write(archivo_cargado.getbuffer())
        st.success("¡Archivo cargado correctamente!")
        st.rerun()

    # Opción 2: Guardar Consulta anterior
    if st.button("Guardar Consulta anterior"):
        if st.session_state.historial:
            # Obtener la consulta más reciente del historial
            ultima_consulta = st.session_state.historial[0]["pregunta"]
            guardar_consulta_en_archivo(ultima_consulta)
            st.session_state.consultas_guardadas = cargar_consultas_guardadas()
            st.success(f"Consulta guardada: '{ultima_consulta}'")
            st.rerun()
        else:
            st.warning("Aún no has realizado ninguna consulta en esta sesión para guardar.")

    # Opción 3: Mostrar botones para invocar consultas guardadas y botón para eliminar
    if st.session_state.consultas_guardadas:
        st.markdown("--- ")
        st.markdown("**Consultas Rápidas Guardadas:**")
        for idx, consulta_salvada in enumerate(st.session_state.consultas_guardadas):
            col_item_query, col_item_delete = st.columns([4, 1])
            with col_item_query:
                if st.button(f"🔍 {consulta_salvada}", key=f"btn_saved_{idx}"):
                    st.session_state.query_to_run = consulta_salvada
                    st.rerun()
            with col_item_delete:
                if st.button("🗑️", key=f"btn_del_{idx}", help="Eliminar esta consulta"):
                    st.session_state.consultas_guardadas.remove(consulta_salvada)
                    guardar_todas_las_consultas(st.session_state.consultas_guardadas)
                    st.toast(f"Consulta eliminada: {consulta_salvada}")
                    st.rerun()

# Lógica de operación principal
with col_izquierda:
    # Si se seleccionó una consulta rápida, se pre-llena en el input de texto
    valor_inicial = st.session_state.query_to_run
    
    # Formulario para enviar consulta
    with st.form(key="form_consulta", clear_on_submit=True):
        pregunta_usuario = st.text_input("Escribe tu consulta aquí:", value=valor_inicial, placeholder="¿Cuántas personas han ingresado?")
        boton_enviar = st.form_submit_button("Enviar")

    # Limpiar la variable temporal para que no se quede pegada
    if boton_enviar:
        st.session_state.query_to_run = ""

    if (boton_enviar or valor_inicial) and pregunta_usuario:
        # Evitar re-ejecución infinita si viene de un botón rápido
        if not api_key:
            st.error("⚠️ No se encontró la credencial 'GEMINI_API_KEY'. Por favor, configúrala en la pestaña de Secrets de tu panel de Streamlit Cloud.")
        else:
            with st.spinner("Analizando los accesos..."):
                try:
                    client = genai.Client(api_key=api_key)

                    ruta_archivo = "accesos_club.csv"
                    if os.path.exists(ruta_archivo):
                        df = pd.read_csv(ruta_archivo)
                    else:
                        df = pd.DataFrame()

                    contexto_datos = df.to_string(index=False) if not df.empty else "No hay datos disponibles."

                    prompt_sistema = """
                    Eres un asistente virtual de análisis de datos para el personal de Servicio al Cliente de un club de golf.
                    Tu tarea es responder preguntas estadísticas basadas EXCLUSIVAMENTE en los datos de accesos provistos.

                    REGLA OBLIGATORIA PARA GRÁFICAS:
                    Si el usuario solicita de cualquier forma una gráfica, gráfico, histograma, visualización, o pide 'graficar', 'mostrar una gráfica' o 'desplegar un gráfico', DEBES proporcionar OBLIGATORIAMENTE un bloque de datos JSON estructurado al final de tu respuesta de texto exactamente con este formato:
                    ```json
                    {
                      "mostrar_grafica": true,
                      "tipo": "barras",
                      "datos": {
                        "Categoría A": valor1,
                        "Categoría B": valor2
                      }
                    }
                    ```
                    Donde la clave 'datos' debe contener las categorías y conteos exactos extraídos de la tabla de datos.
                    """

                    contenido_consulta = f"""
                    Aquí tienes los datos actuales de acceso al club en formato de tabla:
                    {contexto_datos}
                    Pregunta del usuario: {pregunta_usuario}
                    """

                    response = client.models.generate_content( 
                        model="gemini-3.5-flash-lite",
                        contents=contenido_consulta,
                        config={
                            'system_instruction': prompt_sistema,
                            'temperature': 0.1
                        }
                    )

                    respuesta_texto = response.text
                    datos_grafica = None

                    match_json = re.search(r"```json\s*(\{.*?\})\s*```", respuesta_texto, re.DOTALL)
                    if match_json:
                        try:
                            bloque_json = json.loads(match_json.group(1))
                            if bloque_json.get("mostrar_grafica"):
                                datos_grafica = bloque_json.get("datos")
                                respuesta_texto = re.sub(r"```json\s*(\{.*?\})\s*```", "", respuesta_texto, flags=re.DOTALL).strip()
                        except Exception:
                            pass

                    st.session_state.historial.insert(0, { 
                        "pregunta": pregunta_usuario,
                        "respuesta": respuesta_texto,
                        "grafica": datos_grafica
                    })
                    
                    # Forzar recarga limpia si se ejecutó una acción rápida
                    if valor_inicial:
                        st.session_state.query_to_run = ""
                        st.rerun()
                        
                except Exception as e:
                    st.error("Error al realizar tu consulta, prueba en unos minutos o verifica tu cuota de créditos.")

    # Área para mostrar el Historial arriba
    st.markdown("### Historial de consultas")
    contenedor_historial = st.container()

    with contenedor_historial:
        if not st.session_state.historial:
            st.write("*Aún no has realizado ninguna consulta.*")
        else:
            for chat in st.session_state.historial:
                st.markdown(f'<div class="chat-bubble user-bubble"><b>Pregunta:</b> {chat["pregunta"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-bubble bot-bubble"><b>Respuesta:</b> {chat["respuesta"]}</div>', unsafe_allow_html=True)

                if chat.get("grafica"):
                    try:
                        categorias = list(chat["grafica"].keys())
                        valores = list(chat["grafica"].values())

                        fig, ax = plt.subplots(figsize=(6, 3.5))
                        bars = ax.bar(categorias, valores, color="#2196f3", edgecolor="black", alpha=0.85)
                        ax.set_ylabel("Cantidad")
                        ax.set_title("Estadística Solicitada")
                        ax.spines["top"].set_visible(False)
                        ax.spines["right"].set_visible(False)

                        for bar in bars:
                            yval = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, str(int(yval)), ha="center", va="bottom", fontsize=9)

                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close(fig)
                    except Exception as e:
                        st.error(f"No se pudo procesar el gráfico: {e}")

                st.markdown("--- ")
