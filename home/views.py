from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Count
import json
from django.db.models import Count, DateTimeField
from django.db.models.functions import TruncYear

# Create your views here.
def home(request):
    return render(request, 'home.html', {})


'''def charts(request):

    total_societies = Society.objects.count()

    # Retrieve state-wise society counts
    state_data = Society.objects.values('state').annotate(count=Count('state')).order_by('state')
    

    # Retrieve sector-wise society counts
    sector_data = Society.objects.values('society_type').annotate(count=Count('id'))
    
   # Retrieve year-wise society counts
    year_data = Society.objects.annotate(year=TruncYear('date_joined', output_field=DateTimeField())).values('year').annotate(count=Count('year')).order_by('year')
    state_data_json = json.dumps(list(state_data))
    sector_data_json = json.dumps(list(sector_data))
    year_data_list = list(year_data)
    year_data_list = [{'year': str(item['year'])[:4], 'count': item['count']} for item in year_data]
    year_data_json = json.dumps(list(year_data_list))

    context = {
        'total_societies': total_societies,
        'state_data': state_data_json,
        'sector_data': sector_data_json,
        'year_data': year_data_json,
    }

    return render(request, 'charts.html', context)
'''