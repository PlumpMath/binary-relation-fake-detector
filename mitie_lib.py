import sys
import os

mitie_path = os.environ['MITIE_HOME']
sys.path.append(mitie_path)

from mitie import *

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


ner_extractor = None


def get_ner():
    global ner_extractor
    if ner_extractor is None:
        ner_extractor = named_entity_extractor(mitie_path + 'MITIE-models/english/ner_model.dat')
    return ner_extractor


def compare_names(full_name, free_name):
    return full_name.lower() == free_name.lower()


def extract_text_by_xrange(tokens, xr):
    return " ".join([tokens[i] for i in xr])
