# Assignment based on http://www.nasdaq.com/quotes/
# Feel free to use any libraries.
# Make sure that the output format is perfect as mentioned in the problem.
# Also check the second row of the download dataset.
# If it follows a different format, avoid it or remove it.
import argparse
import numpy
ATTRIBUTES = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4, 'volume': 5}


class dataSet:
    """
    Class to store the a general dataset. Might as well reuse this
    """
    def __init__(self, location, header=False):
        with open(location, "r") as myfile:
            self.readData = myfile.readlines()[header:]

    def write(self, location, data):
        with open(location, "w") as outfile:
            outfile.write(str(data)[1:-1])


def transformData(data, attribute):
    """
    Input Parameters:
        data: The data that is read from the file. list of strings
        attribute: The attribute you want to consider from the file

    Returns a list of floats parsed from the ithAttribute of the list of strings
    """
    attributeindex = ATTRIBUTES[attribute]
    transformedData = [0 for x in range(len(data))]
    for i, string in enumerate(data):
        strippedAttributeString = string.split(',')[attributeindex].strip()
        strippedAttributeString = strippedAttributeString.strip('\"')
        transformedData[i] = float(strippedAttributeString)
    return transformedData


def z_score(values):
    '''
    Computes the z score normalization
    Input Parameters:
        values: list of floating point values to normalize


    List of tuples where first element in tuple is original value
    and second element in tuple is min_max normalization of original value
    '''
    originalAndNormalizedValues = []
    mean = numpy.mean(values)
    std = numpy.std(values)
    for value in values:
        normalized = (value - mean) / std
        originalAndNormalizedValues.append((value, normalized))
    return originalAndNormalizedValues

def min_max(values):
    '''
    Computes the min max normalization of a floating point value
    Input Parameters:
        values: list of floating point values to normalize

    Returns list of tuples where first element in tuple is original value
    and second element in tuple is min_max normalization of original value
    '''
    originalAndNormalizedValues = []
    minimum = min(values)
    maximum = max(values)
    difference = maximum - minimum
    for value in values:
        normalized = (value - minimum) / (difference)
        originalAndNormalizedValues.append((value, normalized))
    return originalAndNormalizedValues


def normalization(fileName, normalizationType, attribute):
    '''
    Input Parameters:
        fileName: The comma seperated file that must be considered for the normalization
        attribute: The attribute for which you are performing the normalization
        normalizationType: The type of normalization you are performing
    Output:
        For each line in the input file, print the original "attribute" value and "normalized" value seperated by <TAB>
    '''
    data = dataSet(fileName, header=True).readData
    values = transformData(data, attribute)
    results = None
    if normalizationType == 'z_score':
        results = z_score(values)
    elif normalizationType == 'min_max':
        results = min_max(values)
    for result in results:
        print '{0}\t{1}'.format(result[0], result[1])


def correlation(attribute1, fileName1, attribute2, fileName2):
    '''
    Input Parameters:
        attribute1: The attribute you want to consider from file1
        attribute2: The attribute you want to consider from file2
        fileName1: The comma seperated file1
        fileName2: The comma seperated file2

    Output:
        Print the correlation coefficient
    '''
    correlationCoefficient = 0.0
    data1 = dataSet(fileName1, header=True).readData
    data2 = dataSet(fileName2, header=True).readData
    values1 = transformData(data1, attribute1)
    values2 = transformData(data2, attribute2)
    len1 = len(values1)
    len2 = len(values2)
    if len1 != len2:
        print("Datasets are differently sized!")
        print("{0} has {1} elements".format(fileName1, len1))
        print("{0} has {1} elements".format(fileName2, len2))
        return 0
    mean1 = numpy.mean(values1)
    mean2 = numpy.mean(values2)
    std1 = numpy.std(values1)
    std2 = numpy.std(values2)
    deviationProduct = len1 * std1 * std2
    if deviationProduct == 0:
        print 'Cannot calculate the correlation coefficient because a standard deviation is zero'
    for value1, value2 in zip(values1, values2):
        correlationCoefficient += (value1 - mean1) * (value2 - mean2)
    correlationCoefficient /= (deviationProduct)
    print correlationCoefficient


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Mining HW2')
    parser.add_argument('-f1', type=str,
                        help="Location of filename1. Use only f1 when working with only one file.",
                        required=True)
    parser.add_argument("-f2", type=str,
                        help="Location of filename2. To be used only when there are two files to be compared.",
                        required=False)
    parser.add_argument("-n", type=str,
                        help="Type of Normalization. Select either min_max or z_score",
                        choices=['min_max', 'z_score'],
                        required=False)
    parser.add_argument("-a1", type=str,
                        help="Type of Attribute for filename1. Select either open or high or low or close or volume",
                        choices=ATTRIBUTES,
                        required=False)
    parser.add_argument("-a2", type=str,
                        help="Type of Attribute for filename2. Select either open or high or low or close or volume",
                        choices=ATTRIBUTES,
                        required=False)

    args = parser.parse_args()

    if (args.n and args.a1):
        normalization(args.f1, args.n, args.a1)
    elif (args.f2 and args.a1 and args.a2):
        correlation(args.a1, args.f1, args.a2, args.f2)
    else:
        print "Kindly provide input of the following form:\nDMPythonHW2.py -f1 <filename1> -a1 <attribute> -n <normalizationType> \nDMPythonHW2.py -f1 <filename1> -a1 <attribute> -f2 <filename2> -a2 <attribute>"
