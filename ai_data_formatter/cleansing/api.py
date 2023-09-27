from google import auth
import vertexai


class VertexAIAgent:

    def __init__(self, project_id, location):
        vertexai.init(
            project=project_id,
            location=location,
            credentials=self.__get_credentials()
        )

    def __get_credentials(self):
        """
        Return credentials from Oauth2.0. 
        This method use the identity of the runner agent by default
        """
        credentials, _ = auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        credentials.refresh(auth.transport.requests.Request())
        return credentials
        
    
