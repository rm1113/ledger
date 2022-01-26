import numpy as np
import pandas as pd


class Ledger:
    def __init__(self, filename=None):
        self.columns_ = ['date', 'type', 'subject', 'notes']
        if filename:
            self.data_ = pd.read_csv(filename)
        else:
            self.data_ = pd.DataFrame(columns=self.columns_)
        self.filename_ = filename
        self.payment_type = "оплата"
        self.lesson_type = "урок"

    def set_file(self, filename):
        self.filename_ = filename

    def __check_date_format__(self, date):
        [day, month, year] = date.split(".")
        message = "Wrong date format! Must be DD.MM.YYYY"
        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            raise ValueError(message)
        if not (31 >= int(day) > 0):
            raise ValueError(message)
        if not 12 >= int(month) > 0:
            raise ValueError(message)
        if not 3000 >= int(year) >= 2021:
            raise ValueError(message)

    def __check_subject__(self, subject):
        ss = ["математика", "информатика", "физика"]
        if subject not in ss:
            raise ValueError(f"Subject can be {ss} only!")

    def write_lesson(self, date, subject, notes, save_to_file=True):

        self.__check_date_format__(date)
        self.__check_subject__(subject)
        temp = {}
        for col, item in zip(self.columns_, [date, self.lesson_type, subject, notes]):
            temp[col] = item

        self.data_ = self.data_.append(temp, ignore_index=True)

        if save_to_file and self.filename_:
            self.data_.to_csv(self.filename_, index=False)
            print(f"Data was appended to file!")
        return self.data_

    def write_payment(self, date, payment, duration=1.5, cost=800, to_file=True):
        self.__check_date_format__(date)
        n_lessons = round(payment / duration / cost)

        for _ in range(n_lessons):
            temp = {c: [] for c in self.columns_}
            for col, item in zip(self.columns_, [date, self.payment_type, None, None]):
                temp[col] = item
            self.data_ = self.data_.append(temp, ignore_index=True)

        if to_file and self.filename_:
            self.data_.to_csv(self.filename_, index=False)
            print(f"Data was appended to file!")
        return self.data_

    def check_status(self):
        n = len(self.data_.loc[self.data_["type"] == "урок"]) - len(self.data_.loc[self.data_["type"] == "оплата"])
        if n > 0:
            print(f"В долг проведено {n} занятий.")
        if n == 0:
            print("Количество проведенных и оплаченных уроков совпало")
        if n < 0:
            print(f"Оплачено {-n} уроков вперед")

    def get_data(self):
        return self.data_


if __name__ == "__main__":
    # data = pd.DataFrame(columns=["date",
    #                              "type",
    #                              "subject",
    #                              "notes"])
    # print(data)

    l = Ledger()
    l.set_file("ledger.csv")
    l.write_lesson("31.12.2021", "физика", None)

    a = l.write_payment("12.03.2021", 7200)
    print(a)
    l.check_status()
