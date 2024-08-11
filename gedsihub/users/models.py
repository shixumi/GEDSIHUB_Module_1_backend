from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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

        # Create the specific user type based on role
        role = extra_fields.get('role')
        if role == 'Student':
            Student.objects.create(
                email=user.email,
                registration=user
            )
        elif role == 'Employee':
            Employee.objects.create(
                email=user.email,
                registration=user
            )

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

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student')
    college = models.CharField(max_length=100, blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    # Non specifics
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    lived_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=[('Female', 'Female'), ('Male', 'Male'), ('Intersex', 'Intersex'), ('Prefer not to say', 'Prefer not to say')], default='Prefer not to say')
    gender_identity = models.CharField(max_length=20, choices=GENDER_IDENTITY_CHOICES, default='Prefer not to say')
    preferred_pronoun = models.CharField(max_length=20, choices=PREFERRED_PRONOUN_CHOICES, default='Prefer not to say')
    indigenous_cultural_community = models.CharField(max_length=20, choices=INDIGENOUS_CHOICES, default='Prefer not to say')
    differently_abled = models.CharField(max_length=20, choices=DIFFERENTLY_ABLED_CHOICES, default='Prefer not to say')


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Student"

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee')
    branch_office_section_unit = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    # Non specifics
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    lived_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=[('Female', 'Female'), ('Male', 'Male'), ('Intersex', 'Intersex'), ('Prefer not to say', 'Prefer not to say')], default='Prefer not to say')
    gender_identity = models.CharField(max_length=20, choices=GENDER_IDENTITY_CHOICES, default='Prefer not to say')
    preferred_pronoun = models.CharField(max_length=20, choices=PREFERRED_PRONOUN_CHOICES, default='Prefer not to say')
    indigenous_cultural_community = models.CharField(max_length=20, choices=INDIGENOUS_CHOICES, default='Prefer not to say')
    differently_abled = models.CharField(max_length=20, choices=DIFFERENTLY_ABLED_CHOICES, default='Prefer not to say')


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Employee"
