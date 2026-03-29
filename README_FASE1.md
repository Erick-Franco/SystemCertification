# Sistema de Certificados - Backend Django

**Estado:** Fase 1 Completa ✅  
**Fecha:** Marzo 2026

## Descripción

Sistema profesional de gestión de certificados digitales construido con Django y PostgreSQL. Permite la creación, validación y entrega de certificados asociados a eventos de formación.

## Arquitectura

```
Sistema de Certificados
│
├── Users (Gestión de administradores)
├── Students (Base de estudiantes)
├── Instructors (Base de instructores)
├── Events (Eventos de formación)
│   ├── EventCategory (Categorías de eventos)
│   ├── EventInstructor (Asignación de instructores)
│   └── Enrollment (Inscripciones de estudiantes)
├── Certificados (Gestión de certificados)
│   ├── Template (Plantillas de diseño)
│   └── Certificate (Certificados emitidos)
└── Deliveries (Historial de entregas)
```

## Fase 1: Sistema Funcional Mínimo

### ✅ Completado

#### 1. Modelos Django Profesionales
- **8 modelos** completamente funcionales
- Relaciones correctamente definidas
- `unique_together` constraints para evitar duplicados
- Métodos `__str__` descriptivos
- Meta classes con `ordering`, `verbose_name`, `indexes`

#### 2. Django Admin Completamente Configurado
- **Lista inteligente** (`list_display`, `search_fields`, `list_filter`)
- **Visualización mejorada** con badges de colores y contadores
- **Fieldsets organizados** con secciones colapsibles
- **Búsqueda avanzada** en todos los modelos
- **Filtros por fecha** usando `date_hierarchy`

Modelos en Admin:
- ✅ Users: Roles con badges, admin management
- ✅ Students: Perfil completo, contador de cursos
- ✅ Instructors: Especialidad, eventos asignados
- ✅ Events & Categories: Estadísticas, instructores
- ✅ Enrollments: Asistencia, calificaciones
- ✅ Certificates: Código verificación, templates
- ✅ Delivery Logs: Estado, métodos de entrega

#### 3. Flujo Completo Funcional
```
Usuario Admin
    ↓
1. Crear Categoría de Evento
2. Crear Evento
3. Asignar Instructores al Evento
4. Crear/Importar Estudiantes
5. Registrar Inscripciones
6. Marcar Asistencia
7. Generar Certificados
8. Registrar Entregas
```

Todos estos pasos son funcionales desde el admin sin necesidad de shell.

#### 4. Validaciones de Datos
- Email unique en Users, Instructors, Students
- Document ID unique en Students
- Verification Code unique en Certificate
- Student + Event unique en Enrollment y Certificate
- Event + Instructor unique en EventInstructor
- Campos obligatorios validados

#### 5. Datos de Prueba
Script automatizado `scripts/seed_data.py` que crea:
- 2 usuarios administrativos
- 3 categorías de eventos
- 3 instructores con especialidades
- 3 eventos completos
- 5 estudiantes
- 8 inscripciones (algunos con asistencia)
- 2 plantillas de certificados
- 6 certificados emitidos
- 4 entregas registradas

## Instalación y Uso Rápido

### 1. Crear Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Cargar Datos de Prueba
```bash
python manage.py shell < scripts/seed_data.py
```

### 3. Entrar al Admin
```bash
python manage.py runserver
# Ir a http://localhost:8000/admin/
# Credenciales: admin@test.com / admin123
```

## Flujo de Trabajo para Desarrolladores

### Para Backend

1. **Revisar la estructura:**
   ```bash
   # Ver modelos
   grep -r "class.*Model" --include="*.py" | grep models
   ```

2. **Verificar admin:**
   - Ir a `/admin/` y validar listados
   - Verificar búsqueda y filtros

3. **Añadir funcionalidad:**
   - Seguir patrón de `related_name` usado
   - Agregar métodos útiles al modelo
   - Actualizar admin si agrega campos

### Para APIs (Fase 2)

- Estructura de modelos está lista para Serializers de DRF
- Relaciones bien definidas facilitan nested serializers
- `unique_together` constraints ya validados

### Para Frontend

- Documentación de endpoints estará en Fase 2
- Por ahora, admin sirve para validar datos y estructura

## Configuración por App

### users (Gestión de Admin)
- Model: User (BaseUser personalizado)
- Admin: roles (admin, editor), permisos de staff
- Related Names: templates, created_events, generated_certificates

### students (Base de Estudiantes)
- Model: Student
- Campos: document_id, email (únicos), nombre, teléfono
- Relaciones: enrollments, certificates
- Admin: búsqueda por documento, nombre, email

### instructors (Base de Instructores)
- Model: Instructor
- Campos: email (único), especialidad, bio, firma
- Relaciones: events (muchos-a-muchos mediante EventInstructor)
- Admin: filtro por especialidad, contador de eventos

### events (Eventos de Formación)
- Models: EventCategory, Event, EventInstructor, Enrollment
- Event states: draft, active, finished, cancelled
- Relaciones: categoría, creador, instructores, estudiantes
- Admin: badges por estado, estadísticas de asistencia

### certificados (Certificados)
- Models: Template, Certificate
- Certificate states: pending, generated, sent, failed
- Código verificación: único, hasheable
- Admin: búsqueda por código, preview de plantilla

### deliveries (Historial de Entregas)
- Model: DeliveryLog
- Métodos: email, whatsapp, link
- Estados: success, error, pending
- Admin: historial completo con timestamps

## Restricciones Base de Datos

| Modelo | Campo | Restricción | Razón |
|--------|-------|------------|-------|
| User | email | UNIQUE | Autenticación |
| Student | document_id, email | UNIQUE | Identificación única |
| Instructor | email | UNIQUE | Contacto |
| Certificate | student + event | UNIQUE | Un certificado por curso |
| Enrollment | student + event | UNIQUE | Una inscripción por curso |
| EventInstructor | event + instructor | UNIQUE | Evitar duplicados |

## Validación Completa

Ver `VALIDATION_GUIDE.md` para guía paso a paso de validación en admin.

**Checklist rápido:**
- [ ] Acceder a `/admin/` con credentials de prueba
- [ ] Ver todos los 8 modelos listados
- [ ] Búsqueda funciona en cada sección
- [ ] Filtros aplican correctamente
- [ ] Badges de color se muestran
- [ ] Crear 1 registro nuevo en cada sección
- [ ] Editar registro existente
- [ ] Intentar crear duplicate → Falla
- [ ] Ver relaciones en detalles

## Para Agregar Funcionalidad Futura

### Nuevos Campos
1. Agregar a modelo en `models.py`
2. Crear migración: `python manage.py makemigrations`
3. Correr migración: `python manage.py migrate`
4. Actualizar admin en `admin.py` si es visible

### Nuevas Validaciones
- Agregar `clean()` method en modelo
- Agregar validators en field definition
- Validar en admin con `form_class` o override

### Nuevos Modelos
1. Crear en `models.py` siguiendo patrones existentes
2. Registrar en `admin.py` siguiendo estructura profesional
3. Crear migración y correrla
4. Actualizar documentación

## Notas de Diseño

### UUIDs
Todos los modelos usan `UUIDField` como primary key para:
- Escalabilidad con bases de datos distribuidas
- Seguridad (no expone IDs secuenciales)
- Compatibilidad con APIs modernas

### Timestamps
`created_at` y `updated_at` en todos los modelos para:
- Auditoría
- Ordenamiento automático
- Debugging

### Related Names
Se usa `related_name` en todos los ForeignKey para:
- Acceso inverso fácil (ej: `event.enrollments.all()`)
- Queries más legibles
- Facilitar admin y APIs futuras

## Stack Tecnológico
- Django 5.x
- PostgreSQL (recomendado)
- Django Admin (nativo)
- Python 3.11+

## Siguiente Fase (Fase 2)
- APIs REST con Django REST Framework
- Autenticación JWT
- Endpoints para generar certificados PDF
- Sistema de entregas automáticas
- Dashboard de analíticas

## Soporte

Para dudas sobre estructura o flujo, revisar:
1. Este README
2. `VALIDATION_GUIDE.md`
3. Comentarios en `admin.py`
4. Docstrings en `models.py`

---

**Status:** ✅ Listo para que otros desarrolladores trabajen sin bloqueos
**Última actualización:** Marzo 2026
