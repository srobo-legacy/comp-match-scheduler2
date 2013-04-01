import constraint
import utils


class MaximiseTeamsConstraint(constraint.Constraint):
    def __init__(self, max_blanks, punishment = 12.0):
        self._punishment = punishment
        self._max_blanks = max_blanks

    def evaluate(self, match):
        number_blank = len([x for x in match if not utils.is_actual_entrant(x)])
        if number_blank > self._max_blanks:
            # this is not a viable match at all
            return float('inf')
        return (self._punishment * 2**number_blank) - self._punishment
