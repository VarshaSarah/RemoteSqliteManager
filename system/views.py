from django.shortcuts import render_to_response
from system.models import SystemDetails, DbDetails
from system.forms import SystemDetailsForm, DbDetailsForm, ExecuteSqlForm, SearchForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from system.ssh import connect_remote, ftp_to_sys, searchpathfunc, copy_from_rem, commit_to_rem
from paramiko import SSHClient, SSHConfig, AutoAddPolicy, SSHException
from django import forms
from system.firequery import execQuery, execquery_onload
from django.db import connection
# Create your views here.
import json
import os
import shutil
import time

ssh = SSHClient()
modelDB = DbDetails()
formDB = SearchForm()

def hello(request):
      return render_to_response('hello.html')

def login(request):

    if request.POST:
        form_sys = SystemDetailsForm(request.POST)
        if form_sys.is_valid():
            global syst
            syst = request.POST

            connect_remote(ssh, syst)  #persistent ssh connection call to func in system/ssh.py

            form_db = DbDetailsForm()
            args = {}
            args['form_db'] = form_db
            name = form_sys["hostname"].value()
            
            args['user'] = name
            args.update(csrf(request))
            return render_to_response('searchdb.html', args)
    else:
        form_sys = SystemDetailsForm()
        form_sys.fields['password'].widget = forms.PasswordInput()

    args = {}
    args['form_sys'] = form_sys
    args.update(csrf(request))
    return render_to_response('login.html', args)


def validatesearch(request):  #input path or dbname

    #InputParams = request.POST
    Database_path_string = request.POST["dbpath"]

    if Database_path_string.find("/") != -1:
        print("\n slash found ")
        #give path to copy func
        #copy(request, Database_path_string)  #copy(request, dbstring)
        #return render_to_response("index.html")

        #if request.POST:
            #global formDB
            #formDB = request.POST
        global pathInLocal
        pathInLocal = ftp_to_sys(ssh, Database_path_string)


        form = ExecuteSqlForm()
        args = {}

        args['form_sql'] = form
        args.update(csrf(request))
        return render_to_response("executestring.html", args)


    else:
        list_of_paths = dict()
        print("\n ---> start search")
        list_of_paths = searchpathfunc(ssh, request.POST)
        print("\n ---> end search\n")
        print(list_of_paths)    #done --> cross check here*********************************

        args = {}
        args['form1'] = formDB
        print("before json")
        args['list_of_paths'] = json.dumps(list_of_paths)
        args.update(csrf(request))
        print("\nreached choosedb.html.. should display radio buttons")
        return render_to_response("choosedb.html", args)


def copy(request, anystring=None):
    list_of_rec =dict()
    print("#########\n")
    #print(request)
    print("#########\n")
    print(anystring)
    print("^^^^^^^^^^^\n")
    #if anystring[0] == "/":
        #pathInRem = anystring
    #else:
    global pathInRem
    pathInRem = "/" + anystring

    global pathInLocal, pathInRem
    pathInLocal = ftp_to_sys(ssh, pathInRem)

    if request.POST:
        global formDB
        formDB = request.POST
    form = ExecuteSqlForm()
    list_of_rec = execquery_onload(pathInLocal)
    args = {}

    args['form_sql'] = form
    args['table_records'] = json.dumps(list_of_rec)
    args.update(csrf(request))
    return render_to_response("executestring.html", args)


def validsearch(request, anystring=None):                  #to be removed
    print("#########\n")
    print(request)
    print("#########\n")
    print(anystring)
    print("^^^^^^^^^^^\n")
    pathInRem = "/" + anystring
    print("^^^^^^^^^^^\n")
    print(pathInRem)
    print("^^^^^^^^^^^\n")
    copy(request, pathInRem)
    return render_to_response("index.html")


def execute(request):
    list_of_records = dict()
    if request.POST:
        form_sql = ExecuteSqlForm(request.POST)

        if form_sql.is_valid():
            model = request.POST
            print(request.POST)
            global formDB
            print("\n db path is ----> ")
            print(formDB['dbpath'])
            str = form_sql['query'].value()
            list_of_records = execQuery(pathInLocal, str)
            print("fetched records are \n")
            print(list_of_records)

            args = {}
            args['form_sql'] = form_sql
            args['table_records'] = json.dumps(list_of_records)
            args.update(csrf(request))
            return render_to_response('executestring.html', args)
    else:
        form_sql = ExecuteSqlForm()

    args = {}
    args['form_sql'] = form_sql
    args.update(csrf(request))
    return render_to_response('executestring.html', args)


def commit(request):
    global pathInLocal, pathInRem

    print("hereeeeeeeee")
    global syst
    ipadd = syst['ipaddress']
    #check_instance(ipadd, pathInRem)
    print("\n^^^^^ RREmote path : " + pathInRem)
    navigate_to_instance(ipadd, pathInRem)

    form_db = DbDetailsForm()
    args = {}
    args['form_db'] = form_db
    args['user'] = "user"
    args.update(csrf(request))
    return render_to_response('searchdb.html', args)


def rollback(request):

    global pathInLocal, pathInRem
    print("\n--------> ")
    print(pathInRem)
    copy_from_rem(ssh, pathInRem, pathInLocal)

    form_db = DbDetailsForm()
    args = {}
    args['form_db'] = form_db
    args['user'] = "user"
    args.update(csrf(request))
    return render_to_response('searchdb.html', args)







def check_instance(ipadd, main_db_loc):

    temp_db_loc = main_db_loc.split('/')
    length = len(temp_db_loc)
    temp_db_loc.append(temp_db_loc[length-1])
    temp_db_loc[length-1] = ipadd

    inst_db_loc = "/".join(temp_db_loc)
    #for obj in temp_db_loc:
    #	inst_db_loc += '/'
    #	inst_db_loc += obj

    print("\n instance db loc in check instance :  " + inst_db_loc)
    if(os.path.isfile(inst_db_loc)):
        curr_path = inst_db_loc
        print ("%s already instantiated " %curr_path)
    else:
        curr_path = main_db_loc
        print ("%s using main db " %curr_path)


def navigate_to_instance(ipadd, main_db_loc):

    ######-------generating hostname dir name #########
    print("\n????? remote path : " + main_db_loc)
    temp_db_loc = main_db_loc.split('/')
    length = len(temp_db_loc)
    temp_db_loc.append(temp_db_loc[-1])
    temp_db_loc[-2] = ipadd
    print("\n???????temp db : %s"%temp_db_loc)

    inst_db_loc = ""

    #for index in (range(length-1)):
    #    inst_db_loc += '/'
    #    inst_db_loc += temp_db_loc[index+1]
    inst_db_loc = "/".join(temp_db_loc)
    print("\n???????inst in navigate  : %s"%inst_db_loc)
    commit_to_rem(ssh, inst_db_loc, ipadd, pathInRem, pathInLocal)

