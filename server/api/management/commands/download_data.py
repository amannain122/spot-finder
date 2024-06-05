import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings
import csv

class Command(BaseCommand):
    help = 'Downloads data from Redshift and saves it to a CSV file'

    def handle(self, *args, **kwargs):
        try:
            # Establish connection
            conn = psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT']
            )

            # Create a cursor
            cur = conn.cursor()

            # Execute a query to select data
            cur.execute("SELECT * FROM api_post;")

            # Fetch all rows
            rows = cur.fetchall()

            # Specify the path to save the CSV file
            csv_file_path = 'data.csv'

            # Write data to a CSV file
            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write the header row
                csv_writer.writerow([desc[0] for desc in cur.description])
                # Write data rows
                csv_writer.writerows(rows)

            self.stdout.write(self.style.SUCCESS(f"Data downloaded and saved to '{csv_file_path}'"))

            # Close cursor and connection
            cur.close()
            conn.close()

        except psycopg2.OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Operational error: {e}"))
        except psycopg2.DatabaseError as e:
            self.stdout.write(self.style.ERROR(f"Database error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
