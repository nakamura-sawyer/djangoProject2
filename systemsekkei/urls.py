from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('homes', views.homes, name='homes'),
    path('home/kanrisya/', views.home_kanrisya, name='home_kanrisya'),
    path('juugyouin', views.juugyouin, name='juugyouin'),
    path('register_employee/', views.register_employee, name='register_employee'),
    path('register_success/', views.register_success, name='register_success'),
    path('TBL', views.TBL, name='TBL'),
    path('recode', views.recode, name='recode'),
    path('search_address/', views.search_address, name='search_address'),
    path('jusyo', views.jusyo, name='jusyo'),
    path('update_name', views.update_name, name='update_name'),
    path('name', views.name, name='name'),
    path('home/uketuke/', views.home_uketuke, name='home_uketuke'),
    path('update_password', views.update_password, name='update_password'),
    path('joho', views.joho, name='joho'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('register_success2/', views.register_success2, name='register_success2'),
    path('touroku', views.touroku, name='touroku'),
    path('update_hoken/', views.update_hoken, name='update_hoken'),
    path('update_success/', views.update_success, name='update_success'),
    path('kanri', views.kanri, name='kanri'),
    path('search_name/', views.search_name, name='search_name'),
    path('kensaku', views.kensaku, name='kensaku'),
    path('home/doctor/', views.home_doctor, name='home_doctor'),
    path('kensaku2', views.kensaku2, name='kensaku2'),

    path('shiji', views.shiji, name='shiji'),

    path('sakujo', views.sakujo, name='sakujo'),

    path('kakutei', views.kakutei, name='kakutei'),

    path('rireki', views.rireki, name='rireki')
]