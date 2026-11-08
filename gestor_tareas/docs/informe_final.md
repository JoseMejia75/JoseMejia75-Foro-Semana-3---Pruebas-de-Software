# Informe final de pruebas – Sistema de Gestión de Tareas

**Proyecto:** Sistema de Gestión de Tareas (Plásticos Sustentables)
**Tester:** ______________________  **Fecha:** ______________

## 1. Resumen del proceso
Se desarrolló el sistema con Python, Flask y SQLite, y se probó con pytest siguiendo cuatro niveles: unitarias (validaciones), integración (rutas junto con la base de datos), aceptación (recorridos completos de usuario) y regresión (defectos ya corregidos). Las pruebas se ejecutan automáticamente en GitHub Actions con cada *push* o *pull request*.

## 2. Resultados
- 59 pruebas automatizadas, todas aprobadas en la última ejecución.
- Cobertura de líneas: 99 % (248 de 249 líneas).
- Pendiente: ejecutar y registrar las pruebas manuales CP-25 y CP-26.

## 3. Problemas encontrados y soluciones

| ID | Problema | Cómo se encontró | Solución | Estado |
|----|----------|------------------|----------|--------|
| DEF-01 | Al editar una tarea asignada, el campo "Asignar a" aparecía vacío; al guardar se perdía la asignación. | Revisión exploratoria del flujo de edición | Se carga el usuario asignado en el formulario | Corregido (CP-23) |
| DEF-02 | Buscar `%` o `_` devolvía todas las tareas porque se interpretaban como comodines de SQL. | Prueba exploratoria de la búsqueda | Se escapan los comodines antes de consultar | Corregido (CP-24) |

## 4. Limitaciones y riesgos conocidos
- No hay protección CSRF en los formularios (recomendado agregar Flask-WTF antes de producción).
- No hay límite de intentos de inicio de sesión.
- No se probó la interfaz en un navegador real con Selenium; las pruebas de aceptación usan el cliente de pruebas de Flask.
- Las pruebas de rendimiento y seguridad avanzada quedan fuera del alcance.

## 5. Conclusión
El sistema cumple las funcionalidades clave del Anexo II. Los dos defectos hallados se corrigieron y quedaron cubiertos con pruebas de regresión. Antes de ponerlo en uso real se recomienda agregar CSRF y completar las pruebas manuales.
