def validatePrompt(prompt):
    if not isinstance(prompt, str):
        raise ValueError("Prompt must be a string")
    
    # ensure prompt does not delete tables or rows
    if "DELETE" in prompt.upper():
        raise ValueError("Prompt contains disallowed DELETE operation")
    
    # ensure prompt does not drop tables
    if "DROP" in prompt.upper():
        raise ValueError("Prompt contains disallowed DROP operation")
    
    if "TRUNCATE" in prompt.upper():
        raise ValueError("Prompt contains disallowed TRUNCATE operation")
    
    if "ALTER" in prompt.upper():
        raise ValueError("Prompt contains disallowed ALTER operation")
    
    if "UPDATE" in prompt.upper():
        raise ValueError("Prompt contains disallowed UPDATE operation")
    
    if "INSERT" in prompt.upper():
        raise ValueError("Prompt contains disallowed INSERT operation")

def validateResponse(response):
    if not isinstance(response, str):
        raise ValueError("Response must be a string")
    
    # Add any additional validation logic for the response here
