from __future__ import unicode_literals
import cv2
import glob
import pickle
import numpy as np


class PreProcessing:
    imgWidth = 30
    imgHeight = 30
    n_classes = 6
    data = []
    test_data =[]
    labels_list = []
    test_labels_list = []

    def load_data(self):
        label = [[1, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 1],]
        raw_data = []
        test_raw_data = []
        for i in range(self.n_classes):
            a = "data/" + str(i) + "/train/*.jpeg"
            b = "data/" + str(i) + "/test/*.jpeg"

            raw_data += [cv2.resize(cv2.imread(file, 0), (30, 30), interpolation=cv2.INTER_AREA) for file in glob.glob(a)]
            test_raw_data += [cv2.resize(cv2.imread(file, 0), (30, 30), interpolation=cv2.INTER_AREA) for file in glob.glob(b)]
            self.labels_list += [label[i] for _ in glob.glob(a)]
            self.test_labels_list += [label[i] for _ in glob.glob(b)]
        self.data += self.convert_data(raw_data)
        self.test_data += self.convert_data(test_raw_data)

        return self.data, self.labels_list, self.test_data, self.test_labels_list

    def convert_data(self, raw_data):
        converted_data = []
        for m in range(len(raw_data)):
            temp = []
            for j in range(self.imgHeight):
                for k in range(self.imgWidth):
                    temp.append((raw_data[m][j][k]))

            converted_data.append(temp)
        return converted_data

    def next_batch(self, batch_size):
        for s in range(batch_size):
            batch_data = self.data[0:batch_size * 900]
            batch_labels = self.labels_list[0:batch_size]
        return batch_data, batch_labels
