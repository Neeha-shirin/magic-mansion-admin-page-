# forms.py
from django import forms
from .models import Property,Amenity
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'property_name', 'property_address', 'property_description', 'property_type',
            'price', 'bedrooms', 'bathrooms', 'min_sqft', 'max_sqft', 'location',
            'community', 'amenities', 'status', 'addToHomepage', 'displayOrder',
            'floorplanPDF', 'brochurePDF'
        ]
        widgets = {
            'amenities': forms.CheckboxSelectMultiple(),
            'property_type': forms.Select(attrs={'class': 'form-control'})
        }
      

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['name', 'status']