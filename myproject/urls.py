#import django url file -  importing Django's function url
from django.conf.urls import url

#import view  - view is where we define our diferent views
from . import views

urlpatterns = [
	#view group news with a pagination
	url(r'^viewAll/(?P<category>\w+)/(?P<current_page>\d+)/$', views.view_All, name='view_All'),
	
	#read news
	url(r'^readNews/(\d+)/$', views.read_post, name='read_post'),
	#url(r'^new/(\w+)$', views.new_post, name='new_post'),
	
	#to create new post admin login 
	url(r'^new$', views.new_post_home, name='new_post_home'),
	
	#to create new post admin home page 
	url(r'^new/blog$', views.new_post, name='new_post'),
	
	#staff admin view your post - edit - delete - view
	url(r'^new/blog/view/(?P<current_page>\d+)/$', views.all_my_post, name='all_my_post'),
	
	#staff admin view your post - view(read news)
	url(r'^new/blog/view/read/(?P<post_id>\d+)/$', views.admin_read_post, name='admin_read_post'),
	
	#staff admin view your post - edit(edit news)
	url(r'^new/blog/view/redit/(?P<post_id>\d+)/$', views.admin_edit_post, name='admin_edit_post'),
	
	#staff admin delete your post - delete(remove news)
	url(r'^new/blog/view/redel/(?P<post_id>\d+)/$', views.admin_delete_post, name='admin_delete_post'),
	
	#home page
	url(r'^$', views.post_list_page, name='post_list_page'),
	#pagination of home page
	url(r'^(?P<current_page>\d+)/$', views.post_list_page, name='post_list_page'),
	
	#url(r'^viewmore/(\d+)/$', views.post_list_page, name='post_list_page'),
]