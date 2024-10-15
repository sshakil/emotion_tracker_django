#from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rest_framework.utils import json

from ..models import Day, DayPeriod, Period, Entry, Emotion

# GET /days or /days.json
@csrf_exempt
def day_list(request):
    if request.method == 'GET':
        days = Day.objects.all().values()  # Fetch all days
        return JsonResponse(list(days), safe=False)

# GET /days/fetch or /days/1.json
@csrf_exempt
def day_detail(request):
    data = json.loads(request.body)
    date = data.get('date')

    day = Day.objects.filter(date=date).first()  # Fetch the day by date
    day_json = {}

    if day:
        # Raw SQL query to get the relevant data
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    dp.id as dp_id, 
                    p.name as period_name, 
                    e.uuid as entry_uuid, 
                    em.name as emotion_name
                FROM day_periods dp
                INNER JOIN periods p ON p.id = dp.period_id
                INNER JOIN entries e ON e.day_period_id = dp.id
                INNER JOIN emotions em ON em.id = e.emotion_id
                WHERE dp.day_id = %s
                ORDER BY dp.id
            """, [day.id])

            data = cursor.fetchall()

        # Group the data by day_period ID and structure the JSON response
        periods_json = {}
        for dp_id, period_name, entry_uuid, emotion_name in data:
            if dp_id not in periods_json:
                periods_json[dp_id] = {'name': period_name, 'emotions': []}
            periods_json[dp_id]['emotions'].append({'name': emotion_name, 'uuid': entry_uuid})

        day_json = {
            'date': day.date.isoformat(),
            'periods': list(periods_json.values())
        }

    return JsonResponse(day_json)

# POST /days or /days.json (create a new day with periods and entries)
@csrf_exempt
def day_create(request):
    if request.method == 'POST':
        data = request.POST
        errors = []
        created_entries = []

        try:
            # Find or create Day object
            day, _ = Day.objects.get_or_create(date=data['day']['date'])

            for period in data['day']['periods_attributes']:
                # Find or create Period object
                period_obj, _ = Period.objects.get_or_create(name=period['name'])
                day_period, _ = DayPeriod.objects.get_or_create(day=day, period=period_obj)

                # For each emotion in the period, create entries
                for emotion in period['emotions_attributes']:
                    emotion_obj, _ = Emotion.objects.get_or_create(name=emotion['name'])
                    entry, created = Entry.objects.get_or_create(day_period=day_period, emotion=emotion_obj)

                    if created:
                        created_entries.append({
                            'uuid': entry.uuid,
                            'emotion_name': emotion_obj.name,
                            'period_name': period_obj.name,
                            'date': day.date.isoformat()
                        })

        except Exception as e:
            errors.append(str(e))

        if errors:
            return JsonResponse({'error': errors}, status=400)
        else:
            return JsonResponse({'entries': created_entries}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Helper function to set the day (equivalent to set_day)
def set_day(pk):
    return get_object_or_404(Day, pk=pk)