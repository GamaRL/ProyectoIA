# **Proyecto Final:** __AI/Thenea__

<pre>
<b>Materia:</b> Inteligencia Artificial
<b>Grupo:</b> 6
<b>Alumno:</b>  <a href="mailto:gamaliel.rios@ingenieria.unam.edu">Ríos Lira, Gamaliel</a>; <a href="mailto:marco.sanchez.hdez.333@gmail.com">Sánchez Hernández, Marco Antonio</a>
<b>Fecha:</b> 08/06/2023
</pre>

El proyecto se encuentra desarrollado en dos módulos separados que interactúan 
para conformar la aplicación completa.

## Backend
Se desarrolló haciendo uso del lenguaje de programación `Python` con el 
__framework__ `FastAPI` para construir una __REST API__. De igual forma, se 
utiliza una base de datos montada sobre `PostgreSQL`.

## Frontend
Se desarrolló haciendo uso de tecnologías web: `HTML 5`, `CSS 3` y un poco de 
`JavaScript`. Todo esto, soportado por el lenguaje de programación `C#`, 
haciendo uso de la herramienta `Blazor`, la cual se encuentra integrada en el 
__framework__ `.NET 7`.

## Ejecución de la aplicación
Se creó una capa de abstracción para la infraestructura de la aplicación 
haciendo uso de contenedores. Para esto, se utilizó la plataforma `Docker`, 
con ayuda de la herramienta auxiliar `Docker Compose`. Con lo anterior, para 
ejecutar la aplicación, únicamente se necesita ejecutar:
```bash
$ docker-compose build
```

```bash
$ docker-compose up
```
