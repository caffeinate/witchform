from django import forms

from pprint import pprint

from witchform.cauldron import Cauldron, CauldronFormMixin
from witchform.cauldron_toil import CauldronIngredient

yes_no_choices = [  ('yes', 'Yes'),
                    ('no', 'No'),
                 ]


class HairAllergy(forms.Form, CauldronFormMixin):
    has_hair_allergy = forms.BooleanField(required=False)

class HouseType(forms.Form, CauldronFormMixin):
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

class SuggestReptile(forms.Form, CauldronFormMixin):
    yes_no = forms.ChoiceField(choices=yes_no_choices, required=True, widget=forms.RadioSelect)
    has_small_house = CauldronIngredient('HouseType.has_small_house')

    def ready(self):
        if self.has_small_house.has_value():
            print "has value"
            if self.has_small_house.get_value() == True:
                print "does have small house"
            else:
                print "has big house"
            return True
        return False
    
#     def is_complete(self):
#         return not self.has_small_house.has_value()




class PetsCauldron(Cauldron):

    form_set = [HairAllergy, 
                HouseType,
                SuggestReptile
               ]
