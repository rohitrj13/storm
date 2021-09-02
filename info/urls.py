from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('listen/',views.listen,name='listen'),
    path('base2/phase2',views.phase2,name='phase2'),
    path('listened/<int:stage>',views.listened,name='listened'),
]