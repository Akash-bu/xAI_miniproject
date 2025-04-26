import json
from ontolearn.knowledge_base import KnowledgeBase
from ontolearn.concept_learner import EvoLearner
from ontolearn.learning_problem import PosNegLPStandard
from owlapy.owl_individual import OWLNamedIndividual, IRI
from owlapy.class_expression import OWLClass
from ontolearn.metrics import F1, Accuracy
from ontolearn.utils.static_funcs import verbalize

with open('id1instance_examples.json') as f:
    settings = json.load(f)

kb = KnowledgeBase(path = settings['data_path'])

for target_concept, examples in settings['problems'].items():

    p = set(examples['positive_examples'])
    n = set(examples['negative_examples'])

    print(len(p), '\n\n')
    print(len(n), '\n\n')

    # Ignore owl:Thing to prevent duplicate terminal names
    ignored_classes = {
        OWLClass(IRI.create("http://www.w3.org/2002/07/owl#Thing"))
    }
    target_kb = kb.ignore_and_copy(ignored_classes=ignored_classes)
    

    print(len(list(target_kb.individuals())))

    print("Individual list:")
    for i in target_kb.individuals():
        print(i)


    typed_pos = set(map(OWLNamedIndividual, map(IRI.create, p)))
    typed_neg = set(map(OWLNamedIndividual, map(IRI.create, n)))
    lp = PosNegLPStandard(pos = typed_pos, neg = typed_neg)


    model = EvoLearner(knowledge_base = target_kb, max_runtime = 600)

    model.fit(lp, verbose = False)

    model.save_best_hypothesis(n = 5, path = 'Predictions_{0}'.format(target_concept))

    hypotheses = list(model.best_hypotheses(n = 5))

    all_individual = list(typed_pos.union(typed_neg))

    predictions = model.predict(individuals = all_individuals, hypotheses = hypotheses)

    [print(_) for _ in hypotheses]

# verbalize()