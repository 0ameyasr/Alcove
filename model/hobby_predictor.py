from hobby_model import linear_predictor,random_forest_predictor,radial_predictor,decision_tree_predictor,k_nearest_predictor,naive_bayes_predictor,logistic_predictor
from hobby_model import survey



scores = survey()
print(f"\n(linear_predictor) Your Hobby: {linear_predictor(scores)}")
print(f"(random_forest_predictor) Your Hobby: {random_forest_predictor(scores)}")
print(f"(radial_predictor) Your Hobby: {radial_predictor(scores)}")
print(f"(decision_tree_predictor) Your Hobby: {decision_tree_predictor(scores)}")
print(f"(k_nearest_predictor) Your Hobby: {k_nearest_predictor(scores)}")
print(f"(naive_bayes_predictor) Your Hobby: {naive_bayes_predictor(scores)}")
print(f"(logistic_predictor) Your Hobby: {logistic_predictor(scores)}\n")