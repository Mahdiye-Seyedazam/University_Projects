import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


class ClassScore:
    def __init__(self, siyah=None, sabz=None):
        self.siyah = siyah
        self.sabz = sabz
        self.TP = 0
        self.javab = np.zeros((164, 4))
        self.javab_axar = None
        self.pasox = np.zeros((165, 4))
        self._count_TRUE = 0
        self._count_FALSE = 0
        self._count_NONE = 0

    def score(self):
        gozine = cv2.imread(self.siyah)
        image = cv2.imread(self.sabz)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([36, 25, 25])
        upper_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(
            green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bounding_boxes = []
        javab = np.zeros((164, 4))

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            bounding_boxes.append((x, y, w, h))

        new = bounding_boxes[:-2]
        new.reverse()
        for pos in new:
            cv2.rectangle(
                image, (pos[0], pos[1]), (pos[0] + pos[2], pos[1] + pos[3]), (0, 0, 0), 2)

        answers = []
        for i, box in enumerate(new):
            answer = {
                "gozine": i + 1,
                "coor": (box[0], box[1], box[2], box[3])
            }
            answers.append(answer)

        for index in range(len(new)):
            if new[index][0] == 294 or new[index][0] == 303:
                self.javab[index][0] = 1
            elif new[index][0] == 705 or new[index][0] == 714:
                self.javab[index][1] = 1
            elif new[index][0] == 1116 or new[index][0] == 1125:
                self.javab[index][2] = 1
            elif new[index][0] == 1536 or new[index][0] == 1526:
                self.javab[index][3] = 1

        self.javab_axar = np.insert(self.javab, 148, [[0, 0, 1, 0]], axis=0)

        Total = len(self.javab_axar)

        # =============================================siyah==================================================
        gray = cv2.cvtColor(gozine, cv2.COLOR_BGR2GRAY)
        cropped = gozine[620:2167, 90:1045]

        boxes = [cropped[10:293, 35:176], cropped[330:610, 40:178], cropped[645:925, 40:180], cropped[960:1230, 40:180], cropped[1270:1540, 40:180],
                 cropped[10:293, 295:430], cropped[330:610, 295:430], cropped[645:925,
                                                                              295:430], cropped[960:1230, 295:430], cropped[1270:1540, 295:430],
                 cropped[10:293, 554:695], cropped[330:610, 554:695], cropped[645:925,
                                                                              556:695], cropped[960:1230, 556:695], cropped[1270:1540, 556:695],
                 cropped[10:293, 809:948], cropped[330:610, 809:948]]

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([0, 0, 0])
        color = [0, 255, 0]
        started_y = [(5, 25), (30, 47), (60, 77), (89, 107), (118, 134),
                     (145, 165), (175, 190), (200, 220), (230, 247), (258, 278)]
        started_x = [(2, 25), (35, 62), (73, 98), (108, 133)]
        listt = []
        for img in boxes:
            gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray2, (9, 9), 0)
            _, threshold_ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV)
            inverted_image = cv2.bitwise_not(threshold_)
            # cn , _ = cv2.findContours(inverted_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) --> for find position of y , x
            imagee = cv2.cvtColor(inverted_image, cv2.COLOR_GRAY2BGR)

            for soal in started_y:
                ls = []
                listt.append(ls)
                for gozine in started_x:
                    roi = inverted_image[soal[0]:soal[1], gozine[0]:gozine[1]]
                    count_black_pixels = cv2.countNonZero(255 - roi)
                    ls.append(count_black_pixels)

        for i in range(len(listt)):
            for pos in listt[i]:
                if pos > 1:
                    self.pasox[i][listt[i].index(pos)] = 1
                else:
                    pass

        equal_elements = np.equal(self.pasox, self.javab_axar)
        matching_indices = np.where(equal_elements.all(axis=1))
        self._count_TRUE += len(matching_indices[0])
        matching_count = len(matching_indices[0])
        ones = np.count_nonzero(self.pasox == 1)
        self._count_FALSE += ones - matching_count
        self._count_NONE += len(self.pasox) - (self._count_FALSE + matching_count)

        return (matching_count / Total) * 100

    def repersentaion(self) -> str:
        q = {}
        a = self.javab_axar
        b = self.pasox
        for i in range(len(self.javab_axar)):
            lst = []
            for j in range(4):
                if self.pasox[i][j] == 0 and self.javab_axar[i][j] == 0:
                    lst.append("-")
                if self.pasox[i][j] == 1 and self.javab_axar[i][j] == 1:
                    lst.append("True")
                if self.javab_axar[i][j] == 1 and self.pasox[i][j] == 0:
                    lst.append("TA")
                if self.javab_axar[i][j] == 0 and self.pasox[i][j] == 1:
                    lst.append("False")
            q[i+1] = lst

        d = 5
        df = pd.DataFrame.from_dict(q, orient="index", columns=range(1, 5))
        return df

    def save_status(self):
        q = {}
        for i in range(len(self.javab_axar)):
            lst = []
            for j in range(4):
                if self.pasox[i][j] == 0 and self.javab_axar[i][j] == 0:
                    lst.append("-")
                if self.pasox[i][j] == 1 and self.javab_axar[i][j] == 1:
                    lst.append("True")
                if self.javab_axar[i][j] == 0 and self.pasox[i][j] == 1:
                    lst.append("False")
            q[i+1] = lst

        d = 5
        df = pd.DataFrame.from_dict(q, orient="index", columns=range(1, 5))
        b = ((((f"{self.siyah}").split("."))[1]).split("/"))[1]
        df.to_csv(f"{b}.csv", sep=",")

    @staticmethod
    def save_allstatus(folder_path):
        items = os.listdir(folder_path)
        students = []
        path = []
        key = ''
        for item in items:
            file_path = os.path.join(folder_path, item)
            if os.path.isfile(file_path):
                file_name, file_extension = os.path.splitext(item)
                if file_extension == ".tiff":
                    students.append(file_name)
                    path.append(f"{file_name}{file_extension}")
                if file_extension == ".png":
                    key = f"{file_name}{file_extension}"
        result = {}
        for item in path:
            obj = ClassScore(f"./{item}", f"./{key}")
            obj.score()
            name = (item.split('.'))[0]
            result[name] = [obj._count_TRUE, obj._count_FALSE, obj._count_NONE]
        indexes = ["TRUE", "FALSE", "NONE"]
        df = pd.DataFrame.from_dict(result, orient="index")
        df.columns = indexes
        df.to_csv("save_all_status", sep=",")
        print("saved all status score of student sucssesfully !!")

    @staticmethod
    def save_all(folder_path):
        items = os.listdir(folder_path)
        students = []
        path = []
        key = ''
        for item in items:
            file_path = os.path.join(folder_path, item)
            if os.path.isfile(file_path):
                file_name, file_extension = os.path.splitext(item)
                if file_extension == ".tiff":
                    students.append(file_name)
                    path.append(f"{file_name}{file_extension}")
                if file_extension == ".png":
                    key = f"{file_name}{file_extension}"

        dic = {}
        for item in path:
            obj = ClassScore(f"./{item}", f"./{key}")
            name = (item.split('.'))[0]
            dic[name] = round(obj.score(), 2)

        df = pd.DataFrame.from_dict(dic, orient="index")
        df.to_csv("all_score", sep=",", header=False)
        print("saved all score of student sucssesfully !!")


a = ClassScore(siyah="./SanaZarei.tiff", sabz="kild.png")

a.score()
a.save_all("../opencv")
a.save_allstatus("../opencv")