import cv2
import numpy as np



class FeatureExtraction:



    def mask_generator(self, img, human):
        h1, w1 = img.shape[:2]
        mask = np.zeros(img.shape[:2], np.uint8)
        for (x, y, w, h) in human:
            z = x+int(w/2)
            u = int(w1/8)
            if(z < int(0.4*w1)):
                cv2.line(mask, ((z+u), y), (w1, (4*int(h1/5))), 120, 5)


            elif(z > int(0.58*w1)):
                cv2.line(mask, (z - u, y), (0, (4*int(h1 / 5))), 120, 5)

            else:
                cv2.line(mask, (z - u, y), (0, (2*int(h1 / 3))), 120, 5)
                cv2.line(mask, (z + u, y), (w1, (2*int(h1 / 3))), 120, 5)

            cv2.rectangle(mask, (x, y+h+1), ((x + w), (h1 - 80)), 255, 5)
        return mask


    def grab_cut(self, img, human):
        h1, w1 = img.shape[:2]
        bgModel = np.zeros((1, 65), np.float64)
        fgModel = np.zeros((1, 65), np.float64)
        mask = np.zeros(img.shape[:2], np.uint8)

        rect = (10, 10, w1 - 15, h1 - 15)
        cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        maskey = self.mask_generator(img, human)
        mask[maskey == 120] = 0
        mask[maskey == 255] = 1
        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgModel, fgModel, 5, cv2.GC_INIT_WITH_MASK)
        mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask[:, :, np.newaxis]
        for (x, y, w, h) in human:
            img[0:(y+h+10), 0:w1] = 0
        return img


    def cut_image(self,imageurl):
        img = cv2.imread(imageurl)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        print (face_cascade)
        human = face_cascade.detectMultiScale(gray, 1.3, 3)
        x = FeatureExtraction()
        result = x.grab_cut(img, human)
        cv2.namedWindow('Result',cv2.WINDOW_NORMAL)
        cv2.imshow('Result', result)
        cv2.waitKey(0)
        return result
