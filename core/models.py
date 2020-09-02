from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    slug=models.SlugField(max_length=30,unique=True,null=True,error_messages={'unique':"This URL is already taken"},verbose_name='Your Custom URL',help_text="Choose a custom URL to make your page your own! Remember - once you choose a URL, you won’t be able to change it later.")
    reg=models.IntegerField(default=0)
    outvote_texts = models.IntegerField(default=0)

    zip_regex = RegexValidator(regex=r'^\d{5}$',
                                 message="ZIP Code must be 5 digits and entered in the format: '12345'.")
    zip_code = models.CharField(validators=[zip_regex], max_length=5,verbose_name='ZIP Code')

    phone_regex = RegexValidator(regex=r'^\d{10}$',
                                 message="Phone number must be 10 digits and entered in the format: '1234567890'.")
    phone = models.CharField(validators=[phone_regex], max_length=10,help_text="Use the same phone number that you used to register your Outvote account, if you have one")
    can_text = models.BooleanField(verbose_name='By signing up, you consent to receive periodic text messages from When We All Vote (56005). Message and data rates may apply. Text HELP for more information. Text STOP to stop receiving messages.',default=False)
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

    first_name=models.CharField(max_length=100,verbose_name='First Name',blank=True)
    last_name=models.CharField(max_length=100,verbose_name='Last Name',blank=True)
    city=models.CharField(max_length=100,blank=True)
    state=models.CharField(max_length=2,blank=True)

    def __str__(self):
        return self.first_name

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Volunteer.objects.create(user=instance)
    instance.volunteer.save()

