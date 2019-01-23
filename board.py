import pygame
import sys
import tkinter
from Popup import *
from math import sqrt,pow
import os

class Game():
    def __init__(self):
        self.board_img = None
        self.green_coin = pygame.image.load ("greenCoin.png")
        self.red_coin = pygame.image.load ("redCoin.png")
        self.dead_cell = pygame.image.load ("deadCell.png")

        self.board_size = 0

        self.dict_size = {'x_margin':48,'y_margin':48,'x_gap':85,'y_gap':85}
        self.screen = None
        self.locationsPosList = []
        self.locationsFilledList = []

        self.player1 = 1
        self.player2 = 2

        self.turn = None

    def play(self):
        """Main function of the game"""
        while (not self.end_of_game()):

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP :
                    cell_pos = self.get_nearest_cell()
                    
                    if not self.place_coin(cell_pos):
                        break
                    self.check_changing_colors(cell_pos)

                    self.display()

                    print(self.locationsFilledList)
                    self.switch_turn()


                if event.type == pygame.QUIT:
                    sys.exit()

        self.count_score()
       
       #If the player want to play again the game is reset and the new party will begin
        if Popup().display_score(self.score1,self.score2):
            self.config(str(self.board_size)+"x"+str(self.board_size))
            self.play()


    def config(self,board_size):
        """Load the default board and display it"""
        pygame.init ()
        pygame.display.set_caption('Rolit Game')

        self.board_size = int(board_size.split('x')[0])
        self.board_img = pygame.image.load ("board_"+board_size+".png")
        im_size = self.board_img.get_size()
        self.screen = pygame.display.set_mode ((im_size[0], im_size[1]))
        self.screen.blit (self.board_img, (0,0))
            

        self.locationsFilledList.clear()
        self.fillLists()
        self.score1 = 0
        self.score2 = 0


        self.turn = self.player1
        self.place_dead_cells()

        self.display()


    def display(self):
        """Update and display the board"""
        pygame.display.flip()

    def get_pos_mouse(self):
        """Return the position of the mouse """
        x,y = pygame.mouse.get_pos()
        # print('Coords : {} , {}'.format(x,y))
        return (x,y)

    def get_nearest_cell(self):
        """Find the nearest cell from the position of the mouse"""
        x,y = self.get_pos_mouse()
        #print(x,y)
        nearest_cell = None
        shorter_distance = 10000

        #Not optimised
        for rowLocation in self.locationsPosList:
            for location in rowLocation:
                dist = self.distance((x,y),location)
                if dist<shorter_distance:
                    nearest_cell = location
                    shorter_distance = dist
        return nearest_cell

    def distance(self,fisrt_point:tuple,second_point:tuple):
        """Compute the distance between two positions"""
        return sqrt(pow(fisrt_point[0]-second_point[0],2)+pow(fisrt_point[1]-second_point[1],2))

    def place_dead_cells(self):
        """Place a black cell which allow the game to be fair"""
        i,j = (2,2)
        cell_pos = self.pos_from_cell_index((i,j))
        if self.locationsFilledList[i][j]==0:
            self.add_img(self.dead_cell,cell_pos)
            self.locationsFilledList[i][j]=100
        else :
            print('Cell already full - Coords : {} , {}'.format(i,j))

    def place_coin(self,cell_pos:tuple):
        """Place a coin in a valid cell"""
        i,j = self.cell_index_from_pos(cell_pos)
        print(i,j)
        if self.exist_adjacent_cell((i,j)):
            if self.locationsFilledList[i][j]==0:
                if self.turn==self.player1:
                    self.add_img(self.red_coin,cell_pos)
                else:
                    self.add_img(self.green_coin,cell_pos)
                self.locationsFilledList[i][j]=self.turn
                return True
            else :
                print('Cell already full - Coords : {} , {}'.format(i,j))
        Popup().place_near_coin()
        return False


    def check_changing_colors(self,cell_pos:tuple):
        """Check if some coins near the last coin placed need to be roll and roll them after"""
        index_initial_cell_filled = self.cell_index_from_pos(cell_pos)

        # get the eight coordinates to add from (-1,-1) to (1,1)
        possible_lines = [(i,j) for i in range(-1,2) for j in range(-1,2) if i!=0 or j!=0]


        for l in range(len(possible_lines)):
            stack = []

            while True:
                a = index_initial_cell_filled[0]+possible_lines[l][0]*(len(stack)+1)
                b = index_initial_cell_filled[1]+possible_lines[l][1]*(len(stack)+1)
                # print('Other cell : ({},{})'.format(a,b))

                try :
                    self.locationsFilledList[a][b]
                except IndexError:
                    break
                if(a<0 or b<0):
                    break
                if(self.locationsFilledList[a][b] == 0):
                    break
                elif (self.locationsFilledList[a][b] == self.turn):
                    stack.append((a,b))
                    break
                stack.append((a,b))
                # print(stack)
            if len(stack)>0 and self.locationsFilledList[stack[-1][0]][stack[-1][1]] == self.turn:
                [self.roll(index) for index in stack]
                    

    def switch_turn(self):
        """Let the other player play"""
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    def cell_index_from_pos(self,cell_pos:tuple):
        """Get the index of a cell passing its coordonates"""
        i = int((cell_pos[0]-self.dict_size['x_margin'])/self.dict_size['x_gap'])
        j = int((cell_pos[1]-self.dict_size['y_margin'])/self.dict_size['y_gap'])
        return (j,i)

    def pos_from_cell_index(self,cell_index:tuple):
        """Get the position of a cell passing its indexes"""
        x = cell_index[0] *self.dict_size['x_gap']+ self.dict_size['x_margin']
        y = cell_index[1] *self.dict_size['y_gap']+ self.dict_size['y_margin']
        return (x,y)

    def end_of_game(self):
        """Define whether a game is ended or not"""
        for rowLocation in self.locationsFilledList:
            for location in rowLocation:
                if location == 0 :
                    return False
        return True

    def fillLists(self):
        """Fill the board with zeros and fill the position representation of the board with the potiosioning values"""
        for i in range(self.board_size):
            self.locationsFilledList.append([])
            [self.locationsFilledList[i].append(0) for y in range(self.board_size)]
                

        for i in range(self.board_size):
            x = i * self.dict_size['x_gap']+ self.dict_size['x_margin']
            self.locationsPosList.append([])
            for j in range(self.board_size):
                y = j * self.dict_size['y_gap']+ self.dict_size['y_margin']
                self.locationsPosList[i].append((x,y))

    def add_img(self,img,pos:tuple):
        """Place a coin image on the board"""
        x,y = pos
        x -= img.get_size()[0]/2
        y -= img.get_size()[1]/2
        self.screen.blit(img,(x,y))

    def roll(self,cell_index:tuple):
        """Roll a cell to the color of the other player"""
        # print("Cell to be rolled : ({},{})".format(cell_index[0],cell_index[1]))
        i,j = cell_index
        cell_pos = self.pos_from_cell_index((j,i))
        # print(cell_pos)
        if self.turn==self.player1:
            self.add_img(self.red_coin,cell_pos)
        else:
            self.add_img(self.green_coin,cell_pos)
        self.locationsFilledList[cell_index[0]][cell_index[1]]=self.turn

    def exist_adjacent_cell(self,cell_index:tuple):
        """Test to know if there is a coin in the surrounding cells"""
        possible_cells = [(i,j) for i in range(-1,2) for j in range(-1,2) if i!=0 or j!=0]

        exist = False
        for l in range(len(possible_cells)):
            i = cell_index[0]+possible_cells[l][0]*1
            j = cell_index[1]+possible_cells[l][1]*1

            try :
                self.locationsFilledList[i][j]
            except IndexError:
                continue

            if(i<0 or j<0):
                continue
            if(self.locationsFilledList[i][j] != 0):
                exist = True

        # print(exist)
        return exist


    def count_score(self):
        """Count the fianl score"""
        for rowLocation in self.locationsFilledList:
            for location in rowLocation:
                if location == 1 :
                    self.score1+=1
                elif location == 2 :
                    self.score2+=1


if __name__ == '__main__':
    myB = Game()
    try:
        myB.config(Popup().choose_size())
        myB.play()
    except ValueError:
        print('Game was closed before the beginning')
    
