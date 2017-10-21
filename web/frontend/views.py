from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import urllib.request
import urllib.parse
import json
from .forms import *
from django.views.decorators.csrf import csrf_exempt

__EXP_URL = 'http://exp-api:8000/api/v1/'

def index(request):
	req = urllib.request.Request(__EXP_URL+'home')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	return render(request, 'frontend/index.html', resp)

def book_detail(request, book_id):
	req = urllib.request.Request(__EXP_URL +'book/'+book_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if resp["success"] == True:
		context = {
			"title": resp["result"]["fields"]["title"],
			"year": resp["result"]["fields"]["year_published"],
			"rating": resp["result"]["fields"]["rating"],
		}
		req_2 = urllib.request.Request('http://exp-api:8000/api/v1/author/'+str(resp["result"]["fields"]["author"]))
		resp_json_2 = urllib.request.urlopen(req_2).read().decode('utf-8')
		resp_2 = json.loads(resp_json_2)
		context["author_first"] = resp_2["result"]["fields"]["first_name"]
		context["author_last"] = resp_2["result"]["fields"]["last_name"]
		return render(request, 'frontend/detail.html', context)
	else:
		return redirect('/notfound')

def not_found(request):
	return render(request, 'frontend/404.html', {})

@csrf_exempt
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			post_data = {
				'username': form.cleaned_data['username'],
				'password': form.cleaned_data['password'],
				'first_name': form.cleaned_data['fname'],
				'last_name': form.cleaned_data['lname'],
			}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request(__EXP_URL+'signup', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			if resp_json['success'] == True:
				return HttpResponseRedirect('/index')
			else:
				return render(request, 'frontend/signup.html', {'form': form, 'msg': "Error occured",})
	else:
		form = SignupForm()
	return render(request, 'frontend/signup.html', {'form': form})

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			return
	else:
		form = LoginForm()
	return render(request, 'frontend/signup.html', {'form': form})