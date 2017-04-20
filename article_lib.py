import xml.etree.ElementTree as ET
import pandas as pd
import codecs



def read_article_file_as_datarow(df, path_to_xml):
    with codecs.open(path_to_xml, 'r') as f:
        text = f.read()
        e = ET.fromstring(text)
        df.loc[len(df)] = [
            try_int(e.findall("source_id")[0].text),
            try_int(e.findall("binary_relation_id")[0].text),
            try_int(e.findall("is_revelation")[0].text),
            e.findall("title")[0].text,
            e.findall("url")[0].text,
            e.findall("body")[0].text,
            path_to_xml
        ]


def try_int(s):
    if s is None or len(s) == 0:
        return 0
    else:
        return int(s)


def read_list_of_articles_as_dataset(ls):
    df = pd.DataFrame(columns=[ "SourceId", "BinaryRelationId", "IsRevelation", "Title", "Url", "Body", "Path"])
    for path in ls:
        read_article_file_as_datarow(df, path)
    return df


def join_binary_relations(df):
    path_to_binary_rels = "..\\Data\\fakes.csv"
    br = pd.read_csv(path_to_binary_rels)
    joined = pd.merge(df, br, left_on="BinaryRelationId", right_on="Id")
    del joined["Id"]
    del joined["BinaryRelationId"]
    del joined["Unnamed: 5"]
    return joined

