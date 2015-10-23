from tasks import check_for_tweets
from .menuitems import TwitterMenuItem


def initialize(supervisor):
    supervisor.exts.menuitems.register(TwitterMenuItem)


def post_start(supervisor):
    refresh_rate = supervisor.config['twitter.refresh_rate']
    if not refresh_rate:
        return
    supervisor.exts.tasks.schedule(check_for_tweets,
                                   args=(supervisor,),
                                   delay=refresh_rate,
                                   periodic=False)
