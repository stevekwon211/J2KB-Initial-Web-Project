from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.firstpage, name='first_page'),
    path('homepage', views.homepage, name='homepage'),
    path('aboutus', views.about_us, name='aboutus'),
    path('contactus', views.contact_us, name='contactus'),
    path('photopage', views.photopage, name='photopage'),
    path('memo', views.memo, name='memo'),
    path('todolist', views.todolist, name='todolist'),
    path('generalforum', views.post_list, name='generalforum'),

    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
]
