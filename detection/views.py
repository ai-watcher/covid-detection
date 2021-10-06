# Import Libraries
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import DetectForm, UpdateForm
from .models import Detection
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import os, json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image



# HomePage from where you can Login and SignUp
def home(request):
    return render(request, 'detection/home.html')


# Sign Up New User
def signupuser(request):
    if request.method == 'GET':
        return render (request, "detection/signupuser.html", {"forms":UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render (request, "detection/signupuser.html", {"forms":UserCreationForm(), 'error':'Username already in exist'})
        else:
            # Tell the user password did not match
            return render (request, "detection/signupuser.html", {"forms":UserCreationForm(), 'error':'Password did not match not match'})


# Login User
def loginuser(request):
    if request.method == 'GET':
        return render (request, "detection/loginuser.html", {"forms":AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render (request, "detection/loginuser.html", {"forms":AuthenticationForm(), 'error':'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('home')


# Logout the User
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# List all your Detections Entries from where you can update, delete and create new detections
@login_required
def history(request):
    history = Detection.objects.filter(user=request.user).order_by('-created')
    return render (request, "detection/history.html", {'history': history})


# Define Height and Width of Predict Image
img_height = 224
img_width  = 224

# Open and Read Json File
with open('./models/data_classes.json','r') as f:
    labelInfo=f.read()
labelInfo=json.loads(labelInfo)


# Import VGG-16 Trained Model .h5
model=load_model('./models/covid_detection_vgg16.h5')


# Make Covid-19 Detection
# Function 'makedetection' calling function 'user_data'
@login_required
def makedetection(request):
    new_func = user_data(request)
    if request.method == 'GET':
        return render (request, "detection/makedetect.html", {"form" : DetectForm()})
    else:
        if request.method == 'POST':
            try:
                img_url, main_id = new_func
                new_url = '.'+img_url
                img = image.load_img(new_url, target_size=(img_height, img_width))
                x = image.img_to_array(img)

                x=x/255
                x=x.reshape(1,img_height, img_width,3)
                predict=model.predict(x)
                predictedLabel=labelInfo[str(np.argmax(predict[0]))]

                retreive_data = get_object_or_404(Detection, pk=main_id, user=request.user)
                retreive_data.predictions = predictedLabel
                retreive_data.save(update_fields=["predictions"])

                return render(request, "detection/showpredict.html", {'predictedLabel': predictedLabel, 'img_url' : img_url})

            except ValueError:
                return render (request, "detection/makedetect.html", {"forms" : DetectForm(), 'error': 'Bad Data Entry.Try Again'})


# Give User Details for Covid-19 Detection
@login_required
def user_data(request):
    if request.method == 'POST':
        try:
            form = DetectForm(request.POST, request.FILES)
            if form.is_valid():
                print(request.POST)
                newform = form.save(commit=False)
                newform.user = request.user
                newform.save()
                img_url = newform.image.url
                main_id = newform.id
                return img_url, main_id
        except ValueError:
            return render (request, "detection/makedetect.html", {"forms" : DetectForm(), 'error': 'Bad Data Entry.Try Again'})


# Update existing Detection Data
@login_required
def updatedata(request, user_pk):
    user_data = get_object_or_404(Detection, pk=user_pk, user=request.user)
    if request.method == 'GET':
        form = UpdateForm(instance = user_data)
        return render (request, "detection/updatedata.html", {'user': user_data, 'form': form})
    else:
        try:
            form = UpdateForm(request.POST, instance=user_data)
            if form.is_valid():
                form.save()
                return redirect('history')
        except ValueError:
            return render (request, "detection/updatedata.html", {'user': user_data, 'form': form, 'error': 'Bad Info'})


# Delete the Detection Data
@login_required
def deletedata(request, user_pk):
    user_data = get_object_or_404(Detection, pk=user_pk, user=request.user)
    if request.method == 'POST':
        os.remove(user_data.image.path)
        user_data.delete()
        return redirect('history')

#  About Page
@login_required
def about(request):
    if request.method == 'GET':
        return render(request, 'detection/about.html')