from forum.views import combineDateAndAgo
from .models import Notification

def add_variable_to_context(request):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return {}
    
    # check if in notifications corresponding to the user or the comment.chaiId.user == request.user
    # get the user id from the request
    user_id = request.user.id
    notifications = Notification.objects.all()
    
    # combineDateAndAgo
    # map notifications date to a string "y-m-d" and use combineDateAndAgo to get the time ago
    # for notification in notifications:
    #     notification.date = combineDateAndAgo(notification.date.strftime('%Y-%m-%d'))
    
    
    
    if notifications.filter(user=user_id).exists():
        notificationsData = list(notifications.filter(user=user_id).order_by('-date'))
        
        for notification in notificationsData:
            notification.date = combineDateAndAgo(notification.date.strftime('%Y-%m-%d'))
        
        return {
            'notifications': notificationsData,
            'unread_notifications': notifications.filter(user=user_id, is_read=False).count()
        }
    elif notifications.filter(chatId__id=user_id).exists():
        noticationsData = notifications.filter(chatId__id=user_id).order_by('-date')
        for notification in notificationsData:
            notification.date = combineDateAndAgo(notification.date.strftime('%Y-%m-%d'))
        
        return {
            'notifications': noticationsData,
            'unread_notifications': notifications.filter(chatId__user_id=user_id, is_read=False).count()
        }
    else:
        return {}