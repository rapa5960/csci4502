# /usr/bin/python
# Assignment based on MAGIC Gamma Telescope Data Set ( http://archive.ics.uci.edu/ml/datasets/MAGIC+Gamma+Telescope )
import argparse
import numpy


class dataSet:
    """
    Class to store the MAGIC Gamma Telescope Data Set
    """
    def __init__(self, location):
        with open(location, "r") as myfile:
            self.readData = myfile.readlines()

    def write(self, location, data):
        with open(location, "w") as outfile:
            outfile.write(str(data)[1:-1])


def calculate(data, ithAttribute):
    """
    Input Parameters:
        data: The data that is read from the file. list of strings
        ithAttribute: The ith Attribute for which the various properties must be calculated. int

    Default value of 0,infinity,-infinity are assigned to all the variables as required.
    Objective of the function is to calculate:  N (number of objects), min, max, mean, standard deviation, Q1, median, Q3, IQR
    """
    parsedList = transformData(data, ithAttribute)
    noOfObjects = len(parsedList)
    minValue = min(parsedList)
    maxValue = max(parsedList)
    mean = numpy.mean(parsedList)
    standardDeviation = numpy.std(parsedList)
    q1 = numpy.percentile(parsedList, 25.0)
    q3 = numpy.percentile(parsedList, 75.0)
    median = numpy.median(parsedList)
    iqr = q3 - q1
    return noOfObjects, minValue, maxValue, mean, standardDeviation, q1, median, q3, iqr


def transformData(data, ithAttribute):
    """
    Input Parameters:
        data: The data that is read from the file. list of strings
        ithAttribute: The ith Attribute for which the various properties must be calculated. int

    Returns a list of floats parsed from the ithAttribute of the list of strings
    """
    ithAttributeMinusOne = ithAttribute - 1
    transformedData = [0 for x in range(len(data))]
    for i, string in enumerate(data):
        transformedData[i] = float(string.split(',')[ithAttributeMinusOne])
    return transformedData


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Mining HW1')
    parser.add_argument('--i', type=int,
                        help="ith attribute of the dataset ( limit 1 to 10 )",
                        default=5,
                        choices=set((1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
                        required=True)
    parser.add_argument("--data", type=str,
                        help="Location of the downloaded file",
                        default="magic04.data",
                        required=False)
    parser.add_argument('--export', type=bool,
                        help="prints the dataset into a .txt file",
                        default=False,
                        required=False)
    args = parser.parse_args()
    data = dataSet(args.data)
    print ','.join(map(str, calculate(data.readData, args.i)))
    if args.export:
        data.write("./{0}.txt".format(args.i), transformData(data.readData, args.i))
