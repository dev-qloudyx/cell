from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView
from demo.tasks import send_mail_after_delay

from simulator import settings
from .models import Client
from .forms import ClientForm, MainForm
from django.urls import reverse_lazy 
from django.core.mail import send_mail, get_connection
from django.core.mail.message import EmailMessage
from django.contrib import messages
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


        return super().form_valid(form)

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
    

    def form_valid(self, form):
        
        bug = self.request.POST
        print(bug)
        name = form.cleaned_data['name']
        company = form.cleaned_data['company']
        vidnum = self.request.session.get('vidnum', 1 )
        email1 = form.cleaned_data['email']

    #Mail to self(host) - Este email é para o host com os dados do cliente

        email_subject2 = 'Simulation submitted from ' + str(name) + ' from company ' + str(company)
        email_body2 = 'New simulation submitted from ' + str(email1) +  ' .'
        from_email2 = 'info@smartfreez.com'
        recipient_list2 = settings.EMAIL_HOST_USER
        mail3 = EmailMessage(email_subject2, email_body2, from_email2, recipient_list2)
        mail3.send()


    #1º email para o cliente
        email_subject = 'Hello ' + str(name) + ' from ' + str(company)
        email_body = 'Your simulation was submitted successfully. '
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email1]

        mail1 = EmailMessage(email_subject, email_body, from_email, recipient_list)
        mail1.send()

    #2º email para o cliente 30 minutos depois
        email_subject1 = 'Simulation results'
        email_body1 = 'Here are your simulation results.'
        from_email1 = settings.EMAIL_HOST_USER
        recipient_list1 = [email1]

        #mail2 = EmailMessage(email_subject1, email_body1, from_email1, recipient_list1)
        #mail2.attach_file('demo\static\demo\FILES\Video'+str(vidnum)+'.mp4')
        #mail2.attach_file('demo\static\demo\FILES\Report'+str(vidnum)+'.pdf')
        
        base_path = 'demo/static/demo/FILES/'
        video_file = f'{base_path}Video{vidnum}.mp4'
        report_file = f'{base_path}Report{vidnum}.pdf'


        task = send_mail_after_delay.apply_async(
                (email_subject1, email_body1, from_email1, recipient_list1, video_file, report_file),
                countdown=1800
            )

        messages.success(self.request, "Simulation submitted successfully")
        

        return super().form_valid(form)
        

