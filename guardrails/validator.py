import re

# input validation
def queryValidation(query):
    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    
    # check if its a string (numbers are fine)
    if not re.fullmatch(r"^[A-Za-z0-9\s.,?!'\"()-]+$", query):
        raise ValueError("No special letters allowed")
    
    # flag words like DROP, DELETE, etc
    flaggedTerms = r"\b(DROP|DELETE|TRUNCATE|ALTER|INSERT|UPDATE)\b"
    if re.search(flaggedTerms, query, re.IGNORECASE):
        raise ValueError("Invalid input")


# tool permissions
def toolCallValidation(tool_call, state):
    if not isinstance(tool_call, str):
        return TypeError("Tool call is not a string")
    
    # Determine the SQL operation is allowed
    flaggedOps = r"b\(SELECT|JOIN|WHERE| LEFT JOIN| RIGHT JOIN| INNER JOIN| FULL JOIN)"
    if not  re.search(flaggedOps, tool_call, re.IGNORECASE):
        # check permissions 
        if state["permissions"] == "Limited Access":
            raise PermissionError("Tool request not permitted")
        
        if state["permissions"] == "Seek Approval":
            seekApproval(tool_call)

def seekApproval(tool_call):
    choice = str(input(f"Agent requested to run this command: '{tool_call}' \nDo you approve (Y/N): "))
    
    if isinstance(choice, str):
        if choice.upper == "Y" :
            return True
        if choice.upper == "N":
            raise PermissionError("Tool request not permitted")
        
        raise ValueError("Incorrect Input")
    raise TypeError("Incorrect Input")

# tool output validation
# filter for sensitive information