from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

    
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_validated = True
        user.save(using=self._db)
        return user


    def __str__(self):
        return self.username

class Profile(AbstractBaseUser):
    username = models.CharField(max_length=200, null=False, blank=False,unique=True)
    email = models.EmailField(max_length=100,unique=True)

    #phone = models.CharField(max_length=10)
    phone = PhoneNumberField(null=True, blank=True)

    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    registered_address = models.CharField(max_length=200, null=True, blank=True)
    area_of_operation = models.CharField(max_length=200, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    tan_no = models.CharField(max_length=10, null=True, blank=True)
    officer_authorized = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    service_tax_no = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=40, null=True, blank=True)
    district = models.CharField(max_length=40, null=True, blank=True)
    startup_type = models.CharField(max_length=20, null=True, blank=True)

    is_validated = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)

    '''VALID_STATUS = (
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )
    display_validated = models.CharField(max_length=20, choices=VALID_STATUS, default='Pending')'''
    startup_idea = models.CharField(max_length=1000)
    startup_name = models.CharField(max_length=100)
    is_registered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    
    #=====> very important fields attribute to set <=====
    USERNAME_FIELD = 'username' 

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return "{}:{}:{}".format(self.id, self.email, self.username)

    def __str__(self):
        return f'{self.username}'
    
    @property
    def next_payment_date(self):
        if not self.is_paid:
            return self.date_joined
        return self.date_joined + timezone.timedelta(days=91)

    @property
    def payment_status(self):
        if self.is_paid:
            return "Paid"
        return "Dues"

    def make_payment(self):
        self.is_paid = False
        self.save()




class Grievance(models.Model):
    username = models.CharField(max_length=100, verbose_name="Your name")
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    complain_type = models.CharField(max_length=100)
    complain_startup = models.CharField(max_length=100)
    complainXfeedback = models.CharField(max_length=100)
    complain_date= models.DateTimeField(verbose_name='date of complain', auto_now_add=True)

    USERNAME_FIELD = 'id'
    def __str__(self):
        return self.username

    
class Request(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    
    username = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requests')
    #request_number = models.PositiveIntegerField()
    request_number = models.PositiveIntegerField(default=0)
    request_text = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feedback = models.TextField(max_length=500, null=True, blank=True)

    USERNAME_FIELD = 'username' 
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            # Generate a unique request number when it is not set
            last_request = Request.objects.order_by('-request_number').first()
            self.request_number = last_request.request_number + 1 if last_request else 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return "Request {}: {}".format(self.request_number, self.status)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    username = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    comments = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title