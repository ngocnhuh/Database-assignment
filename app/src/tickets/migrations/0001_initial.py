# Generated by Django 4.0.4 on 2022-06-04 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethods',
            fields=[
                ('method_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'payment_methods',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_location', models.CharField(max_length=50)),
                ('paid', models.BooleanField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'ticket',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LuggageTicket',
            fields=[
                ('lt_id', models.OneToOneField(db_column='ticket_id', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tickets.ticket')),
                ('weight', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'luggage_ticket',
                'managed': False,
            },
            bases=('tickets.ticket',),
        ),
        migrations.CreateModel(
            name='PassengerTicket',
            fields=[
                ('pt_id', models.OneToOneField(db_column='ticket_id', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tickets.ticket')),
                ('seat_num', models.IntegerField()),
            ],
            options={
                'db_table': 'passenger_ticket',
                'managed': False,
            },
            bases=('tickets.ticket',),
        ),
    ]
