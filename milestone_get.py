# -*- coding: utf-8 -*-
from gittle import Gittle
from datetime import datetime ,date
import MySQLdb
from git import Repo
import time
import cStringIO
import json
import os
import pycurl
import redis
import MySQLdb.cursors
db1 = MySQLdb.connect(host="localhost",user="root",passwd="",db="milestone_study",charset='utf8',cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=3600)
#db1 = MySQLdb.connect(host="127.0.0.1",user="influx",passwd="influx1234",db="gitlab",charset='utf8' ,cursorclass=MySQLdb.cursors.DictCursor,connect_timeout=3600)
db1.autocommit(1)
db1.set_character_set('utf8')
ver=db1.cursor()
r = redis.Redis(host="localhost",port=6379,db=0)
format_issues="%s/milestones?page=%s&&access_token=%s&&per_page=100&&state=all"
# select_time="select updated from project_issues where url=%s"
# updated_time="update project_issues set updated=%s where user_url=%s and repo_url=%s"
# updated_repos="update project_issues set error_repo=1 where user_url=%s and repo_url=%s"
# replace_issues="insert ignore  into issues(user_url,repo_url,pr_id,main,updated,number,tag) values(%s,%s,%s,%s,%s,%s,%s)"
# replace_pr="insert ignore into pull_request(user_url,repo_url,pr_id,main,updated,number,tag) values(%s,%s,%s,%s,%s,%s,%s)"

# number_null = 0
def issues_get():
    name=r.rpop("repo_selected_6")
    id = name.split(" ")[1]
 
    #print name
    if(name==None):
        pass
    else:
        url = str(name).split(" ")[0]
        # tag = int(str(name).split(" ")[1])
        print url

        # user_url=url.split(" ")[0]
        # repo_url=url.split(" ")[1]
        # pr_id=url.split(" ")[2]
        # peo_url = url.split(" ")[3]
        page_num=1
        issues_tag = 1
        # ver.execute(select_time,url)
        while (True):
            #print 'abc'
            access_token = r.rpop("access_token")
            it_url=format_issues%(url,page_num,access_token)
            #print it_url
            it_c = pycurl.Curl()
            it_c.setopt(it_c.URL, it_url)
            it_b = cStringIO.StringIO()
            it_c.setopt(it_c.WRITEFUNCTION, it_b.write)
            it_c.setopt(it_c.CONNECTTIMEOUT, 30)
            it_c.setopt(it_c.TIMEOUT, 40)
            it_c.setopt(it_c.SSL_VERIFYPEER, 0)
            it_c.setopt(it_c.SSL_VERIFYHOST, 0)
            it_c.setopt(it_c.FOLLOWLOCATION, 5)
            #print it_url
            try:
                it_c.perform()
            except Exception as ee:
                print ee

                pass
            else:
                it_html = it_b.getvalue().decode("utf-8", "ignore")
                #print it_html
                it_hhh = json.loads(it_html)
                #it_hhh = it_html

                it_b.close()
                if(type(it_hhh)==dict):
                    #print it_hhh
                    if (it_hhh['message'] == 'Not Found'):
                        # ver.execute(updated_repos,(user_url,repo_url))
                        issues_tag=0
                   # print "123321"
                elif(type(it_hhh)==list):
                    if(len(it_hhh)==0):
                        # number_null = number_null+1
                        issues_tag=0
                    else:
                        if (len(it_hhh) < 100):
                            issues_tag = 0
                        #i=1
                        #print url.split("/")[4]
                        #print url.split("/")[5]
                        #fold_name1 = url.split("/")[4]
                        #fold_name2 = url.split("/")[5]
                        fold_name_3 = "D://Milestones_new//"+id#fold_name1 + '&' + fold_name2
                        #print fold_name_3
                        if not os.path.exists(fold_name_3):
                            os.mkdir(fold_name_3)
                        fw = open("%s//%s.txt"%(fold_name_3,page_num),"wb")
                        it_hhh = json.dumps(it_hhh) 
                        fw.write(str(it_hhh))
                        #for it_ii in it_hhh:

                        #    it_ii = json.dumps(it_ii) 
                            #ver.execute("insert into api_ruby_milestone (url, api_milestone) VALUES (%s,%s)",(str(url),str(it_ii)))
                            #print 'sb'
                            #print it_ii
                         #   print(i)
                            #print url.split("/")[4]
                            #print url.split("/")[5]
                            #fold_name1 = url.split("/")[4]
                            #fold_name2 = url.split("/")[5]
                         #   fold_name_4 = str(i)

                         #   print(fold_name_4)
                            #fw = open("%s//%s.txt"%(fold_name_3,fold_name_4),"wb")
                            #fw.write(str(it_ii))
                            #i = i + 1
                            #fold_name = fold_name1 + '&' + fold_name2 +'_' + str(i)
                            #print fold_name
                            #fw = open("txt_api_milestones\%s.txt"%(fold_name,),"wb")
                            #fw.write(str(it_ii))
                            #i = i + 1

                            # try:
                            #     it_ii['number']
                            # except Exception as e :
                            #     pass
                            # else:
                            #     try:
                            #         it_ii['pull_request']
                            #     except Exception as ee:
                            #
                            #         ver.execute(replace_issues,(user_url,repo_url,pr_id,str(it_ii),it_ii['updated_at'],it_ii['number'],peo_url))
                            #     else:
                            #         ver.execute(replace_pr,(user_url,repo_url,pr_id,str(it_ii),it_ii['updated_at'],it_ii['number'],peo_url))
                            #     print 'good'
                    # ver.execute(updated_time,(it_hhh[len(it_hhh)-1]['updated_at'],user_url,repo_url))
                    page_num += 1
                if(issues_tag==0):
                    break
       
        ver.execute("update repo_selected_6 set tag=2 where id=%s",(id,))

if __name__ == "__main__":

    # name = r.rpop("ruby_projects_milestones")
    while(True):
        try:
            issues_get()
        except WindowsError:
            issues_get()
        time.sleep(3)
    # print number_null
