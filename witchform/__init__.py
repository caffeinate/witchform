from cauldron_ingredient import CauldronIngredient

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
