# ORM de Django

> Los QuerySets son **perezosos**: no se ejecuta ninguna consulta hasta que se itera, se convierte en lista, se hace slicing con paso, o se llama a `get()`, `count()`, `exists()`, `first()`, etc.

## Crear registros

```py
from app.models import Modelo

# En dos pasos
instancia = Modelo(campo1="valor", campo2="valor")
instancia.save()

# En un solo paso
Modelo.objects.create(campo1="valor", campo2="valor")

# Obtener o crear (devuelve una tupla: (objeto, creado))
obj, creado = Modelo.objects.get_or_create(
    campo1="valor",
    defaults={"campo2": "otro"},  # solo se usa si hay que crear
)

# Crear masivamente (una sola consulta; no llama a save() ni a señales)
Modelo.objects.bulk_create([
    Modelo(campo1="a"),
    Modelo(campo1="b"),
])
```

## Obtener registros

```py
Modelo.objects.all()                 # Todos los registros
Modelo.objects.get(id=valor)         # Uno solo; lanza Modelo.DoesNotExist o Modelo.MultipleObjectsReturned
Modelo.objects.filter(campo="valor") # Varios (QuerySet, puede estar vacío)
Modelo.objects.exclude(campo="valor")# Todo lo que NO cumple la condición

Modelo.objects.filter(campo="valor").first()   # Primer registro o None
Modelo.objects.filter(campo="valor").last()    # Último registro o None
Modelo.objects.filter(campo="valor").exists()  # True / False (más eficiente que len() o count() para condicionales)
Modelo.objects.filter(campo="valor").count()   # Cantidad de registros
```

> `first()` y `last()` ordenan por clave primaria si el QuerySet no tiene orden definido.

## Actualizar registros

```py
# Un registro
instancia = Modelo.objects.get(id=valor)
instancia.campo = "nuevo_valor"
instancia.save()
instancia.save(update_fields=["campo"])  # Solo actualiza ese campo

# Masivo (una sola consulta; NO llama a save() ni a señales)
Modelo.objects.filter(estado="pendiente").update(estado="completado")

# Actualizar usando el valor actual del campo (evita condiciones de carrera)
from django.db.models import F
Modelo.objects.filter(id=valor).update(contador=F("contador") + 1)

# Actualizar o crear
obj, creado = Modelo.objects.update_or_create(
    campo1="valor",
    defaults={"campo2": "nuevo"},
)

# Actualizar masivamente instancias ya modificadas en memoria
Modelo.objects.bulk_update(lista_de_instancias, ["campo"])
```

## Eliminar registros

```py
# Un registro
instancia = Modelo.objects.get(id=valor)
instancia.delete()

# Masivo (no llama al método delete() del modelo, pero sí respeta cascadas y señales)
Modelo.objects.filter(activo=False).delete()  # Devuelve (total, {"app.Modelo": n})
```

## Filtrar consultas

### Cadenas

```py
Modelo.objects.filter(campo="valor")
Modelo.objects.filter(campo__iexact="valor")        # Igual, sin distinguir mayúsculas
Modelo.objects.filter(campo__contains="subcadena")
Modelo.objects.filter(campo__icontains="subcadena") # Sin distinguir mayúsculas
Modelo.objects.filter(campo__startswith="inicio")
Modelo.objects.filter(campo__endswith="final")
```

### Comparaciones y nulos

```py
Modelo.objects.filter(id__in=[1, 2, 3])
Modelo.objects.filter(id__gt=3)          # Mayor que
Modelo.objects.filter(id__gte=3)         # Mayor o igual que
Modelo.objects.filter(id__lt=2)          # Menor que
Modelo.objects.filter(id__lte=2)         # Menor o igual que
Modelo.objects.filter(id__range=(1, 10)) # Entre 1 y 10 (ambos incluidos)
Modelo.objects.filter(campo__isnull=True)
```

### Fechas

```py
from datetime import date

Modelo.objects.filter(fecha__year=2024)
Modelo.objects.filter(fecha__month=8)
Modelo.objects.filter(fecha__day=1)
Modelo.objects.filter(fecha__gt=date(2022, 1, 1))
Modelo.objects.filter(fecha__range=(date(2024, 1, 1), date(2024, 12, 31)))
Modelo.objects.filter(fecha_hora__date=date(2024, 8, 1))  # Para DateTimeField
```

### Relaciones

```py
# Hacia adelante (ForeignKey)
Modelo.objects.filter(campo_relacionado__campo="valor")

# Inversa (por defecto: nombremodelo_set, o el related_name definido)
autor.libro_set.all()
Autor.objects.filter(libro__titulo__icontains="django")

# ManyToMany
obj.tags.add(tag1, tag2)
obj.tags.remove(tag1)
obj.tags.set([tag1, tag2])  # Reemplaza todo
obj.tags.clear()
```

### Operaciones lógicas (Q objects)

```py
from django.db.models import Q

Modelo.objects.filter(Q(expresión) | Q(expresión))  # OR
Modelo.objects.filter(Q(expresión) & Q(expresión))  # AND (equivale a filter(a, b))
Modelo.objects.filter(~Q(expresión))                # NOT
Modelo.objects.filter(Q(expresión) | Q(expresión)).distinct()  # Evita duplicados (útil con joins)
```

## Optimización

### Prevención del problema N+1

```py
# ForeignKey / OneToOneField (usa JOIN)
Modelo.objects.select_related("campo_relacionado")

# ManyToManyField o relaciones inversas (usa una consulta adicional)
Modelo.objects.prefetch_related("campo_muchos_a_muchos")
```

### Cargar solo lo necesario

```py
# QuerySet de diccionarios
Modelo.objects.values("id", "nombre")

# QuerySet de tuplas
Modelo.objects.values_list("id", "nombre")

# QuerySet de valores sueltos (sin tupla)
Modelo.objects.values_list("id", flat=True)

# Instancias del modelo, pero cargando solo ciertos campos
Modelo.objects.only("id", "nombre")
Modelo.objects.defer("descripcion_larga")
```

## Agregación y anotación

```py
from django.db.models import Count, Avg, Max, Min, Sum

# Un único resultado sobre todo el QuerySet -> devuelve un dict
Modelo.objects.aggregate(total=Count("id"), promedio=Avg("precio"))
# {'total': 10, 'promedio': 25.5}

# Un valor calculado por cada registro (GROUP BY)
Autor.objects.annotate(num_libros=Count("libro"))
Autor.objects.annotate(num_libros=Count("libro")).filter(num_libros__gt=2)
```

## Ordenar y limitar

```py
Modelo.objects.order_by("campo")         # Ascendente
Modelo.objects.order_by("-campo")        # Descendente
Modelo.objects.order_by("campo1", "-campo2")  # Múltiples criterios

Modelo.objects.all()[:10]    # Primeros 10 registros
Modelo.objects.all()[5:15]   # Índices 5 a 14 (base 0), es decir, 10 registros
```

> No se puede aplicar `filter()` ni `order_by()` después de hacer slicing.

## Transacciones

```py
from django.db import transaction

with transaction.atomic():
    a.save()
    b.save()  # Si algo falla, se revierte todo
```
