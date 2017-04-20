import time
from operator import itemgetter
import glob
from article_lib import *
from mitie_lib import *


def process_folder_of_articles(in_folder, out_file, fakes, batch_size=1000, start=0):
    print "Started processing folder %s" % in_folder
    articles = glob.glob(in_folder + "\\*.xml")
    length = len(articles)
    print "Found articles: %i." % length
    all_fakes = 0
    for batch_start in range(start, length, batch_size):
        batch_num = batch_start / batch_size + 1
        print "Processing batch #%i..." % batch_num

        start = time.time()
        batch = [articles[i] for i in range(batch_start, min(batch_start + batch_size, len(articles)))]
        fakes_found = process_batch(batch, out_file, fakes)
        all_fakes += fakes_found
        print "Found %i fakes. Results saved in file: %s. " % (fakes_found, out_file)
        end = time.time()

        batch_time = end - start
        batches_more = (length - batch_start - batch_size) / batch_size
        left_time = batch_time * batches_more

        print "Batch #%i finished. Time spent: %s. To finish: %s" % (batch_num, str(batch_time), str(left_time))

    print "Folder %s done. %i fakes found." % (in_folder, all_fakes)


def process_batch(batch, out_file, fakes):
    df = read_list_of_articles_as_dataset(batch)
    fake_columns = []

    # try to extract relations for each fake
    for fake in fakes.iterrows():
        column_name = "fake_%s" % fake[1]["Id"]
        df[column_name + "_title"] = df.apply(
            lambda row: assign_fake_score(row["Title"], fake[1]["Subject"], fake[1]["Object"], fake[1]["Predicate"]),
            axis=1)
        df[column_name + "_body"] = df.apply(
            lambda row: assign_fake_score(row["Body"], fake[1]["Subject"], fake[1]["Object"], fake[1]["Predicate"]),
            axis=1)
        fake_columns.append(column_name + "_title")
        fake_columns.append(column_name + "_body")

    # split results on two columns
    fake_columns_scores = []
    for fake_column in fake_columns:
        df[fake_column + "_score"] = df.apply(lambda row: row[fake_column][0], axis=1)
        fake_columns_scores.append(fake_column + "_score")

        df[fake_column + "_text"] = df.apply(lambda row: unicode(row[fake_column][1], errors='replace'), axis=1)

        del df[fake_column]

    # calculate results
    fakes_found = df[fake_columns_scores].apply(
        lambda row: 1 if any([row[name] != 0 for name in fake_columns_scores]) else 0, axis=1).sum()

    # remove extra data
    del df["BinaryRelationId"]
    del df["Title"]
    del df["Body"]

    # append to existing file or create new
    if os.path.exists(out_file):
        with open(out_file, 'a') as f:
            df.to_csv(f, header=False, index=False, encoding='utf8')
    else:
        df.to_csv(out_file, index=False, encoding='utf8')
    return fakes_found


# selects the best result
def assign_fake_score(text, subject_text, object_text, predicate):
    if text is None or len(text) < 5:  # magic numbers!
        return 0, ""

    relations = [r for rr in [find_binary_relation_in_text(text.upper(), subject_text, object_text, predicate, False),
                              find_binary_relation_in_text(text.lower(), subject_text, object_text, predicate, False),
                              find_binary_relation_in_text(text, subject_text, object_text, predicate, False)]
                 for r in rr]

    if len(relations) == 0:
        return 0, ""

    relations.sort(key=itemgetter(2), reverse=True)
    best_relation = relations[0]
    relation_text = extract_text_between_entities(best_relation[0], best_relation[1], text)
    return best_relation[2], relation_text
