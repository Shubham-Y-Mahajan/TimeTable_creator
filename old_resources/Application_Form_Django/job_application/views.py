from django.shortcuts import render
from . forms import ApplicationForm
from . models import Form
from django.contrib import messages
# messages is a module that allows you to display messages dynamically
from django.core.mail import EmailMessage
def index(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["FirstName"]
            # form.cleaned_data is a dictionary created by django , we want the value associated with key 'FirstName'
            # note the dictionary keys are taken from name field in forms of .html file

            last_name = form.cleaned_data["LastName"]
            email = form.cleaned_data["Email"]
            date = form.cleaned_data["Date"]
            occupation = form.cleaned_data["occupation"]

            Form.objects.create(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                date=date,
                                occupation=occupation,
                                )

            message_body =  f"Thank you for your submission ,{first_name}." \
                      f"Here are your submitted data:\n{first_name}\n{last_name}\n" \
                      f"{date}\n{occupation}\n Thank You!"

            subject="Form Submission Confirmation"
            email_message = EmailMessage(subject,message_body,to=[email])
            email_message.send()


            messages.success(request,"Form submitted successfully!")



    return render(request,"index.html")
# if you dont put request argument then it raises error

def about(request):
    return render(request,"about.html")