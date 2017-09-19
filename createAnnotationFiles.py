import os


def main():
    """
    Crawls through all folders in directory and creates
    the Annotations folder if not already present
    :return:
    """
    directory = '/home/goring/Documents/DataSets/Sub/2017/Forward'
    for a in os.listdir(directory):
        try:
            os.mkdir(os.path.join(directory, a, "Annotations"))
        except:
            pass

    return True


if __name__ == '__main__':
    main()
