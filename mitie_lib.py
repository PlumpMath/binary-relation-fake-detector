import sys
import os

mitie_path = os.environ['MITIE_HOME']
sys.path.append(mitie_path)

from mitie import *
import itertools

binary_relation_models_path = mitie_path + "MITIE-models/english/binary_relations/"

binary_relation_type_to_model_path = {
    "BORN IN": binary_relation_models_path + "rel_classifier_people.person.place_of_birth.svm",
    "DIED IN": binary_relation_models_path + "rel_classifier_people.deceased_person.place_of_death.svm",
    "INVENTED": binary_relation_models_path + "rel_classifier_law.inventor.inventions.svm",
    "ETHNICITY": binary_relation_models_path + "rel_classifier_people.person.ethnicity.svm",
    "RELIGION": binary_relation_models_path + "rel_classifier_people.person.religion.svm",
    "PARENTS": binary_relation_models_path + "rel_classifier_people.person.parents.svm"
}

binary_relation_type_to_model_obj = {}


def binary_relation_type_to_model(type):
    if type not in binary_relation_type_to_model_obj:
        path = binary_relation_type_to_model_path[type]
        binary_relation_type_to_model_obj[type] = binary_relation_detector(path)

    return binary_relation_type_to_model_obj[type]


def get_tokens(text):
    return tokenize(text)


def find_binary_relation_in_text(text, subject, object_, predicate):
    tokens = get_tokens(text)
    ner = get_ner()
    entities = ner.extract_entities(tokens)
    #for entity in entities:
    #    print_ner(tokens, entity)

    subject_positions = find_name_positions_in_text(tokens, entities, subject)
    object_positions = find_name_positions_in_text(tokens, entities, object_)

    if(len(subject_positions) == 0 or len(object_positions) == 0):
        return []

    results = []
    rel_detector = binary_relation_type_to_model(predicate)
    for subj, obj in itertools.product(subject_positions, object_positions):
        rel = ner.extract_binary_relation(tokens, subj[0], obj[0])

        score = rel_detector(rel)
        relation_bounds = extract_xrange_bounds(subj[0], obj[0], 2, len(tokens))
        relation_text = extract_text_by_xrange(tokens, relation_bounds)
        results.append((subj, obj, score, relation_text))

    return results


def find_name_positions_in_text(tokens, entities, name):
    positions = []
    for entity in entities:
        entity_name = extract_text_by_xrange(tokens, entity[0])
        if(compare_names(name, entity_name)):
            positions.append(entity)

    if(len(positions) == 0):
        # if our name is not Named entity, try to find it in the text
        tt = get_tokens(name)
        for i in range(len(tokens)-len(tt)+1):
            correct = True
            for j in range(len(tt)):
                if(tokens[i+j].lower() != tt[j].lower()):
                    correct = False
                    break
            if(correct):
                p = xrange(i, i+len(tt))
                positions.append((p, "UNKNOWN"))

    return positions


ner_extractor = None
def get_ner():
    global ner_extractor
    if ner_extractor is None:
        ner_extractor = named_entity_extractor(mitie_path + 'MITIE-models/english/ner_model.dat')
    return ner_extractor


def compare_names(full_name, free_name):
    return full_name.lower() == free_name.lower()


## extract text from tokens
def extract_text_by_xrange(tokens, xr):
    return " ".join([tokens[i] for i in xr])


## extract text from tokens with offset
def extract_text_by_xrange(tokens, xr):
    return " ".join([tokens[i] for i in xr])


## combine two xranges in one
def extract_xrange_bounds(xr1, xr2, margin, maxlen):
    start = 0
    for i in xr1:
        start = i
        break

    finish = 0
    for i in xr2:
        finish = i
    finish += 1

    if(finish <= start):
        return extract_xrange_bounds(xr2, xr1, margin, maxlen)

    start = max(start-margin, 0)
    finish = min(finish+margin, maxlen)

    return xrange(start, finish)