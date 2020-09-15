from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Referrer(models.Model):

    name=models.CharField(max_length=100)
    paragraph=models.TextField()
    slug=models.SlugField(max_length=30,unique=True)
    image=models.ImageField(upload_to='referrer/',blank=True)

    def __str__(self):
        return self.name

class Volunteer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    referrer = models.ForeignKey(Referrer, on_delete=models.CASCADE, null=True,blank=True)

    slug=models.SlugField(max_length=30,unique=True,null=True,error_messages={'unique':"This URL is already taken"},verbose_name='Your Custom URL',help_text="Choose a custom URL (Example: janedoe89) to make your page your own! Remember - once you choose a URL, you won’t be able to change it later. Make it fun: use your Instagram, Twitter, MySpace, or even AOL username!")
    reg=models.IntegerField(default=0)
    reg_started = models.IntegerField(default=0)
    outvote_texts = models.IntegerField(default=0)
    tracking=models.CharField(blank=True,max_length=30)

    # zip_regex = RegexValidator(regex=r'^\d{5}$',
    #                              message="ZIP Code must be 5 digits and entered in the format: '12345'.")
    # zip_code = models.CharField(validators=[zip_regex], max_length=5,verbose_name='ZIP Code')
    #
    # phone_regex = RegexValidator(regex=r'^\d{10}$',
    #                              message="Phone number must be 10 digits and entered in the format: '1234567890'.")
    # phone = models.CharField(validators=[phone_regex], max_length=10,help_text="Use the same phone number that you used to register your Outvote account, if you have one")
    # can_text = models.BooleanField(verbose_name='By signing up, you consent to receive periodic text messages from When We All Vote (56005). Message and data rates may apply. Text HELP for more information. Text STOP to stop receiving messages.',default=False)
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
        return self.user.email

class Friend(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='friends')

    first_name=models.CharField(max_length=100,verbose_name='First Name',blank=True)
    last_name=models.CharField(max_length=100,verbose_name='Last Name',blank=True)
    city=models.CharField(max_length=100,blank=True)
    state=models.CharField(max_length=2,blank=True)

    def __str__(self):
        return self.first_name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Volunteer.objects.create(user=instance)
    instance.volunteer.save()



from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, password,first_name,last_name,zip_code,phone,can_text):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            zip_code=zip_code,
            phone=phone,
            can_text=can_text
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,first_name,last_name,zip_code,phone,can_text):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            zip_code=zip_code,
            phone=phone,
            can_text=can_text
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    zip_regex = RegexValidator(regex=r'^\d{5}$',
                               message="ZIP Code must be 5 digits and entered in the format: '12345'.")
    zip_code = models.CharField(validators=[zip_regex], max_length=5, verbose_name='ZIP Code')

    phone_regex = RegexValidator(regex=r'^\d{10}$',
                                 message="Phone number must be 10 digits and entered in the format: '1234567890'.")
    phone = models.CharField(validators=[phone_regex], max_length=10,
                             help_text="Use the same phone number that you used to register your Outvote account, if you have one")
    can_text = models.BooleanField(
        verbose_name='By signing up, you consent to receive periodic text messages from When We All Vote (56005). Message and data rates may apply. Text HELP for more information. Text STOP to stop receiving messages.',
        default=False)



    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','zip_code','phone','can_text']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin