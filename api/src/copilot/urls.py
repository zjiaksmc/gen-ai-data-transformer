from django.urls import path
from . import views

urlpatterns = [
    ## Chat Session
    path('chat/session/', views.ChatSessionList.as_view(), name='chat_session_list'),
    path('chat/session/<str:session_id>', views.ChatSessionDetail.as_view(), name='chat_session_detail'),

    ## Chat Summary
    path('chat/summary/<str:user_id>', views.ChatSummary.as_view(), name='chat_summary')
]