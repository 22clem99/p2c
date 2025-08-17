from cli import P2CShell, CmdExit
import threading
import queue
import logging

# format = ""

# logging.basicConfig(format=format)
logging.basicConfig(level=logging.DEBUG)

p2c_logger = logging.getLogger('P2C')

q = queue.Queue()

p2c_shell = P2CShell(queue=q)

CLI_thread = threading.Thread(target=p2c_shell.cmdloop)

CLI_thread.start()

while True:
    item = q.get()
    print(f"Un objet ! {item} of {type(item)=}")
    if isinstance(item, CmdExit):
        print("exit !!!!!!!!!!!")