# Materia Programación para Analítica de Datos - Flight Delay Dashboard

## URL pública

https://<https://stefania-duarte-flight-dashboard.onrender.com/>

## Descripción

Este proyecto consiste en un dashboard interactivo construido con Dash para visualizar los retrasos promedio de vuelos por aerolínea y por mes.

La persona que ingrese al URL puede seleccionar un año y consultar cinco causas de retraso:

- Carrier Delay
- Weather Delay
- NAS Delay
- Security Delay
- Late Aircraft Delay

## Cómo ejecutarlo en local

Yo utilizo Mac, por eso:

```bash
python3 -m venv .venv
```

## 2. Instalar las dependencias

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## 3. Ejecutar el dashboard

```bash
.venv/bin/python dashboard.py
```

## 4. Abrir el dashboard

En el navegador:

http://127.0.0.1:8050

## Estructura del proyecto

Lo que requerimos para que nuestra URL funcione: 
```text
Proyecto_final/
dashboard.py
airline_data.csv
requirements.txt
Procfile
render.yaml
.python-version
.gitignore
README.md
```

### Descripción de los archivos

### Descripción de los archivos

- `dashboard.py`: es el archivo principal del proyecto. Aquí está el dashboard, el código para organizarlo, procesar los datos y actualizar los gráficos.
- `airline_data.csv`: es la base de datos que utilizamos para hacer el análisis y generar los gráficos.
- `requirements.txt`: contiene las librerías que necesitamos para poder ejecutar el proyecto.
- `Procfile`: indica cómo se debe iniciar la aplicación cuando se publique.
- `render.yaml`: contiene la configuración que vamos a utilizar para desplegar el proyecto en Render.
- `.python-version`: indica la versión de Python que utiliza el proyecto.
- `.gitignore`: indica qué archivos o carpetas no se deben subir al repositorio.
- `README.md`: contiene la información y las instrucciones para entender y ejecutar el proyecto.

## Datos

Utilizamos el archivo `airline_data.csv` visto bien clase. Las principales variables utilizadas son:

- `Year`
- `Month`
- `Reporting_Airline`
- `CarrierDelay`
- `WeatherDelay`
- `NASDelay`
- `SecurityDelay`
- `LateAircraftDelay`

## Sobre los gráficos:

Se utilizaron gráficos de líneas para mostrar la evolución mensual de los retrasos y permitir comparar las aerolíneas.

Cada gráfico utiliza una causa diferente de retraso y la aerolínea se representa mediante el color de la serie.

Los ejes de los gráficos indican el tiempo promedio de retraso en minutos.


```text
Stefania Duarte
26 de septiembre de 2026
```