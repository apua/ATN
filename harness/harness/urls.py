"""harness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from autotest.api import execute_test, monitor_test_execution, list_suts, detail_sut, reserve_sut, TaasView, test_report_page, use_sut

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-reporting/<uuid:te_id>/<name>.html', test_report_page),
    path('test-execution/', execute_test),
    path('test-execution/<uuid:rq_jid>/console/', monitor_test_execution),
    path('sut/', list_suts),
    path('sut/<uuid:uuid>/', detail_sut),
    path('sut/<uuid:uuid>/reserve/', reserve_sut),
    path('sut/<uuid:uuid>/use/', use_sut),
    path('taas/', TaasView.as_view()),
]
