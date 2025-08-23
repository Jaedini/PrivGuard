from PySide6.QtCore import QObject, Signal

class WorkerSignals(QObject):
    progress = Signal(int, str)   # percent, file path
    finished = Signal(str)        # message
    error = Signal(str)           # message
