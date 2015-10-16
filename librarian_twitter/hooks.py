from .menuitems import TwitterMenuItem


def initialize(supervisor):
    supervisor.exts.menuitems.register(TwitterMenuItem)
