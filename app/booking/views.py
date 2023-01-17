from django.shortcuts import render, redirect
from django.http import request, HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

from .models import *

# Create your views here.
@login_required
def index(request):

	context = {
		'rooms': Room.objects.all()
	}
	return render(request, 'booking/home.html', context)


@login_required
def room_details(request, room_id):
	room = Room.objects.get(pk=room_id)
	context = {
		'room': room,
		'meetings' : room.meetings
	}
	return render(request, 'booking/room.html', context)

@login_required
def room_update(request, room_id):
	room = Room.objects.get(pk=room_id)
	context = {
		'room': room,
		'meetings' : room.meetings
	}

	res = {}
	if request.method == "POST":
		data = request.POST

		print(data)

		_id = -1
		if data.get('id'):
			_id = data.get("id")



		title = data.get("title")
		start = data.get("start")
		end = data.get("end")
		allDay = data.get("allDay")
		backgroundColor = data.get("backgroundColor")
		borderColor = data.get("borderColor")

		isRecur = data.get("isRecur")
		if(isRecur == 'false'):
			isRecur = False
		else: isRecur = True

		
		if Meeting.objects.filter(pk=_id).count()==0:
			start_dt = datetime.fromtimestamp(int(start[0:10]))
			end_dt = datetime.fromtimestamp(int(start[0:10])) + timedelta(hours=1)
			print(start_dt)
			print(end_dt)
			#print(check_valid_duration(start_dt, end_dt))
			if(not check_valid_duration(request, start_dt, end_dt, _id)):
				print('here')
				return JsonResponse({})
			else:
				print(title, '2')
				meeting = Meeting()
				meeting.title = title
				meeting.start = start_dt
				meeting.end = end_dt
				meeting.allDay = allDay
				meeting.backgroundColor = backgroundColor
				meeting.borderColor = borderColor 
				meeting.room = Room.objects.get(pk=room_id)
				meeting.user = request.user.profile
				meeting.isrecurring = False
				meeting.save()
		else:
			print(title, '3')
			meeting = Meeting.objects.filter(pk=_id).first()

			start_dt = datetime.fromtimestamp(int(start[0:10]))
			end_dt = datetime.fromtimestamp(int(end[0:10]))
			if(not check_valid_duration(request, start_dt, end_dt, _id)):
				print('here2')
				return JsonResponse({})

			if meeting.user.user == request.user:
				meeting.title = title
				meeting.start = start_dt
				meeting.end = end_dt
				meeting.allDay = allDay
				meeting.backgroundColor = backgroundColor
				meeting.borderColor = borderColor 
				meeting.isrecurring = isRecur
				meeting.save()
			else:
				messages.error(request, "Unauthorized operation")
		

		res = model_to_dict(meeting)
	#return HttpResponseRedirect(reverse('room_details', kwargs={'room_id':room_id}))
	return JsonResponse(res)
	#return render(request, 'booking/room.html', context)
	#return redirect(reverse('room_details', kwargs={'room_id':room_id}))




@login_required
def room_delete(request, room_id):
	res = {}
	if request.method == "POST":
		data = request.POST

		_id = -1
		if data.get('id'):
			_id = data.get("id")

		if Meeting.objects.filter(pk=_id).count()!=0:
			meeting = Meeting.objects.filter(pk=_id).first()	
			if meeting.user.user == request.user:	
				meeting.delete()
		

		res = model_to_dict(meeting)
	return JsonResponse(res)


def check_valid_duration(request, start, end, id):
	if Meeting.objects.filter(end__gte=start, start__lt=end, start__gte=start).exclude(id=id).count() > 0:
		print('invalid date - 1')
		messages.error(request, "Date overlap - Can't update event.")
		return False
	elif end <= start:
		messages.error(request, "Invalid date - End can't be before Start")
		print('invalid date - 2')
		return False
	elif start <= datetime.now() - timedelta(minutes=5):
		messages.error(request, "Invalid date - Can not create in past")
		print('invalid date - 3')
		return False
	else:
		return True
