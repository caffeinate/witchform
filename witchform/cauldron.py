"""
Created on 12 May 2014

@author: si
"""
from witchform import get_form_name, get_ingredients

from pprint import pprint

class Cauldron(object):
    """
    Container and controller for a set of forms
    """
    form_set = [] # must be defined by each child class 

    def __init__(self, current_form=None):
        self.current_form = current_form
        if len(self.form_set) == 0:
            raise NotImplementedError("form_set must be populated by implementing classes")
        
        # re-project into more convenient internal structure
        self._form_set = {}
        for form in self.form_set:
            form_name = get_form_name(form)
            if form_name in self._form_set:
                raise Exception("Cauldron contains duplicate forms [%s]" % form_name)
            self._form_set[form_name] = {   'instance' : form,
                                            'ingredients' : get_ingredients(form)
                                         }
        pprint(self._form_set)
    
