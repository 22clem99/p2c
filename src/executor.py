from cli import Cmd, CmdProject, CmdExit
from fsm.FSMProjectManager import *

import logging

logger = logging.getLogger(__name__)

class P2CCmdExecutor:
    def __init__(self, queue):
        self.queue = queue
        self.cmd_project_exec = self.CmdProjectExecutor()

        self.__do_exit = False

    class CmdProjectExecutor:
        def __init__(self):
            # This dict must contain a couple key (project name)/ Project (class represent a project)
            self.projects = dict()
            self.active_project = None

        def exec_project_cmd(self, cmd: CmdProject):
            # Test that the project exist
            if cmd.project_name in self.projects:
                project = self.projects[cmd.project_name]
            else:
                pass
                # project = P

    class CmdNodeExecutor:
        pass

    def cmd_executor(self):
        while True:
            cmd = self.queue.get()

            if isinstance(cmd, CmdExit):
                logger.debug("An Exit command has been catch by the executor")
                break
            elif isinstance(cmd, CmdProject):
                self.cmd_project_exec.exec_project_cmd(cmd)
            else:
                pass

        logger.info("Executor is about to be finished")
        exit(0)
