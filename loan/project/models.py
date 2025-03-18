from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    student_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='project_user_set',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='project_user_set',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
    
class Rattansi(models.Model):
    # status choices
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # sponsorship status choices
    SPONSORSHIP_CHOICES = (
        ('government', 'Government Sponsored (KUCCPS)'),
        ('self', 'Self Sponsored (PSSP)'),
    )

    # Accomodation status choices
    ACCOMODATION_CHOICES = (
        ('resident', 'Resident'),
        ('non-resident', 'Non-resident'),
    )
    
    # Parental status choices
    PARENTAL_STATUS_CHOICES = (
        ('both_parents', 'Have both parents'),
        ('one_parent', 'Have one parent'),
        ('orphan', 'Total orphan'),
    )

    # Deferment reason choices - fixed the format
    DEFERMENT_CHOICES = (
        ('medical', 'Medical'),
        ('social', 'Social'),
        ('financial', 'Financial'),
        ('academic', 'Academic'),
    )
    
    # Personal details
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rattansi_application')
    school = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    homeAdress = models.CharField(max_length=200)
    telNo = models.CharField(max_length=10)  # Changed to CharField for phone numbers
    homeCounty = models.CharField(max_length=20)
    subCounty = models.CharField(max_length=20)
    
    # next of kin details
    next_of_kin_name = models.CharField(max_length=200)
    next_of_kin_address = models.CharField(max_length=200)
    next_of_kin_no = models.CharField(max_length=10)  # Changed to CharField for phone numbers
    
    # chief details
    name_of_chief = models.CharField(max_length=100)
    name_of_chief_adress = models.CharField(max_length=200)
    name_of_chief_no = models.CharField(max_length=10)  # Changed to CharField for phone numbers
    
    # disability info
    has_disability = models.BooleanField(default=False)
    disability_details = models.CharField(max_length=200, blank=True, null=True)
    
    # student status
    sponsorship_status = models.CharField(max_length=20, choices=SPONSORSHIP_CHOICES)
    accomodation_status = models.CharField(max_length=20, choices=ACCOMODATION_CHOICES)
    
    # family background
    parental_status = models.CharField(max_length=20, choices=PARENTAL_STATUS_CHOICES)
    
    # father's details(if applicable)
    father_age = models.IntegerField(blank=True, null=True)
    fathers_occupation = models.CharField(max_length=100, blank=True, null=True)
    fathers_current_employee = models.CharField(max_length=100, blank=True, null=True)
    fathers_health_status = models.TextField(blank=True, null=True)
    
    # mothers information
    mother_age = models.IntegerField(blank=True, null=True)
    mothers_occupation = models.CharField(max_length=100, blank=True, null=True)
    mothers_current_employee = models.CharField(max_length=100, blank=True, null=True)
    mothers_health_status = models.TextField(blank=True, null=True)
    
    # siblings information
    total_sibling = models.IntegerField()
    university_siblings = models.IntegerField()
    secondary_siblings = models.IntegerField()
    out_of_school_siblings = models.IntegerField()
    out_of_school_reason = models.TextField(blank=True, null=True)
    working_siblings = models.TextField(blank=True, null=True)
    
    # other information
    secondary_fee_payer = models.CharField(max_length=100)
    on_work_study = models.BooleanField(default=False)
    external_support = models.BooleanField(default=False)
    external_support_details = models.TextField(blank=True, null=True)
    fee_balance = models.DecimalField(max_digits=10, decimal_places=2)
    ever_deferred = models.BooleanField(default=False)
    deferment_reason = models.CharField(max_length=50, blank=True, null=True, choices=DEFERMENT_CHOICES)
    additional_info = models.TextField(blank=True, null=True)
    
    # Comments and status
    school_dean_comments = models.TextField(blank=True, null=True)
    student_dean_comments = models.TextField(blank=True, null=True)
    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount_awarded = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # document
    fee_statement = models.FileField(upload_to='fee_statements/', blank=True, null=True)
    death_certificate = models.FileField(upload_to='death_certificates/', blank=True, null=True)
    health_documents = models.FileField(upload_to='health_documents/', blank=True, null=True)
    other_documents = models.FileField(upload_to='other_documents/', blank=True, null=True)
    
    # timestamps
    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - Rattansi Bursary Application"
