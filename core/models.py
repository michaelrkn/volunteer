from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    slug=models.SlugField(max_length=30,unique=True,null=True,error_messages={'unique':"This URL is already taken"},verbose_name='Your Custom URL Suffix',help_text="Once you choose a URL, you may not change it later")
    title=models.CharField(max_length=140,verbose_name='Page Title')
    prompt=models.TextField(max_length=2000,verbose_name='Voting Prompt')
    reg=models.IntegerField(default=0)
    outvote_texts = models.IntegerField(default=0)
    phone_regex = RegexValidator(regex=r'^\d{10}$',
                                 message="Phone number must be entered in the format: '1234567890'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10,blank=True,null=True,help_text="Use the same phone number that you used to register your Outvote account")

    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30)
    # birth_date = models.DateField(null=True, blank=True)

    # raceType = models.CharField(max_length=10, choices=[
    #     ('president', 'Presidential'),
    #     ('house', 'House'),
    #     ('senate', 'Senate'),
    #     ('governor', 'Gubernatorial'),
    # ])

    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)
    # email = models.EmailField(max_length=150)
    # bio = models.TextField()
    # link = models.CharField(max_length=100)
    # tickets = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])

    def __str__(self):
        return self.user.username

class Friend(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='friends')

    first_name=models.CharField(max_length=100,verbose_name='First Name')
    last_name=models.CharField(max_length=100,verbose_name='Last Name')
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=2)
    email = models.EmailField(max_length=100)
    # phone = models.CharField(max_length=20)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+1234567890'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17)

    def __str__(self):
        return self.first_name

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Volunteer.objects.create(user=instance)
    instance.volunteer.save()

