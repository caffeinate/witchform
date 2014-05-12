from django import forms

from pprint import pprint

class HairAllergy(forms.Form):
    has_hair_allergy = forms.BooleanField(required=False)

class HouseType(forms.Form):
    house_type_choices = [  ('flat', 'Flat or Maisonette'),
                            ('farm', 'Farm'),
                         ] 
    houseType = forms.ChoiceField(choices=house_type_choices, required=True, widget=forms.RadioSelect)
    
    @property
    def has_small_house(self):
        
        if not hasattr(self, 'cleaned_data'):
            return None

        pprint(self.cleaned_data)
        
        if True:
            return True
