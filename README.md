TODAS LAS SALIDAS DE LOS ARCHIVOS EJECUTADOS SE ENCUENTRAN EN EL ARCHIVO (SALIDAS.PDF)
se crea la conexión mediante API en Python para obtener los datos (archivo spaceflight_pipeline.py)
desde el browser se descarga una muestra de los datos de Articulos (carpeta json_files --> archivo response_1738701028595.json)
se utiliza el archivo Analisis_Python.py para diferentes estadísticas y analisis se muestran algunas graficas de tendencias, aqui se podría utilizar un modelo de machine learning, podría ser de clasificación, este archivo se puede traducir a SPARK  para una ejecución más rápida y escalable, el py genera un archivo processed_news.csv donde descarga en formato excel lo tratado en los articulos.
se crea el archivo querysSQL _sqlite3_pandas.py simulando una base de datos que se descarga en el archivo news_database.db de la cual se hacen los querys embebidos de SQL con dos SELECT funcionando
los archivos tipo json (response_XXXXXX) son pruebas realizadas con diferentes archivos descargados de la base
se utilizan otros archivos de prueba como revisandoJson.py o conexion.py para revisar variables u otros 
el archivo (Diseño de Arquitectura del Sistema de Análisis de Tendencias en la Industria Espacial.DOCX) esta en word y generaliza una arquitectura en AWS de acuerdo a los servicios 
se trabaja desde Visual Code Studio unido a repositorio en GitHub.
