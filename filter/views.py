from django.shortcuts import render
from django.http import JsonResponse
from startups.models import Profile
from django.db.models import Count
from django.db.models.functions import ExtractYear


def info(request):
    states = Profile.objects.filter(is_accepted=True).values_list('state', flat=True).distinct()
    startup_types = Profile.objects.filter(is_accepted=True).values_list('startup_type', flat=True).distinct()
    registration_years = Profile.objects.filter(is_accepted=True).dates('date_joined', 'year', order='DESC')

    if request.method == 'GET':
        state = request.GET.get('state', '')
        district = request.GET.get('district', '')
        startup_type = request.GET.get('startup_type', '')
        registration_year = request.GET.get('registration_year', '')

        filtered_data = Profile.objects.filter(is_accepted=True)

        if state:
            filtered_data = filtered_data.filter(state=state)

        if district:
            filtered_data = filtered_data.filter(district=district)

        if startup_type:
            filtered_data = filtered_data.filter(startup_type=startup_type)

        if registration_year:
            filtered_data = filtered_data.filter(date_joined__year=registration_year)
    else:
        filtered_data = Profile.objects.filter(is_accepted=True)  # Show all data when no filters are applied

    context = {
        'states': states,
        'startup_types': startup_types,
        'registration_years': registration_years,
        'filter_data': filtered_data
    }

    return render(request, 'filter/info.html', context)


def get_districts_view(request):
    state = request.GET.get('state', '')
    districts = Profile.objects.filter(state=state).values_list('district', flat=True).distinct()
    return JsonResponse({'districts': list(districts)})