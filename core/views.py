from crispy_forms.layout import Submit
from django.forms import modelformset_factory
from django.shortcuts import render

# Create your views here.
from django.core.exceptions import ValidationError

from .forms import SignUpForm, FriendForm, FriendFormSetHelper
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.mail import EmailMessage

from .forms import VolunteerForm
from .models import Volunteer, Friend

# Create your views here.
from django.http import HttpResponse
import civis

def index(request):
    context = {}
    return render(request, 'core/index.html', context)


def profile_check(user):
    # print(user.donator)
    # print(user.donator.location)
    # print(user.donator.birth_date)
    # print(user.donator.full_clean())
    try:
        user.volunteer.full_clean()
    except ValidationError as e:
        return False
    return True

@login_required
@user_passes_test(profile_check, login_url='/profile')
def dashboard(request):


    # context = {'result': 'heres your link' + request.user.volunteer.slug+table[1][1]}
    context = {'pageOwner':request.user}
    return render(request, 'core/dashboard.html', context)



def page(request,urlSlug):
    pageOwner=Volunteer.objects.get(slug=urlSlug)
    # table = civis.io.read_civis_sql("select tracking_id, count(*) from wwav_rtv.rtv_cleaned where lower(tracking_id) = 'msv-custom-"+urlSlug+"' and status not in ('Rejected','Under 18') group by 1", "TMC")
    # print(table)
    # context = {'pageOwner':pageOwner.user,'reg': table[1][1]}
    context = {'pageOwner':pageOwner.user,'reg': pageOwner.reg}
    return render(request, 'core/page.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.refresh_from_db()
            # # user.donator.bio = form.cleaned_data.get('bio')
            # # user.donator.birth_date = form.cleaned_data.get('birth_date')
            # user.donator.first_name = form.cleaned_data.get('first_name')
            # user.donator.last_name = form.cleaned_data.get('last_name')
            # user.donator.email = form.cleaned_data.get('email')
            # user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':

        form = VolunteerForm(request.POST, instance=request.user.volunteer)
        if form.is_valid():
            user = request.user

            user.volunteer = form.save()

            return redirect('friends')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = VolunteerForm(instance=request.user.volunteer)

    context = {'form': form}
    return render(request, 'core/profile.html', context)

@login_required
@user_passes_test(profile_check, login_url='/profile')
def friends(request):
    # FriendFormSet=formset_factory(FriendForm, extra=2)
    FriendFormSet=modelformset_factory(Friend, form=FriendForm, extra=10,max_num=10)

    helper=FriendFormSetHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.template = 'bootstrap/table_inline_formset.html'

    if request.method == 'POST':

        formset = FriendFormSet(request.POST)
        if formset.is_valid():
            friends = formset.save(commit=False)
            for friend in friends:
                friend.volunteer = request.user.volunteer
                friend.save()

            # friend=form.save(commit=False)
            # friend.volunteer = request.user.volunteer
            # friend.save()
            return redirect('dashboard')

        # if a GET (or any other method) we'll create a blank form
    else:
        formset = FriendFormSet()#FriendForm()

    context = {'formset': formset, 'helper': helper}
    return render(request, 'core/friends.html', context)
