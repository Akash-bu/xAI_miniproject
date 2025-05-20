from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF
from collections import defaultdict
import json


g = Graph()
g.parse('aifbfixed_complete.n3', format='n3')

g.serialize(destination='aifb_2005.owl', format = 'xml')

person_type = URIRef("http://swrc.ontoware.org/ontology#Person")
people = set(s for s, p, o in g.triples((None, RDF.type, person_type)))
print("Total people:", len(people))

# Count affiliations
affiliation = URIRef("http://swrc.ontoware.org/ontology#affiliation")

affiliations = set(o for s, p, o in g.triples((None, affiliation, None)))
print("Total distinct affiliations:", len(affiliations))

# to Count affiliations
affiliation_count = defaultdict(int)

for s, p, o in g.triples((None, RDF.type, person_type)):
    for _, _, aff in g.triples((s, affiliation, None)):
        aff_id = str(aff).split("/")[-1]  # e.g., 'id1instance'
        affiliation_count[aff_id] += 1


for aff, count in affiliation_count.items():
    print(f"Affiliation: {aff} ({count} persons)")

all_people = set(s for s, _, _ in g.triples((None, RDF.type, person_type)))
affiliated_people = set(s for s, _, _ in g.triples((None, affiliation, None)))

unaffiliated_people = all_people - affiliated_people
print("People with no affiliation:", len(unaffiliated_people))

target_group = "http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id1instance"

positive_examples = set()
negative_examples = set()

for s, p, o in g.triples((None, affiliation, None)):
    s_str = str(s)
    o_str = str(o)

    if o_str == target_group:
        positive_examples.add(s_str)
    else:
        negative_examples.add(s_str)

# print('Postive examples: ',positive_examples, "\n\n\n")

# print('Negative examples: ',negative_examples)

data = {
    'id1instance': {
        'positive_examples': list(positive_examples),
        'negative_examples': list(negative_examples)
    }
}

with open('id1instance_examples_2005.json', 'w') as f:
    json.dump(data, f, indent = 2)

print('Done!')