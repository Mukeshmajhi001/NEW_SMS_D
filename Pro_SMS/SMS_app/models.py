from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('BBS', 'BBS'),
        ('CSIT', 'CSIT'),
        ('BBA', 'BBA'),
        ('BCA', 'BCA'),
        ('BA', 'BA'),
        ('EED', 'EED'),
        ('BIM', 'BIM'),
        ('BBM', 'BBM'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, unique=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    grand_father_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='students/')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teachers/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.name

class Parent(models.Model):
    # Parent ka model agar alag se chahiye to
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class HomeImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='home/')
    caption = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title or f"Image {self.id}"