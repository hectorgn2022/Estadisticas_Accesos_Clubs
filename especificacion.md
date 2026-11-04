
# Especificación · Estadísticas de Acceso al Club

## 1. Problema y usuario
¿Quién tiene el problema?
El personal de atención al cliente continuamente requiere hacer estadísticas en la información de accesos para saber por ejemplo que edades entran mas en que horarios, Cuantos accesos de personas mayores de 60 años, etc

¿Cómo lo resuelve hoy?
Exporta reportes del sistema a Excel y por medio de búsquedas, subtotales y tablas dinámicas resuelve lo que necesita

¿Qué le molesta de cómo lo hace hoy?
Cuando son consultas repetitivas solicita a desarrollo que se la incluyan en una opción de menú, lo malo es que la mayoría de las consultas se le ocurren al momento y entonces resolver es muy tardado

¿Qué parte resuelve la IA?
Con lenguaje natural el usuario realiza alrededor de los datos de accesos y la IA hace los cálculos o gráficas pertinentes para dar una respuesta
 No resuelve algunas de las preguntas de los usuarios por que no logra entender la pregunta o no tiene los datos para contestar

## 2. Qué hace el producto

1. Permite cargar un archivo CSV de una estructura fija con los datos de acceso de las personas en rango de fechas determinadas. En próximas versiones se realizaran las consultas basándose en MCP o API
2. El usuario teclea una consulta relacionada a los datos que se están manejando, pueden ser datos numéricos, nombres o pedir que se grafique alguna estadística
3. El usuario puede guardar una consulta que le resulto útil para volver a realizarla posteriormente

## 3. Entradas y salidas

El usuario entrega un archivo CSV de estructura fija con una bitácora de accesos que quiere analizar
El usuario teclea preguntas o consultas en relación a los datos que se manejan
El usuario obtiene respuesta del agente IA o grafica los datos solicitados
Ejemplo: “¿Cuántas personas mayores de 60 años han entrado a partir del día 1 de octubre del 2027?  Y obtendrá la respuesta de 23 

## 4. La pieza de IA

Se está usando el modelo gemini-3.5-flash-lite o Gemini-3.8-flash
Se está usando LLM Directo con Aprendizaje de contexto y no se uso RAG por que no era adecuado para trabajar en datos tabulares

## 5. Flujo del usuario

1. El usuario entra y ve una pantalla donde se le permite actualizar el archivo CSV, si no lo actualiza usa el último que subió antes
2. Se le presenta un cuadro de texto donde puede teclear consultas o solicitudes para graficar datos
3. Recibe la respuesta a la pregunta que hizo o la gráfica que solicito

## 6. Restricciones

- Coste cero: capa gratuita de la API y despliegue gratuito en streamlit
- La clave de la API va en secretos, nunca en el código.
- Sin datos personales reales. Los datos utilizados son FAKE
- Lenguaje sencillo, para alguien sin conocimientos técnicos.

## 7. Criterios de aceptación

La app está bien si:
Si al realizar una serie de consultas da los mismos resultados que si se hicieran en Excel
Los casos normales deben responder con una cifra, cifras o gráficas de acuerdo a lo que se solicita| [caso normal] | [qué debe pasar] |
SI se realizan consultas que no puede contestar se configuró para que solo respondiera “No se” y no marque error
Al acabarse la cuota la aplicación indica que el usuario a agotado sus limites de IA y debe esperar o cambiar de plan

## 8. Fuera de alcance 

Conexión directa con la base de datos por medio de MCP o APIs
Tipos complejos de gráficas, solo quedando graficas de Barra o Pay
Datos no incluidos en el archivo CSV
