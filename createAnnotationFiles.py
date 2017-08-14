import os


def main():
    """
    Crawls through all folders in DATA_DIRECTORY and creates
    the Annotations folder if not already present
    :return:
    """
    directory = '/home/goring/Documents/DataSets/Sub/2017/Forward'
    for a in os.listdir(directory):
        try:
            os.mkdir(os.path.join(directory, a, "Annotations"))
        except:
            pass
            # print 'Folder Already Made'

    return True


if __name__ == '__main__':
    main()
