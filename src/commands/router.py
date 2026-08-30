import logging
logger = logging.getLogger(__name__)

class CommandRouter:

    def __init__(self):
        self.commands = {}

    def register(self, name, handler):
        """Register a command handler."""
        self.commands[name] = handler

    def handle(self, message: str, user_id: str) -> str:
        """Route an incoming message to the appropriate handler."""

        message = message.strip()
        #logger.debug(user_id)
        logger.debug(f"msg: {message}, user_id: {user_id}")
        if not message:
            return "No command provided."

        parts = message.split()

        command = parts[0].lower()
      
        # Remove the leading /
        command = command.lstrip("/")

        args = parts[1:]
       
        handler = self.commands.get(command)

        if handler is None:
            return f"Unknown command: {command}"
        
        try:
           
            return handler.execute(args, user_id)

        except Exception:
            logger.exception(
                "Error executing command: %s",
                command,
            )

            return "An error occurred while executing the command."
