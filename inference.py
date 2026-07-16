from ollama import chat, ShowResponse, show, ChatResponse, list
import ollama 

class InferenceEngine:
    def __init__(self):
        self.models = [m.model for m in ollama.list().models] #gemma 3:1b is also avaliable
        self.active_model: str = None
    
    def loadModel (self, model_name:str):
        model_name = model_name.strip()

        if model_name in [m.strip() for m in self.models]:
            self.active_model = model_name
        else:
            raise ValueError(f"Model '{model_name}' is not available.")

    def modelInfo(self):
        if self.active_model is None:
            raise ValueError("No active model set. Please set an active model before retrieving model info.")
        
        # Assuming the model info can be retrieved from the chat function
        response: ShowResponse = show(self.active_model)
        print('Model Information:')
        print(f'Modified at:   {response.modified_at}')
        print(f'Template:      {response.template}')
        print(f'Modelfile:     {response.modelfile}')
        print(f'License:       {response.license}')
        print(f'Details:       {response.details}')
        print(f'Model Info:    {response.modelinfo}')
        print(f'Parameters:    {response.parameters}')
        print(f'Capabilities:  {response.capabilities}')


    def generate(self, prompt: str, tools:list[dict] = None) -> ChatResponse:
        if self.active_model is None:
            raise ValueError("No active model set. Please set an active model before generating.")

        # safegaurd would check and sanitize prompt here
        # The prompt is now a list containing the context and the user input, which is passed to the chat function
        response : ChatResponse = chat (self.active_model, messages=prompt, tools=tools)

        # safegaurd would check response here

        return response
    

        