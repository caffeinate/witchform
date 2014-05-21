'''
Created on 13 May 2014

@author: si
'''


class CauldronIngredient(object):
    def __init__(self, source):
        """
        @param source: a string representing a form.property
        """
        self.source = source
        self.value = None
        self.value_set = False

    def __str__(self):
        return self.get_source_name()
    
    def get_source_name(self):
        """
        @return: String - full name of form.property. e.g. 'HouseType.has_small_house'
        """
        return self.source
    
    def has_value(self):
        """
        might need to use tri-state so use this.
        @return: bool - never None
        """
        return self.value_set

    def set_value(self, value):
        self.value = value
        self.value_set = True
    
    def get_value(self):
        return self.value



def get_form_name(form):
    """
    @param form: not initialised & unbounded form
    @return: string of simplified name
    """

    """
    can't just user form.__class__.__name__ because of multiple inheritance...
    >>> str(h)
    "<class 'pet_chooser.forms.HouseType'>"
    >>> h.__class__.__name__
    'DeclarativeFieldsMetaclass'
    >>> type(h)
    <class 'django.forms.forms.DeclarativeFieldsMetaclass'>
    >>> f = str(h)[1:-2]
    >>> f
    "class 'pet_chooser.forms.HouseType"
    """
    f = str(form)[1:-2]
    return f.split(".")[-1]

def get_ingredients(form):
    """
    Forms belonging to a cauldron declare the inputs needed from other forms.

    @param form: not initialised & unbounded form
    @return: dictionary of 'form.property' -> <CauldronIngredient> 
             Former is in class declaration, later is source_form.property
    """
    ingredients = {}
    for k,v in form.__dict__.iteritems():
        if isinstance(v, CauldronIngredient):
            ingredients[v.source] = v
    return ingredients



class _CauldronForm(object):
    def __init__(self, form):
        """
        @param form: forms.Form + CauldronFormMixin unbounded instance
        """
        self.instance_unbounded = form
        self.form_name = get_form_name(form)
        self._instance = None
        self.ingredients = get_ingredients(form)
        self.has_values = False
        self.values = {}
    
    def __str__(self):
        return self.form_name

    def set_values(self, values):
        """
        This form has already been submitted by the user with these values
        """
        self.has_values = True
        self.values = values
    
    def is_complete(self):
        """
        don't show to user if complete.
        
        If has_values then user has been shown then form but the form could also
        invalidate itself by returning True to it's is_complete.
        
        @return: bool
        """
        instance_complete = self.instance.is_complete()
        if instance_complete == None:
            return self.has_values

        return instance_complete
    
    @property
    def instance(self):
        """
        instantiate on demand
        """
        if not self._instance:
            self._instance = self.instance_unbounded(initial=self.values)
        return self._instance

    def populate_from_POST(self, post_data):
        """
        instantiate form with unclean data from form
        @param post_data: is probably going to be request.POST
        @return: the django form
        """
        # maybe - if already initialised just fill the form
        self._instance = self.instance_unbounded(post_data)
        return self._instance

    def ingredients_required(self, form_name):
        """
        for the given form, return list of ingredients the current form needs.

        @param form_name: String
        @return: list of property names (string) OR empty list for nothing
        """
        required = []
        for form_property, ingredient in self.ingredients.iteritems():
            required_form = form_property.split('.')[0]
            if required_form == form_name:
                required.append(form_property.split('.')[1])
        return required
    
    def set_ingredient(self, form_property, ingredient_value):
        """
        @param form_property: String of full form name. e.g. 'HouseType.has_small_house'
        """
        self.ingredients[form_property].set_value(ingredient_value)
    

    def ready(self):
        return self.instance.ready()
