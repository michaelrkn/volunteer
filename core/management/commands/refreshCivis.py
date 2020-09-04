from core.models import Volunteer
import civis

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refreshes civis data'

    def handle(self, *args, **options):
        table = civis.io.read_civis_sql(
            "select tracking_id, sum(case when status in ('Step 1','Step 2','Step 3','Step 4') then 1 else 0 end), sum(case when status='Complete' then 1 else 0 end) from wwav_rtv.rtv_cleaned where tracking_id like '%Mob_2020_VR_MO-Contest_%' group by 1",
            "TMC")
        self.stdout.write(self.style.SUCCESS('Made RTV query'))
        for row in table[1:]:
            try:
                #print(row[0][row[0].startswith('msv-custom-') and len('msv-custom-'):])
                v = Volunteer.objects.get(slug=row[0].split('Mob_2020_VR_MO-Contest_',1)[-1])
                v.reg = row[2]
                v.reg_started=row[1]
                # print(v)
                # print(v.reg)
                v.save()
            except Volunteer.DoesNotExist:
                pass
        self.stdout.write(self.style.SUCCESS('Updated RTV counts'))
        # outvote = civis.io.read_civis_sql(
        #     "select distinct phone, actions_performed from wwav_outvote.users where phone is not null",
        #     "TMC")
        # self.stdout.write(self.style.SUCCESS('Made Outvote query'))
        # for row in outvote[1:]:
        #
        #     # v = Volunteer.objects.get(phone=row[0])
        #     vols = Volunteer.objects.filter(phone=row[0][-10:])
        #     if vols.exists():
        #         for v in vols.iterator():
        #             v.outvote_texts = row[1]
        #             # print(v)
        #             # print(v.reg)
        #             v.save()
        #
        # self.stdout.write(self.style.SUCCESS('Updated Outvote counts'))
