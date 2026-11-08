# Documentación de pruebas – Sistema de Gestión de Tareas

Resultado de la última ejecución: **59 pruebas, 59 aprobadas, 0 fallidas. Cobertura de líneas: 99 %** (`pytest --cov=app`).

## 1. Casos de prueba por funcionalidad

| ID | Nivel | Tipo | Funcionalidad | Caso | Resultado esperado | Estado |
|----|-------|------|---------------|------|--------------------|--------|
| CP-01 | Unitaria | Auto | Registro | Usuario vacío, de 2 caracteres o solo espacios | Se rechaza con mensaje | Aprobado |
| CP-02 | Unitaria | Auto | Registro | Correos válidos e inválidos (sin @, sin dominio, con espacios) | Solo los válidos pasan | Aprobado |
| CP-03 | Unitaria | Auto | Registro | Contraseña corta, solo letras o solo números | Se rechaza | Aprobado |
| CP-04 | Unitaria | Auto | Tareas | Título vacío o de más de 100 caracteres | Se rechaza (100 exactos sí pasa) | Aprobado |
| CP-05 | Unitaria | Auto | Tareas | Fecha en formato incorrecto o imposible (2026-13-45) | Se rechaza; vacía es válida | Aprobado |
| CP-06 | Integración | Auto | Registro | Registro correcto | Usuario guardado, contraseña cifrada, correo en minúsculas | Aprobado |
| CP-07 | Integración | Auto | Registro | Usuario o correo duplicado | Mensaje de error | Aprobado |
| CP-08 | Integración | Auto | Inicio de sesión | Credenciales correctas / contraseña mala / usuario inexistente | Entra / mensaje de error | Aprobado |
| CP-09 | Integración | Auto | Sesión | Cerrar sesión y entrar a rutas protegidas | Redirige al login | Aprobado |
| CP-10 | Integración | Auto | Tareas | Crear tarea válida / sin título / fecha mala | Se guarda / se rechaza | Aprobado |
| CP-11 | Integración | Auto | Tareas | Editar y eliminar tarea propia | Cambios reflejados / tarea borrada | Aprobado |
| CP-12 | Integración | Auto | Tareas | Abrir o borrar tarea inexistente | Error 404 | Aprobado |
| CP-13 | Integración | Auto | Asignación | Asignar a usuario existente / inexistente | Se asigna / mensaje de error | Aprobado |
| CP-14 | Integración | Auto | Asignación | El asignado ve la tarea y la marca completada | Funciona | Aprobado |
| CP-15 | Integración | Auto | Autorización | El asignado intenta editar o eliminar | Error 403 | Aprobado |
| CP-16 | Integración | Auto | Autorización | Otro usuario intenta ver, editar o borrar una tarea ajena | No la ve; error 403 | Aprobado |
| CP-17 | Integración | Auto | Filtros | Completadas / pendientes | Solo muestra las del estado | Aprobado |
| CP-18 | Integración | Auto | Búsqueda | Por título y por descripción | Solo coincidencias | Aprobado |
| CP-19 | Integración | Auto | Perfil | Editar perfil, correo inválido, usuario repetido | Se guarda / error | Aprobado |
| CP-20 | Integración | Auto | Perfil | Cambiar contraseña (correcta, actual mala, nueva débil) | Entra con la nueva / error | Aprobado |
| CP-21 | Aceptación | Auto | Flujo completo | Supervisor crea y asigna; operario completa; supervisor elimina | Flujo sin errores | Aprobado |
| CP-22 | Aceptación | Auto | Acceso | Entrar sin sesión / lista vacía | Login / "No hay tareas" | Aprobado |
| CP-23 | Regresión | Auto | Edición | Abrir editar una tarea asignada | El campo asignado aparece precargado (DEF-01) | Aprobado |
| CP-24 | Regresión | Auto | Búsqueda | Buscar `%` | Busca el texto literal (DEF-02) | Aprobado |
| CP-25 | Sistema | Manual | Usabilidad | Revisar mensajes, botones y navegación en navegador | Claros y consistentes | Pendiente de ejecutar |
| CP-26 | Sistema | Manual | Exploratoria | Textos largos, caracteres especiales, doble clic en botones | Sin errores visibles | Pendiente de ejecutar |

Los casos CP-25 y CP-26 son manuales: se ejecutan abriendo la aplicación con `python run.py` y quedan por registrar.

## 2. Análisis de cobertura

| Módulo | Líneas | No cubiertas | Cobertura |
|--------|--------|--------------|-----------|
| app/__init__.py | 14 | 0 | 100 % |
| app/auth.py | 52 | 0 | 100 % |
| app/db.py | 20 | 0 | 100 % |
| app/profile.py | 37 | 0 | 100 % |
| app/tasks.py | 93 | 1 | 99 % |
| app/validators.py | 33 | 0 | 100 % |
| **Total** | **249** | **1** | **99 %** |

La cobertura mide líneas ejecutadas por las pruebas, no que el sistema esté libre de errores.
