import json
import ijson
import time

from multiprocessing import Process

dataText = open('dataParallel.txt', 'w')


def process_input(data):
    for crime in data:
        crimeText = json.dumps(crime)
        dataText.write(crimeText + '\n')


if __name__ == '__main__':
    with open('testData.json') as f:
        dataJSON = ijson.items(f, 'data.item')

        # START the timer
        start = time.time()

        p = Process(target=process_input, args=(dataJSON,))
        p.start()
        p.join()

        # END the timer
        end = time.time()
        print('processing time: ', end - start)

        dataText.close()
