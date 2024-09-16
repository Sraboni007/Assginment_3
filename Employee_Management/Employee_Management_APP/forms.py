from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'address', 'phone_number', 'short_description']  # Exclude salary and designation

    # Custom validation for name (ensure no digits are included)
    def clean_name(self):
       name = self.cleaned_data.get('name')  # Accessing name after validation
       if any(char.isdigit() for char in name):
          raise forms.ValidationError("The name should not contain digits.")
       return name

    # Custom validation for address (ensure no digits are included)
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if any(char.isdigit() for char in address):
            raise forms.ValidationError("The address should not contain digits.")
        return address

    # Custom validation for phone number (allow digits and optionally + sign)
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

    # Overriding the save method to handle salary and designation before saving
    def save(self, commit=True):
        employee = super().save(commit=False)
        
        if not self.instance.pk:  # If this is a new employee (no primary key yet)
            # Set salary and designation here (they were initially provided, so they're non-editable later)
            employee.salary = self.cleaned_data.get('salary')
            employee.designation = self.cleaned_data.get('designation')
        
        if commit:
            employee.save()
        return employee

    # Custom constructor to pass initial data for salary and designation on first form submission
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If this is a new instance, allow salary and designation in form
            self.fields['salary'] = forms.DecimalField(max_digits=10, decimal_places=2)
            self.fields['designation'] = forms.ChoiceField(choices=Employee.DESIGNATION_CHOICES)
        else:  # Make the fields read-only for existing instances
            self.fields['salary'] = forms.DecimalField(max_digits=10, decimal_places=2, initial=self.instance.salary, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            self.fields['designation'] = forms.ChoiceField(choices=Employee.DESIGNATION_CHOICES, initial=self.instance.designation, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
