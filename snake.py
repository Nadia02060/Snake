from tkinter import *
from random import randint


UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

UPLOAD_TIME = 100
SNAKE_HEAD_SIZE = 10
SNAKE_SPAWN_POINT = 0
SNAKE_ALIVE = True
SNAKE_COLOR = "orange"
JUMP_LENGHT = 10
flag = 1
FOOD_COLOR = "Red"  

    
class Main:
    snake_head_move_direction = RIGHT
    body_blocs = []
    body_blocs_coords = []
    food_id = None
    score = 0
    coords_for_new_bloc = []
    move_keys = [UP, DOWN, LEFT, RIGHT]
    
    #Construction du terrain+serpent
    
            
    def __init__(self) :
        
        self.root = Tk()
        self.root.title("Snake")
        self.root.config(background="grey")
        self.boutonA = Button(self.root, text="Play",width= 5, height= 1, anchor= CENTER, font="Arial 25 italic", command=Tk.command, bg="White")    
        self.root.bind("<Any-KeyPress>", self.change_direction)
        self.root.bind("<Button-1>", self.move_snake_head)
        
        
        self.root.focus_set()
        self.playground = Canvas(self.root, width= 500, height= 500, bg="White" )
        self.scoreLab= Label(self.root, text="Score: " + str(self.score), font="Arial 15 bold", fg="white", bg="grey")
        self.snake_head = self.playground.create_rectangle(SNAKE_SPAWN_POINT+ 1, 1,  SNAKE_HEAD_SIZE + SNAKE_SPAWN_POINT - 1, SNAKE_HEAD_SIZE - 1, fill=SNAKE_COLOR, outline= SNAKE_COLOR)
        self.body_blocs.append(self.snake_head)
        self.body_blocs_coords.append(self.playground.coords(self.snake_head))
        
        for n in range(3):
            bloc_spawn_point = 10 * n
            self.body_blocs.append(self.playground.create_rectangle(bloc_spawn_point, 0, SNAKE_HEAD_SIZE+ bloc_spawn_point, SNAKE_HEAD_SIZE, fill=SNAKE_COLOR, outline= SNAKE_COLOR))
            self.body_blocs_coords.append(self.playground.coords(self.body_blocs[n]))
        
        
        self.body_blocs_coords = self.body_blocs_coords[:-1]
        self.scoreLab.pack()
        self.boutonA.pack(side= BOTTOM, pady= 10)
        self.playground.pack()
        self.generate_snake_food()
        self.root.after(UPLOAD_TIME, self.move_snake_head)
        self.root.mainloop()
        
    #Les mouvements du serpent avec les flèches    
    def change_direction(self, event) :    
        key = event.keysym
        if key == RIGHT:
            self.snake_head_move_direction = RIGHT
        elif key == LEFT:
            self.snake_head_move_direction = LEFT
        elif key == UP:
            self.snake_head_move_direction = UP
        elif key == DOWN:
            self.snake_head_move_direction = DOWN        
       
            
            
    
    #Déplacement du serpent    
    def move_snake_head(self) :
        snake_head_coords = self.playground.coords(self.snake_head)
    
        global SNAKE_ALIVE
        if (snake_head_coords[0] >= 500 or snake_head_coords[0] < 0) or (snake_head_coords[1] >= 500) or (snake_head_coords[1] < 0): 
            self.game_over()
                
        if SNAKE_ALIVE:
            new_x = 0
            new_y = 0
            if self.snake_head_move_direction == RIGHT:
                 new_x = JUMP_LENGHT
            elif self.snake_head_move_direction == LEFT:
                 new_x = -JUMP_LENGHT   
            elif self.snake_head_move_direction == UP:
                 new_y = -JUMP_LENGHT
            elif self.snake_head_move_direction == DOWN:
                 new_y = JUMP_LENGHT   
                 
            
            
            self.follow_snake_head()
            
            self.playground.move(self.snake_head, new_x, new_y)     
            self.body_blocs_coords[0] = self.playground.coords(self.snake_head)
            
            self.check_contacts()
            
            self.root.after(UPLOAD_TIME, self.move_snake_head)

        
    
    #Bloc des coordonnées 
    def follow_snake_head(self):
        num_of_blocs = len(self.body_blocs)
        reversed_body_blocs = self.body_blocs[: : -1]
        reversed_body_blocs_coords = self.body_blocs_coords[:: -1]
        for n in range (num_of_blocs):
            if n < num_of_blocs - 1:
                new_coords_index = n 
                new_coords = reversed_body_blocs_coords [new_coords_index] [:]
                self.playground.coords(reversed_body_blocs[n], new_coords [0], new_coords [1], new_coords [2], new_coords [3])
        
        for n in range (num_of_blocs):  
            if n > 0:
                self.body_blocs_coords[n - 1] = self.playground.coords(self.body_blocs[n - 1])
               
               
        self.coords_for_new_bloc = self.body_blocs_coords[num_of_blocs - 2] [:]
            
    #Nourriture du serpent
    def generate_snake_food(self):
        x_coords = randint(0, 49)
        y_coords = randint(0, 49)
        x_coords *= 10
        y_coords *= 10
        
        food_coords = [x_coords + 1, y_coords + 1, x_coords + 9, y_coords + 9]
        while food_coords in self.body_blocs_coords:
             food_coords = [x_coords + 1, y_coords + 1, x_coords + 9, y_coords + 9]
        
        self.food_id = self.playground.create_oval(food_coords[0], food_coords[1], food_coords[2], food_coords[3], fill=FOOD_COLOR, outline= FOOD_COLOR)

        
    def check_contacts(self):
        detect_coords = self.playground.coords(self.snake_head)
        overlapped_items = self.playground.find_overlapping (detect_coords[0], detect_coords[1], detect_coords[2], detect_coords[3])

        if self.food_id in overlapped_items:
            self.playground.delete(self.food_id)
            self.generate_snake_food()
            self.add_score()
      
        if any(i in overlapped_items for i in self.body_blocs[1:]):
            self.game_over()
    
    #Fin du jeu
    def game_over(self):
         global SNAKE_ALIVE
         SNAKE_ALIVE = False
         self.playground.create_text(250, 250, anchor=CENTER, text="Perdu", font="Arial 25 bold", fill="Black")
    
    
    #Compteur
    def add_score(self):
         self.score += 1
         self.scoreLab["text"]= "Score: " + str(self.score)     
         new_bloc = self.playground.create_rectangle(self.coords_for_new_bloc[0], self.coords_for_new_bloc[0], self.coords_for_new_bloc[0], self.coords_for_new_bloc[3], fill=SNAKE_COLOR, outline=SNAKE_COLOR)
         self.body_blocs.append(new_bloc)
         self.body_blocs_coords.append(self.playground.coords(new_bloc)) 
         


if __name__ == "__main__":       
   Main()                
