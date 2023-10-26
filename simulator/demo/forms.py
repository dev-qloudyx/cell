from django import forms
from .models import Client


class ClientForm(forms.Form):
    name = forms.CharField(max_length=30)
    company = forms.CharField(max_length=50)
    email = forms.EmailField()
    video = forms.CharField(max_length=5)
    
    class Meta:
        model = Client
        fields = ['name','company', 'email', 'video']



freezer_choice = (
    ("Select Option", "Select Option"),
    ("CELL", "CELL (SmartFreez's unidirectional CRF)"),
    ("Norma Airblast", "Norma Airblast"),
    ("Norma Bag", "Norma Bag"),
    ("Radial freezer", "Radial freezer (e.g., CoolCell®)"),
    ("Scale", "Scale"),
)

container_choice = (
    ("Select Option", "Select Option"),
    ("Bag", "Bag"),
    ("Vial", "Vial"),
)

subcontainer_choice = (
    ("Select Option", "Select Option"),
    ("Custom vial", "Custom vial"),
    ("Standard Cryovial(2 mL)", "Standard Cryovial(2 mL)"),
    ("Vial Cellon® (10 mL)", "Vial Cellon® (10 mL)"),
)

fill_choice = (
    ("Select Option", "Select Option"),
    ("1 mL", "1 mL"),
    ("1.2 mL", "1.2 mL"),
    ("1.4 mL", "1.4 mL"),
    ("1.6 mL", "1.6 mL"),
)
    
biomix_choice = (
    ("Select Option", "Select Option"),
    ("Cryostor®", "Cryostor®"),
    ("DMSO", "DMSO"),
    ("Custom", "Custom"),
)

solute_choice = (
    ("Select Option", "Select Option"),
    ("0.15", "0.15"),
    ("0.10", "0.10"),
    ("0.05", "0.05"),
    ("0.025", "0.025"),
    ("0.01", "0.01"),
)
cooling_choice = (
    ("Select Option", "Select Option"),
    ("0.5", "0.5"),
    ("1", "1"),
    ("2", "2"),
    ("5", "5"),
)


form_fields = {
    'freezer': forms.ChoiceField(choices=freezer_choice, widget=forms.Select, initial="Select Option", label="Freezer Type") ,
    'container': forms.ChoiceField(choices=container_choice, widget=forms.Select, initial="Select Option" , label="Container Type"),
    'subcontainer': forms.ChoiceField(choices=subcontainer_choice, widget=forms.Select, initial="Select Option" , label="Container Sub-Type"),
    'fill': forms.ChoiceField(choices=fill_choice, widget=forms.Select , initial="Select Option", label="Fill Volume"),
    'biomixture': forms.ChoiceField(choices=biomix_choice, widget=forms.Select, initial="Select Option", label="Biomixture"),
    'solutefraction': forms.ChoiceField(choices=solute_choice, widget=forms.Select , initial="Select Option", label="Mass fraction of principal solute"),
    'transitiontemp': forms.IntegerField(initial= -32, widget=forms.NumberInput(attrs={'readonly': 'readonly'}) , label="Glass transition temperature, Tg'(°C)"),
    'cooling': forms.ChoiceField(choices=cooling_choice, widget=forms.Select, initial="Select Option" , label="Cooling-rate (°C/min)"),
    'finaltemp': forms.IntegerField(initial= -80, widget=forms.NumberInput(attrs={'readonly': 'readonly'}), label="Final temperature (°C)"),
}

class MainForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)

        # Iterate through the dictionary and add fields to the form
        for field_name, field in form_fields.items():
            self.fields[field_name] = field