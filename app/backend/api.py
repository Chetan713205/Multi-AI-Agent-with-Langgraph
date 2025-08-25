from fastapi import FastAPI, HTTPException # Displays the Error details 403, 200, 404
from pydantic import BaseModel # is used to define the structure and data types of your request
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings 
from app.common.custom_exception import CustomException
from app.common.logger import get_logger 

logger = get_logger(__name__) 

app = FastAPI(title = "Multi AI Agent")

class RequestState(BaseModel): 
    model_name : str
    system_prompt : str 
    messages : list[str]
    allow_search : bool
    
@app.post('/chat')  # When a POST request is made to the /chat URL, run the function below 
def chat_endpoint(request : RequestState):
    logger.info(f"Received request for model : {request.model_name}")
    
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.error(f"Model {request.model_name} is not allowed")
        raise HTTPException(status_code = 403, detail = "Invalid Model Name")
    
    try: 
        response = get_response_from_ai_agents(
            model_name=request.model_name,
            system_prompt=request.system_prompt,
            messages=request.messages,
            allow_search=request.allow_search
        )
        logger.info(f"Sucessfully got response from AI Agent{request.model_name}")
        return {"response" : response}
    
    except CustomException as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")