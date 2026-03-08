from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max

from bimber_app.models import Match
from chat.models import ChatMessage
from bimber_app.models import CustomUser


@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    Match.objects.get_or_create(
        from_user=request.user,
        to_user=other_user,
        defaults={'is_like': True}
    )

    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')

    return render(request, 'room.html', {
        'other_user': other_user,
        'chat_messages': messages
    })

@login_required
def chat_list(request):
    messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).values('sender', 'recipient').annotate(last_msg=Max('timestamp')).order_by('-last_msg')

    chat_users_ids = set()
    for m in messages:
        chat_users_ids.add(m['sender'] if m['sender'] != request.user.id else m['recipient'])

    chat_users = CustomUser.objects.filter(id__in=chat_users_ids)

    return render(request, 'chat_list.html', {'chat_users': chat_users})