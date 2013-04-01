import sched


def partial_schedule(configuration, past_matches):
    scheduler = sched.Scheduler(configuration)
    scheduler.compute_partial_schedule(past_matches)
    return scheduler.matches


def full_schedule(configuration):
    scheduler = sched.Scheduler(configuration)
    scheduler.compute_full_schedule()
    return scheduler.matches
