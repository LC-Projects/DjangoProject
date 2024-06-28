from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from django_filters import FilterSet, CharFilter, ModelChoiceFilter

from .models import Chat, Message, Category
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from django_filters.views import FilterView


class ChatFilterSet(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Name')
    category = ModelChoiceFilter(queryset=Category.objects.all(), label='Category')


class ChatFilterView(LoginRequiredMixin, FilterView):
    model = Chat
    template_name = 'chats/home.html'
    context_object_name = 'datas'
    filterset_class = ChatFilterSet


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chats/chat_detail.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        messages = Message.objects.filter(chat=chat)
        datas = []
        for message in messages:
            datas.append({
                'id': message.id,
                'content': message.content,
                'is_bot': message.is_bot,
                'created_at': message.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            })
        context['messages'] = datas
        return context


@login_required
def chat_delete(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})
    else:
        try:
            chat = request.POST.get('chat_id')
            chat = Chat.objects.get(id=chat)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Chat not found'})
        else:
            chat.delete()
            return JsonResponse({'status': 'Valid'})


def add_message(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})
    else:
        chat = request.POST.get('chat')
        content = request.POST.get('content')
        is_bot = request.POST.get('is_bot', False)
        message = Message(chat_id=chat, content=content, is_bot=is_bot)
        message.save()
        # Convert the message object to a dictionary
        message_dict = model_to_dict(message)
        return JsonResponse({'status': 'Valid', 'new_message': message_dict})
