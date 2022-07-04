from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import lib.config_settings as _cs
_settings = _cs.Settings()

import lib.filelib as fl

direc = _settings['mynotes']['direc']
trash = _settings['mynotes']['trash']
_backup_dir = _settings['mynotes']['_backup_dir']

model = None
tree=None
display=None

#if text file, display content
def _display_file():
    filepath =  _get_filepath()#get filepath of selected item
    print('Filepath: ',filepath)
    if _is_txt_file(filepath):
        with open(filepath,'r+',encoding = "ISO-8859-1") as file:
            display.setText(file.read())
    else:
        display.setText('')

def _update_file():
    filepath = _get_filepath()
    if _is_txt_file(filepath):
        try:
            with open(filepath,'w+',encoding = "ISO-8859-1") as file:
                txt = display.toPlainText().encode("ISO-8859-1", 'ignore')
                txt = txt.decode("ISO-8859-1")
                file.write(txt)
        except Exception as e:
            _msgbox("File not updated. Exception Error: "+ str(e))


def _backup():
    pass
    #fl.copy_entire_dir



def _delete():
    try:
        fl.move_item(_get_filepath(),trash)
        _display_file()
    except Exception as e:
            print("Exception deleting. Error: " + str(e))


def __rename():
    existing_file = _get_filepath()
    existing_name = fl.get_filename(existing_file)
    new_name, ok = QInputDialog.getText(QInputDialog(), '__rename', 'New Name: ', QLineEdit.Normal, existing_name) #popup msg box to __rename
    if ok:
        fl.rename(new_name,existing_file,autofill_existing_ext=True)


def __create_file_folder(file=False):
    try:
            name, ok = QInputDialog.getText(QInputDialog(), 'Name...', 'Enter Name: ') #popup msg box to enter name
            if ok:
                path = _get_filepath()#get existing node
                if _is_txt_file(path): #if file
                    path=fl.get_dir(path) #get containing folder

            if file: #if creating a file
                path = fl.join(path,name,ext='txt') #join folder and name
                fl.create_empty_file(path)
            else: #if creating folder
                fl.create_folder(name,path)

    except Exception as e:
            print("Exception creating file/folder. Error: " + str(e))    

def _create_file():
    __create_file_folder(True)

def _create_folder():
    __create_file_folder()    
    
            
def _msgbox(txt):
    output = QMessageBox()
    output.setText(txt)
    output.exec()

def _is_txt_file(filepath):
    return fl.is_file(filepath) and fl.get_extension(filepath)=='txt'

def _get_filepath(): #get filepath of currently selected element
    return model.filePath(tree.currentIndex())




def notebk():  
    qapp = QApplication([])
    window = QWidget()
    window.setGeometry(QRect(1900, 50, 1900, 2150)) ###locx,loc,wi,h


    ## tree
    global tree
    tree = QTreeView()
    tree.setGeometry(QRect(0, 5, 500, 1000))


    # file model system
    global model
    model = QFileSystemModel()  # create file model
    model.setRootPath(direc)  # set file model folder

    # finish setting up tree
    tree.setModel(model)  # link created file model to tree
    tree.setRootIndex(model.index(model.rootPath()))
    tree.clicked.connect(_display_file)
    tree.collapsed.connect(_display_file)
    #tree.currentItemChanged.connect(_display_file)

    tree.setSortingEnabled(True)
    tree.sortByColumn(0,Qt.AscendingOrder)

    #create button section

    btn_add_file = QPushButton() #'create file' button
    btn_add_file.setText("Add File")
    btn_add_file.clicked.connect(_create_file)

    btn_add_folder = QPushButton()
    btn_add_folder.setText("Add Folder")
    btn_add_folder.clicked.connect(_create_folder)

    btn__delete = QPushButton()
    btn__delete.setText("delete")
    btn__delete.clicked.connect(_delete)

    btn___rename = QPushButton()
    btn___rename.setText("rename")
    btn___rename.clicked.connect(__rename)

    btn__backup = QPushButton()
    btn__backup.setText("backup")
    btn__backup.clicked.connect(_backup)

    btn_layout = QHBoxLayout() #button will run horizontal

    btn_layout.addWidget(btn_add_file) #add buttons horiz layout
    btn_layout.addWidget(btn_add_folder)
    btn_layout.addWidget(btn__delete)
    btn_layout.addWidget(btn___rename)
    btn_layout.addWidget(btn__backup)

    btns_widget = QWidget() #create temp widget
    btns_widget.setLayout(btn_layout) #add buttons layout to temp widget


    #set up textbox to display text
    global display
    display = QTextEdit()

    font = display.font() #create font obj
    font.setPointSize(14) #set font obj size

    display.setFont(font) #set widget to above size

    display.textChanged.connect(_update_file)

    #LHS of display
    splitter1 = QSplitter(Qt.Vertical) #splitter orientation, default is horizon
    splitter1.addWidget(btns_widget)
    splitter1.addWidget(tree)
    splitter1.setSizes([50,10000])

    #RHS of display
    splitter2 = QSplitter(Qt.Horizontal)
    splitter2.addWidget(splitter1)
    splitter2.addWidget(display)
    splitter2.setSizes([500, 600])


    hbox = QHBoxLayout()

    hbox.addWidget(splitter2)

    window.setLayout(hbox)

    window.show()
    qapp.exec_()


if __name__ == "__main__":
    notebk()

import lib.metalib as _meta
exec(_meta.print_funcs('_meta'))
