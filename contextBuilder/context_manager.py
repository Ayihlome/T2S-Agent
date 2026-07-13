from contextBuilder.sys_prompt import system_prompt

class ContextBuilder:
    def __init__(self):
        self.max_tokens = 128000
        self.system_prompt = system_prompt
        self.context_window = 88000
        self.history= []

    def tokenizer(self, prompt):
        estimated_tokens = len(prompt) // 4
        return estimated_tokens
    
    def add_to_history(self, input):
        # Add user input to history
        if isinstance(input, dict):
            self.history.append(input)
        elif isinstance(input, str):
            self.history.append({"role": "user", "content": input})
        
    def build_context(self):
        # Build context with system prompt and history
        context = [{"role":"system", "content": self.system_prompt}]
        context.extend(self.history)
    
        # Estimate tokens and check against max_tokens
        estimated_tokens = self.tokenizer(context)
        if self.max_tokens is not None and estimated_tokens > self.context_window:
            # If context exceeds max tokens, truncate history
            while estimated_tokens > self.context_window and len(self.history) > 0:
                del self.history[0:2] # Remove the last 2 entries from history
                context = [{"role":"system", "content": self.system_prompt}]
                context.extend(self.history)
                estimated_tokens = self.tokenizer(context)

        return context


