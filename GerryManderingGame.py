import tkinter
from tkinter import *
import time


class GerryMander(Frame):
    def __init__(self,master):
        Frame.__init__(self,master=None)
        self.x = self.y = 0
        self.canvas = Canvas(master,  cursor="cross")
        self.canvas.config(background = "white")
        self.blue1 = self.canvas.create_rectangle(0, 500, 200, 80, fill='blue')
        self.blue2 = self.canvas.create_rectangle(200, 100, 500, 80, fill='blue')
        self.red1 = self.canvas.create_rectangle(0, 0, 500, 80, fill='red')
        self.red2 = self.canvas.create_rectangle(200, 400, 500, 100, fill='red')
        
        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
        self.sbarv.grid(row=0,column=1,stick=N+S)
        self.sbarh.grid(row=1,column=0,sticky=E+W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)


        self.rect = None

        self.start_x = None
        self.start_y = None 
        global count
        count = IntVar(self)

        global countR
        countR = IntVar(self)

        global countB
        countB = IntVar(self)

        global length_blue1
        length_blue1 = IntVar(self)
        length_blue1.set(4)

        global length_blue2
        length_blue2 = IntVar(self)
        length_blue2.set(4)

        global length_red1
        length_red1 = IntVar(self)
        length_red1.set(4)

        global length_red2
        length_red2 = IntVar(self)
        length_red2.set(3)


    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        #if not self.rect:
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill="", outline="white", width=3)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)


    #this variable is to count the number of districts made
    numPrint = None
    bluePrint = None
    redPrint = None
    winPrint = None
       
    #this method determines what happens when you release your click (when the rectangle is made)           
    def on_button_release(self, event):
        self.canvas.delete(self.numPrint)
        count.set(count.get() + 1)
        self.numPrint = self.canvas.create_text(70,10,fill="white", font="Times 16 bold", text = ("districts: " + str(count.get())))
        #print("y = " + str(event.x))
        #print("x = " + str(event.y))
        result_blue1 = self.canvas.find_overlapping(0, 500, 200, 80)
        result_blue2 = self.canvas.find_overlapping(200, 100, 500, 80)
        result_red1 = self.canvas.find_overlapping(0, 0, 500, 80)
        result_red2 = self.canvas.find_overlapping(200, 400, 500, 100)

        #if it is in all of them
        if len(result_blue1) > length_blue1.get() and len(result_red1) > length_red1.get() and len(result_blue2) > length_blue2.get() and len(result_red2) > length_red2.get():
            #print("all overlap")
            side1_bool = False #false for blue, true for red
            no_winner = False
            
            length_blue1.set(len(result_blue1))
            length_red1.set(len(result_red1))
            length_blue2.set(len(result_blue2))
            length_red2.set(len(result_red2))

            coords_drawn = self.canvas.coords(self.rect) #1
            coords_blue1 = self.canvas.coords(self.blue1) #2
            coords_red1 = self.canvas.coords(self.red1) #3
            coords_blue2 = self.canvas.coords(self.blue2) #4
            coords_red2 = self.canvas.coords(self.red2) #5

            topOfBlue1 = coords_blue1[1]
            topOfBlue1 = topOfBlue1 - 80
            bottomOfRed1 = topOfBlue1

            topOfDrawn = coords_drawn[1] - 80
            bottomOfDrawn = coords_drawn[3] - 80
            total_side1 = topOfDrawn + bottomOfDrawn
            #print(total_side1)

            sideOfBlue1 = coords_blue1[2]
            #print("the x center: " + str(sideOfBlue1))
            sideOfBlue1 = sideOfBlue1 - 200
            sideOfRed1 = sideOfBlue1

            side1OfDrawn = coords_drawn[0] - 200
            side2OfDrawn = coords_drawn[2] - 200
            total_sides = side1OfDrawn + side2OfDrawn
            #print(total_sides)

            if total_side1 > 0:
                #print("majority blue for side 1")
                side1_bool = False
            elif total_side1 < 0:
                #print("majority red for side 1")
                side1_bool = True
            else:
                #print("no clear winner for side 1")
                no_winner = True

            #the other side will always be a red majority because there is little blue
            #print("majority red for side 2")
            side2_bool = True

            if side2_bool == True and side1_bool == True or total_sides > 0:
                #print("majority is red")
                countR.set(countR.get() + 1)
            elif side2_bool == True and side1_bool == False and no_winner == True or total_sides < 0:
                #print("majoirty is blue")
                countB.set(countB.get() + 1)
            elif side2_bool == True and side1_bool == False and no_winner == False:
                print("there is no winner")

        #if it is blue2 and both reds
        elif len(result_blue2) > length_blue2.get() and len(result_red2) > length_red2.get() and len(result_red1) > length_red1.get():
            length_blue2.set(len(result_blue2))
            length_red2.set(len(result_red2))
            length_red1.set(len(result_red1))

            coords1 = self.canvas.coords(self.rect)

            topOfDrawnto_botOfRed = coords1[1] - 80
            bottomOfDrawnto_botOfBlue = coords1[3] - 100
            total_red = topOfDrawnto_botOfRed + bottomOfDrawnto_botOfBlue
            total_area = coords1[0] * coords1[1]
            total_blue = total_area - total_red
            #print("red: " + str(total_red))
            #print("blue: " + str(total_blue))

            if total_red > 6.0:
              #print("majority red")
              countR.set(countR.get() + 1)
            else:
              #print("majority blue")
              countB.set(countB.get() + 1)
              
        #if it is in blue1 and red1
        elif len(result_blue1) > length_blue1.get() and len(result_red1) > length_red1.get():
            #print("blue1 and red1")
            length_blue1.set(len(result_blue1))
            length_red1.set(len(result_red1))

            coords1 = self.canvas.coords(self.rect)
            coords2 = self.canvas.coords(self.blue1)
            coords3 = self.canvas.coords(self.red1)

            topOfBlue = coords2[1]
            topOfBlue = topOfBlue - 80
            bottomOfRed = topOfBlue

            topOfDrawn = coords1[1] - 80
            bottomOfDrawn = coords1[3] - 80
            total = topOfDrawn + bottomOfDrawn
            print(total)

            if total > 0:
                #print("majority blue")
                countB.set(countB.get() + 1)
            elif total < 0:
                #print("majority red")
                countR.set(countR.get() + 1)
            else:
                print("no clear winner")

        #if it is in blue1 and red2
        elif len(result_blue1) > length_blue1.get() and len(result_red2) > length_red2.get():
            length_blue1.set(len(result_blue1))
            length_red2.set(len(result_red2))
            #print("blue1 and red2")

            coords1 = self.canvas.coords(self.rect)
            coords2 = self.canvas.coords(self.blue1)
            coords3 = self.canvas.coords(self.red2)

            sideOfBlue = coords2[2]
            sideOfBlue = sideOfBlue - 200
            sideOfRed = sideOfBlue

            side1OfDrawn = coords1[0] - 200
            side2OfDrawn = coords1[2] - 200
            total = side1OfDrawn + side2OfDrawn
            print(total)

            if total < 0:
                #print("majority blue")
                countB.set(countB.get() + 1)
            elif total > 0:
                #print("majority red")
                countR.set(countR.get() + 1)
            else:
                print("no clear winner")
            
        #if it is blue2 and red1
        elif len(result_blue2) > length_blue2.get() and len(result_red1) > length_red1.get():
            #print("blue2 and red1")
            length_blue2.set(len(result_blue2))
            length_red1.set(len(result_red1))
            
            coords1 = self.canvas.coords(self.rect)
            coords2 = self.canvas.coords(self.blue2)
            coords3 = self.canvas.coords(self.red1)

            topOfBlue = coords2[1]
            topOfBlue = topOfBlue - 80
            bottomOfRed = topOfBlue

            topOfDrawn = coords1[1] - 80
            bottomOfDrawn = coords1[3] - 80
            total = topOfDrawn + bottomOfDrawn
            #print(total)

            if total > 0:
                #print("majority blue")
                countB.set(countB.get() + 1)
            elif total < 0:
                #print("majority red")
                countR.set(countR.get() + 1)
            else:
                print("no clear winner")

        #if it is blue2 and red2
        elif len(result_blue2) > length_blue2.get() and len(result_red2) > length_red2.get():
            #print("blue2 and red2")
            length_blue2.set(len(result_blue2))
            length_red2.set(len(result_red2))
            
            coords1 = self.canvas.coords(self.rect)
            coords2 = self.canvas.coords(self.blue2)
            coords3 = self.canvas.coords(self.red2)

            topOfRed = coords3[1]
            topOfRed = topOfRed - 100
            bottomOfBlue = topOfRed

            topOfDrawn = coords1[1] - 100
            bottomOfDrawn = coords1[3] - 100
            total = topOfDrawn + bottomOfDrawn
            #print(total)

            if total < 0:
                #print("majority blue")
                countB.set(countB.get() + 1)
            elif total > 0:
                #print("majority red")
                countR.set(countR.get() + 1)
            else:
                print("no clear winner")

        #if it is just in blue1
        elif len(result_blue1) > length_blue1.get():
            #print(result_blue1)
            length_blue1.set(len(result_blue1))
            #print("there is only overlap in blue, blue majority")
            countB.set(countB.get() + 1)

        #if it is just in blue2
        elif len(result_blue2) > length_blue2.get():
            #print(result_blue2)
            length_blue2.set(len(result_blue2))
            #print("there is only overlap in blue, blue majority")
            countB.set(countB.get() + 1)

        #if it is just in red1
        elif len(result_red1) > length_red1.get():
            #print(result_red1)
            length_red1.set(len(result_red1))
            #print("there is only overlap in red, red majority")
            countR.set(countR.get() + 1)

        #if it is just in red2
        elif len(result_red2) > length_red2.get():
            #print(result_red2)
            length_red2.set(len(result_red2))
            #print("there is overlap in red, red majority")
            countR.set(countR.get() + 1)

        print("number of districts: " + str(count.get()))
        print("red is currently: " + str(countR.get()))
        print("blue is currently: " + str(countB.get()))

        #if the district count is 5
        if count.get() == 5:
            self.canvas.delete(self.numPrint)

            if countR.get() > countB.get():
                final = "you made red win!"

            elif countR.get() < countB.get():
                final = "you made blue win!"
            
            else:
                final = "you made it a draw!"
                
            self.redPrint = self.canvas.create_text(60,10,fill="white", font="Times 16 bold", text = ("Red: " + str(countR.get())))
            self.bluePrint = self.canvas.create_text(60,30,fill="white", font="Times 16 bold", text = ("Blue: " + str(countB.get())))
            self.winPrint = self.canvas.create_text(110,50,fill="white", font="Times 16 bold", text = final)

        pass

    

    #this method restarts the board clean
    def refresh(self):
        self.canvas.delete("all")
        self.__init__(None)



#running the game              
if __name__ == "__main__":
    root=Tk()
    map1 = GerryMander(root)
    def redo():
        time.sleep(0.8)
        map1.refresh()

    root.title("Gerrymandering Game")
    instruct = Label(root, text = "draw 5 districts for the area and try to make one color win!")
    instruct.grid(row=4, column=0, columnspan=2)
    
    endButton = Button(root, text="refresh", command=redo)
    endButton.grid(row=6, column=0, columnspan=2)
 
    instruct2 = Label(root, text = "Look at your squares, how many are mostly blue verses red?")
    instruct2.grid(row=8, column=0, columnspan=2)


    root.resizable(True, True)
    
    root.mainloop()




    
