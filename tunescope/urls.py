# tunescope/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin and Accounts URLs
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # For login, logout, etc.
    path('accounts/', include('accounts.urls')),           # For your custom signup

    # Main pages linked directly to templates
 
    path('', TemplateView.as_view(template_name='w.html'), name='w_page'),
    path('analyzer/', TemplateView.as_view(template_name='analyzer.html'), name='analyzer'),
    path('metronome/', TemplateView.as_view(template_name='metronome.html'), name='metronome'),
    path('pitch/', TemplateView.as_view(template_name='pitch.html'), name='pitch'),
    path('record/', TemplateView.as_view(template_name='record.html'), name='record'),
    path('scale/', TemplateView.as_view(template_name='scale.html'), name='scale'),
    path('virerecord/', TemplateView.as_view(template_name='virerecord.html'), name='virerecord'),
    path('tutorial/', TemplateView.as_view(template_name='tut.html'), name='tut'),
    path('tuner/', TemplateView.as_view(template_name='tuner.html'), name='tuner'),
    
    # The signup.html is likely handled by your 'accounts.urls', but if not, you can add it here too:
    # path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
]