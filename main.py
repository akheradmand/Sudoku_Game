import sys
import random
from functools import partial
from sudoku import Sudoku
from PySide6.QtWidgets import *
from main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menu_new.triggered.connect(self.new_game)
        self.ui.menu_open_file.triggered.connect(self.open_file)
        self.line_edits=[[None for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                new_cell=QLineEdit()
                self.ui.grid_layout.addWidget(new_cell,i,j)
                # new_cell.textChanged.connect(partial(self.validation,i,j))
                self.line_edits[i][j]=new_cell
        self.new_game()
        for i in range(0,9):
            for j in range(0,9):
                self.line_edits[i][j].textChanged.connect(partial(self.validation,i,j))

    def open_file(self):
        file_path=QFileDialog.getOpenFileName(self,"Open File...")[0]
        # print(file_path)
        f=open(file_path, "r")
        big_text=f.read()
        rows=big_text.split("\n")
        puzzle_board=[[None for i in range(9)] for j in range(9)]
        for i in range(len(rows)):
            cells=rows[i].split(" ")
            for j in range(len(cells)):
                puzzle_board[i][j]=int(cells[j])
        # print(puzzle_board)

        for i in range(9):
            for j in range(9):
                self.line_edits[i][j].setReadOnly(False)
                if puzzle_board[i][j] != 0:
                    self.line_edits[i][j].setText(str(puzzle_board[i][j]))
                    self.line_edits[i][j].setReadOnly(True)
                else:
                    self.line_edits[i][j].setText("")

    def new_game(self):
        puzzle=Sudoku(3,seed=random.randint(1,1000)).difficulty(0.5)
        # print(puzzle.board)
        for i in range(9):
            for j in range(9):
                self.line_edits[i][j].setReadOnly(False)
                # self.line_edits[i][j].setStyleSheet("background-color:white")
                if puzzle.board[i][j] != None:
                    self.line_edits[i][j].setText(str(puzzle.board[i][j]))
                    self.line_edits[i][j].setReadOnly(True)
                    # self.line_edits[i][j].setStyleSheet("background-color:gray")
                else:
                    self.line_edits[i][j].setText("")

    def check(self,i,j):
        for m in range(0,9):
            for n in range(0,9):
                self.line_edits[m][n].setStyleSheet("background-color:white")
        
        number1=self.line_edits[i][j].text()
        for k in range(0,9):
            number2=self.line_edits[i][k].text()
            if j != k and number2 != "" and number1==number2:
                self.line_edits[i][j].setStyleSheet("background-color:red")
                # self.line_edits[i][k].setStyleSheet("background-color:blue")
                return False
            
        for k in range(0,9):
            number2=self.line_edits[k][j].text()
            if i != k and number2 != "" and number1==number2:
                self.line_edits[i][j].setStyleSheet("background-color:red")
                # self.line_edits[k][j].setStyleSheet("background-color:blue")
                return False
                
        if 0<=i<3:
            if 0<=j<3:
                self.square_check(i,j,0,0,number1)
            elif 3<=j<6:
                self.square_check(i,j,0,3,number1)
            elif 6<=j<9:
                self.square_check(i,j,0,6,number1)
        elif 3<=i<6:
            if 0<=j<3:
                self.square_check(i,j,3,0,number1)
            elif 3<=j<6:
                self.square_check(i,j,3,3,number1)
            elif 6<=j<9:
                self.square_check(i,j,3,6,number1)
        elif 6<=i<9:
            if 0<=j<3:
                self.square_check(i,j,6,0,number1)
            elif 3<=j<6:
                self.square_check(i,j,6,3,number1)
            elif 6<=j<9:
                self.square_check(i,j,6,6,number1)

        return True

    def square_check(self,i,j,lower_row_bound,lower_col_bound,number1):
        for m in range(lower_row_bound,3+lower_row_bound):
            for n in range(lower_col_bound,3+lower_col_bound):
                number2=self.line_edits[m][n].text()
                if m!=i and n!=j and number2 != "" and number1==number2:
                    self.line_edits[i][j].setStyleSheet("background-color:red")
                    # self.line_edits[m][n].setStyleSheet("background-color:blue")
                    return False

    def validation(self,i,j,text):
        if text not in ["1","2","3","4","5","6","7","8","9"]:
            self.line_edits[i][j].setText("")
            
        self.check(i,j)
        complete=1
        for x in range(9):
            for y in range(9):
                if self.line_edits[x][y].text() == "":
                    complete=0
                    break
            
        if complete==1 and self.check(i,j)==True:
            msg_box= QMessageBox()
            msg_box.setText("🎉You Win🎉")
            msg_box.exec()

if __name__=="__main__":
    app=QApplication(sys.argv)

    window=MainWindow()
    window.show()

    app.exec()
    