from statemachine import State
from statemachine import StateMachine
from cli import Cmd, CmdProject


class FSMProjectManager(StateMachine):
    s_idle         = State(initial=True)
    s_create       = State()
    s_open_project = State()
    s_delete       = State()
    s_close        = State()
    s_inactive     = State()
    s_active       = State()
    s_edited   = State()
    s_save     = State()


    t_idle = s_idle.to.itself()

    t_create      = s_idle.to(s_create, cond="is_create_cmd")
    t_create_done = s_create.to(s_inactive)

    t_open      = s_idle.to(s_open_project, cond="is_create_cmd")
    t_open_done = s_open_project.to(s_inactive)

    t_inactive = s_inactive.to.itself()

    t_set_active   = s_inactive.to(s_active, cond="is_create_cmd")
    t_set_inactive = s_active.to(s_inactive)

    t_active = s_active.to.itself()

    t_set_active   = s_active.to(s_edited, cond="is_setactive_cmd")

    t_edited = s_edited.to.itself()

    t_save      = s_edited.to(s_save, cond="is_save_cmd")
    t_save_done = s_save.to(s_active)

    t_close      = s_inactive.to(s_close, cond="is_close_cmd")
    t_close_done = s_close.to(s_idle)

    t_delete      = s_inactive.to(s_delete, cond="is_delete_cmd")
    t_delete_done = s_delete.to(s_idle)

    async def is_create_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.CREATE

    async def is_open_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.OPEN

    async def is_save_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.SAVE

    async def is_delete_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.DELETE

    async def is_close_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.CLOSE

    async def is_setactive_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.SETACTIVE

    async def is_unsetactive_cmd(self, cmd: CmdProject):
        return cmd.subcmd == CmdProject.SubCmdProject.UNSETACTIVE

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

    def do_create_state(self):
        pass

