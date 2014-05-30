from django import forms

from pprint import pprint

from witchform.cauldron import Cauldron, CauldronFormMixin
from witchform.cauldron_toil import CauldronIngredient

yes_no_choices = [  ('yes', 'Yes'),
                    ('no', 'No'),
                 ]

class SkinType(forms.Form, CauldronFormMixin):
    copy = "Do you have an allergy or dislike?"
    hair_or_fur = forms.BooleanField(required=False)
    scales = forms.BooleanField(required=False)
    claws_or_sharp_teeth = forms.BooleanField(required=False)

    @property
    def likes_hair_or_fur(self):
        return not self.cleaned_data['hair_or_fur']

    @property
    def likes_scales(self):
        return not self.cleaned_data['scales']

    @property
    def likes_claws_or_sharp_teeth(self):
        return not self.cleaned_data['claws_or_sharp_teeth']


class SmallChildren(forms.Form, CauldronFormMixin):
    copy = "Do you have any small children?"
    small_children = forms.ChoiceField(choices=yes_no_choices, required=True, widget=forms.RadioSelect)

    @property
    def has_small_children(self):
        return self.cleaned_data['small_children']=='yes'


class HouseType(forms.Form, CauldronFormMixin):
    house_type_choices = [  ('flat', 'Flat or Maisonette'),
                            ('mansion', 'Mansion or Stately home'),
                            ('farm', 'Farm'),
                         ] 
    houseType = forms.ChoiceField(choices=house_type_choices, required=True, widget=forms.RadioSelect)
    
    @property
    def has_small_house(self):        
        houseType = self.cleaned_data['houseType']
        return houseType not in ['farm', 'mansion']


class SuggestCrocodile(forms.Form, CauldronFormMixin):
    how_about_a_crocodile = forms.ChoiceField(choices=yes_no_choices, required=True, widget=forms.RadioSelect)
    has_small_house = CauldronIngredient('HouseType.has_small_house')
    has_small_children = CauldronIngredient('SmallChildren.has_small_children')
    likes_scales = CauldronIngredient('SkinType.likes_scales')
    likes_claws_or_sharp_teeth = CauldronIngredient('SkinType.likes_claws_or_sharp_teeth')

    def ready(self):

        x =(self.has_small_house.has_value() \
        and self.has_small_children.has_value() \
        and self.likes_scales.has_value() \
        and not self.is_complete())

        return x
    
    def is_complete(self):
        
        """
        i.e. returning True means don't show this form
        """

        # Demonstrating that all three ingredients need a particular value
        if self.has_small_house.has_value() and self.has_small_house.get_value() == True:
            return True

        if self.has_small_children.has_value() and self.has_small_children.get_value() == True:
            return True
        
        if self.likes_scales.has_value() and self.likes_scales.get_value() == False:
            return True

        # returning None means the _CauldronForm decides if values have been set
        return None


class PetsCauldron(Cauldron):

    form_set = [SkinType,
                SmallChildren,
                HouseType,
                SuggestCrocodile
               ]
