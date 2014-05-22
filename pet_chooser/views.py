from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from pprint import pprint

from forms import PetsCauldron, HouseType

def witch_journey(request, form_name=None):

    context_vars = {}
#     pprint(settings.TEMP_DATA)
    
    if request.method == 'POST':

        cauldron = PetsCauldron(form_name)
        form = cauldron.current_form.populate_from_POST(request.POST)
        if form.is_valid():
            
            cauldron.save()
            # be good and redirect
            return HttpResponseRedirect(reverse('named_form',
                                                args=(cauldron.next_form.form_name,)
                                       ))

    else:
        cauldron = PetsCauldron(form_name)
        form = cauldron.current_form.instance

    context_vars['form'] = form
    context_vars['cauldron'] = cauldron


    return render_to_response('main_page.html',
                              context_vars,
                              context_instance=RequestContext(request))