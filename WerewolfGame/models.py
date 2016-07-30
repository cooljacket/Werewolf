# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Room(models.Model):
	room_id = models.SmallIntegerField(verbose_name='房间id', primary_key=True)
	numOfAllPeople = models.SmallIntegerField(verbose_name='村落人数')
	numOfPlayer = models.SmallIntegerField(verbose_name='进入房间的玩家人数')
	role_queue = models.CharField(verbose_name='角色队列', max_length=100)
	config_msg = models.CharField(verbose_name='配置信息', max_length=100)
	god_token = models.CharField(verbose_name='法官的token', max_length=64)

	def __str__(self):
		return 'room_id: {0}'.format(self.room_id)

	class Meta:
		verbose_name_plural = '游戏房间'