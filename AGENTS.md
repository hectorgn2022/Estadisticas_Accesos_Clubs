
# AGENTS.md · Estadísticas de Acceso al Club
Api de Gemini con Google-genai y  LLM y modelo Gemini-3.5-flash-lite

## Qué es este proyecto
Aplicación que responde consultas estadísticas sobre los datos de accesos de personas al club

## Cómo está hecho

- Python 3.12.
- Interfaz: Streamlit 
- IA: Api de Gemini con Google-genai y  LLM y modelo Gemini-3.5-flash-lite
- Archivos: accesos_clubs.csv, app.py, requirements.txt, especificación.md
- Liga de especificación: https://github.com/hectorgn2022/Estadisticas_Accesos_Clubs/blob/main/requirements.txt

## Reglas
- La clave de la API va SIEMPRE en secretos (`st.secrets` en la ruta A, variable de entorno `GEMINI_API_KEY` en la ruta B). Nunca en el código, en el README ni en el chat.
- Cada llamada a la API va dentro de `try/except` y muestra un mensaje claro para el usuario.
- Textos de la interfaz en español, sencillos, pensados para alguien sin conocimientos técnicos.
- Cambios pequeños: uno por petición. Al terminar, explica qué has cambiado y por qué.
- Si añades una librería, añádela también a `requirements.txt` y dilo.
- No uses datos personales reales. Para probar, inventa ejemplos.

## Cómo comprobar que funciona
- https://estadisticasaccesosclubs-rc4gf2qfnofw4jpb6sqptw.streamlit.app/
- Casos de prueba (entrada → lo que esperamos):
  1. [Entre las edades de 45 a 60 años ¿Cuantos hombre y mujeres han venido?] → [Masculino 7, Femenino 4]
  2. [Despliega una grafica de barras que muestra cuantas personas han entrado por tipo de socio] → [TITULAR: 36 accesos, HIJO 36 accesos, CONYUTE: 28 accesos y la graficación de estos datos
  3. ¿Cuántas brujas volaron sobre el club?] → No hay registros de brujas volando sobre las instalaciones

## Qué no hacer
- No borres ni reescribas el README sin preguntar.
- No cambies el modelo ni la arquitectura sin preguntar.
- No hagas push ni despliegues sin que yo lo haya revisado.
