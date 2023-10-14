from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.template.loader import render_to_string

from pinax.referrals.models import ReferralResponse

from .models import PersonalInfo
from .forms import PersonalInfoForm, EduForm, OthersForm
from .utils import EmailThread


def index(request):
    return render(request, 'app/index.html')


def tracks(request):
    return render(request, 'app/tracks.html')


def process(request):
    return render(request, 'app/process.html')


@login_required()
def apply(request):

    obj = get_object_or_404(PersonalInfo, user=request.user)
    form = PersonalInfoForm(instance=obj)

    if request.method == "POST":
        form = PersonalInfoForm(request.POST,
                                request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your contact details was submitted successfully!')
            return redirect('apply_edu')
        # print(form.errors)   

    if obj.completed:
        messages.info(request, 'You have already applied, take test!')
        return render(request, 'app/start_test.html')
    

    context = {'form': form}

    return render(request, 'app/personal_information.html', context)


@login_required()
def apply_edu(request):

    obj = get_object_or_404(PersonalInfo, user=request.user)
    form = EduForm(instance=obj)

    if request.method == "POST":
        form = EduForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your education details was submitted successfully!')
            return redirect('apply_others')
            

    if obj.completed:
        messages.info(request, 'You have already applied, take test!')
        return render(request, 'app/start_test.html')

    context = {'form': form}
    return render(request, 'app/p_info_edu.html', context)


@login_required()
def apply_others(request):

    obj = get_object_or_404(PersonalInfo, user=request.user)
    form = OthersForm(instance=obj)

    if request.method == "POST":
        form = OthersForm(request.POST, instance=obj)

        if form.is_valid():
            new_data = form.save(commit=False)
            new_data.completed = True
            new_data.save()
            messages.success(
                request, 'Your application was submitted successfully, take test!')
            return render(request, 'app/start_test.html')

    if obj.completed:
        messages.info(request, 'You have already applied, take test!')
        return render(request, 'app/start_test.html')

    

    context = {'form': form}
    return render(request, 'app/p_info_others.html', context)



def continue_login(request):
    return render(request, 'app/continue_login.html')


def faq(request):
    return render(request, 'app/faq.html')


def application_closed(request):
    return render(request, 'app/application_closed.html')

def dashboard(request):
    refer = PersonalInfo.objects.get(user = request.user)
    context = { 'refer': refer }
    return render(request, 'app/dashboard.html', context)

def referred_landing(request):
    referral = ReferralResponse.objects.filter( session_key = request.session.session_key).first()
    
    referral_code = PersonalInfo.objects.get(referral = referral.referral)
   
    context = {'referrer': referral_code.user}
    return render(request, 'app/referred_landing', context)


def take_test(request):
    return render(request, 'app/take_test.html')

def contact(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        message = request.POST.get('message', None)

        now = timezone.now()
        time = now.strftime("%d %B, %Y, %H:%M:%S")

        subject = f"New message from {fullname}"

        context = {
            'fullname': fullname,
            'phone': phone,
            'email': email,
            'message': message,
            'time': time
        }
        body = render_to_string('app/emails/contact.txt', context)

        EmailThread(subject, body, ['cap@edubridgeacademy.com']).start()
        data = {'success': 'Hang on! We will get back to you!'}
        return JsonResponse(data)

    return render(request, 'app/contact.html')