from src.evaluation import score_seniority, score_comp, score_list, validate_prediction

def test_seniority():
    assert score_seniority('Senior', 'senior') == 1.0
    assert score_seniority('mid', 'senior') == 0.0

def test_comp():
    assert score_comp(None, None) == 1.0
    assert score_comp(None, 2000) == 0.0
    assert score_comp(105000, 100000) == 1.0
    assert score_comp(130000, 100000) == 0.0
    assert score_comp(110000, 100000) == 1.0

def test_list():
    assert score_list(None, None) == 1.0
    assert score_list(None, ['a', 'b']) == 0.0
    assert score_list([], []) == 1.0
    assert score_list(['a', 'b'], ['a', 'b']) == 1.0
    assert score_list(['a', 'b'], ['a', 'c']) == 0.5
    assert score_list(['a', 'b'], ['y', 'z']) == 0.0

def test_validate_prediction():
    good = {
    "required_skills": ["problem solving", "communication"],
    "tech_stack": ["Python", "AWS"],
    "seniority": "senior",
    "avg_comp_range": 150000,
    }
    assert validate_prediction(good) is not None

    bad_seniority = {
    "required_skills": ["problem solving"],
    "tech_stack": ["Python"],
    "seniority": "principal",
    "avg_comp_range": 150000,
    }
    assert validate_prediction(bad_seniority) is None

    bad_comp = {
    "required_skills": ["problem solving"],
    "tech_stack": ["Python"],
    "seniority": "senior",
    "avg_comp_range": "200k",
    }
    assert validate_prediction(bad_comp) is None
