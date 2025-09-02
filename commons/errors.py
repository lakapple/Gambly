class UserIsNotAdminError(Exception):
    def __init__(self, message="User is not admin"):
        self.message = message
        super().__init__(self.message)
