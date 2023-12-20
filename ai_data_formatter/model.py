from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field, fields
from dataclasses_json.cfg import config
from dataclasses_json import dataclass_json
from sqlalchemy import String, MetaData, Table, Column, Integer, Identity
from sqlalchemy.orm import registry
from vertexai.language_models._language_models import ChatMessage


mapper_registry = registry()
metadata_obj = MetaData()


@dataclass_json
@dataclass
class ChatMessageHistory(ChatMessage):

    id: int = field(init=False, metadata=config(exclude=lambda x:True))
    session_id: str = None
    timestamp: str = None

    def base(self):
        return ChatMessage(self.content, self.author)

    @classmethod
    def extend(
        cls,
        chat_message: ChatMessage,
        session_id: str
    ):
        return cls(
            content=chat_message.content,
            author=chat_message.author,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )


"""
CREATE TABLE public.chat_message_history (
	id serial NOT NULL,
	"content" varchar NULL,
	author varchar NULL,
	session_id varchar NOT NULL,
	"timestamp" varchar NOT null,
	CONSTRAINT chat_message_history_pk PRIMARY KEY (id)
);

CREATE UNIQUE INDEX chat_message_idx on chat_message_history (session_id, timestamp);

ALTER TABLE chat_message_history 
ADD CONSTRAINT unique_chat_message_id
UNIQUE USING INDEX chat_message_idx;
"""


chat_message_history = Table(
    "chat_message_history",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("content", String()),
    Column("author", String(32)),
    Column("session_id", String(32)),
    Column("timestamp", String(50))
)

mapper_registry.map_imperatively(ChatMessageHistory, chat_message_history)
