from django.db import models

from django.contrib.auth.models import AbstractUser

from ckeditor_uploader.fields import RichTextUploadingField
import datetime


# Create your models here.

STATUS_CHOICES = (
   (True,'Active'),
   (False,'Inactive')
)

ROLE_CHOICES = (
    ('property','property'),
    ('blog','blog')
  )

class CustomUser(AbstractUser):
  phonenumber = models.PositiveIntegerField(null=True,blank=True)

  role = models.CharField(max_length=80,choices=ROLE_CHOICES)

  is_active = models.BooleanField(default=True,choices=STATUS_CHOICES)

  is_staff = models.BooleanField(default=True)

  REQUIRED_FIELDS = ['email']


BLOG_CHOICES = (
  ('publish','publish'),
  ('draft','draft')
)

ACTIVE_CHOICES = (
  (True,'Active'),
  (False,'Inactive')
)









ACTIVE_STATUS = (
  (True,'Active'),
  (False,'Inactive')
)

BUTTON_STATUS = (
  ('publish','Publish'),
  ('draft','Draft')
)


class Blog(models.Model):
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=200)
  is_active = models.BooleanField(default=False,choices=ACTIVE_STATUS)
  img = models.ImageField(upload_to='banner')
  status  =  models.CharField(max_length=100,choices=BUTTON_STATUS)
  add_to_homepage = models.BooleanField(default=False)
  reorder = models.PositiveIntegerField(default=0)
  date = models.DateField(default=datetime.date.today)


  def __str__(self):
    return self.title


BUILDER_STATUS = (
  (True,'Active'),
  (False,'Inactive')
)

class BlogGallery(models.Model):
  blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
  image = models.ImageField(upload_to='blog_gallery')

class Builder(models.Model):
  name = models.CharField(max_length=80)
  logo = models.ImageField(upload_to='img_logo')
  status = models.BooleanField(default=False,choices=BUILDER_STATUS)
  add_to_homepage = models.BooleanField(default=False)
  reorder = models.PositiveIntegerField(default=0)


class BuilderLogos(models.Model):
  builder = models.ForeignKey(Builder,on_delete=models.CASCADE)
  image = models.ImageField(upload_to='builder_logos')





COMMUNITY_STATUS = (
  (True,'Active'),
  (False,'Inactive')
)

class Community(models.Model):
  name = models.CharField(max_length=100)
  status = models.BooleanField(default=False,choices=COMMUNITY_STATUS)

  def __str__(self):
     return self.name



# PROPERTY SECTION

# models.py

from django.db import models





STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('draft', 'Draft'),
]


class Information(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    property_name = models.CharField(max_length=255)
    property_address = models.TextField()
    property_description = models.TextField()
    property_type = models.ForeignKey('PropertyType', on_delete=models.SET_NULL, null=True, blank=True)
    builder = models.ForeignKey(Builder,on_delete=models.CASCADE)
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    information = models.ForeignKey(Information,on_delete=models.CASCADE)
   
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    min_sqft = models.PositiveIntegerField()
    max_sqft = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
  
    amenities = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    addToHomepage = models.BooleanField(default=False)
    displayOrder = models.PositiveIntegerField(null=True, blank=True)

    floorplanPDF = models.FileField(upload_to='floorplans/', blank=True, null=True)
    brochurePDF = models.FileField(upload_to='brochures/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    
    
class Amenity(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

    def __str__(self):
        return self.name
    
    


class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    def __str__(self):
        return self.name
    

class PropertyGallery(models.Model):
   propertyimage = models.ForeignKey(PropertyImage,on_delete=models.CASCADE)
   img = models.ImageField(upload_to='imgs/')

    



  



  

