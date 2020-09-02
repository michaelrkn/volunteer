from core.models import Volunteer
import civis

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refreshes civis data'

    def handle(self, *args, **options):
        table = civis.io.read_civis_sql(
            "select tracking_id, count(*) from wwav_rtv.rtv_cleaned where lower(tracking_id) like 'msv-custom-%' and status not in ('Rejected','Under 18') group by 1",
            "TMC")
        for row in table[1:]:
            try:
                #print(row[0][row[0].startswith('msv-custom-') and len('msv-custom-'):])
                v = Volunteer.objects.get(slug=row[0][row[0].startswith('msv-custom-') and len('msv-custom-'):])
                v.reg = row[1]
                # print(v)
                # print(v.reg)
                v.save()
            except Volunteer.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('Ran'))
