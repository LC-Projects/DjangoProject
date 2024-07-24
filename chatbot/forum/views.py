import datetime
from django.shortcuts import render

# Create your views here.

def AllForumsView(request):
    template_name = 'forum/home.html'
    
    # TODO: Retrive all catergories, get the count of posts in each category and display them in the leftside bar
    # categories = Category.objects.all()
    
    # To get icons: https://fontawesome.com/search
    
    context = {}
    context['leftside'] = [
        {
            'hr': True
        },
        {
            'color': 'white',
            'bg': 'red',
            'link': '#', 
            'icon': '<i class="fa-solid fa-kitchen-set"></i>', 
            'label': 'Recipes', 
            'count': 10
        },
        {
            'color': 'white',
            'bg': 'blue',
            'link': '#', 
            'icon': '<i class="fa-solid fa-calculator"></i>', 
            'label': 'Math', 
            'count': 10
        },
    ]
    
    context['recipe'] = [
        {
            'title': 'How to make a cake',
            'author': 'John Doe',
            'date': combineDateAndAgo('2021-09-01'),
            'content': 'This is how you make a cake',
            'comments': 10,
            'likes': 100
        },
        {
            'title': 'How to make a pizza',
            'author': 'Jane Doe',
            'date': combineDateAndAgo('2024-03-01'),
            'content': 'This is how you make a pizza',
            'comments': 10,
            'likes': 100
        }
    ]
    
    return render(request, template_name, context)



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