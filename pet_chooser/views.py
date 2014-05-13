from django.shortcuts import render_to_response
from django.template import RequestContext


from pprint import pprint

from forms import PetsCauldron, HouseType

def witch_journey(request, form_name=None):

    context_vars = {}
    
    if request.method == 'POST':

        cauldron = PetsCauldron(form_name)
        form = HouseType(request.POST)
        if form.is_valid():
            
            cauldron.save()
            
            pprint(form.cleaned_data)
            
            if form.has_small_house:
                print "small house when valid"
#             json_string = simplejson.dumps(location_extract)
#             return HttpResponse(content=json_string, mimetype='application/json')
#         else:
#             json_string = simplejson.dumps([])
#             return HttpResponse(content=json_string, mimetype='application/json')
    else:
        cauldron = PetsCauldron()
        form = HouseType()
        if form.has_small_house == None:
            print "small house when init"


    context_vars['form'] = form
    context_vars['cauldron'] = cauldron


    return render_to_response('main_page.html',
                              context_vars,
                              context_instance=RequestContext(request))