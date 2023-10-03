from django import forms
from todolist_app.models import TaskList

class Taskform(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'done']