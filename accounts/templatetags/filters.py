from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter
def add_password_class(field):
    return field.as_widget(attrs={"class": "form-control form-password"})
