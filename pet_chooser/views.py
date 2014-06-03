from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from pprint import pprint

from forms import PetsCauldron, HouseType

def witch_journey(request, form_name=None):

    context_vars = {}
    pprint(settings.TEMP_DATA)
    
    if request.method == 'POST':

        cauldron = PetsCauldron(form_name)
        form = cauldron.current_form.populate_from_POST(request.POST)
        if form.is_valid():
            
            cauldron.save()
            next_form = cauldron.next_form
            if next_form:
                next_page = reverse('named_form', args=(next_form.form_name,))
            else:
                next_page = reverse('finished')

            # be good and redirect
            return HttpResponseRedirect(next_page)

    else:
        cauldron = PetsCauldron(form_name)
        current_form = cauldron.current_form
        if current_form == None:
            return HttpResponseRedirect(reverse('finished'))

        form = current_form.instance

    context_vars['form'] = form
    context_vars['cauldron'] = cauldron


    return render_to_response('main_page.html',
                              context_vars,
                              context_instance=RequestContext(request))

def finished_journey(request):

    cauldron = PetsCauldron()

    context_vars = {'get' : {} }

    for form_name, property_name, pet_name in [('SuggestGerbil', 'get_gerbil', 'gerbil'),
                                               ('SuggestHorse', 'get_horse', 'horse'),
                                               ('SuggestCrocodile', 'get_croc', 'crocodile')
                                              ]:
        try:
            result = cauldron.get_form_data(form_name)['resulting_ingredients'][property_name]
        except:
            result = False

        context_vars['get'][pet_name] = result


    return render_to_response('finished.html',
                          context_vars,
                          context_instance=RequestContext(request))
