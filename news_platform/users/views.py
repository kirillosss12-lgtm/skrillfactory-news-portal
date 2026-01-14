from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_edit.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = '/'

    # 1. Сначала получаем объект пользователя
    def get_object(self, queryset=None):
        return self.request.user

    # 2. Затем передаем данные в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем проверку для кнопки "Стать автором"
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group, created = Group.objects.get_or_create(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        user.groups.add(authors_group)
    return redirect('user_edit')