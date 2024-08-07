# Dictionary with possible API responses
response_messages = {
    "not_empty": "The search parameter cannot be empty!",
    "not_success_external": "The remote server response is not successful.",
    "no_results": "No results.",
    "no_summary": "Incomplete information."
}

class ApiResponse:
    """
    Class representing an API response.
    
    Attributes:
    - status: status of the response (0 - OK, 5 - WARN, 10 - ERROR, 20 - FAILURE)
    - response: content of the response (depends on the status)
    - response_id: response identifier
    """
    def __init__(self, response, status):
        self.status = status
        if status == 0:
            self.response = response
        else:
            self.response = response_messages[response]
        self.response_id = response