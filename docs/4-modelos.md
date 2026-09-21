# Campos y tipos de datos en Django

## Opciones comunes a todos los campos

| Opción                      | Descripción                                        |
|-----------------------------|----------------------------------------------------|
| `null=True`                 | Permite `NULL` en la base de datos                 |
| `blank=True`                | Permite vacío en validaciones y formularios        |
| `default=...`               | Valor por defecto (puede ser un callable)          |
| `unique=True`               | Valor único en la tabla                            |
| `db_index=True`             | Crea un índice                                     |
| `choices=...`               | Restringe a opciones definidas (ver `TextChoices`) |
| `help_text`, `verbose_name` | Textos para formularios y admin                    |

> **`null` vs `blank`**: en `CharField` y `TextField` se recomienda usar solo `blank=True` (la cadena vacía representa "sin valor"). Usar `null=True` genera dos valores posibles para "vacío".

> **Validación**: Django valida en formularios y en `full_clean()`, **no** al llamar a `save()`.

## Cadenas

- **`CharField`**: texto corto. Requiere `max_length` (tamaño de la columna `VARCHAR`).
  - PostgreSQL y MySQL en modo estricto imponen el límite. SQLite no.
  - En MySQL, el máximo real depende del charset y del tamaño total de la fila (65.535 bytes en InnoDB).
  - Desde Django 4.2, en PostgreSQL `max_length` es opcional.
- **`TextField`**: texto largo. En Django no tiene longitud máxima, así que el límite lo define la base de datos. Si se indica `max_length`, solo afecta al widget del formulario.

## Números

| Campo                       | Rango                                                  |
|-----------------------------|--------------------------------------------------------|
| `SmallIntegerField`         | -32.768 a 32.767                                       |
| `IntegerField`              | -2.147.483.648 a 2.147.483.647                         |
| `BigIntegerField`           | -9.223.372.036.854.775.808 a 9.223.372.036.854.775.807 |
| `PositiveSmallIntegerField` | 0 a 32.767                                             |
| `PositiveIntegerField`      | 0 a 2.147.483.647                                      |
| `PositiveBigIntegerField`   | 0 a 9.223.372.036.854.775.807                          |

> Los rangos son los garantizados por Django en todas las bases de datos soportadas. Las restricciones de los campos `Positive*` se aplican también a nivel de base de datos (`CHECK` o `UNSIGNED`).

- **`DecimalField`**: números decimales exactos. Requiere `max_digits` (total de dígitos, incluidos los decimales) y `decimal_places` (dígitos a la derecha del punto). Devuelve `decimal.Decimal`. Ideal para dinero.

```py
precio = models.DecimalField(max_digits=10, decimal_places=2)
```

- **`FloatField`**: coma flotante de doble precisión (aproximadamente ±1,8 × 10³⁰⁸, con ~15 dígitos significativos). No apto para cálculos financieros por sus imprecisiones.

## Fechas y horas

- **`DateField`**: fecha (`datetime.date`).
- **`DateTimeField`**: fecha y hora. Con `USE_TZ = True` trabaja con datetimes conscientes de zona horaria.
- **`TimeField`**: hora.
- **`DurationField`**: período de tiempo (`timedelta`).

`DateField` y `DateTimeField` aceptan:

- `auto_now_add=True`: se establece al crear el registro.
- `auto_now=True`: se actualiza en cada `save()`.

## Identificadores

- **`AutoField`**: entero autoincremental de 32 bits, usado como clave primaria.
- **`BigAutoField`**: igual, pero de 64 bits. Es el valor por defecto en proyectos nuevos desde Django 3.2 (`DEFAULT_AUTO_FIELD`).
- **`SmallAutoField`**: autoincremental de 16 bits.
- **`UUIDField`**: identificador universal único. No es secuencial ni adivinable, y es útil en sistemas distribuidos o para exponer IDs en URLs.

```py
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

## Relaciones entre modelos

- **`ForeignKey`**: relación uno a muchos. Requiere `on_delete`. Se puede definir `related_name` para la relación inversa.

```py
autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")
```

- **`OneToOneField`**: relación uno a uno. Requiere `on_delete` y se usa, por ejemplo, para extender el modelo de usuario con un perfil.
- **`ManyToManyField`**: relación muchos a muchos. Django crea la tabla intermedia automáticamente. Con `through=` se puede usar un modelo intermedio propio para guardar datos adicionales de la relación.

### `on_delete`

Define qué ocurre con los objetos que **referencian** al objeto eliminado:

- `CASCADE`: elimina también los objetos que lo referencian.
- `PROTECT`: impide la eliminación lanzando `ProtectedError`.
- `RESTRICT`: impide la eliminación lanzando `RestrictedError`, pero permite eliminar si el objeto también se borra por otra cascada (Django 3.1+).
- `SET_NULL`: establece la clave en `NULL` (requiere `null=True`).
- `SET_DEFAULT`: establece la clave en su valor por defecto (requiere `default`).
- `SET(valor_o_callable)`: establece la clave en el valor indicado.
- `DO_NOTHING`: no hace nada en Django. Si la base de datos impone restricciones de clave foránea, se produce un `IntegrityError`.

## Archivos

- **`FileField`**: guarda la ruta del archivo en la base de datos. El archivo se almacena en el *storage* configurado (por defecto, el sistema de archivos bajo `MEDIA_ROOT`, aunque puede ser S3 u otro). Se define el destino con `upload_to`.
- **`ImageField`**: subclase de `FileField` que valida que el archivo sea una imagen. Requiere **Pillow** y admite `height_field` y `width_field`.
- **`BinaryField`**: guarda datos binarios directamente en la base de datos. No es editable en formularios por defecto y puede afectar el rendimiento con archivos grandes.

## Otros tipos de campo

- **`BooleanField`**: `True` o `False`. Para permitir nulos, usar `null=True` (`NullBooleanField` fue eliminado en Django 4.0).
- **`EmailField`**: valida formato de correo (`max_length=254` por defecto).
- **`URLField`**: valida formato de URL (`max_length=200` por defecto).
- **`SlugField`**: cadenas amigables para URL (`max_length=50` y `db_index=True` por defecto).
- **`JSONField`**: almacena JSON. Soportado en todas las bases de datos oficiales desde Django 3.1.
- **`ArrayField`**: exclusivo de PostgreSQL (`django.contrib.postgres.fields`). Requiere `base_field`.

```py
tags = ArrayField(models.CharField(max_length=20), default=list)
```

- **`GenericIPAddressField`**: direcciones IPv4 o IPv6. Con `protocol="IPv4"` acepta solo IPv4. (`IPAddressField` fue eliminado en Django 1.9).

## Choices con enumeraciones

```py
class Estado(models.TextChoices):
    PENDIENTE = "P", "Pendiente"
    COMPLETADO = "C", "Completado"

estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.PENDIENTE)
```
