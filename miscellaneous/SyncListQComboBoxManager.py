from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QStringListModel


class SyncListQComboBoxManager():
    """
    QComboBox Manager with synchronized combobox list.
    This class is non include/exclude condition.

    Use:
        1. SyncListQComboBoxManager.build(self.u_info)  # Create singleton instance of manager.
        2. comboBox = SyncListQComboBoxManager.get().create(...)   # Create SyncListQComboBox instance.
    """
    
    singletonObj = None
    
    
    def __init__(self, u_info):
        self.selectedSaveIdx = dict()
        self.model = QStringListModel([""])
        self.my_u_info = u_info


    @classmethod
    def get(cls):
        """
        Get singleton instance.
        """
        if not cls.singletonObj:
            raise RuntimeError("Error, singleton instance is not exist. Please execute build().")
        return cls.singletonObj

    
    @classmethod
    def build(cls, u_info):
        """
        Create singleton instance.
        """
        if not cls.singletonObj:
            cls.singletonObj = cls(u_info)

        return cls.singletonObj        


    def isInclude(self, fileName):
        return True


    def isExclude(self, fileName):
        return False


    def addModel(self, elem):
        """
        When want to add file element to model without using QCombobox interface.
        """
        
        if (not self.isInclude(elem)) or self.isExclude(elem):
            return
        
        stringList = self.model.stringList()
        
        if elem in stringList:
            return
        
        stringList.append(elem)
        self.model.setStringList(stringList)


    def removeModel(self, elem):
        """
        When want to add file element to model without using QCombobox interface.
        """

        stringList = self.model.stringList()

        stringList.remove(elem)
        self.model.setStringList(stringList)


    def create(self, component, idx):
        """
        Create SyncListQComboBox instance.
        """
                
        key = str(component.__class__.__name__) + str(idx)
        combo = self.SyncListQComboBox(self, key)
        combo.setModel(self.model)

        if key in self.selectedSaveIdx.keys():
            combo.setCurrentIndex(self.selectedSaveIdx[key]['idx'])
        
        return combo


    def saveSelected(self, origin, idx, key):

        if idx == -1 and key in self.selectedSaveIdx.keys():
           findIdx = origin.findText(self.selectedSaveIdx[key]['text'])
           if findIdx > -1:
               origin.setCurrentIndex(findIdx)
           return
        
        if origin.isInit:
            origin.isInit = False
            return
        else:
            
            if (not self.isInclude(origin.currentText())) or self.isExclude(origin.currentText()):
                origin.removeItem(idx)

            self.selectedSaveIdx[key] = {'idx': idx, 'text': origin.currentText()}


    class SyncListQComboBox(QComboBox):

        def __init__(self, manager, key):
            super().__init__()
            self.isInit = True
            self.currentIndexChanged.connect(lambda idx: manager.saveSelected(self, idx, key))


class SyncListQComboBoxExcludeDjojMtifManager(SyncListQComboBoxManager):
    
    def isExclude(self, fileName):
        if not fileName:
            return False
        
        if not fileName in self.my_u_info.open_files_type.keys():
            return False
        
        return self.my_u_info.open_files_type[fileName] == 'Dojo' or self.my_u_info.open_files_type[fileName] == 'mtif'

    
class SyncListQComboBoxOnlyDojoManager(SyncListQComboBoxManager):
    
    def isInclude(self, fileName):
        if not fileName:
            return True
        
        if not fileName in self.my_u_info.open_files_type.keys():
            return True
        
        return self.my_u_info.open_files_type[fileName] == 'Dojo'
