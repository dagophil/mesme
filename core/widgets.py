from PyQt5.QtWidgets import QFormLayout, QTimeEdit
from PyQt5.QtCore import QTime


class WeekTimeEdit(QFormLayout):
    """
    The WeekTimeEdit is a QWidget input for time (hours, minutes) per week day.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        times = 5*[QTime(8, 0)] + 2*[QTime(0, 0)]

        self._time_inputs = {}

        for day, time in zip(self._days, times):
            time_input = QTimeEdit(time=time)
            self._time_inputs[day] = time_input
            self.addRow(day + ":", time_input)

    def get_time(self, day):
        """
        Returns the input time of the given day. Valid days are "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su".
        :param day: The day.
        :return: Returns the input time.
        """
        if day in self._time_inputs:
            return self._time_inputs[day].time()
        else:
            raise IndexError("Invalid key: " + day)

    def items(self):
        """
        Returns a dict {day: time}, where day is the day ("Mo", "Tu", ...) and time is the corresponding QTime input
        value.
        :return: Returns the {day: time} dict.
        """
        return [(day, self._time_inputs[day].time()) for day in self._days]
