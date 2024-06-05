# Assestment

- Paso 1 -> Crear base de datos con el comando: python .\db\create_db.py
- Paso 2 -> Levantar el servidor: uvicorn app:app --host 0.0.0.0 --port 8000
- Paso 3 -> Ejecutar el jupyter notebook para comprobar que funciona todo.

**Nota muy importante** -> Debido a que recientemente he tenido que eliminar docker de mi ordenador por tema de espacio, no he podido comprobar si he dockerizado correctamente la API.
Por ello, la forma de levantar el servidor no es a través de docker. Además de que la creación de la base de datos tampoco la he dockerizado. Soy consciente.

**Autentificación** -> La forma de autentificación es muy simple. Se hace una solicitud a un cierto endpoint que solo pide el correo electrónico del usuario. Devuelve un token si el email está almacenado en la bbdd.
Cuando se realizan las llamadas a la api, se tiene que añadir dicho token. Todo esto se puede ver en test.ipynb.

## TODO
- Añadir documentación a las funciones.
- Almacenar las queries en un archivo a parte.
- Dockerizar la aplicación.
- Añadir captura de errores.
- Añadir logs.

## Get user data filtered by user ID -> Can be accessed by users with "user" and "admin" role.
Notas: Es extraño que cualquier usuario puede acceder a los datos de los demás usuarios. ¿Puede que lo haya entendido mal?



