import os
import time
import uuid

from vertexai.language_models import TextGenerationModel
from .api import VertexAIAgent


class Model:
    """
    Model interface
    """
    
    def predict(self):
        raise NotImplementedError("Predicting interface is not implemented")

    def train(self, data):
        raise NotImplementedError("Training interface is not implemented")


class PromptTextGenModel(Model, VertexAIAgent):

    def __init__(
        self, 
        project_id="generative-ai-demo-398901", 
        location="us-central1",
        model_id="text-bison@001"
    ):
        super().__init__(project_id, location)
        self.model = TextGenerationModel.from_pretrained(model_id)
        self.parameters = {}
    
    def predict(self, input, structured_prompt=None):
        """
        Generate content for given input, with instruction from
        structured prompt
        """
        model_input = structured_prompt.format(input) if structured_prompt else input

        response = self.model.predict(
            model_input, 
            **self.parameters
        )

        return response.text


class TunedTextGenModel(Model, VertexAIAgent):

    def __init__(
        self, 
        project_id="generative-ai-demo-398901", 
        location="us-central1",
        model_id="29s42rdt"
    ):
        super().__init__(project_id, location)
        self.model = TextGenerationModel.get_tuned_model(model_id)
        self.parameters = {}

    def predict(self, input, structured_prompt=None):
        """
        Generate content for given input, with instruction from
        structured prompt
        """
        model_input = structured_prompt.format(input) if structured_prompt else input

        response = self.model.predict(
            model_input, 
            **self.parameters
        )

        return response.text

    def train(self, data):
        pass