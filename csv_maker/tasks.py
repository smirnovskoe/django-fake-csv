import csv
import uuid
from io import StringIO

from django.core.files.base import ContentFile
from faker import Faker

from core.celery import app
from . import models


@app.task
def build_csv(csv_columns_types: list,
              row_count: int,
              col_sep=",",
              str_chr='"'):
    """Build CSV file with fake data"""
    fake = Faker()

    faker_mapper = {
        'company': fake.company,
        'job': fake.job,
        'full_name': fake.name,
        'phone': fake.phone_number,
        'address': fake.address,
        'email': fake.email,
        'domain_name': fake.domain_name,
        'date': fake.date_of_birth,
    }
    csv_columns_types.sort(key=lambda tpl_: tpl_[2])

    headers = [elem[0] for elem in csv_columns_types]
    types = [elem[1] for elem in csv_columns_types]

    uuid_ = str(uuid.uuid4())
    f_name = f'csv_{uuid_}.csv'

    csv_file = open(f_name, mode='w', encoding='utf-8')

    csv_buffer = StringIO()
    writer = csv.writer(
         #csv_file,
         #delimiter=col_sep,

        csv_buffer,
    )

    writer.writerow(headers)

    for _ in range(row_count):
        new_row = list()
        for col_type, col_name in zip(types, headers):
            new_row.append(faker_mapper[col_type]())
        writer.writerow(new_row)

    django_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))

    ds = models.Dataset()

    ds.csv_file.save(
        f_name, django_file
    )

    return ds.csv_file.url


if __name__ == '__main__':
    data = [
        ('My Full Name', 'Full Name', 0),
        ('My Company', 'Company', 1),
        ('My Job', 'Job', 2)
    ]

    build_csv(data)
