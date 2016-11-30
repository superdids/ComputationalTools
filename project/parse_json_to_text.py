import json
import ijson
import time

import multiprocessing
from joblib import Parallel, delayed

dataText = open('dataTest.txt', 'w')


def processInput(crime):
    # for crime in dataJSON:
    crimeText = json.dumps(crime)
    dataText.write(crimeText + '\n')


if __name__ == '__main__':
    with open('testData.json') as f:
        start = time.time()
        dataJSON = ijson.items(f, 'data.item')
        end = time.time()
        print('loading time: ', end - start)
        start = time.time()
        # dataText = open('dataTest.txt', 'w')
        num_cores = multiprocessing.cpu_count()
        # Parallel(n_jobs=num_cores)(delayed(processInput)(crime) for crime in dataJSON)
        for crime in dataJSON:
            processInput(crime)
        end = time.time()
        print('processing time: ', end - start)

        dataText.close()
