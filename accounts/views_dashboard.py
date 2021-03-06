from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View, UpdateView

import cloudinary
import cloudinary.uploader
import cloudinary.api

from .forms import UserCreationForm, UserUpdateForm, ThemeForm
from .models import User
from .polices import IsRootOrAdm, IsSalesMan

from address.models import Address


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')

class ListUserView(LoginRequiredMixin, IsRootOrAdm, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'dashboard/list_users.html'
    paginate_by = 1

    def get_queryset(self):
        filtro = self.request.GET.get('filtro')
        if filtro == 'adm':
            queryset = User.objects.filter(nivel=1)
        elif filtro == 'vendedor':
            queryset = User.objects.filter(nivel=2)
        elif filtro == 'cliente':
            queryset = User.objects.filter(nivel=3)
        else:
            queryset = User.objects.all()
        return queryset

class DetailUserTaxedView(LoginRequiredMixin, IsRootOrAdm, TemplateView):
    template_name = 'dashboard/detail_user.html'

    def get_context_data(self, **kwargs):
        context = super(DetailUserTaxedView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        context['user_taxed'] = user
        context['address'] = Address.objects.filter(user=pk)
        return context

class ChangeStatusUserView(LoginRequiredMixin, IsRootOrAdm, View):
    status = 0
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.status = self.status
        user.save()
        return redirect(reverse_lazy('accounts:detail_user_cadastrado', kwargs={'pk':user.pk}))

class ChangeNivelUserView(LoginRequiredMixin, IsRootOrAdm, View):
    nivel = 3
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.nivel = self.nivel
        user.save()
        return redirect(reverse_lazy('accounts:detail_user_cadastrado', kwargs={'pk':user.pk}))

class ProfileView(LoginRequiredMixin, IsSalesMan, DetailView):
    model = User
    context_object_name = 'user_taxed'
    template_name = 'dashboard/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        pk = self.request.user.pk
        context['form_up'] = UserUpdateForm(self.request.POST or None, instance=context['user_taxed'])
        context['address'] = Address.objects.filter(user=pk)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form_up']
        form_password = context['form_password']
        if form.is_valid():
            form.save()
        return self.render_to_response(context)

    def get_object(self):
        return self.request.user

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/settings.html'

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        context['form_change_password'] = PasswordChangeForm(self.request.user, self.request.POST)
        context['theme_form'] = ThemeForm(self.request.POST or None, instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_change_password = context['form_change_password']
        theme_form = context['theme_form']
        if form_change_password.is_valid():
            form_change_password.save()
            return redirect(reverse_lazy('accounts:logout'))
        if theme_form.is_valid():
            theme_form.save()
        return redirect(reverse_lazy('accounts:profile'))

class UploadImg(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        filep = self.request.FILES['avatar']
        filep.name = str(user.pk)
        avatar = cloudinary.uploader.upload(filep, folder='User' ,public_id=user.email)
        user.avatar = avatar['secure_url']
        user.save()
        return redirect(reverse_lazy('accounts:profile'))



#Modificar_User_Taxed
create_user = CreateUserView.as_view()
list_user = ListUserView.as_view()
detail_user_taxed = DetailUserTaxedView.as_view()
#Status_User_Taxed
active = ChangeStatusUserView.as_view()
disable = ChangeStatusUserView.as_view(status=1)
block = ChangeStatusUserView.as_view(status=2)
#Nivel_User_Taxed
adm = ChangeNivelUserView.as_view(nivel=1)
salesman = ChangeNivelUserView.as_view(nivel=2)
customer = ChangeNivelUserView.as_view()
#Modificar_User_logado
profile = ProfileView.as_view()
upload_view = UploadImg.as_view()
settings_view = SettingsView.as_view()
