import numpy as np
from collections import defaultdict
from operator import itemgetter
dataset_filename = "/Users/kddr/PycharmProjects/affinity_dataset.txt"
X = np.loadtxt(dataset_filename)
n_samples, n_features = X.shape
print("This dataset has {0} samples and {1} features".format(n_samples, n_features))
valid_rules=defaultdict(int)
invalid_rules=defaultdict(int)
num_occurances=defaultdict(int)
features = ["bread", "milk", "cheese", "apples", "bananas"]
for sample in X:
    for premis in range(4):
        if sample[premis]==0:
            continue
        num_occurances[premis]+=1
        for conclusion in range(n_features):
            if premis==conclusion:
                continue
            if sample[conclusion]==1:
                valid_rules[(premis,conclusion)]+=1
            else:
                invalid_rules[(premis,conclusion)]+=1
support =valid_rules
confidence=defaultdict(float)
for premis,conclusion in valid_rules.keys():
    rule=(premis,conclusion)
    confidence[rule]=valid_rules[rule]/num_occurances[premis]


#for premise, conclusion in confidence:
#    premise_name = features[premise]
#    conclusion_name = features[conclusion]
#    print("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
#    print(" - Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
#    print(" - Support: {0}".format(support[(premise, conclusion)]))
#    print("")


def print_rule(premise,conclusion,supoort,confidence,features):
    premis_name=features[premise]
    conclusion_name=features[conclusion]
    print("Rule:If a presion buys {0} then will also buy {1}".format(premis_name,conclusion_name))
    print("-Support:{0}".format(support[(premise,conclusion)]))
    print("-Confidence:{0:.3f}".format(confidence[(premise,conclusion)]))
premise = 3
conclusion = 1
#print_rule(premise, conclusion, support, confidence, features)

sorted_support=sorted(support.items(),key=itemgetter(1),reverse=True)
for index in range(5):
    print("Rule #{0}".format(index+1))
    premise,conclusion=sorted_support[index][0]
    print_rule(premise,conclusion,support,confidence,features)
sorted_confidence=sorted(confidence.items(),key=itemgetter(1),reverse=True)
for index in range(5):
    print("Rule #{0}".format(index+1))
    premise,conclusion=sorted_confidence[index][0]
    print_rule(premise,conclusion,support,confidence,features)