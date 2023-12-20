import os
import time
import uuid
from ratelimiter import RateLimiter
from io import StringIO
import pandas as pd

from vertexai.language_models import CodeChatModel
from vertexai.language_models._language_models import ChatMessage
from ..core.api import VertexAIAgent, SessionHistoryService, ChatSessionEndpoint
from ..utils.prompt import freeform_prompt, web_search_prompt, proprietary_search_prompt

rate_limiter = RateLimiter(max_calls=50, period=60)


class ChatModel():
    """
    Model interface
    """

    def preprocess(self, input):
        """
        Specify how to format the input
        """
        return input

    def postprocess(self, output):
        """
        Specify how to clean up the output
        """
        return output

    def send_message(self, input):
        """
        Generate content for given input, with instruction from
        structured prompt
        """
        if input == "" or not input:
            self.preprocess("")
            return self.postprocess("")
        input_text = self.preprocess(input)

        response = self.chat_session.send_message(
            input_text
        )

        return self.postprocess(response.text)

    def train(self, data):
        raise NotImplementedError("Training interface is not implemented")


class PromptCodeChatSession(ChatModel, VertexAIAgent, SessionHistoryService):
    """
    Initialize the pre-trained model with custom prompt design
    """

    def __init__(
        self,
        project_id,
        location,
        model_config,
        session_id=None,
        dbclient=None,
        pre_load_model=False
    ):
        VertexAIAgent.__init__(self, project_id, location)
        SessionHistoryService.__init__(self, dbclient)
        self.parameters = model_config.parameters
        self.prompt = model_config.prompt
        self.model_id = model_config.model_id
        self.pre_load_model = pre_load_model
        if session_id:
            self.message_history = self.get_session_history(session_id=session_id)
            self._session_id = session_id
        else:
            self.message_history = []
            self._session_id = uuid.uuid4().hex
        
        if self.pre_load_model == True:
            self.chat_session = CodeChatModel.from_pretrained(
                    self.model_id
                ).start_chat(
                    context=self.prompt.context,
                    message_history=self.message_history,
                    **self.parameters
                )
        else:
            self.chat_session = ChatSessionEndpoint(
                model_api_endpoint=self.model_api_endpoint,
                model_id=self.model_id,
                context=self.prompt.context,
                parameters=self.parameters,
                message_history=self.message_history
            )
    
    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self.message_history = self.get_session_history(session_id=session_id)
        if self.pre_load_model == True:
            self.chat_session = CodeChatModel.from_pretrained(
                self.model_id
            ).start_chat(
                context=self.prompt.context,
                message_history=self.message_history,
                **self.parameters
            )
        else:
            self.chat_session = ChatSessionEndpoint(
                model_api_endpoint=self.model_api_endpoint,
                model_id=self.model_id,
                context=self.prompt.context,
                parameters=self.parameters,
                message_history=self.message_history
            )
        self._session_id = session_id

    def preprocess(self, input):
        """
        Specify how to format the input
        """
        raw_message = freeform_prompt(input, self.prompt)
        ## Log the message
        self.log_session_history(self._session_id, ChatMessage(
            content=raw_message, author="user"))
        return raw_message

    def postprocess(self, output):
        """
        Create chat message and share back
        Attach author
        """
        ## Log the message
        self.log_session_history(self._session_id, ChatMessage(
            content=output, author="bot"))
        return output

    def pandas2str(self, sample_data: pd.DataFrame):
        """
        Convert dataframe to string
        """
        csv_buffer = StringIO()
        sample_data.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
    
    def send_sample_data(self, input):
        """
        Provide some sample data for the AI Agent to remember.
        It will use this to test the generated code.
        """
        sample_data_text = f"remember these sample data for later testing. {input}"
        self.log_session_history(self._session_id, ChatMessage(
            content=sample_data_text, author="user"))
        response = self.chat_session.send_message(
            sample_data_text
        )
        return self.postprocess(response.text)
    
    def send_web_search(self, input, **kwargs):
        """
        Search the web
        """
        search_query = web_search_prompt(
            input,
            self.prompt,
            ua=kwargs.get("ua", None),
            number_results=kwargs.get("number_results", 5)
        )
        self.log_session_history(self._session_id, ChatMessage(
            content=search_query, author="user"))
        response = self.chat_session.send_message(
            search_query
        )
        return self.postprocess(response.text)
    
    def send_proprietary_search(self, input, **kwargs):
        """
        Search the proprietary github repositories
        """
        search_query = proprietary_search_prompt(
            input,
            self.prompt,
            number_results=kwargs.get("number_results", 5)
        )
        self.log_session_history(self._session_id, ChatMessage(
            content=search_query, author="user"))
        response = self.chat_session.send_message(
            search_query
        )
        return self.postprocess(response.text)