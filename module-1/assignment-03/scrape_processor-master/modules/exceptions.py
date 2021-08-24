class EmptyProductDescriptionException(Exception):
    def __init__(self, p_name):
        self.p_name = p_name
        self.msg=msg = f'Error: {self.p_name} description.yml is empty p_name'
        Exception.__init__(self, self.msg)   