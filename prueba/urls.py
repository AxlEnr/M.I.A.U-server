from django.urls import path
from . import views

urlpatterns = [

    # Pet URLs
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<uuid:pet_id>/', views.pet_detail, name='pet_detail'),

    # StatusHistory URLs
    path('status-history/', views.status_history_list, name='status_history_list'),
    path('status-history/<uuid:history_id>/', views.status_history_detail, name='status_history_detail'),

    # Post URLs
    path('posts/', views.post_list, name='post_list'),
    path('posts/<uuid:post_id>/', views.post_detail, name='post_detail'),

    # ImgsPost URLs
    path('imgs-post/', views.imgs_post_list, name='imgs_post_list'),
    path('imgs-post/<uuid:img_id>/', views.imgs_post_detail, name='imgs_post_detail'),

    # Comments URLs
    path('comments/', views.comments_list, name='comments_list'),
    path('comments/<uuid:comment_id>/', views.comments_detail, name='comments_detail'),

    # Notifications URLs
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<uuid:notification_id>/', views.notifications_detail, name='notifications_detail'),

    # Chats URLs
    path('chats/', views.chats_list, name='chats_list'),
    path('chats/<uuid:chat_id>/', views.chats_detail, name='chats_detail'),

    # AdoptionFilters URLs
    path('adoption-filters/', views.adoption_filters_list, name='adoption_filters_list'),
    path('adoption-filters/<uuid:filter_id>/', views.adoption_filters_detail, name='adoption_filters_detail'),

    # UsersProfile URLs
    path('users-profile/', views.users_profile_list, name='users_profile_list'),
    path('users-profile/<uuid:profile_id>/', views.users_profile_detail, name='users_profile_detail'),

    # Logs URLs
    path('logs/', views.logs_list, name='logs_list'),
    path('logs/<uuid:log_id>/', views.logs_detail, name='logs_detail'),

    # PasswordResets URLs
    path('password-resets/', views.password_resets_list, name='password_resets_list'),
    path('password-resets/<uuid:reset_id>/', views.password_resets_detail, name='password_resets_detail'),

    # EmailVerifications URLs
    path('email-verifications/', views.email_verifications_list, name='email_verifications_list'),
    path('email-verifications/<uuid:verification_id>/', views.email_verifications_detail, name='email_verifications_detail'),
]