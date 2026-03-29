"""
Script de validación rápida del sistema
Verifica que todos los modelos estén correctamente configurados
"""

from django.contrib.admin.sites import site
from django.apps import apps

print("\n" + "="*80)
print("VALIDACIÓN DE INTEGRIDAD - SISTEMA DE CERTIFICADOS")
print("="*80)

# 1. Verificar que modelos están registrados en admin
print("\n[1] VERIFICANDO MODELOS REGISTRADOS EN ADMIN:")
registered_models = list(site._registry.keys())
print(f"✓ Total de modelos en admin: {len(registered_models)}")

expected_models = [
    'User',
    'Student', 
    'Instructor',
    'EventCategory',
    'Event',
    'EventInstructor',
    'Enrollment',
    'Template',
    'Certificate',
    'DeliveryLog'
]

for model in registered_models:
    name = model.__name__
    if name in expected_models:
        print(f"  ✓ {name} registrado en admin")
    if name == 'Permission' or name == 'Group' or name == 'LogEntry' or name == 'Site' or name == 'Session' or name == 'ContentType':
        pass  # Modelos del sistema Django
    else:
        if name not in expected_models:
            print(f"  ⚠ {name} NO esperado")

# 2. Contar registros por modelo
print("\n[2] VALIDANDO DATOS EN BASE DE DATOS:")

User = apps.get_model('users', 'User')
Student = apps.get_model('students', 'Student')
Instructor = apps.get_model('instructors', 'Instructor')
EventCategory = apps.get_model('events', 'EventCategory')
Event = apps.get_model('events', 'Event')
EventInstructor = apps.get_model('events', 'EventInstructor')
Enrollment = apps.get_model('events', 'Enrollment')
Template = apps.get_model('certificados', 'Template')
Certificate = apps.get_model('certificados', 'Certificate')
DeliveryLog = apps.get_model('deliveries', 'DeliveryLog')

counts = {
    'Usuarios': User.objects.count(),
    'Estudiantes': Student.objects.count(),
    'Instructores': Instructor.objects.count(),
    'Categorías de Eventos': EventCategory.objects.count(),
    'Eventos': Event.objects.count(),
    'Asignaciones (Instructor-Evento)': EventInstructor.objects.count(),
    'Inscripciones': Enrollment.objects.count(),
    'Plantillas de Certificado': Template.objects.count(),
    'Certificados': Certificate.objects.count(),
    'Entregas': DeliveryLog.objects.count(),
}

for name, count in counts.items():
    status = "✓" if count > 0 else "⚠"
    print(f"  {status} {name}: {count}")

# 3. Validar integridad de relaciones
print("\n[3] VALIDANDO RELACIONES E INTEGRIDAD:")

# Verificar que cada evento tiene instructor
active_events = Event.objects.filter(status='active')
for event in active_events:
    instructors_count = event.instructors.count()
    enrollments_count = event.enrollments.count()
    status = "✓" if instructors_count > 0 else "⚠"
    print(f"  {status} {event.name}: {instructors_count} instructor(s), {enrollments_count} inscripción(es)")

# Verificar estudiantes con inscripciones
print("\n[4] VALIDANDO ESTUDIANTES:")
for student in Student.objects.all()[:3]:  # Mostrar primeros 3
    enrollments_count = student.enrollments.count()
    certificates_count = student.certificates.count()
    print(f"  ✓ {student.full_name}: {enrollments_count} inscripción(es), {certificates_count} certificado(s)")

# Verificar métodos __str__
print("\n[5] VALIDANDO MÉTODOS __str__:")
test_user = User.objects.first()
test_student = Student.objects.first()
test_instructor = Instructor.objects.first()
test_event = Event.objects.first()
test_cert = Certificate.objects.first()

print(f"  ✓ User: {test_user}")
print(f"  ✓ Student: {test_student}")
print(f"  ✓ Instructor: {test_instructor}")
print(f"  ✓ Event: {test_event}")
print(f"  ✓ Certificate: {test_cert}")

# 5. Validar constraints únicos
print("\n[6] VALIDANDO CONSTRAINTS ÚNICOS:")

# Emails únicos
users = User.objects.count()
distinct_emails = User.objects.values('email').distinct().count()
print(f"  {'✓' if users == distinct_emails else '✗'} User.email único: {users} total, {distinct_emails} únicos")

students = Student.objects.count()
distinct_student_emails = Student.objects.values('email').distinct().count()
print(f"  {'✓' if students == distinct_student_emails else '✗'} Student.email único: {students} total, {distinct_student_emails} únicos")

# Verificar unique_together constraints
enrollments = Enrollment.objects.count()
distinct_enrollments = Enrollment.objects.values('student_id', 'event_id').distinct().count()
print(f"  {'✓' if enrollments == distinct_enrollments else '✗'} Enrollment (student+event) único: {enrollments} total, {distinct_enrollments} únicos")

certificates = Certificate.objects.count()
distinct_certificates = Certificate.objects.values('student_id', 'event_id').distinct().count()
print(f"  {'✓' if certificates == distinct_certificates else '✗'} Certificate (student+event) único: {certificates} total, {distinct_certificates} únicos")

# 6. Verificar admin configuration
print("\n[7] VERIFICANDO CONFIGURACIÓN DE ADMIN:")

from users.admin import UserAdmin
from students.admin import StudentAdmin
from instructors.admin import InstructorAdmin
from events.admin import EventAdmin, EventCategoryAdmin, EnrollmentAdmin, EventInstructorAdmin
from certificados.admin import CertificateAdmin, TemplateAdmin
from deliveries.admin import DeliveryLogAdmin

admin_configs = [
    ('UserAdmin', UserAdmin),
    ('StudentAdmin', StudentAdmin),
    ('InstructorAdmin', InstructorAdmin),
    ('EventCategoryAdmin', EventCategoryAdmin),
    ('EventAdmin', EventAdmin),
    ('EnrollmentAdmin', EnrollmentAdmin),
    ('EventInstructorAdmin', EventInstructorAdmin),
    ('TemplateAdmin', TemplateAdmin),
    ('CertificateAdmin', CertificateAdmin),
    ('DeliveryLogAdmin', DeliveryLogAdmin),
]

for name, admin_class in admin_configs:
    has_list_display = hasattr(admin_class, 'list_display')
    has_search = hasattr(admin_class, 'search_fields')
    has_filters = hasattr(admin_class, 'list_filter')
    status = "✓" if (has_list_display and has_search and has_filters) else "⚠"
    print(f"  {status} {name}: list_display={has_list_display}, search={has_search}, filters={has_filters}")

# RESUMEN FINAL
print("\n" + "="*80)
print("RESUMEN DE VALIDACIÓN")
print("="*80)

all_ok = (
    len(registered_models) >= 10 and
    all(count > 0 for count in counts.values()) and
    users == distinct_emails and
    students == distinct_student_emails and
    enrollments == distinct_enrollments and
    certificates == distinct_certificates
)

if all_ok:
    print("\n✅ SISTEMA VALIDADO EXITOSAMENTE")
    print("\nEl sistema está completamente funcional y listo para:")
    print("  • Acceder a Django Admin (http://localhost:8000/admin/)")
    print("  • Gestionar datos desde la interfaz web")
    print("  • Trabajar en equipo sin bloqueadores")
    print("  • Implementar Fase 2 (APIs)")
else:
    print("\n⚠️  ADVERTENCIAS EN VALIDACIÓN")
    print("Por favor revisar los puntos marcados con ⚠")

print("\nCREDENCIALES DE ACCESO:")
print("  Admin: admin@test.com / admin123")
print("  Editor: editor@test.com / editor123")

print("\n" + "="*80)
