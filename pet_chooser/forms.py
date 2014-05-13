from django import forms

from pprint import pprint

from witchform.cauldron import Cauldron
from witchform.cauldron_ingredient import CauldronIngredient

yes_no_choices = [  ('yes', 'Yes'),
                    ('no', 'No'),
                 ]


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
        
        if True:
            return True

class SuggestReptile(forms.Form):
    yes_no = forms.ChoiceField(choices=yes_no_choices, required=True, widget=forms.RadioSelect)
    has_small_house = CauldronIngredient('HouseType.has_small_house')



class PetsCauldron(Cauldron):

    form_set = [HairAllergy, 
                HouseType,
                SuggestReptile
               ]
