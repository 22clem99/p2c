from cli import Cmd, CmdProject, CmdExit
from cli import CLIEventExit, CLIEventCmdSuccessful
from fsm.FSMProjectManager import *
from data_modele.project import P2CProject

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

            # The list command is not managed as other subcmd
            # this function just display the list of project open
            # and doesn't interact with project or FSM's project
            if cmd.subcmd == CmdProject.SubCmdProject.LIST_:
                output = self.__get_project_list_as_str()
            # The create command is not managed as other subcmd
            # this function will create a new project object with is own
            # FSM
            elif cmd.subcmd == CmdProject.SubCmdProject.CREATE:
                project = P2CProject(name=cmd.project_name)
                fsm = FSMProjectManager()
                self.projects[project.uid] = (project, fsm)
                output = f"New project created with the UID {project.uid:8} created"
            else:
                logger.debug(f"Project '{cmd.project_name}' exit")

            return output

        # def __is_project_exist(self, uid):
        #     for project in self.projects:
        #         if project.uid == name:
        #             return True
        #     return False

        def __get_project_list_as_str(self):
            name_str_col = "Name"
            uid_str_col  = "UID"

            list_of_projects =f"|{name_str_col:15}|{uid_str_col:9}|"
            list_of_projects =f"{len(list_of_projects)*"-"}\n{list_of_projects}\n{len(list_of_projects)*"-"}\n"

            for key, project in self.projects.items():
                list_of_projects += f"|{project.name:14} |{project.uid:8} |\n"
            return list_of_projects

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
