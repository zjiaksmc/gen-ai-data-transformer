import sys
import os
import datetime

from django.conf import settings
from django.core.cache import cache

from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.serializers import Serializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import randomname

from ai_data_formatter.copilot.model import PromptCodeChatSession
from ai_data_formatter.config import ModelConfig, DBClient
from ai_data_formatter.core.api import SessionHistoryService

from .models import *
from .serializers import *

dbclient = DBClient.from_dict(
    {
        "db": {
            "url": f'postgresql://{settings.DATABASES.get("gen_ai").get("USER")}:{settings.DATABASES.get("gen_ai").get("PASSWORD")}@{settings.DATABASES.get("gen_ai").get("HOST")}/{settings.DATABASES.get("gen_ai").get("NAME")}'
        },
        "cache": {
            "url": f'{settings.CACHES.get("gen_ai").get("LOCATION")}/{settings.CACHES.get("gen_ai").get("OPTIONS",{"db":"0"}).get("db","0")}',
            "expire_time_second": None
        }
    }
)
model_config = ModelConfig.from_dict(settings.COPILOT)


class ChatSessionList(GenericAPIView):
    """
    Retrieve list of chat sessions
    """
    serializer_class = ChatSessionSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="copilot-chat-session-list",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="User ID",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Status of the chat session",
                type=openapi.TYPE_INTEGER
            )
        ],
    )
    def get(self, request):
        """
        Retrieve all chat sessions
        """
        try:
            session_list = ChatSession.objects.all()
            if request.GET.get("user_id"):
                session_list = session_list.filter(user_id=request.GET.get("user_id"))
            if request.GET.get("is_active"):
                session_list = session_list.filter(is_active=request.GET.get("is_active"))
            session_serializer = ChatSessionSerializer(session_list, many=True)
            return Response({
                "session": session_serializer.data,
                "count": len(session_list),
                "timestamp": datetime.datetime.now()
            }, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message":"Error when retrieving chat: {}".format(sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="copilot-chat-session-create"
    )
    def post(self, request):
        """
        Create a chat session
        """
        try:
            session = PromptCodeChatSession(
                project_id=settings.GCP_PROJECT_ID, 
                location=settings.GCP_LOCATION,
                model_config=model_config,
                session_id=None,
                dbclient=dbclient
                )
            chat_session, created = ChatSession.objects.get_or_create(
                session_id=session.session_id,
                defaults={
                    "session_name": randomname.get_name()[:49],
                    "created_dt": datetime.datetime.now(),
                    "user_id": request.data.get("user_id"),
                    "email": request.data.get("email"),
                    "is_active": 1
                }
            )
            if created:
                # Load the sample data
                # file_path = request.data.get("sample_data_url", settings.DEFAULT_SAMPLE_URL)
                # test_data = pd.read_csv(file_path)
                # res = session.load_sample_data(test_data)
                return Response({
                    "session_id": chat_session.session_id,
                    "session": ChatSessionSerializer(chat_session).data,
                    "conversation": [{
                        "content": msg.content,
                        "author": msg.author
                        } for msg in session.message_history
                    ],
                    "timestamp": datetime.datetime.now(),
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": f"Session {session.session_id} already exist"
                }, status=status.HTTP_409_CONFLICT)
        except:
            return Response(
                {"message":"Error when creating chat: {}".format(sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ChatSessionDetail(GenericAPIView):
    """
    Manage a single chat session
    """
    serializer_class = ChatSessionSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="copilot-chat-session-get-message"
    )
    def get(self, request, session_id):
        """
        Retrieve chat session history
        """
        try:
            chat_session = ChatSession.objects.get(
                session_id=session_id
            )
            chat_session_serializer = ChatSessionSerializer(chat_session)
            session_hist_service = SessionHistoryService(
                dbclient=dbclient
            )
            return Response({
                "session_id": session_id,
                "session": chat_session_serializer.data,
                "conversation": [{
                    "content": msg.content,
                    "author": msg.author
                    } for msg in session_hist_service.get_session_history(session_id=chat_session.session_id)
                ],
                "timestamp": datetime.datetime.now()
            }, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response(
                {"message":f"Session {session_id} does not exist"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except:
            return Response(
                {"message":"Error when retrieving chat {}: {}".format(session_id, sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="copilot-chat-session-new-message"
    )
    def post(self, request, session_id):
        """
        Post new question to a chat session
        """
        try:
            chat_session = ChatSession.objects.get(
                session_id=session_id,
                is_active=1
            )
            tool = request.data.get("tool", "chat")
            tool_args = request.data.get("tool_args", {})
            message_type = request.data.get("type", 100)
            message = request.data.get("message")
            if tool == "chat":
                session = PromptCodeChatSession(
                    project_id=settings.GCP_PROJECT_ID, 
                    location=settings.GCP_LOCATION,
                    model_config=model_config,
                    session_id=chat_session.session_id,
                    dbclient=dbclient
                )
                if message_type == 120:
                    message = f"remember these sample data for later testing. {message}"
                    res = session.send_sample_data(message)
                else:
                    res = session.send_message(message)
            elif tool == "proprietary_search":
                model_config.model_id = "codechat-bison-32k@002"
                model_config.parameters = {
                    "max_output_tokens": 8000,
                    "temperature": 0.9
                }
                session = PromptCodeChatSession(
                    project_id=settings.GCP_PROJECT_ID, 
                    location=settings.GCP_LOCATION,
                    model_config=model_config,
                    session_id=chat_session.session_id,
                    dbclient=dbclient,
                    ignore_message_history=True
                )
                session.message_history = []
                res = session.send_proprietary_search(message, number_results=10)
            elif tool == "web_search":
                user_agent = tool_args.get("user_agent", None)
                if not user_agent:
                    raise ValueError("Web search must be requested with a user agent")
                model_config.model_id = "codechat-bison@002"
                model_config.parameters = {
                    "max_output_tokens": 2048,
                    "temperature": 0.9
                }
                session = PromptCodeChatSession(
                    project_id=settings.GCP_PROJECT_ID, 
                    location=settings.GCP_LOCATION,
                    model_config=model_config,
                    session_id=chat_session.session_id,
                    dbclient=dbclient,
                    ignore_message_history=True
                )
                res = session.send_web_search(message, ua=user_agent, number_results=10)
            else:
                session = PromptCodeChatSession(
                    project_id=settings.GCP_PROJECT_ID, 
                    location=settings.GCP_LOCATION,
                    model_config=model_config,
                    session_id=chat_session.session_id,
                    dbclient=dbclient
                )
                res = session.send_message(message)

            return Response(
                {
                    "session_id": chat_session.session_id,
                    "conversation": res,
                    "timestamp": datetime.datetime.now()
                },
                status=status.HTTP_200_OK
            )
        except ChatSession.DoesNotExist:
            return Response(
                {
                    "message": f"Session {session_id} does not exist or is no longer active",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except:
            return Response(
                {
                    "message":"Error when post message: {}".format(sys.exc_info()),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="copilot-chat-session-delete"
    )
    def delete(self, request, session_id):
        """
        Mark a chat session inactive
        """
        try:
            ChatSession.objects.filter(session_id=session_id).update(is_active=0)
            return Response({"message": "Successfully deactivate the chat session"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(
                {"message":"Error when deactivating the chat session {}: {}".format(session_id, sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatSummary(GenericAPIView):
    """
    Retrieve the statistics for a user
    """
    serializer_class = Serializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="copilot-chat-summary"
    )
    def get(self, request, user_id):
        """
        Retrieve chat history statistics for a user
        """
        try:
            return Response({}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message":"Error when retrieving chat statistics {}: {}".format(user_id, sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )