
# Estadísticas de Acceso al Club
Enlace: https://estadisticasaccesosclubs-rc4gf2qfnofw4jpb6sqptw.streamlit.app/
Autor: Héctor Pedro González Fuentes
## Pitch
Personal de atención a clientes de clubes deportivo necesitan saber que personas están viniendo, edades, sexos, tipos de socio para poder así planear sus próximas actividades como clínicas, curos, entrenamientos.
La app tiene los registros de datos de acceso en un periodo determinado y por medio de lenguaje natural interpretará preguntas para analizar los datos que tiene y dar las respuestas. La respuesta puede ser en cantidades escalares o gráficas comparativas.
Se uso la IA para interpretar las consultas en lenguaje natural y analizar los datos que tiene para brindar respuestas a las consultas
Como generar una pequeña aplicación sin usar programación, como integrar los diferentes modelos de googleia
Estos son algunos ejemplos de datos
Fecha	Hora	Socio	Tipo Socio	Nombre	Edad	Sexo
01/10/2025	04:59	1185	CONYUGE	Lafuente Roca Biel	75	Femenino
01/10/2025	04:59	1185	TITULAR	Montoya Prado Leonardo	78	Masculino
01/10/2025	04:59	341	CONYUGE	Palomo Palacios Pedro Jose	63	Femenino
01/10/2025	04:59	341	TITULAR	Peña Heredia Antoni	92	Masculino
01/10/2025	04:59	1311	CONYUGE	Carvajal Cuadrado Ana	68	Femenino
01/10/2025	04:59	1311	TITULAR	Galvez De La Fuente Maria Begoña	70	Masculino
01/10/2025	04:59	151	HIJO/A	Blazquez Bonilla Cristina	24	Masculino

Y algunas consultas de ejemplo podrán ser
* Despliega una grafica de barras que muestra cuantas personas han entrado por tipo de socio
* ¿Entre las edades de 45 a 60 años ¿Cuantos hombre y mujeres han venido?

## El problema

El problema lo tiene el personal de atención a clientes de clubes deportivos. Son consultas que se ofrecen al momento y no se pueden automatizar por que son diferentes cada vez. Lo resuelven exportando información a Excel y ahí hacen búsquedas, subtotales y tablas dinámicas

## Qué hace la app

•	El usuario puede subir una hoja format CSV con los registros de acceso del periodo que quiere analizar
•	EL usuario realiza consultas en lenguaje natural
•	Puede guardar la consulta si considera que la puede usar repetidamente

## La pieza de IA
Se usa el modelo Gemini-3.5-flash-lite utilizando un enfoque LLM con técnicas de Aprendizaje de Contexto utilizando gooogleai 
RAG no se maneja bien con datos tabulares y las pruebas resultaron positivas al usar LLM y Aprendizaje de Contexto
En caso de fallas la aplicación la aplicación manda un mensaje para que vuelva a hacer la consulta mas tarde o revise si sus cuotas ya se terminaron

## Cómo la he construido
Se utilizó Gemini Colab
Fichero de agente: https://github.com/hectorgn2022/Estadisticas_Accesos_Clubs/blob/main/AGENTS.md
**Prompt1:
Soy desarrollador de software en un club deportivo y de golf.
Tengo que desarrollar una aplicación que ayude al personal de Servicio a cliente a sacar estadísticas sobre los accesos de las personas que entran al club.
La estadística se basa en una lista de Excel o CSV que incluye los siguientes datos:
Fecha: La fecha de ingreso al club Hora: Hora de ingreso Socio: Clave númerica del socio Tipo de Socio: (TITULAR, CONYUGE, HIJO) Nombre: Nombre de la persona Edad: Edad de la persona Sexo: Sexo de la persona, (Masculino o femenino)
Las estadísticas que se obtendrán serán a partir de un chat donde se realizarán las consultas en lenguaje natural y la aplicación resolverá la respuesta o un “No se”
**Prompt2:
Ahora necesito conformar una aplicación que subirá en la nube. Para ello requiero publicar la aplicación en streamlit La aplicación mostrará a) Un titulo “Estadísticas de Acceso al Club” b) Un subtitulo que diga “Captura tu consulta y oprime ” c) Abajo ofrecer un menu a la derecha con las siguientes opciones: Cargar Archivo CSV, Guardar Consulta anterior (La cual por el momento no hace nada) d) En la parte de operación mostrará un campo texto donde el usuario tecleará su consulta y el botón enviar, a continuación se responderá la pregunta. Tanto la pregunta como la respuesta deben irse mostrando de manera histórica en la parte de arriba
**Prompt3:
Requiero que en la barra lateral de opciónes el botón "Guardar Consulta anterior" guarde en un archivo de texto la consulta y ademas agregue un botón adicional debajo de "Guardar Consulta anterior" para que esa consulta ya quede como un botón y poderla invocar mas adelante
**Prompt4:
Poner un incono junto a la consulta guardada para poder borrarla. Si el usuario la oprime entonces borrar esa consulta

**Qué delegué al agente y qué revisé a mano:**
En general todo el desarrollo lo delegué al agente (Fue parte de mi propósito). Manualmente realice pruebas y por medio de prompts mas sencillos fui haciendo ajustes a la aplicación.

## Prueba y mejora
La mayor parte de las pruebas las hice yo y traté de eliminar los errores que ya tenía. Posteriormente pedí a a un cliente que ya usa nuestro sistema y que es del departamento de atención a cliente que lo usara y me pasara sus comentarios
Salieron muchas respuestas de “No se” si llegamos a tener error 503 y 429

## Capturas

!Pantalla Inicial(https://github.com/hectorgn2022/Estadisticas_Accesos_Clubs/blob/main/Pantalla%20inicial.png)
!Primera Consulta Realizada(https://github.com/hectorgn2022/Estadisticas_Accesos_Clubs/blob/main/Primera%20consulta%20realizada.png)
!Interaccion con la IA en COALB(https://github.com/hectorgn2022/Estadisticas_Accesos_Clubs/blob/main/Interacci%C3%B3n%20con%20la%20IA%20en%20COLAB.png)
!No se puede interpretar la consulta (https://github.com/hectorgn2022/Estadisticas_Accesos_Clubs/blob/main/No%20puede%20interpretar%20la%20consulta.png)
