from django.contrib.admin import AdminSite

class AutoServiceAdminSite(AdminSite):
    site_header = 'Auto Service admin'

autoserviceadmin = AutoServiceAdminSite(name='autoserviceadmin')
