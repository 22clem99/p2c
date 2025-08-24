from cli import Cmd, CmdProject, CmdExit
from cli import CLIEventExit, CLIEventCmdSuccessful
from fsm.FSMProjectManager import *
from data_modele.project import P2CProject

from prettytable import PrettyTable

from statemachine import exceptions

import logging

logger = logging.getLogger(__name__)

class P2CCmdExecutor:
    def __init__(self, queue_input=None, queue_output=None):
        self.queue_input  = queue_input
        self.queue_output = queue_output
        self.cmd_project_exec = self.CmdProjectExecutor()

    class CmdProjectExecutor:
        def __init__(self):
            # This dict must contain a couple key (project name)/ Project (class represent a project)
            self.projects = dict()
            self.active_project = None

        def exec_project_cmd(self, cmd: CmdProject):
            output = ""

            if cmd.subcmd == CmdProject.SubCmdProject.LIST_:
                output = self.__get_project_list_as_str()
            elif cmd.subcmd == CmdProject.SubCmdProject.CREATE:
                project = P2CProject(name=cmd.parsed_args["name"])
                self.projects[project.uid] = project
                output = f"New project created with the UID {project.uid:8} created"

                # Send event to the FSM
                self.projects[project.uid].fsm.send_cmd_event("t_create", cmd)
            else:
                project = self.projects[cmd.parsed_args["uid"]]

                if cmd.subcmd == CmdProject.SubCmdProject.OPEN:
                    event = "t_open"
                elif cmd.subcmd == CmdProject.SubCmdProject.SAVE:
                    event = "t_save"
                elif cmd.subcmd == CmdProject.SubCmdProject.DELETE:
                    event = "t_delete"
                elif cmd.subcmd == CmdProject.SubCmdProject.CLOSE:
                    event = "t_close"
                elif cmd.subcmd == CmdProject.SubCmdProject.SETACTIVE:
                    event = "t_set_active"
                elif cmd.subcmd == CmdProject.SubCmdProject.UNSETACTIVE:
                    event = "t_set_unactive"
                else:
                    logger.fatal("Subcmd unknow")
                    exit(2)
                # Send to the FSM the CMD
                try:
                    self.projects[project.uid].fsm.send_cmd_event(event, cmd)
                except exceptions.TransitionNotAllowed:
                    output = f"Can't run the command {cmd.subcmd} as the project is in the state {project.fsm.current_state}"
            return output

        def __get_project_list_as_str(self):

            table = PrettyTable()
            table.field_names = ["Name", "UID", "Active"]
            table.align = 'l'
            table.align["Acvtive"] = 'c'
            table.max_width = 15

            for key, project in self.projects.items():
                table.add_row([project.name, project.uid, f"{"Yes" if project.fsm.is_active() else ""}"])

            return table

    class CmdNodeExecutor:
        pass

    def cmd_executor(self):
        while True:
            cmd = self.queue_input.get()
            if isinstance(cmd, CmdExit):
                logger.debug("An Exit command has been catch by the executor")
                self.queue_output.put(CLIEventExit())
                break
            elif isinstance(cmd, CmdProject):
                output = self.cmd_project_exec.exec_project_cmd(cmd)
                self.queue_output.put(CLIEventCmdSuccessful(output))
            else:
                pass

        logger.info("Executor is about to be finished")
        exit(0)
