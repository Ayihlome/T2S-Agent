import datetime
import uuid
import json
from dataclasses import dataclass, asdict
from inference import InferenceEngine
from contextBuilder.context_manager import ContextBuilder


contextManager = ContextBuilder()
engine = InferenceEngine()

class AgentLogger:

    def __init__(self):
        self.session = AgentSession(
            session_id = str(uuid.uuid4()),
            trace_id = str(uuid.uuid4())
        )
        self.metrics = Metrics()
        self.conversation = ConversationTrace()
        self.tool_calls = []
    
    def startSession (self):
        self.session.started_at = datetime.datetime.now()
        
    def endSession(self):
        self.session.ended_at = datetime.datetime.now()
        self.metrics.total_latency = self.session.ended_at - self.session.started_at 
        self.metrics.llm_latency = self.session.ended_at - self.session.started_at



    def llm(self, response):
        self.conversation.response = response

    def start_tool(self, tool_request):
        # Initailize a current tool object that will evoke the ToolTrace object between start and finish
        self.conversation.tool = tool_request
        self.current_tool = ToolTrace(
            tool_name=tool_request["tool"],
            arguments=tool_request["arguments"],
            started_at=datetime.datetime.now()
        )
    

    def finish_tool(self, result):
        self.current_tool.result = result
        self.current_tool.ended_at = datetime.datetime.now()
        self.current_tool.duration = self.current_tool.ended_at - self.current_tool.started_at
        self.metrics.tool_latency = self.current_tool.ended_at - self.current_tool.started_at
        self.tool_calls.append(self.current_tool)


    def context(self, window:list[dict]):
        # This happens at the end of the session
        self.metrics.total_tokens = contextManager.tokenizer(json.dumps(window))

    def saveLog(self):
        trace = {
                "session": asdict(self.session),
                "metrics":asdict(self.metrics),
                "tools_called": [asdict(call) for call in self.tool_calls],
                "conversation": asdict(self.conversation)
            }
        
        with open("logs.json", "a+") as file:
            json.dump(trace, file, indent=4, default=str)
            file.write("\n")
            

@dataclass
class AgentSession:
    session_id: str
    trace_id:str 

    started_at: datetime | None = None
    ended_at: datetime | None = None

    model: str = "gemma 4:e2b"

@dataclass
class Metrics:

    prompt_tokens: int = 0 
    completion_tokens: int = 0 
    total_tokens: int = 0 

    llm_latency: float = 0
    tool_latency: float = 0
    total_latency: float = 0

@dataclass
class ConversationTrace:
    prompt: list[dict] | None = None
    response: str | None = None
    tool: dict | None = None

@dataclass
class ToolTrace:

    tool_name: str
    arguments: str
    result: any | None = None

    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration: float | None = None
    
    success: bool | None = None