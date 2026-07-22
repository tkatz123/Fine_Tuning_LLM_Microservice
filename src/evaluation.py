import statistics
import json

def score_seniority(predicted: str, true: str) -> float:

    #Cleans predicted values
    clean_predicted = predicted.strip().lower()
    clean_true = true.strip().lower()

    #Returns 1 if predicted and true values match
    if clean_predicted == clean_true:
        return 1.0
    else:
        return 0.0
    
def score_comp(predicted: float | None, true: float | None) -> float:

    #Both null they agree there is no salary
    if predicted is None and true is None:
        return 1.0
    
    #Exactly one is null they disagree
    if predicted is None or true is None:
        return 0.0
    
    clean_predicted = float(predicted)
    clean_true = float(true)

    #return 1 if predicted value is +/- 10% of the true value
    if clean_predicted >= (clean_true * 0.9) and clean_predicted <= (clean_true * 1.1):
        return 1.0
    else:
        return 0.0
    
def score_list(predicted: list[str], true: list[str]) -> float:

    #Checks to see if lists are none or empty first
    if predicted is None and true is None:
        return 1.0

    if predicted is None or true is None:
        return 0.0

    if len(predicted) == 0 and len(true) == 0:
        return 1.0

    #If not null or empty strips and lowers all strings in lists
    pred_set = {s.strip().lower() for s in predicted}
    true_set = {s.strip().lower() for s in true}

    #Gets length of both lists
    tp = len(pred_set & true_set)

    #If length of both lists are 0 return 0
    if tp == 0:
        return 0.0

    #Calculate precision and recalls
    precision = tp / len(pred_set)
    recall = tp / len(true_set)

    #Calculate F1 score
    F1 = 2 * precision * recall / (precision + recall)

    return F1

def score_record(predicted: dict, true: dict) -> dict:

    #Returns a dictionary with a score for each field
    return {
        'seniority': score_seniority(predicted['seniority'], true['seniority']),
        'comp': score_comp(predicted['avg_comp_range'], true['avg_comp_range']),
        'skills': score_list(predicted['required_skills'], true['required_skills']),
        'tech_stack': score_list(predicted['tech_stack'], true['tech_stack'])
    }

def evaluate(predictions: list[dict], true: list[dict]) -> dict:

    #Create empty lists to store scores in
    seniority_scores = []
    comp_scores = []
    skills_scores = []
    tech_scores = []

    #Iterates over both lists in unison, calling the score record function and storing each value in the dedicated list
    for pred, gold in zip(predictions, true):

        result = score_record(pred, gold)

        seniority_scores.append(result['seniority'])
        comp_scores.append(result['comp'])
        skills_scores.append(result['skills'])
        tech_scores.append(result['tech_stack'])

    #Returning the mean score for each list
    return{
        'seniority': statistics.mean(seniority_scores),
        'comp': statistics.mean(comp_scores),
        'skills': statistics.mean(skills_scores),
        'tech_stack': statistics.mean(tech_scores)
    }

if __name__ == "__main__":

    test_data = []

    with open("data/processed/test.jsonl", "r") as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                test_data.append(json.loads(clean_line))

    print(evaluate(test_data, test_data))
