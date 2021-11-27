import argparse
import regex as re
import spacy


def read_labels(file_path):
    """
    Returns a list of all the labels in the input file
    Assumes each line is formatted "/author/repo\tlabel1,label2,label3,..."
    :param file_path: The path including the name of the input file with above format
    :return: a set of issue labels
    """
    p = re.compile("/.*/.*\t((.+,+)*.+)")  # Pattern of each line
    labels = set()  # The set of issue labels that will be returned

    with open(file_path, 'r', errors='ignore') as file:
        lines = file.readlines()
        for line in lines:
            m = p.match(line.strip())
            if m is None:
                continue
            labels_string = m.group(1)
            issue_labels = labels_string.split(",")
            labels.update(issue_labels)  # Add this line's labels to set
    return labels


def relevant_label_embeddings(relevant_labels):
    """
    Creates a dict of the relevant label embeddings
    :param relevant_labels: The list of labels
    :return: a dict with the string labels mapped to the corresponding word vector embeddings
    """
    global nlp_lg
    relevant_dict = {}  # key = label, value = embedding
    for label in relevant_labels:
        relevant_dict[label] = nlp_lg(label)
    return relevant_dict


def calc_label_similarities(labels_file, relevant_embeddings, issues_file=None):
    """
    Computes the cosine similarities between each label and all the relevant labels
    :param labels_file: The path to the file containing issue labels
    :param relevant_embeddings: The embedded word vector representations of the relevant labels
    :param issues_file: The path to the file containing issues descriptions
    :return: a dict containing the similarity measures between each label and all of the relevant labels
    """
    global nlp_lg

    labels = read_labels(labels_file)

    # Compare labels to the relevant labels
    similarity_dict = {}  # key = label, value = list of similarity values
    for label in labels:
        enc_label = nlp_lg(label)
        similarity_dict[label] = list(map(enc_label.similarity, relevant_embeddings))

    # Search for relevant tags within issues descriptions if descriptions are provided
    if issues_file is not None:
        # TODO: Implement comparisons within issue description
        # likely requires another function to parse different file format
        pass

    return similarity_dict


def apply_threshold(similarities, threshold, filename=None):  #, labels_only=False):
    """
    Filters out labels that do not have similarity with at least one of the relevant labels
    :param similarities: The dictionary of labels with corresponding similarity values
    :param threshold: The similarity threshold
    :param filename: The output file to place results in
    :return: Prints all labels and the corresponding list of similarities to the console or to a file
    """

    # TODO: Consider % of relevant labels rather than any label
    values = [(label, similarity_list) for label, similarity_list in similarities.items() if any(sim >= threshold for sim in similarity_list)]

    if filename is not None:
        with open(filename, 'w') as outfile:
            for label, _ in values:
                outfile.write(label + '\n')
    else:  # Print to standard out
        print('There are', len(values), 'labels above the threshold', threshold)
        for label, similarity_list in values:
            print(label, similarity_list)


'''
Requirements:
 > python -m spacy download en_core_web_lg
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract security-relevant issue labels.')
    parser.add_argument('-l', '--labels-file', required=True, type=str, help='The path to the input file with issue labels')
    parser.add_argument('-r', '--relevant-labels', type=str, nargs='+', help='The labels to compare against')
    parser.add_argument('-i', '--issues-file', type=str, help='The path to the file containing issue descriptions to search more thoroughly for the labels')
    parser.add_argument('-o', '--out-file', type=str, help='The path to the file to output a list of relevant labels to')
    parser.add_argument('-t', '--threshold', type=float, help='The similarity threshold to use for determining which labels are similar enough')
    args = parser.parse_args()

    print_to_file = False
    if args.relevant_labels is None:
        args.relevant_labels = ['security', 'vulnerability']
    if args.issues_file is not None:
        print_to_file = True
    if args.threshold is None:
        args.threshold = 0.46

    # Load SpaCy word embeddings
    nlp_lg = spacy.load("en_core_web_lg")

    # Obtain embeddings of relevant labels
    relevantLabelEmbeddings = relevant_label_embeddings(args.relevant_labels)
    relevantEmbeddings = relevantLabelEmbeddings.values()

    # Calculate label similarities
    label_similarities = calc_label_similarities(args.labels_file, relevantEmbeddings, args.issues_file)

    # Filter out labels that fall below the threshold
    apply_threshold(label_similarities, args.threshold, args.out_file)

