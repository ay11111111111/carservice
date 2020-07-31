from django.contrib.admin import AdminSite

class AutoServiceAdminSite(AdminSite):
    site_header = 'Auto Service Admin'
    site_title = 'Auto Service Admin'

autoserviceadmin = AutoServiceAdminSite(name='autoserviceadmin')
