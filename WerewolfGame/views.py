# -*- coding: utf-8 -*-
from django.shortcuts import render

from WerewolfGame.models import Room
import random

all_possible_rooms = range(1000, 10000)
abbr2idx = {'yyj': 0, 'nw': 1, 'cunmin': 2, 'sw': 3, 'hunter': 4, 'lr': 5, 'qbt': 6}
names = [u'预言家', u'女巫', u'村民', u'守卫', u'猎人', u'狼人', u'丘比特']


# 法官创建房间的页面
def start_game(request):
	return render(request, 'start_game.html')


# 普通玩家的页面
def play_game(request):
	return render(request, 'play_game.html')


# CSRF_COOKIE, request.META
def create_room(request):
	# people=6&lr=1&cunmin=2&yyj=1&nv=1&qbt=1&sw=1&hunter=1
	numOfAllPeople = request.POST['people']
	config_msg = u'配置：总共{0}人'.format(numOfAllPeople)

	role_queue = []
	for abbr, idx in abbr2idx.items():
		num = int(request.POST.get(abbr, 0))
		config_msg += u'，{0}{1}'.format(num, names[idx])
		if num:
			role_queue += [str(idx)] * num
	random.shuffle(role_queue)
	role_queue_str = ','.join(role_queue)
	all_room_ids = getAllRoomsId()

	for i in all_possible_rooms:
		if not (i in all_room_ids):
			room_id = i
			if Room.objects.get_or_create(
				room_id = room_id, 
				numOfAllPeople = numOfAllPeople, 
				numOfPlayer = 0, 
				role_queue = role_queue_str,
				config_msg=config_msg):
				return render(request, 'create_success.html', locals())
			
	return render(request, 'create_fail.html')


# 要用一种机制防止客户端多次占用一个角色？
def enter_room(request):
	print(request)
	room_id = request.POST.get('room_id', None)
	if not room_id:
		return render(request, 'play_game.html')
	try:
		room = Room.objects.get(room_id=room_id)
		if room.numOfPlayer >= room.numOfAllPeople:
			return render(request, 'play_game.html')
		room.numOfPlayer += 1
		room.save()
		config_msg = room.config_msg
		role_queue = room.role_queue.split(',')
		index = int(role_queue[room.numOfPlayer-1])
		role_msg = u'你的身份是：{0}'.format(names[index])
		return render(request, 'playing.html', locals())
	except Room.DoesNotExist:
		return render(request, 'play_game.html')


# 后续可以使用token来做验证。
def finish_game(request, room_id):
	try:
		room = Room.objects.get(room_id=room_id)
		room.delete()
		return render(request, 'start_game.html')
	except Room.DoesNotExist:
		return render(request, 'play_game.html')


def about_game(request):
	return render(request, 'help.html')


def getAllRoomsId():
	all_rooms = Room.objects.all()
	all_room_ids = set()
	for room in all_rooms:
		all_room_ids.add(room.room_id)
	return all_room_ids


def genGodId():
	pass