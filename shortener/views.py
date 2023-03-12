from django.shortcuts import render, redirect
from shortener.models import Users

# Create your views here.
def index(request):
    user = Users.objects.filter(username="admin").first()
    # user = Users.objects.get(username="admin")
    email = user.email if user else "Anonymous User!"
    print(email)
    print(request.user.is_authenticated)
    # if request.user.is_authenticated is False:
    #     email = "Anonymous User!"
    # print(email)
    return render(request, "base.html", {"welcome_msg" : f"Hello {email}"})

def redirect_test(requset):
    print("Go Redirect")
    return redirect("index")


