#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'yang'

import sys
import json
import demjson
import os
import re
import pymysql
import datetime
import multiprocessing


def dealTimeProblem(date_time):
	if date_time is None:
		date_time="0000-00-00 00:00:00"
	date_time_temp = date_time.replace("T", " ").replace("Z", "")
	date_time_change = date_time_temp.replace("-07:00", "").replace("-08:00", "").replace("+08:00", "")
	if date_time_temp[-6:] == "-07:00":
		temp = datetime.datetime.strptime(date_time_change,"%Y-%m-%d %H:%M:%S")
		time = temp+datetime.timedelta(hours=7)
		time = time.strftime("%Y-%m-%d %H:%M:%S")
	elif date_time_temp[-6:] == "-08:00":
		temp = datetime.datetime.strptime(date_time_change, "%Y-%m-%d %H:%M:%S")
		time = temp + datetime.timedelta(hours=8)
		time = time.strftime("%Y-%m-%d %H:%M:%S")
	elif date_time_temp[-6:] == "+08:00":
		temp = datetime.datetime.strptime(date_time_change, "%Y-%m-%d %H:%M:%S")
		time = temp - datetime.timedelta(hours=8)
		time = time.strftime("%Y-%m-%d %H:%M:%S")
	else:
		time = date_time_temp
	return time


def parseMilestone(repo_id,repo,cur):
	basic_path = "D://Milestones_new"
	for page in range(1,100):
		file_path = basic_path+"//%s//%d.txt"%(repo_id,page)
		try:
			input_file = open(file_path,'rb')
		except Exception as e:
			return
		milestone_content = input_file.read()#.decode()
		#milestone_content = re.sub("u\\","",milestone_content)
		#milestone_content = re.sub("\\\",","\",",milestone_content)
		#milestone_content = re.sub("u'","\'",milestone_content)
		#milestone_content = re.sub("':","\":",milestone_content)
		#milestone_content = re.sub("',","\",",milestone_content)
		#milestone_content = re.sub("'}","\"}",milestone_content)
		#milestone_content = re.sub("None","\"None\"",milestone_content)
		#milestone_content = re.sub("False","\"False\"",milestone_content)
		#milestone_content = re.sub("True","\"True\"",milestone_content)
		#milestone_content = re.sub("'","\"",milestone_content)
		#print(milestone_content)
		#milestones = milestone_content
		#print(type(milestone_content.decode()))
		milestones = json.loads(milestone_content)
		#print(milestones)
		#return
		for milestone in milestones:
			try:
				number = milestone['number']
				state = milestone['state']
			#	try:
			#		if milestone['title'] is None:
			#			title = ""
			#		else:
			#			title = milestone['title'].decode("utf-8").replace("\"","").replace("'","").replace("\\","")
			#	except Exception as e:
			#		title = ""
			#	try:
			#		if milestone['description'] is None:
			#			description = ""
			#		else:
			#			description = milestone['description'].decode("utf-8").replace("\"","").replace("'","").replace("\\","")
			#	except Exception as e:
			#		description = ""
				open_issues = milestone['open_issues']
				closed_issues = milestone['closed_issues']
				created_at = dealTimeProblem(milestone['created_at'])
				closed_at = dealTimeProblem(milestone['closed_at'])
				due_on = dealTimeProblem(milestone['due_on'])
				try:
					query = "insert into milestones_2(repo_id,repo,number,state,open_issues,closed_issues,"\
							"created_at,closed_at,due_on)" \
							" values(%s,\"%s\",%s,\"%s\",%s,%s,\"%s\",\"%s\",\"%s\")"%\
							(repo_id,repo,number,state,open_issues,closed_issues,created_at,closed_at,due_on)
					cur.execute(query)
				except pymysql.Error as e:
					print(e)
			except Exception as e:
				print(e)

def getMilestoneInfo(start,end):
	conn = pymysql.connect(host='localhost',user='root',passwd='',db='milestone_study')
	cur = conn.cursor()
	conn_1 = pymysql.connect(host='localhost',user='root',passwd='',db='milestone_study')
	cur_1 = conn_1.cursor()
	conn_insert = pymysql.connect(host='localhost', user='root', passwd='', db='milestone_study')
	cur_insert = conn_insert.cursor()
	#conn_insert.set_character_set('utf8')
	try:
		query = "select id,repo from repo_selected_6"
		#query = "select repo_id,repo from milestone_study.milestones group by repo having count(*)>99"
		print(query)
		cur.execute(query)
		data = cur.fetchone()
		while data != None:
			print(data[0])
			repo_id = data[0]	
			repo = data[1]
			parseMilestone(repo_id,repo,cur_insert)
			data = cur.fetchone()
	except pymysql.Error as e:
		print("Mysql Error!");
	cur.close()
	conn.close()
	cur_1.close()
	conn_1.close()
	cur_insert.close()
	conn_insert.close()

if __name__ == '__main__':
	progress = []
	for id in range(0, 1):
		progress.append(multiprocessing.Process(target=getMilestoneInfo, args=(id * 3400, (id + 1) * 3400)))
		progress[id].start()

	for id in range(0, 1):
		progress[id].join()