from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django_filters import FilterSet, CharFilter, ModelChoiceFilter

from .models import Chat, Message, Category
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from django_filters.views import FilterView

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

import os
import re
import markdown

# Initialize LangChain with your API key or necessary configuration
langchain_client = ChatOpenAI(api_key=os.environ.get('API_KEY', ''))


class ChatFilterSet(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Name')
    category = ModelChoiceFilter(queryset=Category.objects.all(), label='Category')


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class ChatFilterView(FilterView):
    model = Chat
    template_name = 'chats/home.html'
    context_object_name = 'datas'
    filterset_class = ChatFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class ChatDetailView(DetailView):
    model = Chat
    template_name = 'chats/chat_detail.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        messages = Message.objects.filter(chat=chat)
        datas = []
        for message in messages:
            content = message.content

            content = process_content(content)

            datas.append({
                'id': message.id,
                'content': markdown.markdown(content),
                'is_bot': message.is_bot,
                'created_at': message.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            })
        context['messages'] = datas
        context['body_class'] = 'chat-detail-page-body'
        return context


@login_required(login_url='auth:login')
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


@login_required(login_url='auth:login')
def add_message(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})
    else:
        chat = request.POST.get('chat')
        content = request.POST.get('content')
        is_bot = request.POST.get('is_bot', False)

        # Save the user's message
        message = Message(chat_id=chat, content=content, is_bot=is_bot)
        message.save()

        # Retrieve the last 5 messages for context
        context_messages = Message.objects.filter(chat_id=chat).order_by('-created_at')[:5]

        # Create LangChain message objects for the context
        langchain_messages = []
        for msg in reversed(context_messages):
            if msg.is_bot:
                langchain_messages.append(AIMessage(content=msg.content))
            else:
                langchain_messages.append(HumanMessage(content=msg.content))

        # Add the new user message to the context
        langchain_messages.append(HumanMessage(content=content))

        # Get the bot's response with context
        bot_response = langchain_client.invoke(langchain_messages)  # Adjust this line if needed

        # Save the bot's response as a message
        bot_message = Message(chat_id=chat, content=bot_response.content, is_bot=True)
        bot_message.save()

        message_dict = {
            'id': message.id,
            'content': message.content,
            'is_bot': message.is_bot,
            'created_at': message.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        }

        bot_message_dict = {
            'id': bot_message.id,
            'content': bot_message.content,
            'is_bot': bot_message.is_bot,
            'created_at': bot_message.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        }

        return JsonResponse({'status': 'Valid', 'new_message': message_dict, 'bot_response': bot_message_dict})


@login_required(login_url='auth:login')
def create_chat(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})
    else:
        name = request.POST.get('name')
        category = request.POST.get('category')
        chat = Chat(name=name, category_id=category, user=request.user)
        chat.save()
        return JsonResponse({'status': 'Valid', 'chat': {
            'id': chat.id,
            'name': chat.name,
            'category': chat.category.name,
            'created_at': chat.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            'detail_url': f'/chats/detail/{chat.id}/'
        }})


def process_content(content):
    # This pattern matches text enclosed in triple backticks with an optional language specifier,
    # single backticks, and any other text.
    pattern = r'(```(\w+)?(.*?)```|`.*?`|[^`]+)'

    def replace_line_breaks(match):
        text = match.group(0)
        # Check if the text is code (enclosed in backticks) or plain text.
        if text.startswith('```'):
            language = match.group(2)
            code_block = match.group(3)
            if language:
                return f'<pre><code class="language-{language}">{code_block}</code></pre>'
            else:
                return f'<pre><code>{code_block}</code></pre>'
        elif text.startswith('`'):
            return f'<code>{text[1:-1]}</code>'
        else:
            return text.replace('\n', '<br>')  # Replace line breaks in plain text.

    # Use the sub function to replace line breaks in plain text while keeping code blocks unchanged.
    content = re.sub(pattern, replace_line_breaks, content, flags=re.DOTALL)

    return content
