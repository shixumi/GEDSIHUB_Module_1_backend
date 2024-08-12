from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

COLLEGE_CHOICES = [
        ('CAF', 'College of Accountancy and Finance'),
        ('CADBE', 'College of Architecture, Design, and the Built Environment'),
        ('CAL', 'College of Acts and Letters'),
        ('CBA', 'College of Business Administration'),
        ('COC', 'College of Communication'),
        ('CCIS', 'College of Computer and Information Sciences'),
        ('COED', 'College of Education'),
        ('CE', 'College of Engineering'),
        ('CHK', 'College of Human Kinetics'),
        ('CL', 'College of Law'),
        ('CPSPA', 'College of Political Science and Public Administration'),
        ('CSSD', 'College of Social Sciences and Development'),
        ('CS', 'College of Science'),
        ('CTHTM', 'College of Tourism, Hospitality and Transportation Management'),
    ]

SECTOR_CHOICES = [
    ('Office of the Executive Vice President', 'Office of the Executive Vice President'),
    ('Office of the Vice President for Academic Affairs', 'Office of the Vice President for Academic Affairs'),
    ('Office of the Vice President for Planning and Finance', 'Office of the Vice President for Planning and Finance'),
    ('Office of the Vice President for Student Affairs and Services', 'Office of the Vicec President for Student Affairs and Services'),
    ('Office of the Vice President for Administration', 'Office of the Vice President for Administration'),
    ('Office of the Vice President for Campuses', 'Office of the Vice President for Campuses'),
    ('Office of the Vice President for Research, Extension, and Development', 'Office of the Vice President for Research, Extension, and Development'),
    ('Office of the President', 'Office of the President'),
]

SEX_CHOICES = [
    ('Male', 'Male'), 
    ('Intersex', 'Intersex'), 
    ('Prefer not to say', 'Prefer not to say'),
]

GENDER_IDENTITY_CHOICES = [
        ('Cisgender', 'Cisgender'),
        ('Transgender', 'Transgender'),
        ('Agender', 'Agender'),
        ('Gender Fluid', 'Gender Fluid'),
        ('Gender Queer', 'Gender Queer'),
    ]

PREFERRED_PRONOUN_CHOICES = [
        ('She/Her', 'She/Her'),
        ('He/Him', 'He/Him'),
        ('They/Them', 'They/Them'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

INDIGENOUS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

DIFFERENTLY_ABLED_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Prefer not to say', 'Prefer not to say'),
    ]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The E-mail field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=30, choices=[('Student', 'Student'), ('Employee', 'Employee')], default='Student')
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student')
    college = models.CharField(max_length=100, blank=True, null=True, choices=COLLEGE_CHOICES)
    program = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)

    # Non specifics
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    lived_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default='Prefer not to say')
    gender_identity = models.CharField(max_length=20, choices=GENDER_IDENTITY_CHOICES, default='Cisgender')
    preferred_pronoun = models.CharField(max_length=20, choices=PREFERRED_PRONOUN_CHOICES, default='Prefer not to say')
    indigenous_cultural_community = models.CharField(max_length=20, choices=INDIGENOUS_CHOICES, default='Prefer not to say')
    differently_abled = models.CharField(max_length=20, choices=DIFFERENTLY_ABLED_CHOICES, default='Prefer not to say')

    def clean(self):
        super().clean()
        # Custom validations
        if self.year and not self.year.isdigit():
            raise ValidationError({'year': 'Year must be a number'})
        if self.birthday and self.birthday > timezone.now().date():
            raise ValidationError({'birthday': 'Birthday cannot be a future date'})

    def __str__(self):
        if self.user and hasattr(self, 'first_name') and hasattr(self, 'last_name'):
            return f"{self.first_name} {self.last_name} - Student"
        return f"Student {self.id}"  # Default identifier if no personal details

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee')
    branch_office_section_unit = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES, default='Prefer not to say')

    # Non specifics
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    lived_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default='Prefer not to say')
    gender_identity = models.CharField(max_length=20, choices=GENDER_IDENTITY_CHOICES, default='Prefer not to say')
    preferred_pronoun = models.CharField(max_length=20, choices=PREFERRED_PRONOUN_CHOICES, default='Prefer not to say')
    indigenous_cultural_community = models.CharField(max_length=20, choices=INDIGENOUS_CHOICES, default='Prefer not to say')
    differently_abled = models.CharField(max_length=20, choices=DIFFERENTLY_ABLED_CHOICES, default='Prefer not to say')

    def clean(self):
        super().clean()
        # Custom validations
        if self.birthday and self.birthday > timezone.now().date():
            raise ValidationError({'birthday': 'Birthday cannot be a future date'})

    def __str__(self):
        if self.user and hasattr(self, 'first_name') and hasattr(self, 'last_name'):
            return f"{self.first_name} {self.last_name} - Employee"
        return f"Employee {self.id}"  # Default identifier if no personal details
