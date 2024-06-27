from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Chat, Message
from django.shortcuts import render
from django.http import JsonResponse

@login_required
# Create your views here.
def chat_list(request, category=None):
    datas=[]
    chats = Chat.objects.filter(category=category)
    for chat in chats:
        datas.append({
            'id': chat.id,
            'name': chat.name,
            'created_at': chat.created_at.strftime('%d/%m/%Y'),
        })

    return JsonResponse({'datas': datas})

@login_required
def chat_detail(request, chat):
    chat = Chat.objects.get(id=chat)
    messages = Message.objects.filter(chat=chat)
    datas = []
    for message in messages:
        datas.append({
            'id': message.id,
            'content': message.content,
            'is_bot': message.is_bot,
            'created_at': message.created_at.strftime('%d/%m/%Y'),
        })

    return JsonResponse({'datas': datas})

@login_required
def chat_delete(request, chat):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})
    else:
        try:
            chat = Chat.objects.get(id=chat)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Chat not found'})
        else:
            chat.delete()
            return JsonResponse({'status': 'Valide'})