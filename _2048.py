
import random
import copy
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time


class Tile():
	def __init__(self,value,x,y):
		self.value = value
		self.x = x
		self.y = y

class Board():
	def __init__(self,rows,collumns):
		

		self.rows = rows
		self.collumns = collumns
		self.board = []
		self.points = 0

		for row in range(rows):
			cur_row = []
			for col in range(collumns):
				cur_row.append(Tile(0,row,col))

			self.board.append(cur_row)

		for i in range(2):
			ran_pos = self.random_position()
			self.board[ran_pos[0]][ran_pos[1]] = Tile(2,ran_pos[0],ran_pos[1])

	def add_number(self):
		ran_pos = self.random_position()
		self.board[ran_pos[0]][ran_pos[1]] = random.choice((
			Tile(2,ran_pos[0],ran_pos[1]),
			Tile(4,ran_pos[0],ran_pos[1])
			))

	def random_position(self):
		positions = []
		
		for row in self.board:
			for col in row:
				if col.value == 0:
					positions.append((col.x,col.y))

		return random.choice(positions)

	def print(self):
		for row in self.board:
			cur_row = ""
			for col in row:
				cur_row += str(col.value) + ", "

			print(cur_row)

		print(f"cur points {self.points}")

	@property
	def status(self):

		board_status = 0
		for row in self.board:
			for col in row:
				if col.value == 2048:
					return 2
				elif col.value == 0:
					board_status = 1

		if board_status == 1:
			return 0

		for x_offset in (-1, 1):
			moved_board = copy.deepcopy(self)
			moved_board.move(x_offset=x_offset)
			if moved_board.board != self.board:
				return 0

		for y_offset in (-1, 1):
			moved_board = copy.deepcopy(self)
			moved_board.move(y_offset=y_offset)
			if moved_board.board != self.board:
				return 0

		return 1

	def move(self,x_offset=0,y_offset=0):

		if y_offset != 0:
			for i in range(self.collumns):
				for row in self.board:
					for col in row:
						if col.value != 0:
							if (col.y != 0 and y_offset == -1) or (col.y != self.collumns-1 and y_offset == 1):
								if row[col.y+y_offset].value == 0:
									row[col.y+y_offset].value = col.value
									row[col.y].value = 0

								elif row[col.y+y_offset].value == col.value:
									row[col.y+y_offset].value = col.value * 2
									row[col.y].value = 0

									self.points += col.value * 2

		if x_offset != 0:
			for i in range(self.rows):
				for row in self.board:
					for col in row:
						if col.value != 0:
							if (col.x != 0 and x_offset == -1) or (col.y != self.rows-1 and y_offset == 1):
								if self.board[col.x+x_offset][col.y].value == 0:
									self.board[col.x+x_offset][col.y].value = col.value
									self.board[col.x][col.y].value = 0

								elif self.board[col.x+x_offset][col.y].value == col.value:
									self.board[col.x+x_offset][col.y].value = col.value * 2
									self.board[col.x][col.y].value = 0

									self.points += col.value * 2

		self.add_number()

			
class MainWindow(QMainWindow):

	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("2048")
		self.board = Board(4,4)

		self.update_layout()


	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Up:
			self.board.move(x_offset = -1)
		elif event.key() == Qt.Key_Down:
			self.board.move(x_offset = 1)

		elif event.key() == Qt.Key_Left:
			self.board.move(y_offset = -1)
		elif event.key() == Qt.Key_Right:
			self.board.move(y_offset = 1)

		board_status = self.board.status
		if board_status != 0:
			self.game_end(board_status)
			return

		self.update_layout()

	def update_layout(self):

		self.layout = QGridLayout()

		for row in self.board.board:
			for col in row:
				self.layout.addWidget(QLabel(f"{col.value}"), col.x, col.y)

		self.widget = QWidget()
		self.widget.setLayout(self.layout)

		self.setCentralWidget(self.widget)

	def game_end(self, board_status):

		self.layout = QVBoxLayout()

		if board_status == 1:
			self.layout.addWidget(QLabel("Prohrál jsi!"))

		elif board_status == 2:
			self.layout.addWidget(QLabel("Vyhrál jsi!"))

		self.widget = QWidget()
		self.widget.setLayout(self.layout)

		self.setCentralWidget(self.widget)
		


def main():

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()

if __name__ == "__main__":
	main()