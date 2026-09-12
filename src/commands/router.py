from commands.exceptions import CommandValidationError

import logging
logger = logging.getLogger(__name__)

class CommandRouter:

    def __init__(self, chat):
        self.commands = {}
        self.chat = chat

    def register(self, name, handler):
        """Register a command handler."""
        self.commands[name] = handler

    def handle(self, message: str, user_id: str) -> str:
        """Route an incoming message to the appropriate handler."""

        message = message.strip()

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
        except CommandValidationError as e:
            logger.info(
                "Command validation failed: command=%s user_id=%s reason=%s",
                command,
                user_id,
                e
            )
            self.chat.send(str(e), user_id)
            return None
        except Exception:
            logger.exception(
                "Error executing command: %s",
                command,
            )

            self.chat.send(
                "An error occurred while executing the command.", 
                user_id
            )
            return None
            #return "An error occurred while executing the command."
