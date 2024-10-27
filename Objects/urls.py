from django.urls import path
from Objects import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.main,name='main'),
    path('<int:id>/',views.object_instance,name='object'),
    path('record/',views.record,name='record')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)



