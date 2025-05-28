from google.cloud import secretmanager
import os

#PATH = os.get('PATH', None)

def get_secret() -> str:
    """
    Retrieve secret from GCP Secret Manager
    """
   # if PATH:
   #     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH
        
    secret_client = secretmanager.SecretManagerServiceClient()
    name = secret_client.secret_version_path(
        project="733286937483",
        secret="ai-agent-ai-key",
        secret_version="latest"
    )
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
