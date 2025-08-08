from faker import Faker
import csv
import os

fake = Faker()

def gen(n=100, path='data/demo_contacts.csv'):
    fields = [
        'name', 'email', 'phone', 'job_title', 'company', 'city',
        'note', 'department', 'website'
    ]

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for _ in range(n):
            writer.writerow({
                'name': fake.name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'job_title': fake.job(),
                'company': fake.company(),
                'city': fake.city(),
                'note': fake.sentence(nb_words=12),
                'department': fake.job().split()[-1] + " Dept.",
                'website': fake.url()
            })

    print(f"{n} demo CRM contacts written to: {path}")

if __name__ == '__main__':
    gen(500)