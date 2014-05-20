"""
Created on 12 May 2014

@author: si
"""
from django.conf import settings
from django.utils import simplejson

from cauldron_toil import _CauldronForm

from pprint import pprint

class Cauldron(object):
    """
    Container and controller for a set of forms
    """
    form_set = [] # must be defined by each child class
    
    def __init__(self, current_form_name=None):

        if len(self.form_set) == 0:
            raise NotImplementedError("form_set must be populated by implementing classes")
        
        # re-project into more convenient internal structure
        self._form_set = {}
        for form in self.form_set:
            f = _CauldronForm(form)
            if f.form_name in self._form_set:
                raise Exception("Cauldron contains duplicate forms [%s]" % f.form_name)
            self._form_set[f.form_name] = f

        if current_form_name and current_form_name not in self._form_set:
            raise Exception("Unknown form")
        self._current_form_name = current_form_name


    @property
    def current_form(self):
        if self._current_form_name:
            # I am here
            return self._form_set[self._current_form_name]
        else:
            a_ready_form = self._get_ready_forms()[0]
            return self._form_set[a_ready_form.form_name]

    
    def _get_complete_forms(self):
        """
        @return: subset list of self._form_set of forms that have been filled in.
        
            TODO - think about whether to include forms that have fallen out of scope
            if the user has changed answers and therefore flow through the forms
        """
        # TODO
        pass
    
    def _get_ready_forms(self):
        """
        @return: subset list of self._form_set
        
        subset is a list of forms who's-
        (i) ingredients are ready (i.e. the form that creates the ingredient has finished)
        (ii) .ready() method returns True
        (iii) has not already been called
        """
        
        # TODO 
        
        ready = []
        for form_name,cauldron_form in self._form_set.iteritems():
            if len(cauldron_form.ingredients) == 0 and cauldron_form.ready():
                ready.append(cauldron_form)
        return ready
    
    def save(self):
        """
        
        """
        # TODO
        json = self.current_form.save_serialise()
        settings.TEMP_DATA[self.current_form.form_name] = json
        pprint(settings.TEMP_DATA)


class CauldronFormMixin(object):
    
    def ready(self):
        """
        Might be implemented by subclasses.
        @return bool: if form can be displayed i.e. form as is ready for user input
        """
        return True

    def build_form(self):
        """
        Might be implemented by subclasses.
        Builds anything needed prior to form being rendered. e.g. populates multiple choice fields
        """
        pass
    
    def save_serialise(self):
        """
        This is called by the parent Cauldron.
        @return: string of serialised fields from form. Currently uses json
        """
        json_string = simplejson.dumps(self.cleaned_data)
        return json_string
        