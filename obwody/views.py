from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Gmina, Obwód


def index(request):
    gminy = Gmina.objects.order_by('name')
    context = {'gminy': gminy}
    return render(request, 'obwody/index.html', context)


def gmina(request, gmina_id):
    gmina = get_object_or_404(Gmina, pk=gmina_id)
    obwody = Obwód.objects.filter(gmina=gmina)
    context = {'gmina': gmina, 'obwody': obwody}
    return render(request, 'obwody/gmina.html', context)

@transaction.atomic
def obwód(request, obwód_id):
    obwód = get_object_or_404(Obwód, pk=obwód_id)

    try:
        cards_old = int(request.POST['cards_old'])
        cards = int(request.POST['cards'])
        voters_old = int(request.POST['voters_old'])
        voters = int(request.POST['voters'])

        if cards < 0 or voters < 0:
            messages.error(request, "Liczby muszą być nieujemne.")
        elif cards_old != obwód.cards:
            messages.error(request, "Wystąpił konflikt zapisu dla ilości kart do głosowania: "
                                    "zapisujesz %d a ktoś inny zapisał %d." % cards % obwód.cards)
        elif voters_old != obwód.voters:
            messages.error(request, "Wystąpił konflikt zapisu dla ilości uprawnionych do głosowania: "
                                    "zapisujesz %d a ktoś inny zapisał %d." % voters % obwód.voters)
        else:
            obwód.cards = cards
            obwód.voters = voters
            obwód.save()
            messages.success(request, "Zapisano pomyślnie!")

    except KeyError:
        messages.error(request, "Proszę wypełnić wszystkie pola.")
    except ValueError:
        messages.error(request, "Niepoprawne dane.")

    return HttpResponseRedirect(reverse('gmina', args=(obwód.gmina_id,)))