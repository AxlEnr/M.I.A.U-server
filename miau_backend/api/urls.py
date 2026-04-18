from django.urls import path, include

urlpatterns = [
    path('adoptionfilters/', include('adoptionfilters.urls')),
    path('chats/', include('chats.urls')),
    path('codeqr/', include('codeQR.urls')),
    path('comments/', include('comments.urls')),
    path('emailverification/', include('emailverification.urls')),
    path('imgspost/', include('imgspost.urls')),
    path('logs/', include('logs.urls')),
    path('notifications/', include('notifications.urls')),
    path('passwordresets/', include('passwordresets.urls')),
    path('posts/', include('post.urls')),
    path('users/', include('user.urls')),
    path('pets/', include('pet.urls')),
    path('statushistory/', include('statushistory.urls')),
]
