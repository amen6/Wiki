from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import markdown
import random
import re



class do(forms.Form):
     title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'title','placeholder':'Title'}),label='')
     text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id':'text','placeholder':'Content'}), label='')

class editing(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id':'text'}), label='')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request , 'encyclopedia/entryNF.html', {
            'title': title
        })

    return render(request , 'encyclopedia/entry.html', {
            'title': markdown.markdown(util.get_entry(title)),
            'name': title
    })

def search(request):
    searched = request.GET.get('q').lower()
    all_entries = util.list_entries()
    files=[filename for filename in all_entries if searched in filename.lower()]
    if util.get_entry(searched) != None:
        return render (request, 'encyclopedia/entry.html',{
            'title': markdown.markdown(util.get_entry(searched))
            })

    if len(files) == 0:
        return render(request, 'encyclopedia/entryNF.html',{
                'title': searched
        })

    elif len(files) > 0:
        pattern = re.compile(searched)
        entries = [pattern for pattern in files]
        title = [title for title in entries]
        return render(request, 'encyclopedia/results.html', {
                    'entries': entries
                })

def create(request):
    if request.method == 'POST':
        form = do(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            if util.get_entry(title):
                messages.error(request, 'Title already exist')
                return render(request, 'encyclopedia/create.html',{
                'do': do
                })
            util.save_entry(title,text)
            return render(request,'encyclopedia/entry.html',{
                'title': markdown.markdown(util.get_entry(title))
                })
        messages.error(request, 'invalid title or text')
        return render(request, 'encyclopedia/create.html',{
        'do': do
        })
    else:
        return render(request, 'encyclopedia/create.html',{
        'do': do
        })

def edit(request, title):
    entry = util.get_entry(title)

    if request.method == 'POST':
        form = editing(request.POST)
        entry = util.get_entry(title)
        if form.is_valid():
            save = form.cleaned_data['text']
            util.save_entry(title,save)
            return render(request, 'encyclopedia/entry.html',{
                'title': markdown.markdown(util.get_entry(title)),
                'name': title
            })

    else:
        if util.get_entry(title) == None:
            return render(request , 'encyclopedia/entryNF.html', {
                'title': title
            })

        else:
            data = util.get_entry(title)
            context = {
                'editing': editing(initial={'text':data}),
                'title': title
            }

            return render(request, 'encyclopedia/edit.html', context)

def random_page(request):
    all_names = util.list_entries()
    random_number = random.randint(0, len(all_names) - 1)
    title = all_names[random_number]
    page = markdown.markdown(util.get_entry(title))

    return render(request, 'encyclopedia/entry.html', {
            'title': page,
            'name': title
    })
