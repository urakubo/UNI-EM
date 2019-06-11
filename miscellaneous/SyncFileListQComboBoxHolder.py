from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QStringListModel


class SyncFileListQComboBoxHolder():

    selectedSaveIdx = dict()
    model = QStringListModel([""])

    @staticmethod
    def addModel(elem):
        stringList = SyncFileListQComboBoxHolder.model.stringList()
        
        if elem in stringList:
            #print("dup")
            return
        
        stringList.append(elem)
        SyncFileListQComboBoxHolder.model.setStringList(stringList)

    @staticmethod
    def create(component, idx):
                
        key = str(component.__class__.__name__) + str(idx)
        combo = SyncFlileListQComboBox(key)
        combo.setModel(SyncFileListQComboBoxHolder.model)

        if key in SyncFileListQComboBoxHolder.selectedSaveIdx.keys():
            combo.setCurrentIndex(SyncFileListQComboBoxHolder.selectedSaveIdx[key])
        
        return combo

    @staticmethod
    def syncCandiate(origin, idx, key):
        
        if origin.isInit:
            origin.isInit = False
            return
        else:
            SyncFileListQComboBoxHolder.selectedSaveIdx[key] = idx


class SyncFlileListQComboBox(QComboBox):

    def __init__(self, key):
        super().__init__()
        self.isInit = True
        self.currentIndexChanged.connect(lambda idx: SyncFileListQComboBoxHolder.syncCandiate(self, idx, key))

