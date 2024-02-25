# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

# -------------------------------------------------
# Clase Observer
class Subject():
    def __init__(self):
        self.observadores = []

    def add_observer(self, observer):
        self.observadores.append(observer)

    def notify_obervers(self):
        for observer in self.observadores:
            observer.notify(self)