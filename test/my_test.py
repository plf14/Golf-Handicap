from app.handicap import calc_handicap
from app.post import calc_differential
import pytest

def test_calc_handicap():
    """
    This function tests the calc_handicap function which is called upon when a user clicks to calculate their handicap
    This function tests both positive and negative handicaps (negative handicaps are expressed as '+#')
    """
    differentials = [
        5, 5, 2, 3, 4,
        5, 0, 7, 5, 2, 
        4, 8, 6, 1, 4, 
        2, 4, 3, 3, 12
    ]
    differentials_2 = [
        5, 5, -2, -3, 4,
        5, 0, 7, 5, -2, 
        4, 8, 6, -1, 4, 
        -2, 4, -3, -3, 12
    ]
    num_scores = 20
    result = calc_handicap(differentials, num_scores)
    result_2 = calc_handicap(differentials_2, num_scores)
    assert result == 2
    assert result_2 == "+2.0"


def test_calc_differential():
    """
    This function tests the calc_differential function which is called upon when a user posts their score
    """
    score = 83
    rating = 72
    slope = 113
    result = calc_differential(score, rating, slope)
    assert result == 11
