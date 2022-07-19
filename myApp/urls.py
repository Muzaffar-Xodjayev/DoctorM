from django.urls import path
from .views import *


urlpatterns = [
    path('',intro, name = 'intro-page'),
    path('home/',homePage, name = 'home-page'),
    path('about/',about, name = 'about-page'),
    path('contact/',contact, name = 'contact-page'),
    path('feedback/',feedbacks, name = 'feedback-page'),
    path('new_f/',new_feed, name = 'new-feedback-page'),
    path('profile/',profile, name = 'profile-page'),
    path('edit_profile/',edit_profile, name = 'edit-profile-page'),
    path('my_questions/',my_questions, name = 'question-page'),
    path('delete_feed/<int:pk>/',feed_delete, name = 'feed-delete-page'),
    path('update_feed/<int:pk>/',feed_update, name = 'feed-update-page'),
    path('check_user/',check_user, name = 'check-user'),
    path('forgot_password/',forgot_password, name = 'forgot-password-page'),
    path('reset_password/',reset_password, name = 'reset-password-page'),
    path('p_detail/<slug:slug>/',prob_detail, name = 'p-detail-page'),
    path('signup/',signup, name = 'signup-page'),
    path('login/',login_page, name = 'login-page'),
    path('logout/',logout_page, name = 'logout-page'),
]