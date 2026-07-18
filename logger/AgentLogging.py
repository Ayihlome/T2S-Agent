class AgentLogger:
    @staticmethod
    def llm(response):
        print("-----LLM-----")
        print(response)
    
    @staticmethod
    def tools(name, agrs):
        print("----Tool Call----")
        print("Tool: ", name)
        print("Arguments: ", agrs)
    
    @staticmethod
    def results(output):
        print("----Tool Results----")
        print(output)
    
    @staticmethod
    def context(window:list):
        print("----Context Window---")
        for msg in window:
            print(msg)