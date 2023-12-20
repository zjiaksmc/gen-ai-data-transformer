import os
import time
import uuid

import numpy as np
from vertexai.language_models import TextGenerationModel
from ..core.api import VertexAIAgent, TextGenerationEndpoint
from ..utils.prompt import structured_prompt, freeform_prompt

RETRY = 5
RETRY_INTERVAL = 3

class Model:
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
    

    def predict(self, input):
        """
        Generate content for given input, with instruction from
        structured prompt
        """
        if input == "" or not input:
            return (input, input)
        input_text = self.preprocess(input)

        if self.model:
            time_start = time.time()
            while time.time() - time_start <= RETRY_INTERVAL*RETRY:
                try:
                    response = self.model.predict(
                        input_text
                    )
                    output_text = self.postprocess(response.text)
                    return [input, output_text]
                except:
                    time.sleep(RETRY_INTERVAL)
                    continue
            return [input, ""]
        else:
            return [input, ""]
    

    def batch_predict(self, inputs):
        """
        Generate content for given input, with instruction from
        structured prompt
        """
        predict_vt = np.vectorize(
            self.predict,
            otypes=[list]
        )

        return predict_vt(inputs)


    def train(self, data):
        raise NotImplementedError("Training interface is not implemented")


class PromptTextGenModel(Model, VertexAIAgent):
    """
    Initialize the pre-trained model with custom prompt design
    """
    def __init__(
        self, 
        project_id, 
        location,
        model_config,
        pre_load_model=False
    ):
        VertexAIAgent.__init__(self, project_id, location)
        if pre_load_model == True:
            self.model = TextGenerationEndpoint(
                model_api_endpoint=TextGenerationModel.from_pretrained(model_config.model_id),
                model_id=model_config.model_id,
                parameters=model_config.parameters
            )
        else:
            self.model = TextGenerationEndpoint(
                model_api_endpoint=self.model_api_endpoint,
                model_id=model_config.model_id,
                parameters=model_config.parameters
            )
        self.prompt = model_config.prompt


    def preprocess(self, input):
        """
        Specify how to format the input
        """
        return structured_prompt(input, self.prompt)
    

    def postprocess(self, output):
        """
        Specify how to clean up the output
        """
        return output.lstrip().split("\n")[0].strip()


class TunedTextGenModel(Model, VertexAIAgent):
    """
    Initialize the fine-tuned model
    """
    def __init__(
        self, 
        project_id, 
        location,
        model_config,
        pre_load_model=False
    ):
        VertexAIAgent.__init__(project_id, location)
        if pre_load_model == True:
            self.model = TextGenerationEndpoint(
                model_api_endpoint=TextGenerationModel.get_tuned_model(model_config.model_id),
                model_id=model_config.model_id,
                parameters=model_config.parameters
            )
        else:
            self.model = TextGenerationEndpoint(
                model_api_endpoint=self.model_api_endpoint,
                model_id=model_config.model_id,
                parameters=model_config.parameters
            )
        self.prompt = model_config.prompt


    def preprocess(self, input):
        """
        Specify how to format the input
        """
        return freeform_prompt(input, self.prompt)
    

    def postprocess(self, output):
        """
        Specify how to clean up the output
        """
        return output.lstrip().split("\n")[0].strip()
    

    def train(self, data):
        pass