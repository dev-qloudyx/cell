from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView
from .models import Client
from .forms import ClientForm, MainForm
from django.urls import reverse_lazy 
from django.core.mail import send_mail, get_connection
from django.core.mail.message import EmailMessage
# Create your views here.



class MainForm(FormView):
    form_class = MainForm
    template_name = "demo/simulator.html"
    success_url = 'success/'


    def form_valid(self, form):
        
        options =[]
        choicelist = self.request.POST
        for item in choicelist:
            options.extend(choicelist.getlist(item)) 
        # print(options)

        vdt = 0
        def check_solute(vdt):
            if "0.15" in options:
                check_cool(vdt)
            elif "0.10" in options:
                vdt +=2
                check_cool(vdt)
            elif "0.05" in options:
                vdt +=4
                check_cool(vdt)
            elif "0.01" in options:
                vdt +=6
                check_cool(vdt)

        def check_cool(vdt):
            if "1" in options:
                print(vdt)
                self.request.session['vidnum'] = vdt
            else:
                vdt +=1
                print(vdt)
                self.request.session['vidnum'] = vdt
                 
        if "CELL" in options:
            vdt +=1
            check_solute(vdt)         
        else:
            vdt +=9
            check_solute(vdt)


        # video = 0
        # if "CELL" in options:
        #     video += 1
        #     if "0.15" in options:
        #         if "1" in options:
        #             print("1")
        #             print(video)
        #         else:
        #             print("2")
        #     elif "0.10" in options:
        #         if "1" in options:
        #             print("3")
        #         else:
        #             print("4")
        #     elif "0.05" in options:
        #         if "1" in options:
        #             print("5")
        #         else:
        #             print("6")
        #     elif "0.01" in options: 
        #             if "1" in options:
        #                 print("7")
        #             else:
        #                 print("8")
        # else:
        #     video += 9
        #     if "0.15" in options:
        #         if "1" in options:
        #             print("9")
        #         else:
        #             print("10")
        #     elif "0.10" in options:
        #         if "1" in options:
        #             print("11")
        #         else:
        #             print("12")
        #     elif "0.05" in options:
        #         if "1" in options:
        #             print("13")
        #         else:
        #             print("14")
        #     elif "0.01" in options:
        #             if "1" in options:
        #                 print("15")
        #             else:
        #                 print("16")
                
            
                

        return super().form_valid(form)

    # def __init__(self, **kwargs):
    #     disable_choice = ["Bag"]
    #     for choice in MainForm :
    #         if choice == disable_choice:





# def registration_view(request):
#     if request.method == 'POST':
#         form = MainForm(request.POST)     
#     else:
#         form = MainForm()

#     return render(request, 'demo/simulator.html', {'form': form})
    
class ClientForm(CreateView):
    model = Client
    fields = ["name","company", "email"]
    template_name = "demo/client.html"
    success_url = reverse_lazy('simulator')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vidnum = self.request.session.get('vidnum', 1 )
        context['video'] = vidnum  
        return context
    

    # def get_initial(self):
    #         initial = super().get_initial()
    #         vidnum = self.request.session.get('vidnum', 1)  # Get the 'video' value from the session
    #         initial['video'] = vidnum  # Set the 'video' value in the initial data
    #         return initial




    def form_valid(self, form):
        
        bug = self.request.POST
        print(bug)
        name = form.cleaned_data['name']
        company = form.cleaned_data['company']
        vidnum = self.request.session.get('vidnum', 1 )
        email1 = form.cleaned_data['email']
        email2 = 'muffs2398@gmail.com'

        email_subject = 'Hello ' + str(name) + ' from ' + str(company)
        email_body = 'Your simulation was submitted successfully. '
        from_email = email2
        recipient_list = [email1]

        email_subject1 = 'Simulation submitted from ' + str(name) + ' from company ' + str(company)
        email_body1 = 'The video number and report is ' + str(vidnum)
        from_email1 = email1
        recipient_list1 = [email2]
        
        with get_connection() as connection:
            mail1 = EmailMessage(email_subject, email_body, from_email, recipient_list,  connection=connection)
            mail2 = EmailMessage(email_subject1, email_body1, from_email1, recipient_list1,  connection=connection)
            mail1.send()
            mail2.send()

        return super().form_valid(form)
        

