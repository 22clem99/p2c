from cli import P2CShell, CmdExit
from executor import P2CCmdExecutor
import threading
import queue
import logging

'''
Logger utilities
'''
logging.basicConfig(level=logging.DEBUG)
p2c_logger = logging.getLogger(__name__)

'''
This queue is used to send CMD from generator thread of CMD (CLI and GUI)
to the consumer thread (CMD executor)
'''
q = queue.Queue()


'''
Create the P2C shell as a thread
'''
p2c_shell = P2CShell(queue=q)
CLI_thread = threading.Thread(target=p2c_shell.cmdloop)
CLI_thread.start()


'''
Create the command executor as a Thread
'''
p2c_executor = P2CCmdExecutor(queue=q)
exec_thread = threading.Thread(target=p2c_executor.cmd_executor)
exec_thread.start()

# while True:
#     item = q.get()
#     print(f"Un objet ! {item} of {type(item)=}")
#     if isinstance(item, CmdExit):
#         print("exit !!!!!!!!!!!")

'''
As the executor execute command, if a command need to stopped all the
application, the return of this function do need to kill other
thread
'''
exec_thread.join()
p2c_logger.debug("The executor thread finished")

CLI_thread.join()
p2c_logger.debug("The CLI thread finished")

p2c_logger.info("Exit P2C! Have a nice day :)")