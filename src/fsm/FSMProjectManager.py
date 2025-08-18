from statemachine import State
from statemachine import StateMachine

class FSMProjectManager(StateMachine):
    s_idle = State(initial=True)
    s_create = State()
    s_open_project = State()
    s_delete = State()
    s_close = State()
    s_active = State()
    s_inactive = State()

    t_idle = s_idle.to.itself()

    t_create      = s_idle.to(s_create)
    t_create_done = s_create.to(s_inactive)

    t_open      = s_idle.to(s_open_project)
    t_open_done = s_open_project.to(s_inactive)

    s_inactive = s_inactive.to.itself()

    t_close      = s_inactive.to(s_close)
    t_close_done = s_close.to(s_idle)

    t_delete      = s_inactive.to(s_delete)
    t_delete_done = s_delete.to(s_idle)

    t_save      = s_inactive.to(s_delete)
    t_save_done = s_delete.to(s_idle)

class SubFSMProjectStatus(StateMachine):
