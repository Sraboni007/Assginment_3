from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'address', 'phone_number', 'short_description']  

   
    def clean_name(self):
       name = self.cleaned_data.get('name')  
       if any(char.isdigit() for char in name):
          raise forms.ValidationError("The name should not contain digits.")
       return name

   
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if any(char.isdigit() for char in address):
            raise forms.ValidationError("The address should not contain digits.")
        return address

   
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        is_valid = False
        if phone_number.strip()[0] == "+" and phone_number.strip()[1:].isdigit():
            is_valid = True
        elif phone_number.isdigit():
            is_valid = True
        if not is_valid:
             raise forms.ValidationError("Enter a valid phone number.")
            
        if Employee.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An employee with this phone number already exists.")
        return phone_number


    def save(self, commit=True):
        employee = super().save(commit=False)
        
        if not self.instance.pk:  
          
            employee.salary = self.cleaned_data.get('salary')
            employee.designation = self.cleaned_data.get('designation')
        
        if commit:
            employee.save()
        return employee

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk: 
            self.fields['salary'] = forms.DecimalField(max_digits=10, decimal_places=2)
            self.fields['designation'] = forms.ChoiceField(choices=Employee.DESIGNATION_CHOICES)
        else:  
            self.fields['salary'] = forms.DecimalField(max_digits=10, decimal_places=2, initial=self.instance.salary, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            self.fields['designation'] = forms.ChoiceField(choices=Employee.DESIGNATION_CHOICES, initial=self.instance.designation, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
