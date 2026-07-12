from inference import InferenceEngine

llm = InferenceEngine()

llm.loadModel(model_name="gemma3:1b")

model = llm.modelInfo()
print(model)

prompt = "What is the capital of France?"


response = llm.generate(prompt=prompt)
print(response)

