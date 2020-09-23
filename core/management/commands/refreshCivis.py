from core.models import Volunteer, User
import civis

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refreshes civis data'

    def handle(self, *args, **options):
        table = civis.io.read_civis_sql(
            "select tracking_id, sum(case when status in ('Step 1','Step 2','Step 3','Step 4') then 1 else 0 end), sum(case when status='Complete' then 1 else 0 end) from wwav_rtv.rtv_cleaned where tracking_id like '%Mob_2020_VR_MO-Contest_%' or tracking_id like 'vcc_%' group by 1",
            "TMC")
        self.stdout.write(self.style.SUCCESS('Made RTV query'))
        for row in table[1:]:
            try:
                #print(row[0][row[0].startswith('msv-custom-') and len('msv-custom-'):])
                v = Volunteer.objects.get(slug=row[0].split('vcc_',1)[-1].split('Mob_2020_VR_MO-Contest_',1)[-1])
                v.reg = row[2]
                v.reg_started=row[1]
                # print(v)
                # print(v.reg)
                v.save()
            except Volunteer.DoesNotExist:
                pass
        self.stdout.write(self.style.SUCCESS('Updated RTV counts'))
        outvote = civis.io.read_civis_sql(
            "select right(phone,10) as phone, count(m.id) as num from wwav_outvote.messages m left join wwav_outvote.users u on sender_id=u.id where phone is not null group by 1 having num>0",
            "TMC",use_pandas=True)
        self.stdout.write(self.style.SUCCESS('Made Outvote query'))
        outvote=outvote.astype({'phone': 'string'})

        for u in User.objects.all():

            matches=outvote.loc[lambda outvote: outvote['phone'] == u.phone]

            if not matches.empty:
                u.volunteer.outvote_texts = matches['num'].max()
                u.volunteer.save()

        # for row in outvote[1:]:
        #
        #     # v = Volunteer.objects.get(phone=row[0])
        #     users = User.objects.filter(phone=row[0][-10:])
        #     if users.exists():
        #         for u in users.iterator():
        #             u.outvote_texts = row[1]
        #             # print(v)
        #             # print(v.reg)
        #             u.save()

        self.stdout.write(self.style.SUCCESS('Updated Outvote counts'))

        actblue = civis.io.read_civis_sql(
            "SELECT email, sum(amount) as num FROM tmc_ab.wwav_donations group by 1",
            "TMC", use_pandas=True)
        self.stdout.write(self.style.SUCCESS('Made ActBlue query'))
        # actblue = actblue.astype({'phone': 'string'})

        for v in Volunteer.objects.filter(actblue_email__isnull=False):

            matches = actblue.loc[lambda actblue: actblue['email'] == v.actblue_email]

            if not matches.empty:
                v.actblue_donations = matches['num'].max()
                v.save()



        self.stdout.write(self.style.SUCCESS('Updated ActBlue counts'))


        analytics = civis.io.read_civis_sql(
            "SELECT source, sum(users) as num FROM wwav_vcc.analytics where campaign='vcc_vbm' group by 1",
            "TMC", use_pandas=True)
        self.stdout.write(self.style.SUCCESS('Made Google Analytics query'))
        # actblue = actblue.astype({'phone': 'string'})

        for v in Volunteer.objects.all():

            matches = analytics.loc[lambda analytics: analytics['source'] == v.slug]

            if not matches.empty:
                v.vbm_users = matches['num'].max()
                v.save()



        self.stdout.write(self.style.SUCCESS('Updated Google Analytics counts'))
