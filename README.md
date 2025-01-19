# API de Gestión de Libros

Este proyecto es una API RESTful creada con **Django REST Framework** (Django RF) que utiliza **MongoDB** como base de datos para gestionar una colección de **libros**. La API permite realizar operaciones CRUD (crear, leer, actualizar, eliminar) sobre los libros.

---

### Índice

1. [Descripción](#descripción)
2. [Tecnologías utilizadas](#tecnologías-utilizadas)
3. [Instalación](#instalación)
4. [Uso de la API](#uso-de-la-api)
5. [Ejecutar el proyecto con Docker](#ejecutar-el-proyecto-con-docker)

6. [Agregar Libros de Prueba](#agregar-libros-prueba)

7. [Test Unitarios y Coverage](#test-unit-coverage)

---

## Descripción

Esta API permite gestionar una base de datos de **libros** utilizando **MongoDB**. Los usuarios pueden realizar operaciones como:

- **Crear un libro**: Insertar un nuevo libro en la base de datos.
- **Obtener todos los libros**: Listar todos los libros almacenados.
- **Actualizar un libro**: Modificar un libro existente.
- **Eliminar un libro**: Eliminar un libro de la base de datos.
---

## Tecnologías utilizadas

Este proyecto está desarrollado con las siguientes tecnologías:

- **Python 3.12**
- **Django 3.1.12**
- **Django REST Framework 3.14.0**
- **Djongo 1.3.7** (para conectar Django con MongoDB)
- **MongoDB** (base de datos NoSQL)
- **JWT** (para autenticación de usuarios)
- **Docker** (para contenerización y facilitar el entorno de desarrollo)
- **Docker Compose** (para gestionar la orquestación de contenedores)

---

## Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/wcgarcia5/seek_test.git
cd seek_test
```

## Uso de la API
En el repositorio se encuentran 2 Archivos llamados
```bash
postman.json
Swagger.json
```
estos muestran como usar el API

## Ejecutar el proyecto con Docker
```bash
docker-compose up --build
```

## Agregar Libros de Prueba
Cuando hayas clonado el repositorio y creado tu access_token puedes correr la peticion que se encuentra en postman llamada "Migrate Books (Bulk Create)" o hacer un curl si deseas tu mismo agregar los libros

```bash
curl --location 'localhost:8000/api/books/migrate' \
--header 'Authorization: Bearer {{token}}' \
--header 'Content-Type: application/json' \
--data '[
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "published_date": "2008-08-11",
        "genre": "Programming",
        "price": 45.99
    }
]'
```

## Test Unitarios y Coverage
```bash
coverage run manage.py test 
coverage report
coverage html
```