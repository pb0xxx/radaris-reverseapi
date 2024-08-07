class Result:
    """
    Class representing a search result.
    
    Attributes:
    - name: name of the person
    - href: URL to the person's profile
    """
    def __init__(self, name, href):
        self.name = name
        self.href = href