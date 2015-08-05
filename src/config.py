

class MakeConfig():
  def __init__():
#    how many schedules should the script attempt to create
#    (this is not VALID schedules, just schedules in general)
#    Of these, the valid ones will be scored.
#    Larger values will mean more chance of randomly coming across a better
#    schedule, but computational time will scale directly with this number.
     self.generate_this_many_schedules = 200

#    For each of the above schedules, we will make this many attempts
#    at finding a maximal-independent-set of the correct length.
#    Smaller numbers are fine for sparse timetables, but more densly packed
#    timetables require many more iterations to find the best.
     self.maximum_attempts_per_schedule = 10












config = makeConfig()

