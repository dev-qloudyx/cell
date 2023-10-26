from django.views.generic.edit import FormView, CreateView
from demo.tasks import send_mail_after_delay, send_mail_after_delay_2
from simulator import settings
from .models import Client
from .forms import MainForm
from django.urls import reverse_lazy 
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vidnum = self.request.session.get('vidnum', 1 )
        context['video'] = vidnum  
        return context
    
    def get_success_url(self):

        current_path = self.request.path
        success_url = current_path

        return success_url

    

    def form_valid(self, form):
        
        parameters = { 
            1: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.15",
                  "Cooling rate (ºC/min)":"1"
                  },
            2: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.15",
                  "Cooling rate (ºC/min)":"5"
                  },
            3: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.10",
                  "Cooling rate (ºC/min)":"1"
                  },
            4: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.10",
                  "Cooling rate (ºC/min)":"5"
                  },
            5: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.05",
                  "Cooling rate (ºC/min)":"1"
                  },
            6: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.05",
                  "Cooling rate (ºC/min)":"5"
                  },
            7: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.01",
                  "Cooling rate (ºC/min)":"1"
                  },
            8: {"Type of Freezer":"CELL (SmartFreez's unidirectional CRF)",
                  "Mass fraction of DMSO":"0.01",
                  "Cooling rate (ºC/min)":"5"
                  },
            9: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.15",
                  "Cooling rate (ºC/min)":"1"
                  },
            10: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.15",
                  "Cooling rate (ºC/min)":"5"
                  },
            11: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.10",
                  "Cooling rate (ºC/min)":"1"
                  },
            12: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.10",
                  "Cooling rate (ºC/min)":"5"
                  },
            13: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.05",
                  "Cooling rate (ºC/min)":"1"
                  },
            14: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.05",
                  "Cooling rate (ºC/min)":"5"
                  },
            15: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.01",
                  "Cooling rate (ºC/min)":"1"
                  },
            16: {"Type of Freezer":"Radial freezer (e.g., CoolCell®)",
                  "Mass fraction of DMSO":"0.01",
                  "Cooling rate (ºC/min)":"5"
                  },
        }

        bug = self.request.POST
        print(bug)
        name = form.cleaned_data['name']
        company = form.cleaned_data['company']
        vidnum = self.request.session.get('vidnum', 1 )
        email1 = form.cleaned_data['email']

    #1º Mail to self(host) - Este email é para o host com os dados do cliente

        email_subject2 = 'New Simulation Submitted'
        email_body2 = '''
New simulation submitted from ''' + str(name) +  ''' with the email '''  + str(email1) + '''.

The set of selected options is:

Type of Freezer: ''' + str(parameters[vidnum]["Type of Freezer"]) + '''
Biomixture: DMSO + Culture medium
Mass fraction of DMSO: ''' + str(parameters[vidnum]["Mass fraction of DMSO"]) + '''
Cooling rate (ºC/min): ''' + str(parameters[vidnum]["Cooling rate (ºC/min)"])
        
        from_email2 = settings.EMAIL_HOST_USER
        recipient_list2 = [settings.EMAIL_HOST_USER]
        mail3 = EmailMessage(email_subject2, email_body2, from_email2, recipient_list2)
        mail3.send()

    #2º Mail to self(host) - Este email é para ser enviado 30 minutos depois
        email_subject3 = 'Report Sent'
        email_body3 = '''Report sent to from ''' + str(name) +  ''' with the email '''  + str(email1) + '''.'''


        task = send_mail_after_delay_2.apply_async(
                (email_subject3, email_body3, from_email2, recipient_list2),
                countdown=1800
            )
        
    #1º email para o cliente
        email_subject = 'SMARTFREEZSIM® Platform - Preparing your Simulation!'
        email_body = '''
Dear ''' + str(name) + ''',
Thank you for your submission to the SMARTFREEZSIM® platform. We are delighted to welcome you to our simulation network, your interest and collaboration is greatly appreciated.
        
In the next hour, you will receive a simulation that has been developed with the parameters you selected in the SMARTFREEZSIM® platform.
We hope that our simulations can provide useful insight. If you have any questions or require assistance, please do not hesitate to contact us at support@smartfreez.com.

We expect this can be the start of a fruitfull collaboration.

Best regards,
The SMARTFREEZ team'''

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email1]

        mail1 = EmailMessage(email_subject, email_body, from_email, recipient_list)
        mail1.send()

    #2º email para o cliente 30 minutos depois
        email_subject1 = 'SMARTFREEZSIM® Platform - Your Simulation is ready!'
        email_body1 = '''
Dear ''' + str(name) + ''',

Your simulation in our SMARTFREEZSIM® platform is now ready. You will find it below with the related Report for:

Type of Freezer: ''' + str(parameters[vidnum]["Type of Freezer"]) + '''
Biomixture: DMSO + Culture medium
Mass fraction of DMSO: ''' + str(parameters[vidnum]["Mass fraction of DMSO"]) + '''
Cooling rate (ºC/min): ''' + str(parameters[vidnum]["Cooling rate (ºC/min)"]) + '''

For more SMARTFREEZSIM® parameters, SMARTFREEZ solutions or other information, please contact our team at info@smartfreez.com.     

Best regards,
The SMARTFREEZ team'''

        from_email1 = settings.EMAIL_HOST_USER
        recipient_list1 = [email1]

       
        
        base_path = 'demo/static/demo/FILES/'
        video_file = f'{base_path}Video{vidnum}.mp4'
        report_file = f'{base_path}Report{vidnum}.pdf'


        task = send_mail_after_delay.apply_async(
                (email_subject1, email_body1, from_email1, recipient_list1, video_file, report_file),
                countdown=1800
            )

        messages.success(self.request, "Simulation submitted successfully")
        

        return super().form_valid(form)
        

