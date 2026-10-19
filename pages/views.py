from django.shortcuts import render
from django.views.generic import TemplateView
from .models import TutoringHour
from django.views.generic import DetailView
from .models import TAProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import TutoringHourForm
from .models import TAProfile



class HomePageView(TemplateView):
    template_name = "home.html"

    #prepare info to send to homepage
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #renders in HTML
        context["tutoring_hours"] = (
            TutoringHour.objects
            .select_related("ta", "ta__user") #TA & User retrieval 
            .prefetch_related("ta__courses") #Each TA course
            .all() #every tutoring hour record
        )

        context["is_ta"] = (
            self.request.user.is_authenticated
            and TAProfile.objects.filter(
                user=self.request.user
            ).exists()
        )
        return context

# retrieve a specific TA profile and make it available
class TAProfileDetailView(DetailView):
    model = TAProfile
    template_name = "ta_detail.html"
    context_object_name = "ta"

#LoginrequiredMixIn -> require sign in. Createview -> displays and submits
class TutoringHourCreateView(LoginRequiredMixin, CreateView):
    model = TutoringHour
    form_class = TutoringHourForm
    template_name = "add_tutoring_hour.html"
    success_url = reverse_lazy("home") #returns TA to homepage after save

#dispatch() -> Non-TA, not able to access page.
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not TAProfile.objects.filter(user=request.user).exists():
                raise PermissionDenied(
                    "Only registered TAs can add tutoring hours."
    )
        return super().dispatch(request, *args, **kwargs)

#form_valid -> assigns hours to signed in TA
    def form_valid(self, form):
        form.instance.ta = TAProfile.objects.get(
            user=self.request.user
        )

        return super().form_valid(form)

