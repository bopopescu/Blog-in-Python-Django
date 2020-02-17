from django.shortcuts import render, redirect
from myproject.models import tb_address_book, postRecord, userRecord
from myproject.forms import savePost, LoginPost
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime
import random
import math
import os
#!c:/Python34/python.exe
import cgi
#import mysql.connector
import mysql.connector as conn
from mysql.connector import Error

#view news at home pages
def post_list_page(request,current_page=1):
	#check if session exist then empty or delete items
	if request.session.has_key('fullname'):
		del request.session['fullname']
	#results = tb_address_book.objects.all()
	# or results = tb_address_book.objects.raw(sql)
	
	
	current_page = int(current_page)
	total_record = postRecord.objects.filter(del_status=0).count()
	limit_record = 10
	total_pages = math.ceil(total_record / limit_record)
	#context['total_page_range'] = range(1,total_pages)
	t_offset = (current_page - 1) * limit_record
	previous_page = current_page - 1
	next_page = current_page + 1
	
	if previous_page >= 1:
		has_previous_page = 1
	else:
		has_previous_page = 0
		
	if next_page <= total_pages:
		has_next_page = 1
	else:
		has_next_page = 0
	
	sql = ("select * from postRecord where del_status='{2}' order by id desc limit {0} OFFSET {1} ").format(limit_record,t_offset,0)
	results = postRecord.objects.raw(sql)
	#results = postRecord.objects.all()[2:5]
	
	result_politics = postRecord.objects.filter(postType="Politics",del_status=0).order_by('-id')[:7]
	result_sports = postRecord.objects.filter(postType="Sports",del_status=0).order_by('-id')[:5]
	result_others = postRecord.objects.filter(postType="Others",del_status=0).order_by('-id')[:5]
	
	sherif_top = postRecord.objects.filter(del_status=0).order_by('-id')[:5]
	
	return render(request, "myproject/base.html", {'sherif' : results,'politics_s' : result_politics,'sports_s' : result_sports,'others_s' : result_others,'total_pages' : range(1,total_pages + 1),'total_pages_all' : total_pages,'current_page' : current_page,'has_next_page' : has_next_page,'has_previous_page' : has_previous_page,'previous_page' : previous_page,'next_page' : next_page,'sherif_top' : sherif_top})
	
#read a news	
def read_post(request, post_id):
	if request.session.has_key('fullname'):
		del request.session['fullname']
	result_search = postRecord.objects.filter(postId=post_id).order_by('id')[:1]
	
	result_politics = postRecord.objects.filter(postType="Politics").order_by('-id')[:3]
	result_sports = postRecord.objects.filter(postType="Sports").order_by('-id')[:3]
	result_others = postRecord.objects.filter(postType="Others").order_by('-id')[:3]
	return render(request, "myproject/readPost.html", {'sherif' : result_search, 'politics_s' : result_politics, 'sports_s' : result_sports,'others_s' : result_others })

#searh news by category	
def view_All(request, category, current_page=1):
	if request.session.has_key('fullname'):
		del request.session['fullname']
	#result_search = postRecord.objects.filter(postType=category).order_by('-id').all()
	
	current_page = int(current_page)
	total_record = postRecord.objects.filter(postType=category,del_status=0).count()
	limit_record = 10
	total_pages = math.ceil(total_record / limit_record)
	#context['total_page_range'] = range(1,total_pages)
	t_offset = (current_page - 1) * limit_record
	previous_page = current_page - 1
	next_page = current_page + 1
	
	if previous_page >= 1:
		has_previous_page = 1
	else:
		has_previous_page = 0
		
	if next_page <= total_pages:
		has_next_page = 1
	else:
		has_next_page = 0
	
	sql = ("select * from postRecord where postType = '{2}' and del_status='{3}' order by id desc limit {0} OFFSET {1} ").format(limit_record,t_offset,category,0 )
	results = postRecord.objects.raw(sql)
	
	
	result_politics = postRecord.objects.filter(postType="Politics",del_status=0).order_by('-id')[:5]
	result_sports = postRecord.objects.filter(postType="Sports",del_status=0).order_by('-id')[:5]
	result_others = postRecord.objects.filter(postType="Others",del_status=0).order_by('-id')[:5]
	return render(request, "myproject/base_category.html", {'sherif' : results,'politics_s' : result_politics,'sports_s' : result_sports,'others_s' : result_others,'total_pages' : range(1,total_pages + 1),'total_pages_all' : total_pages,'current_page' : current_page,'has_next_page' : has_next_page,'has_previous_page' : has_previous_page,'previous_page' : previous_page,'next_page' : next_page,'search_category' : category})
	
def new_post(request):
	errorMesg = ""
	if request.session.has_key('fullname'):
		if request.method =='POST':
			form = savePost(request.POST,request.FILES)
			if form.is_valid():
				#author = form.cleaned_data['author']
				#clean_data will put default value in the field if no value is provided from the form u can still accept the values like bellow
				#postTitle = form['postTitle']
				postTitle = form.cleaned_data['postTitle']
				postBody = form.cleaned_data['postBody']
				postType = form.cleaned_data['postType']
				postFile = request.FILES['picture']
				author = request.session['fullname']
				
				#postFile.name	-	the file Name
				#postFile.size	#-	the file size in bytes
				#postFile.content_type	#-	the file content type i.e 'application/pdp' 'image/jpeg'
				#postDate = datetime.datetime.now()#.set('Africa/Lagos').now()
				
				req_size = (postFile.size / 1024)
				if req_size <= 100 and (postFile.content_type == "image/jpeg" or postFile.content_type == "image/jpg") :
					postId = random.randint(2567438945,9826549019)
					postDate = timezone.now()
					newsFolder = ("myproject/static/newsFile/{0}").format(postId)
					os.mkdir(newsFolder)
					New_fileName = postFile.name
					New_fileName_d = New_fileName.split(".")
					
					newsFolder = newsFolder + "/" + "file." + New_fileName_d[1]
					
					#fn = os.path.basename(postFile.filename)
					with open(newsFolder, 'wb+') as dest:
						for chunk in request.FILES['picture'].chunks():
							dest.write(chunk)
					
					post = postRecord(author=author,postTitle=postTitle,postBody=postBody,postType=postType,postDate=postDate,postId=postId,del_status='0')
					post.save()
					errorMesg=""
					#post.author = request.user
					#post.postDate = timezone.set('Africa/Lagos').now()
					#post.save()
					
					#reload the page like a get request
					return HttpResponseRedirect('/myproject/new/blog')
				else:
					errorMesg = "Error: File size must Be 100kb or less and must be jpeg or jpg extension !"
			else:
				errorMesg = "Error: Pleae Provide Correct and Valid Details !"
		else:
			form = savePost()
		#result_politics = postRecord.objects.filter(postType="Politics").order_by('-id')[:1]
		#result_sports = postRecord.objects.filter(postType="Sports").order_by('-id')[:1]
		#result_others = postRecord.objects.filter(postType="Others").order_by('-id')[:1]
		#return render(request, "myproject/new_blog.html", {'form': form, 'politics_s' : result_politics, 'sports_s' : result_sports,'others_s' : result_others, 'errorMesg' : errorMesg })
		return render(request, "myproject/new_blog.html", {'form': form, 'fullname' : request.session['fullname'], 'errorMesg' : errorMesg })
	else:
		return HttpResponseRedirect('/myproject/')
#loging admin
def new_post_home(request):
	errorMesg = ""
	if request.method =='POST':
		formlogin = LoginPost(request.POST)
		if formlogin.is_valid():
			userID = formlogin.cleaned_data['userID']
			userPassword = formlogin.cleaned_data['userPassword']
			verify_d = userRecord.objects.filter(userID=userID,userPassword=userPassword).count()
			if verify_d == 1 :
				errorMesg=""
				verify_data = userRecord.objects.filter(userID=userID,userPassword=userPassword)[:1]
				#load page to post news
				for j in verify_data:
					request.session['fullname'] = j.FullName
				return HttpResponseRedirect('/myproject/new/blog')
			else:
				errorMesg = "Error: Fail To LogIn User Name or Password is incorrect !"
		else:
			errorMesg = "Error: Pleae Provide Correct and Valid Details !"
	else:
		formlogin = LoginPost()
	result_politics = postRecord.objects.filter(postType="Politics").order_by('-id')[:1]
	result_sports = postRecord.objects.filter(postType="Sports").order_by('-id')[:1]
	result_others = postRecord.objects.filter(postType="Others").order_by('-id')[:1]
	return render(request, "myproject/blog_login.html", {'form': formlogin, 'politics_s' : result_politics, 'sports_s' : result_sports,'others_s' : result_others, 'errorMesg' : errorMesg })
	
#staff view your news
def all_my_post(request,current_page=1):
	#check if session exist then empty or delete items
	if request.session.has_key('fullname'):
		#del request.session['fullname']
		#results = tb_address_book.objects.all()
		# or results = tb_address_book.objects.raw(sql)
		
		#results = tb_address_book.objects.filter(id=1).order_by('id').all()
		fullname = request.session['fullname']
		current_page = int(current_page)
		total_record = postRecord.objects.filter(author=fullname,del_status=0).count()
		limit_record = 4
		total_pages = math.ceil(total_record / limit_record)
		#context['total_page_range'] = range(1,total_pages)
		t_offset = (current_page - 1) * limit_record
		previous_page = current_page - 1
		next_page = current_page + 1
		
		if previous_page >= 1:
			has_previous_page = 1
		else:
			has_previous_page = 0
			
		if next_page <= total_pages:
			has_next_page = 1
		else:
			has_next_page = 0
		
		sql = ("select * from postRecord where author = '{2}' and del_status='{3}' order by id desc limit {0} OFFSET {1} ").format(limit_record,t_offset,fullname,0)
		results = postRecord.objects.raw(sql)
		
		return render(request, "myproject/view_edit_post.html", {'sherif' : results, 'fullname' : fullname, 'total_pages' : range(1,total_pages + 1),'total_pages_all' : total_pages,'current_page' : current_page,'has_next_page' : has_next_page,'has_previous_page' : has_previous_page,'previous_page' : previous_page,'next_page' : next_page})
	else:
		return HttpResponseRedirect('/myproject/')
#read a news		
def admin_read_post(request, post_id):
	if request.session.has_key('fullname'):
		fullname = request.session['fullname']
		result_search = postRecord.objects.filter(postId=post_id,author=fullname,del_status=0).order_by('id')[:1]
		
		return render(request, "myproject/adminReadpost.html", {'sherif' : result_search, 'fullname' : fullname })
	else:
		return HttpResponseRedirect('/myproject/')
#edit news admin
def admin_edit_post(request,post_id):
	errorMesg =postId= ""
	if request.session.has_key('fullname'):
		fullname = request.session['fullname']
		if request.method =='POST':
			form = savePost(request.POST,request.FILES)
			if form.is_valid():
				#author = form.cleaned_data['author']
				#clean_data will put default value in the field if no value is provided from the form u can still accept the values like bellow
				#postTitle = form['postTitle']
				postTitle = form.cleaned_data['postTitle']
				postBody = form.cleaned_data['postBody']
				postType = form.cleaned_data['postType']
				postFile = request.FILES['picture']
				author = request.session['fullname']
				postId = request.session['postId']
				#postFile.name	-	the file Name
				#postFile.size	#-	the file size in bytes
				#postFile.content_type	#-	the file content type i.e 'application/pdp' 'image/jpeg'
				#postDate = datetime.datetime.now()#.set('Africa/Lagos').now()
				
				req_size = (postFile.size / 1024)
				if req_size <= 100 and (postFile.content_type == "image/jpeg" or postFile.content_type == "image/jpg") :
					#postId = random.randint(2567438945,9826549019)
					postDate = timezone.now()
					newsFolder = ("myproject/static/newsFile/{0}").format(postId)
					if not os.path.exists(newsFolder):
						os.mkdir(newsFolder)
					New_fileName = postFile.name
					New_fileName_d = New_fileName.split(".")
					#print(os.path.isdir("/home/el"))
					#print(os.path.exists("/home/el/myfile.txt"))
					newsFolder = newsFolder + "/" + "file." + New_fileName_d[1]
					
					#fn = os.path.basename(postFile.filename)
					with open(newsFolder, 'wb+') as dest:
						for chunk in request.FILES['picture'].chunks():
							dest.write(chunk)
					post = postRecord.objects.filter(postId=post_id,author=fullname,del_status=0).update(postTitle=postTitle,postBody=postBody,postType=postType)
					errorMesg=""
					#post.author = request.user
					#post.postDate = timezone.set('Africa/Lagos').now()
					#post.save()
					
					#reload the page like a get request
					return HttpResponseRedirect('/myproject/new/blog/view/1')
				else:
					errorMesg = "Error: File size must Be 100kb or less and must be jpeg or jpg extension !"
			else:
				errorMesg = "Error: Pleae Provide Correct and Valid Details !"
		else:
			request.session['postId'] = post_id
			#retrieve the values 
			b = postRecord.objects.filter(postId=post_id,author=fullname,del_status=0).values_list('postTitle','postType','postBody')[:1]
			for j in b:
				form = savePost(initial={'postTitle':j[0],'postType':j[1],'postBody':j[2]},auto_id=False)
		return render(request, "myproject/update_blog.html", {'form': form, 'fullname' : request.session['fullname'], 'errorMesg' : errorMesg })
	else:
		return HttpResponseRedirect('/myproject/')
#delete news
def admin_delete_post(request, post_id):
	if request.session.has_key('fullname'):
		fullname = request.session['fullname']
		#result_search = postRecord.objects.filter(postId=post_id,author=fullname).delete()[:1]
		result_search = postRecord.objects.filter(postId=post_id,author=fullname).update(del_status='1')
		return redirect(all_my_post, current_page = 1)
	else:
		return HttpResponseRedirect('/myproject/')