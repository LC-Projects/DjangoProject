import datetime
from django.shortcuts import render
from django.urls import reverse

from chats.models import Chat, Category, Comment, Message


# Create your views here.

def AllForumsView(request):
    template_name = 'forum/home.html'

    # TODO: Retrive all catergories, get the count of posts in each category and display them in the leftside bar
    categories = Category.objects.all()
    public_chats = Chat.objects.filter(is_private=False)
    comments = Comment.objects.all()
    messages = Message.objects.filter(is_bot=False)

    categories_data = []
    categories_data.append(
        {
            'hr': True
        }
    )
    categories_data.append(
        {
            'color': 'white',
            'bg': 'red',
            'link': reverse('forum:home'),
            'icon': '<i class="fa-solid fa-kitchen-set"></i>',
            'label': 'All',
            'count': public_chats.count()
        }
    )
    for category in categories:
        category_data = {
            'color': 'white',
            'bg': 'red',
            'link': reverse('forum:home_slug', args=[category.slug]),
            'icon': '<i class="fa-solid fa-kitchen-set"></i>',
            'label': category.name,
            'count': public_chats.filter(category=category).count(),
            'slug': category.slug
        }
        categories_data.append(category_data)
    # To get icons: https://fontawesome.com/search

    chats_datas = []
    for chat in public_chats:
        message = messages.filter(chat=chat).order_by('created_at').first()
        message_content = f"{message.content[:30]}..." if message else ''
        chat_data = {
            'id': chat.id,
            'title': chat.name,
            'author': chat.user.username,
            'date': combineDateAndAgo(chat.created_at.strftime('%Y-%m-%d')),
            'content': message_content,
            'comments': comments.filter(chat=chat).count(),
            # 'likes': chat.likes.count()
        }
        chats_datas.append(chat_data)
    context = {}
    context['leftside'] = categories_data

    context['recipe'] = chats_datas

    return render(request, template_name, context)

def ForumByCategoryView(request, slug):
    template_name = 'forum/home.html'
    categories = Category.objects.all()
    public_chats = Chat.objects.filter(is_private=False)
    public_chats_cat = public_chats.filter(category__slug=slug)
    comments = Comment.objects.all()
    messages = Message.objects.filter(is_bot=False)

    categories_data = []
    categories_data.append(
        {
            'hr': True
        }
    )
    categories_data.append(
        {
            'color': 'white',
            'bg': 'red',
            'link': reverse('forum:home'),
            'icon': '<i class="fa-solid fa-kitchen-set"></i>',
            'label': 'All',
            'count': public_chats.count()
        }
    )
    for category in categories:
        category_data = {
            'color': 'white',
            'bg': 'red',
            'link': reverse('forum:home_slug', args=[category.slug]),
            'icon': '<i class="fa-solid fa-kitchen-set"></i>',
            'label': category.name,
            'count': public_chats.filter(category=category).count(),
            'slug': category.slug
        }
        categories_data.append(category_data)
    # To get icons: https://fontawesome.com/search

    chats_datas = []
    for chat in public_chats_cat:
        message = messages.filter(chat=chat).order_by('created_at').first()
        message_content = f"{message.content[:30]}..." if message else ''
        chat_data = {
            'id': chat.id,
            'title': chat.name,
            'author': chat.user.username,
            'date': combineDateAndAgo(chat.created_at.strftime('%Y-%m-%d')),
            'content': message_content,
            'comments': comments.filter(chat=chat).count(),
            # 'likes': chat.likes.count()
        }
        chats_datas.append(chat_data)
    context = {}
    context['leftside'] = categories_data

    context['recipe'] = chats_datas

    return render(request, template_name, context)


# UTILS FUNCTIONS
def convertDateToFrenchFormat(date):
    # 2021-09-01
    # 01/09/2021
    return date[8:] + '/' + date[5:7] + '/' + date[:4]


def TimeAgo(date):
    # 2021-09-01
    # until now

    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    now = datetime.datetime.now()
    diff = now - date

    # Assuming diff is a datetime.timedelta object
    if diff.days >= 365.25:
        years = int(diff.days // 365.25)
        months = int((diff.days % 365.25) // 30.44)
        return f'{years} {"year" if years == 1 else "years"} and {months} {"month" if months == 1 else "months"} ago'
    elif diff.days >= 30.44:
        months = int(diff.days // 30.44)
        return f'{months} {"month" if months == 1 else "months"} ago'
    elif diff.days > 0:
        return f'{diff.days} {"day" if diff.days == 1 else "days"} ago'
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f'{hours} {"hour" if hours == 1 else "hours"} ago'
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f'{minutes} {"minute" if minutes == 1 else "minutes"} ago'
    else:
        return f'{diff.seconds} {"second" if diff.seconds == 1 else "seconds"} ago'


def combineDateAndAgo(date):
    return convertDateToFrenchFormat(date) + ' (' + TimeAgo(date) + ')'
