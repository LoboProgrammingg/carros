from django.db import migrations, models
from django.conf import settings

def populate_user_ids(apps, schema_editor):
    Car = apps.get_model('cars', 'Car')
    User = apps.get_model(settings.AUTH_USER_MODEL)

    # Obtenha todos os carros onde user_id é nulo
    cars_without_user = Car.objects.filter(user_id=None)

    # Atribua user_id para esses carros
    for car in cars_without_user:
        # Exemplo: Atribuir ao primeiro usuário encontrado, ajuste conforme necessário
        user = User.objects.first()  # Ajuste conforme necessário para selecionar o usuário correto
        car.user = user
        car.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0012_delete_carphoto'),  # Dependência da sua migração anterior
    ]

    operations = [
        migrations.RunPython(populate_user_ids, reverse_code=migrations.RunPython.noop),

        # Sua migração original que altera o campo user_id
        migrations.AlterField(
            model_name='car',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
