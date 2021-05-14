from django.shortcuts import render


def index(request):
    return render(request, 'attendance/index.html')


def room(request, room_name):
    return render(request, 'attendance/room.html', {
        'room_name': room_name
    })
