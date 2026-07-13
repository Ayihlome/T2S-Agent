from ollama import chat, ShowResponse, show

class InferenceEngine:
    def __init__(self):
        self.models = ['gemma3:1b']
        self.active_model: str = None
    
    def loadModel (self, model_name:str):
        if model_name in self.models:
            self.active_model = model_name  #don't load a model we dont have locally
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


    def generate(self, prompt: str) -> str:
        if self.active_model is None:
            raise ValueError("No active model set. Please set an active model before generating.")

        # safegaurd would check and sanitize prompt here
        # The prompt is now a list containing the context and the user input, which is passed to the chat function
        response = chat(self.active_model, messages=prompt)

        # safegaurd would check response here

        return response['message']['content']
    

        