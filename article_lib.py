import xml.etree.ElementTree as ET
import pandas as pd

def read_article_file_as_datarow(df, path_to_xml):
    e = ET.parse(path_to_xml).getroot()
    is_revelation = e.findall("is_revelation")[0].text
    if(is_revelation is None or len(is_revelation) == 0):
        is_revelation = 0
    else:
        is_revelation = int(is_revelation)
    df.loc[len(df)] = [int(e.findall("source_id")[0].text), int(e.findall("binary_relation_id")[0].text), is_revelation, e.findall("title")[0].text, e.findall("url")[0].text, e.findall("body")[0].text]

def read_list_of_articles_as_dataset(ls):
    df = pd.DataFrame(columns=[ "SourceId", "BinaryRelationId", "IsRevelation", "Title", "Url", "Body" ])
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

