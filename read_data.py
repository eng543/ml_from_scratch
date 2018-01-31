import argparse
import os
import re

def main():
    """
    Reads data from specified file and stores in Data object
    """

    parser = argparse.ArgumentParser(description='Tool for reading in data from file and storing in Data object')
    parser.add_argument('--train', help='Training file name', required=True)
    # parser.add_argument('--test', help='Test file name, to make predictions on', required=True)
    # parser.add_argument('--pred', help='Output file name for predictions, defaults to test_name.pred')
    args = parser.parse_args()

    # if not args.pred:
    #     args.pred = args.test + '.pred'

    assert os.path.isfile(args.train)

    training_data = read_data(args.train)


def read_data(filename):
    """ This method loads and returns the data stored in filename. If the data is labelled training data, it returns labels too.

    Parameters:
        filename: the location of the training data or test data you want to load

    Returns:
        data: a list of InstanceData objects
    """

    # empty list to store Data objects
    instances = []

    ## make robust to different delimiters

    with open(filename, 'r') as rf:
        lines = rf.readlines()

        heading = lines[0].strip()
        heading = re.split(r'[,|\t]+', heading)
        feature_names = Features(names=heading)

        if filename.find('train') != -1:
            for i in range(1, len(lines)):
                line = lines[i].strip()
                line = re.split(r'[,|\t]+', line)

                instances.append(InstanceData(user_id=line[0], features=line[1:-1], label=line[-1]))
        else:
            for i in range(1, len(lines)):
                line = lines[i].strip()
                line = re.split(r'[,|\t]+', line)

                instances.append(InstanceData(user_id=line[0], features=line[1:], label=None))

    data = Data(feature_names, instances)

    print 'Done loading. Read ' + str(len(instances)) + ' instances.'
    

    return data


class Data(object):
    """
        A class to store list of InstanceData objects, feature names, and any other shop-keeping information
    """

    def __init__(self, features, instances):
        self.features = features
        self.instances = instances


class InstanceData(object):
    """
    A class to store attributes associated with each instance in the data file, including label if applicable
    """

    def __init__(self, user_id, features, label):
        self.user_id = user_id
        self.features = features
        self.label = label


class Features(object):
    """
    A class to store features names associated with feature attribute in InstanceData obje ct
    """

    def __init__(self, names):
        self.names = names 


if __name__ == '__main__':
    main()