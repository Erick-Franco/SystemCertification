"""
Script para crear datos de prueba mínimos para validar el sistema.
Uso: python manage.py shell < scripts/seed_data.py
"""

import json
from datetime import datetime, timedelta
from uuid import uuid4
from decimal import Decimal

from django.contrib.auth import get_user_model
from students.models import Student
from instructors.models import Instructor
from events.models import EventCategory, Event, EventInstructor, Enrollment
from certificados.models import Template, Certificate
from deliveries.models import DeliveryLog

User = get_user_model()

print("=" * 80)
print("INICIANDO CREACIÓN DE DATOS DE PRUEBA")
print("=" * 80)

# ============================================================================
# 1. CREAR USUARIOS ADMINISTRATIVOS
# ============================================================================
print("\n[1] Creando usuarios administrativos...")

try:
    admin_user = User.objects.get(email='admin@test.com')
    print(f"✓ Usuario admin ya existe: {admin_user}")
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        email='admin@test.com',
        full_name='Admin User',
        password='admin123'
    )
    print(f"✓ Usuario admin creado: {admin_user}")

try:
    editor_user = User.objects.get(email='editor@test.com')
    print(f"✓ Usuario editor ya existe: {editor_user}")
except User.DoesNotExist:
    editor_user = User.objects.create_user(
        email='editor@test.com',
        full_name='Editor User',
        password='editor123',
        role='editor',
        is_staff=True
    )
    print(f"✓ Usuario editor creado: {editor_user}")

# ============================================================================
# 2. CREAR CATEGORÍAS DE EVENTOS
# ============================================================================
print("\n[2] Creando categorías de eventos...")

categories_data = [
    {'name': 'Programación', 'description': 'Cursos de programación en diversos lenguajes'},
    {'name': 'Diseño', 'description': 'Cursos de diseño gráfico y UX/UI'},
    {'name': 'Data Science', 'description': 'Cursos de análisis de datos'},
]

categories = {}
for cat_data in categories_data:
    cat, created = EventCategory.objects.get_or_create(**cat_data)
    if created:
        print(f"✓ Categoría creada: {cat.name}")
    else:
        print(f"✓ Categoría ya existe: {cat.name}")
    categories[cat_data['name']] = cat

# ============================================================================
# 3. CREAR INSTRUCTORES
# ============================================================================
print("\n[3] Creando instructores...")

instructors_data = [
    {
        'full_name': 'Dr. Juan Pérez',
        'email': 'juan.perez@test.com',
        'phone': '+34 600 100 200',
        'specialty': 'Python & Django',
        'bio': 'Instructor de programación con 15 años de experiencia',
    },
    {
        'full_name': 'María García López',
        'email': 'maria.garcia@test.com',
        'phone': '+34 600 100 201',
        'specialty': 'Diseño UX/UI',
        'bio': 'Diseñadora de experiencia de usuario especializada en web',
    },
    {
        'full_name': 'Carlos Martínez Rodríguez',
        'email': 'carlos.martinez@test.com',
        'phone': '+34 600 100 202',
        'specialty': 'Data Science & Machine Learning',
        'bio': 'Data scientist con experiencia en IA',
    },
]

instructors = {}
for inst_data in instructors_data:
    instructor, created = Instructor.objects.get_or_create(
        email=inst_data['email'],
        defaults=inst_data
    )
    if created:
        print(f"✓ Instructor creado: {instructor.full_name}")
    else:
        print(f"✓ Instructor ya existe: {instructor.full_name}")
    instructors[inst_data['email']] = instructor

# ============================================================================
# 4. CREAR EVENTOS
# ============================================================================
print("\n[4] Creando eventos...")

today = datetime.now().date()
events_data = [
    {
        'name': 'Django Avanzado - Semestre 2026',
        'description': 'Curso intensivo de Django Framework con patrones profesionales',
        'category': categories['Programación'],
        'event_date': today + timedelta(days=7),
        'end_date': today + timedelta(days=14),
        'duration_hours': 40,
        'location': 'Aula 101 - Campus Principal',
        'status': 'active',
        'created_by': admin_user,
        'instructors': ['juan.perez@test.com']
    },
    {
        'name': 'Diseño Web Moderno 2026',
        'description': 'Aprende los principios modernos de diseño web',
        'category': categories['Diseño'],
        'event_date': today + timedelta(days=10),
        'end_date': today + timedelta(days=20),
        'duration_hours': 30,
        'location': 'Sala de Diseño - Piso 2',
        'status': 'active',
        'created_by': admin_user,
        'instructors': ['maria.garcia@test.com']
    },
    {
        'name': 'Intro a Data Science con Python',
        'description': 'Introducción a análisis de datos y machine learning',
        'category': categories['Data Science'],
        'event_date': today + timedelta(days=5),
        'end_date': today + timedelta(days=15),
        'duration_hours': 35,
        'location': 'Laboratorio de Datos - Piso 3',
        'status': 'active',
        'created_by': admin_user,
        'instructors': ['carlos.martinez@test.com']
    },
]

events = {}
for evt_data in events_data:
    instructors_list = evt_data.pop('instructors')
    
    event, created = Event.objects.get_or_create(
        name=evt_data['name'],
        event_date=evt_data['event_date'],
        defaults=evt_data
    )
    
    if created:
        print(f"✓ Evento creado: {event.name}")
        
        # Asignar instructores al evento
        for inst_email in instructors_list:
            event_instructor, _ = EventInstructor.objects.get_or_create(
                event=event,
                instructor=instructors[inst_email],
                defaults={'role': 'principal'}
            )
    else:
        print(f"✓ Evento ya existe: {event.name}")
    
    events[evt_data['name']] = event

# ============================================================================
# 5. CREAR ESTUDIANTES
# ============================================================================
print("\n[5] Creando estudiantes...")

students_data = [
    {
        'document_id': '12345678-A',
        'first_name': 'Ana',
        'last_name': 'López García',
        'email': 'ana.lopez@test.com',
        'phone': '+34 600 200 100',
    },
    {
        'document_id': '87654321-B',
        'first_name': 'Roberto',
        'last_name': 'Sánchez Martínez',
        'email': 'roberto.sanchez@test.com',
        'phone': '+34 600 200 101',
    },
    {
        'document_id': '11223344-C',
        'first_name': 'María',
        'last_name': 'González Rodríguez',
        'email': 'maria.gonzalez@test.com',
        'phone': '+34 600 200 102',
    },
    {
        'document_id': '44556677-D',
        'first_name': 'Fernando',
        'last_name': 'Díaz López',
        'email': 'fernando.diaz@test.com',
        'phone': '+34 600 200 103',
    },
    {
        'document_id': '99887766-E',
        'first_name': 'Sofia',
        'last_name': 'Ruiz García',
        'email': 'sofia.ruiz@test.com',
        'phone': '+34 600 200 104',
    },
]

students = {}
for std_data in students_data:
    student, created = Student.objects.get_or_create(
        email=std_data['email'],
        defaults=std_data
    )
    if created:
        print(f"✓ Estudiante creado: {student.full_name}")
    else:
        print(f"✓ Estudiante ya existe: {student.full_name}")
    students[std_data['email']] = student

# ============================================================================
# 6. CREAR INSCRIPCIONES (ENROLLMENTS)
# ============================================================================
print("\n[6] Creando inscripciones de estudiantes...")

# Inscribir estudiantes en eventos
enrollment_plan = {
    'Django Avanzado - Semestre 2026': [
        ('ana.lopez@test.com', True, Decimal('8.5')),
        ('roberto.sanchez@test.com', True, Decimal('7.8')),
        ('maria.gonzalez@test.com', False, None),
    ],
    'Diseño Web Moderno 2026': [
        ('maria.gonzalez@test.com', True, Decimal('9.0')),
        ('fernando.diaz@test.com', True, Decimal('8.2')),
    ],
    'Intro a Data Science con Python': [
        ('ana.lopez@test.com', True, Decimal('7.5')),
        ('sofia.ruiz@test.com', True, Decimal('8.8')),
        ('fernando.diaz@test.com', False, None),
    ],
}

for event_name, enrollments_data in enrollment_plan.items():
    event = events[event_name]
    for student_email, attendance, grade in enrollments_data:
        student = students[student_email]
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            event=event,
            defaults={
                'attendance': attendance,
                'grade': grade,
                'notes': f"Inscripción automática - Test data"
            }
        )
        if created:
            status = "✓ Asistió" if attendance else "✗ Ausente"
            print(f"  ✓ Inscripción: {student.first_name} en {event.name} [{status}]")

# ============================================================================
# 7. CREAR PLANTILLAS DE CERTIFICADOS
# ============================================================================
print("\n[7] Creando plantillas de certificados...")

templates_data = [
    {
        'name': 'Certificado Azul Profesional',
        'category': 'Profesional',
        'background_url': 'https://example.com/templates/blue-professional.png',
        'preview_url': 'https://example.com/templates/preview/blue-professional.png',
        'layout_config': {
            'title_size': 48,
            'footer_color': '#003366',
            'signature_required': True,
        },
        'created_by': admin_user,
    },
    {
        'name': 'Certificado Verde Académico',
        'category': 'Académico',
        'background_url': 'https://example.com/templates/green-academic.png',
        'preview_url': 'https://example.com/templates/preview/green-academic.png',
        'layout_config': {
            'title_size': 44,
            'footer_color': '#006633',
            'signature_required': False,
        },
        'created_by': admin_user,
    },
]

templates = {}
for tmpl_data in templates_data:
    template, created = Template.objects.get_or_create(
        name=tmpl_data['name'],
        defaults=tmpl_data
    )
    if created:
        print(f"✓ Plantilla creada: {template.name}")
    else:
        print(f"✓ Plantilla ya existe: {template.name}")
    templates[tmpl_data['name']] = template

# ============================================================================
# 8. CREAR CERTIFICADOS
# ============================================================================
print("\n[8] Creando certificados...")

# Crear certificados para inscripciones con asistencia
from django.utils import timezone
import hashlib

certificates_to_create = [
    ('ana.lopez@test.com', 'Django Avanzado - Semestre 2026', 'Certificado Azul Profesional'),
    ('ana.lopez@test.com', 'Intro a Data Science con Python', 'Certificado Verde Académico'),
    ('roberto.sanchez@test.com', 'Django Avanzado - Semestre 2026', 'Certificado Azul Profesional'),
    ('maria.gonzalez@test.com', 'Diseño Web Moderno 2026', 'Certificado Azul Profesional'),
    ('fernando.diaz@test.com', 'Diseño Web Moderno 2026', 'Certificado Azul Profesional'),
    ('sofía.ruiz@test.com', 'Intro a Data Science con Python', 'Certificado Verde Académico'),
]

certificates = {}
for student_email, event_name, template_name in certificates_to_create:
    student = students[student_email]
    event = events[event_name]
    template = templates[template_name]
    
    # Generar código de verificación único
    verification_code = hashlib.md5(
        f"{student.id}{event.id}{timezone.now().isoformat()}".encode()
    ).hexdigest()[:20].upper()
    
    certificate, created = Certificate.objects.get_or_create(
        student=student,
        event=event,
        defaults={
            'template': template,
            'generated_by': admin_user,
            'verification_code': verification_code,
            'status': 'generated',
            'pdf_url': f'https://example.com/certificates/{student.id}/{event.id}.pdf',
            'expires_at': timezone.now() + timedelta(days=365),
        }
    )
    
    if created:
        print(f"✓ Certificado creado: {student.first_name} - {event.name}")
    else:
        print(f"✓ Certificado ya existe: {student.first_name} - {event.name}")
    
    key = f"{student_email}_{event_name}"
    certificates[key] = certificate

# ============================================================================
# 9. CREAR LOGS DE ENTREGA
# ============================================================================
print("\n[9] Creando logs de entrega...")

deliveries_to_create = [
    ('ana.lopez@test.com', 'Django Avanzado - Semestre 2026', 'email', 'ana.lopez@test.com', 'success'),
    ('ana.lopez@test.com', 'Intro a Data Science con Python', 'email', 'ana.lopez@test.com', 'success'),
    ('roberto.sanchez@test.com', 'Django Avanzado - Semestre 2026', 'whatsapp', '+34600200101', 'success'),
    ('maria.gonzalez@test.com', 'Diseño Web Moderno 2026', 'email', 'maria.gonzalez@test.com', 'pending'),
]

for student_email, event_name, method, recipient, status in deliveries_to_create:
    key = f"{student_email}_{event_name}"
    if key in certificates:
        certificate = certificates[key]
        delivery, created = DeliveryLog.objects.get_or_create(
            certificate=certificate,
            delivery_method=method,
            defaults={
                'sent_by': admin_user,
                'recipient': recipient,
                'status': status,
                'error_message': '' if status != 'error' else 'Email no válido',
            }
        )
        
        if created:
            status_display = "✓ Enviado" if status == 'success' else "⏳ Pendiente" if status == 'pending' else "✗ Error"
            print(f"✓ Entrega: {certificate.student.first_name} via {method} [{status_display}]")

# ============================================================================
# RESUMEN Y VALIDACIÓN
# ============================================================================
print("\n" + "=" * 80)
print("RESUMEN DE DATOS CREADOS")
print("=" * 80)

print(f"\n✓ Usuarios: {User.objects.count()}")
print(f"✓ Instructores: {Instructor.objects.count()}")
print(f"✓ Estudiantes: {Student.objects.count()}")
print(f"✓ Eventos: {Event.objects.count()}")
print(f"✓ Inscripciones: {Enrollment.objects.count()}")
print(f"✓ Plantillas: {Template.objects.count()}")
print(f"✓ Certificados: {Certificate.objects.count()}")
print(f"✓ Entregas: {DeliveryLog.objects.count()}")

print("\n" + "=" * 80)
print("CREDENCIALES DE ACCESO")
print("=" * 80)
print(f"Admin: admin@test.com / admin123")
print(f"Editor: editor@test.com / editor123")

print("\n" + "=" * 80)
print("✓ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
print("=" * 80)
