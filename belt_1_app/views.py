from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        # print(request.POST)

        errors = User.objects.validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            hashed_pw = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()

            this_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=hashed_pw,
            )
            request.session['user_id'] = this_user.id
            return redirect('/')
    return redirect('/')


def login(request):
    if request.method == "POST":
        this_user = User.objects.filter(email=request.POST['email'])
        if len(this_user) == 1:  # Filter return a list on objects that exist in our DB
            this_user = this_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                # storing the user identity in our sessions here
                request.session['user_id'] = this_user.id
                return redirect('/welcome')

        messages.error(request, "Email or Password not found")

    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def dashboard(request):

    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(
            request, "You need to register or log in if you already have an account!")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_jobs': Job.objects.all(),
        }
        # messages.success(request, "Successfully Logged in!")
    return render(request, 'dashboard.html', context)


def add_job(request):

    return render(request, 'add_job_page.html')


def add(request):
    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(
            request, "You need to register or log in if you already have an account!")
        return redirect('/')

    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addJob')
        else:
            print(request.POST)
            this_user = User.objects.get(id=request.session['user_id'])

            job_object = Job.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                location=request.POST['location'],
                user=this_user,
            )

    return redirect('/welcome')


def view(request, id):
    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(
            request, "You need to register or log in if you already have an account!")
        return redirect('/')
    job_with_id = Job.objects.filter(id=id)
    if len(job_with_id) > 0:
        job_object = job_with_id[0]
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'job': Job.objects.get(id=job_object.id),
        }
        return render(request, 'view_job.html', context)
    else:
        messages.error(request, "Job not found")
        return redirect('/welcome')


def edit(request, id):
    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(
            request, "You need to register or log in if you already have an account!")
        return redirect('/')
    job_with_id = Job.objects.filter(id=id)
    if len(job_with_id) > 0:
        job_object = job_with_id[0]
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'job': Job.objects.get(id=job_object.id),
        }
        return render(request, 'edit_page.html', context)
    else:
        messages.error(request, "Job not found")
        return redirect('/welcome')


def make_edit(request, id):  # add validations
    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(request, "You need to Login on create an account!")
        return redirect('/')
    if request.method == 'POST':
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                    messages.error(request, value)
        else:
            job_with_id = Job.objects.filter(id=id)
            if len(job_with_id) > 0:
                job_object = job_with_id[0]
                # print(request.POST)
                this_job = Job.objects.get(id=job_object.id)
                # Validating to prevent the logged in user from editting other peoples job *****
                if this_job.user.id == request.session['user_id']:
                    this_job.title = request.POST['title']
                    this_job.description = request.POST['description']
                    this_job.location = request.POST['location']
                    this_job.save()
    return redirect('/welcome')


def delete(request, id):

    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(request, "You need to Login on create an account!")
        return redirect('/')

    if request.method == 'POST':

        job_with_id = Job.objects.filter(id=id)
        if len(job_with_id) > 0:
            job_object = job_with_id[0]
            this_user = User.objects.get(id= request.session['user_id']) # logged in user object
            job_to_be_deleted = Job.objects.get(id=job_object.id)
            # Validating to prevent the logged in user from deleting other peoples Job *****
            # only users who created the Job can delete
            if job_object.user.id == request.session['user_id'] or job_object in this_user.user_jobs.all():
                job_to_be_deleted.delete()      # Checking if that job exists in the users list of jobs even if someone else created it
    return redirect('/welcome')


def add_job_to_user(request, id):
    if 'user_id' not in request.session:  # making sure only logged in users are using the app
        messages.error(request, "You need to Login on create an account!")
        return redirect('/')

    if request.method == "POST":
        job_with_id = Job.objects.filter(id =id)
        if len(job_with_id) > 0:
            job_object = job_with_id[0]

            user_adding_job = User.objects.get(id=request.session['user_id'])

            user_adding_job.user_jobs.add(job_object)
            
            #favJob.user_job.add(user_adding_job)
        return redirect('/welcome')

