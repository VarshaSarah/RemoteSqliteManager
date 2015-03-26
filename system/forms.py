__author__ = 'rigel'
from django import forms
from system.models import SystemDetails, DbDetails, QueryDetails


class SystemDetailsForm(forms.ModelForm):

    class Meta:
        model = SystemDetails
        fields = ('hostname', 'password', 'ipaddress')


class DbDetailsForm(forms.ModelForm):

    class Meta:
        model = DbDetails
        fields = ('dbpath',)

class ExecuteSqlForm(forms.ModelForm):

    class Meta:
        model = QueryDetails
        fields = ('query',)


class SearchForm(forms.ModelForm):

    class Meta:
        model = DbDetails
        #fields = ('Database_Name', 'Database_Path')