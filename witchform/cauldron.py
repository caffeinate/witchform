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

        self._update_formset()

        if current_form_name and current_form_name not in self._form_set.keys():
            raise Exception("Unknown form [%s]" % current_form_name)
        self._current_form_name = current_form_name


    def _update_formset(self):
        # re-project into more convenient internal structure
        self._form_set = {}
        for form in self.form_set:
            f = _CauldronForm(form)
            if f.form_name in self._form_set:
                raise Exception("Cauldron contains duplicate forms [%s]" % f.form_name)

            if f.form_name in settings.TEMP_DATA:
                d = simplejson.loads(settings.TEMP_DATA[f.form_name]['form_fields'])
                f.set_values(d)

            # load ingredients if available (i.e. if form has been filled in by user
            for fq_ingredient in f.ingredients_required_from_form():
                target_form, required_ingredient = fq_ingredient.split(".")
                if target_form in settings.TEMP_DATA \
                and 'resulting_ingredients' in settings.TEMP_DATA[target_form] \
                and required_ingredient in settings.TEMP_DATA[target_form]['resulting_ingredients']:
                    i = settings.TEMP_DATA[target_form]['resulting_ingredients'][required_ingredient]
                    f.set_ingredient(fq_ingredient, i)

            self._form_set[f.form_name] = f



    @property
    def current_form(self):
        if self._current_form_name:
            # I am here
            return self._form_set[self._current_form_name]
        else:
            a_ready_form = self._get_in_demand_forms()[0]
            return self._form_set[a_ready_form.form_name]

    
    def _get_complete_forms(self):
        """
        @return: subset list of self._form_set of forms that have been filled in.
        
            TODO - think about whether to include forms that have fallen out of scope
            if the user has changed answers and therefore flow through the forms
        """
        # TODO
        pass

    def _get_not_complete_forms(self):
        """
        @return: subset list of self._form_set of forms that aren't  is_complete()
        """
        f = []
        for cauldron_form in self._form_set.itervalues():
            if not cauldron_form.is_complete():
                f.append(cauldron_form)
        return f
    
    def _get_ready_forms(self):
        """
        @return: subset list of self._form_set
        
        subset is a list of forms who's-
        (i) ingredients are ready (i.e. the form that creates the ingredient has finished
                                   OR has no ingredients )
          AND
        (ii) .ready() method returns True
          AND
        (iii) has not already been called
        """        
        # TODO
        ready = []
        for cauldron_form in self._form_set.itervalues():
            # len(cauldron_form.ingredients) == 0 and
            if cauldron_form.ready()\
            and not cauldron_form.is_complete():
                ready.append(cauldron_form)
        return ready

    def _get_in_demand_forms(self):
        """
        @return: subset list of self._form_set

        subset is a list of forms which are ready and where another form (which isn't is_complete)
        is expecting an ingredient from it.
        """

        # TODO make less brutish
        d = []
        ready_forms = self._get_ready_forms()
        not_complete = self._get_not_complete_forms()
        for f in not_complete:
            for ff in ready_forms:
                if len(f.ingredients_required_from_form(form_name=ff.form_name)) > 0:
                    print "%s is in demand from %s" % (ff, f)
                    d.append(ff)
        return d

    def save(self):
        """
        save current form then re-calculate which other forms are now ready
        """

        # TODO - temp save data to memory that is persistent between requests
        #        does serialise the forms but needn't as it's memory

        django_form = self.current_form.instance
        json = django_form.save_serialise()
        self.current_form.set_values(django_form.cleaned_data)
        form_name = self.current_form.form_name
        settings.TEMP_DATA[form_name] = { 'form_fields' : json }

        if self.current_form.is_complete():
            # @see note in CauldronFormMixin
            fresh_ingredients = self._get_required_ingredients(self.current_form)
            settings.TEMP_DATA[form_name]['resulting_ingredients'] = fresh_ingredients
        
        self._update_formset()


    @property
    def next_form(self):
        on_demand_forms = self._get_in_demand_forms()
        if len(on_demand_forms) > 0:
            return on_demand_forms[0]
        return None


    def _get_required_ingredients(self, current_cauldron_form):
        """
        get ingredients that are in demand by other forms
        @param current_cauldron_form: source of ingredients - i.e. other forms need these ingredients
        @return: dict short_ingedient_name => ingredient_value
        """
        form_name = current_cauldron_form.form_name
        fresh_ingredients = {}
        for cauldron_form in self._form_set.itervalues():
            ingredients = cauldron_form.ingredients_required_from_form(form_name)
            for fq_ingredient in ingredients:
                short_ingredient = fq_ingredient.split(".")[1]
                ready_ingredient = getattr(current_cauldron_form.instance, short_ingredient)
                print "%s needs ingredient %s which has value of %s" % (cauldron_form.form_name, fq_ingredient, ready_ingredient)
                fresh_ingredients[short_ingredient] = ready_ingredient
        return fresh_ingredients
                


class CauldronFormMixin(object):
    
    copy = "" # to override - displayed above input boxes; probably a question or statement
    
    """
    Notes-
    - @property[s] will only be called if is_complete() is True
    
    """
    
    def ready(self):
        """
        Might be implemented by subclasses.
        @return bool: if form can be displayed i.e. form as is ready for user input
        """
        return True
    
    def is_complete(self):
        """
        @return None (unknown to form); True or False if this form has been completed by user
        
        @see: _CauldronForm.is_complete()
        """
        return None

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
        