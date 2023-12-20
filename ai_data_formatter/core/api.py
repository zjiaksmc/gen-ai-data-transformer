import os
import logging
import redis
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass, field, fields
from dataclasses_json import dataclass_json
from google import auth
import vertexai
import pandas as pd
import requests
import time 
import pickle
import json

from vertexai.language_models._language_models import ChatMessage
from ..model import ChatMessageHistory


@dataclass_json
@dataclass
class ModelAPIResponse:

    text: str
    raw_response: Any


@dataclass_json
@dataclass
class ModelAPIEndpoint:

    headers: Dict[str, str]
    base_url: str


@dataclass
class TextGenerationEndpoint:

    model_api_endpoint: Union[ModelAPIEndpoint, Any]
    model_id: str
    parameters: Optional[dict]

    def predict(self, input_text):
        if isinstance(self.model_api_endpoint, ModelAPIEndpoint):
            return self.__raw_predict(
                input_text
            )
        else:
            return self.model_api_endpoint.predict(
                input_text, 
                **self.parameters
            )
    
    def __raw_predict(self, input_text):
        data={
            "instances": [
                {
                    "prompt": input_text
                }
            ],
            "parameters": self.parameters
        }
        response = requests.post(
            url=f"{self.model_api_endpoint.base_url}/{self.model_id}:predict",
            headers=self.model_api_endpoint.headers,
            data=json.dumps(data)
        )
        try:
            return ModelAPIResponse(
                text=response.json().get("predictions")[0].get("content"),
                raw_response=response
            )
        except:
            return ModelAPIResponse(
                text="",
                raw_response=response
            )


@dataclass
class ChatSessionEndpoint:

    model_api_endpoint: Union[ModelAPIEndpoint, Any]
    model_id: str
    context: Optional[str]
    parameters: Optional[dict]
    message_history: Optional[List[ChatMessage]] = field(default_factory=list)

    def send_message(self, message):
        messages = [
            {
                "content": m.content,
                "author": m.author
            } for m in self.message_history
        ]
        messages.append(
            {
                "content": message,
                "author": "user"
            }
        )
        data={
            "instances": [
                {
                    "context": self.context,
                    "messages": messages
                }
            ],
            "parameters": self.parameters
        }
        response = requests.post(
            url=f"{self.model_api_endpoint.base_url}/{self.model_id}:predict",
            headers=self.model_api_endpoint.headers,
            data=json.dumps(data)
        )
        try:
            res = ModelAPIResponse(
                text=response.json().get("predictions")[0].get("candidates")[0].get("content"),
                raw_response=response
            )
        except:
            res = ModelAPIResponse(
                text="Sorry, I do not have an answer to this question.",
                raw_response=response
            )
        
        self.message_history.append(ChatMessage(
            content=message,
            author="user"
        ))
        self.message_history.append(ChatMessage(
            content=res.text,
            author="bot"
        ))
        return res


class VertexAIAgent:
    """
    Agent to handle API initiation and authorization
    """

    def __init__(self, project_id, location, **kwargs):
        vertexai.init(
            project=project_id,
            location=location,
            credentials=self.__get_credentials(),
            **kwargs
        )
        self.model_api_endpoint = ModelAPIEndpoint(
            base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models",
            headers={
                "Authorization": f"Bearer {self.__get_credentials().token}",
                "Content-Type": "application/json"
            },
        )

    def __get_credentials(self):
        """
        Return credentials from Oauth2.0. 
        This method uses the identity of the runner agent by default
        """
        credentials, _ = auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        credentials.refresh(auth.transport.requests.Request())
        return credentials
    

class RDBMS:
    """
    Relational database system wrapper
    """

    def __init__(self, db=None, timeout=60):
        self.db = db
        self.timeout = timeout

    @classmethod
    def from_url(cls, url: str, **kwargs):
        """
        Initiate db management system from URL
        """
        try:
            db = create_engine(url, pool_pre_ping=True)
            return cls(
                db=db,
                timeout=kwargs.get("timeout", 60)
            )
        except ConnectionError:
            logging.warning(
                "RDBMS is not available, setup relational database to allow storing chat session history")
            return cls(
                db=None
            )


class CacheLocal(dict):

    def set(self, keyname, value, **kwargs):
        self.setdefault(keyname, value)


class CacheMS:
    """
    Cache management system wrapper
    """
    def __init__(self, cache, expire_time_second):
        self.expire_time_second = expire_time_second
        self.cache = cache

    @classmethod
    def from_url(cls, url: str, **kwargs):
        """
        Initiate cache management system from URL
        """
        try:
            cache = redis.Redis.from_url(url)
            cache.ping()
            logging.info("Cache is available through Redis server.")
            return cls(
                cache=cache,
                expire_time_second=kwargs.get("expire_time_second", 60)
            )
        except ConnectionError:
            logging.warning(
                "Cache server cannot be connected at the moment, try it later.")
            return cls(
                cache=CacheLocal(),
                expire_time_second=None
            )
        except:
            logging.warning(
                "Cache is not available, setup Redis cache to accelerate searching.")
            return cls(
                cache=CacheLocal(),
                expire_time_second=None
            )

    def set(self, key: str, value: Any, **kwargs):
        """
        Push general value to cache
        """
        self.cache.set(key, pickle.dumps(value), **kwargs)

    def get(self, key: str, default: Any, **kwargs):
        """
        Get general value from cache
        """
        value_serialized = self.cache.get(key, **kwargs)
        if value_serialized is None:
            value = default
        else:
            value = pickle.loads(value_serialized)
        return value


class SessionHistoryService:
    """
    Manage the chat session history
    """

    def __init__(self, dbclient=None):
        self.rdbms = RDBMS.from_url(dbclient.db.url) if dbclient else None
        self.cachems = CacheMS.from_url(
            dbclient.cache.url) if dbclient else None

    def __load_session_history(self, session_id):
        """
        Load chat message from database
        """
        try:
            with Session(self.rdbms.db) as conn:
                query = select(ChatMessageHistory).where(
                    ChatMessageHistory.session_id == session_id)
                chat_messages = conn.scalars(query).all()
            return chat_messages
        except:
            logging.warning(
                "RDBMS is not available, no session history will be retrieved for this chat session")
            return []

    def __persist_session_history(self, session_id):
        """
        Persist chat message to RDBMS
        """
        chat_message_histories = [ChatMessageHistory.extend(
            chat_message, session_id).to_dict()
            for chat_message in self.cachems.get(f"session_logging_queue:{session_id}", [])
        ]
        try:
            with Session(self.rdbms.db) as conn:
                query = insert(ChatMessageHistory).values(
                    chat_message_histories
                )
                query = query.on_conflict_do_update(
                    constraint="unique_chat_message_id",
                    set_=dict(
                        content=query.excluded.content,
                        author=query.excluded.author,
                    )
                )
                conn.execute(query)
                conn.commit()
        except:
            logging.warning(
                "RDBMS is not available, no session history will be persist for this chat session")
    
    def get_session_history(self, session_id=None):
        """
        Load all session history messages from Cache
        If not available, load from the RDBMS
        """
        if not session_id:
            return []
        materialized_messages = [h.base() for h in self.__load_session_history(session_id)]
        cached_messages = self.cachems.get(f"session_logging_queue:{session_id}", [])
        return materialized_messages + cached_messages

    def log_session_history(self, session_id, chat_message):
        """
        Queue the chat message to CacheMS
        """
        temp_queue = self.cachems.get(f"session_logging_queue:{session_id}", [])
        last_logging_timestamp = self.cachems.get(f"session_logging_timestamp:{session_id}", int(time.time()))
        time_gap = int(time.time()) - last_logging_timestamp
        if len(temp_queue) >= 6 or time_gap >= 60:
            self.__persist_session_history(session_id)
            temp_queue = []
        temp_queue.append(chat_message)
        self.cachems.set(
            f"session_logging_queue:{session_id}",
            temp_queue
        )
        self.cachems.set(
            f"session_logging_timestamp:{session_id}",
            int(time.time())
        )