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
    @return: list of tuples ('ingredient', 'form.property'). 
             Former is in class declaration, later is source_form.property
    """
    ingredients = []
    for k,v in form.__dict__.iteritems():
        if isinstance(v, CauldronIngredient):
            ingredients.append((v, v.source))
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

    @property
    def instance(self):
        """
        instantiate on demand
        """
        if not self._instance:
            self._instance = self.instance_unbounded()
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

    def ready(self):
        return self.instance.ready()
