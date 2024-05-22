from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AddPostView,EditProfilePageView,CreateProfilePageView,PasswordsChangeView,FriendView,AddCommentView,DeletePostView,UpdatePostView,ShowProfilePageView,AddRecommondationView,RecommandationsListView,AddTransportView,TransportListView,AddLogementView,LogementListView,AddEvenementView,EvenementListView,AddEventSocialView,EventSocialListView,AddEventClubView,EventClubListView,AddStageView,StageListView,AddReservationView,AddTransportReservationView,create_post_and_stage,send_private_message,private_messages,followers_list,user_profile
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home,name='home'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('signup/', views.signup,name='signup'),
    path('<int:pk>/edit_profile_page/',EditProfilePageView.as_view(),name='edit_profile_page'),


    path('<int:pk>/profile/',ShowProfilePageView.as_view(),name='show_profile_page'),
    path('create_profile_page/',CreateProfilePageView.as_view(),name='create_profile_page'),
    path('add_post/',AddPostView.as_view(),name="add_post"),
    path('create_post_and_stage/',views.create_post_and_stage,name="create_post_and_stage"),

    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('add_recommondation/',AddRecommondationView.as_view(),name="add_recommondation"),
     path('recommandations_list/', RecommandationsListView.as_view(), name='recommandations_list'),

    
     path('add_transport/',AddTransportView.as_view(),name="add_transport"),
       path('transport_list/', TransportListView.as_view(), name='transport_list'),

 path('add_reservationt/<int:transport_id>/', views.AddTransportReservationView, name='add_reservationt'),

 path('add_reservationl/<int:logement_id>/', views.AddLogementReservationView, name='add_reservationl'),
 
 path('add_reservations/<int:stage_id>/', views.AddStageReservationView, name='add_reservations'),

    path('add_logement/', AddLogementView.as_view(), name="add_logement"),
    path('logement_list/', LogementListView.as_view(), name='logement_list'),

   
  path('add_stage/', AddStageView.as_view(), name='add_stage'),
    path('stage_list/', StageListView.as_view(), name='stage_list'),


      path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),

    

  



    path('add_evenement/',AddEvenementView.as_view(),name="add_evenement"),
    path('evenement_list/', EvenementListView.as_view(), name='evenement_list'),

    
    path('add_eventSocial/',AddEventSocialView.as_view(),name="add_eventSocial"),
    path('eventSocial_list/', EventSocialListView.as_view(), name='eventSocial_list'),

 path('add_eventClub/',AddEventClubView.as_view(),name="add_eventClub"),
    path('eventClub_list/', EventClubListView.as_view(), name='eventClub_list'),


    path('password/',PasswordsChangeView.as_view(template_name='base/change-password.html')),
    path('password_success/', views.password_success, name="password_success"),
    path('friends/',FriendView.as_view(),name='friends'),
    path('post/<int:pk>/comment/',AddCommentView.as_view(),name='add_comment'),
    path('like-post',views.like_post,name='like-post'),
    path('post/<int:pk>/remove',DeletePostView.as_view(),name="delete_post"),
    #path('post/edit/<int:pk>',UpdatePostView.as_view(),name="update_post"),
     path('update_post/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('search',views.search,name='search'),
     path('searchs/', views.searchstage, name='searchs'),

      path('searchl/', views.LogementListView.as_view(), name='searchl'),

    path('logements/', LogementListView.as_view(), name='logement_list'),

    path('follow',views.follow,name='follow'),


     path('user_likes/', views.user_likes, name='user_likes'),

     path('add_reservation/<int:event_id>/', AddReservationView, name='add_reservation'),
     path('add_transport_reservation/<int:transport_id>/', AddTransportReservationView, name='add_transport_reservation'),

    path('send/', send_private_message, name='send_private_message'),
    path('messages/', private_messages, name='private_messages'),
    path('followers/', followers_list, name='followers_list'),
     path('profile/<str:username>/', user_profile, name='user_profile'),

     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)