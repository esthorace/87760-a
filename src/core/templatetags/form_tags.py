from django import template
from django.forms import CheckboxInput, CheckboxSelectMultiple, Select, Textarea
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="bs_field")
def bs_field(field):
    if field.is_hidden:
        return field.as_widget()

    widget = field.field.widget
    attrs = {}

    if isinstance(widget, CheckboxSelectMultiple):
        control_class = "form-check-input"
    elif isinstance(widget, Select):
        control_class = "form-select"
    elif isinstance(widget, CheckboxInput):
        control_class = "form-check-input"
    else:
        control_class = "form-control"
        attrs["placeholder"] = " "
        if isinstance(widget, Textarea):
            attrs["rows"] = "4"

    if field.errors:
        control_class += " is-invalid"
    attrs["class"] = control_class

    control = field.as_widget(attrs=attrs)

    error_html = mark_safe("")
    if field.errors:
        error_html = format_html(
            '<div class="invalid-feedback d-block">{}</div>',
            " ".join(str(error) for error in field.errors),
        )

    help_html = mark_safe("")
    if field.help_text:
        help_html = format_html(
            '<div class="form-text text-muted">{}</div>', field.help_text
        )

    label = format_html(
        '<label for="{}">{}</label>', field.id_for_label, field.label or ""
    )

    if control_class.startswith("form-check-input"):
        return format_html(
            '<div class="form-check mb-3">{}<label class="form-check-label" '
            'for="{}">{}</label>{}{}</div>',
            control,
            field.id_for_label,
            field.label or "",
            error_html,
            help_html,
        )

    return format_html(
        '<div class="form-floating mb-3">{}{}{}{}</div>',
        control,
        label,
        error_html,
        help_html,
    )
