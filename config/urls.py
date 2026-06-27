from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from core import frontend_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', frontend_views.register, name='register'),
    path('register/done/', frontend_views.register_done, name='register_done'),
    path('', frontend_views.dashboard, name='dashboard'),
    path('courses/', frontend_views.course_list, name='course_list'),
    path('courses/<uuid:pk>/', frontend_views.course_detail, name='course_detail'),
    path('assignments/<uuid:pk>/', frontend_views.assignment_detail, name='assignment_detail')
]