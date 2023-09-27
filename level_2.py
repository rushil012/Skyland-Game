# assignment: PA 5
# author: Rushil Nagpal
# date: June 9, 2023
# file: level_2.py is the second-level of PA 5 skyland game.
# description of output : avatar has to collect all the trophies(eggs) to win and avoid fish attack.

from tkinter import *
import tkinter.font as font
import math
import subprocess
import sys
WIDTH, HEIGHT = 600, 400 # global variables (constants) go here
CLOCK_RATE = 15
START_X, START_Y = 20, 350
END_X, END_Y = 400, 350

class OceanLand:
    
    def __init__(self, canvas):
        
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.canvas.bind_all('<KeyPress-Alt_L>', self.restart)
        self.canvas.bind_all('<KeyPress-2>', self.advance_to_next_level)
        self.land = Land(canvas)
        self.trophy = Trophy(canvas)
        
        self.fish1 = AI(canvas,50,230)
        self.fish2 = AI(canvas,500,145)
        self.fish3 = AI(canvas,100,330)
        self.avatar = Avatar(canvas)
        self.score = 0
        self.paused = False
        self.endgame = False
        self.time = 0
        self.var3 = 6
        self.var = False
        self.text = canvas.create_text(150, 370, text=f'Score: {self.score} Time: {self.time} ',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
        
        self.update()
        
        
    def restart(self, event=None):

        self.avatar.replace()
        self.trophy.replace()
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.time=0
        self.score = 0
        self.paused = False
        self.canvas.delete(self.text)
        self.text = canvas.create_text(150, 370, text=f'Score: {self.score} Time: {self.time} ',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
        
        
    def pause(self, event=None):
        self.paused = not self.paused  # Toggle the pause state
        if self.paused:
            if self.var:
                self.text = canvas.create_text(150, 370, text=f'GAME OVER YOU DIED , PRESS LEFT ALT TO RESTART',
                                       font=font.Font(family='Helveca', size='15', weight='bold'))
            elif self.var3 == 6:
                self.canvas.itemconfig(self.text, text=f'Score: {self.score} Time: {self.time:.2f} sec')
            elif self.score != 6:
                self.canvas.itemconfig(self.text, text=f'Score: {self.score} Time: {self.time:.2f} sec')
        else:
            self.canvas.itemconfig(self.text, text=f'Score: {self.score} Time: {self.time:.2f} sec')
           
    

    def update(self):
        if self.paused:
            pass
        else:
            self.avatar.update(self.land, self.trophy)
            self.time += 0.016
            self.canvas.itemconfig(self.text, text=f'Score: {self.score} Time: {self.time:.2f} sec')
            self.eatable = True
            self.var = False
            t = self.canvas.coords(self.avatar.head)
            a = self.canvas.coords(self.avatar.torso)
            self.fish1.update_for_1(self.eatable)
            self.fish2.update_for_2(self.eatable)
            self.fish3.update_for_1(self.eatable)
            if self.fish2.check_for_eat(t,a):
                self.var = True
                self.var3 = 8
                self.canvas.delete(self.text)
                self.pause()
                self.canvas.unbind_all('<KeyPress-space>')
            if self.fish1.check_for_eat(t,a):
                self.var3 = 8
                self.var = True
                self.canvas.delete(self.text)
                self.pause()
                self.canvas.unbind_all('<KeyPress-space>')
            if self.fish3.check_for_eat(t,a):
                self.var3 = 8
                self.var = True
                self.canvas.delete(self.text)
                self.pause()
                self.canvas.unbind_all('<KeyPress-space>')
            self.land.update()
            self.land.update1()
            if self.avatar.find_trophy(self.trophy.get_trophy()):
                self.score +=1 
            
            if self.score == 6:
                    self.canvas.delete(self.text)
                    self.var3 = 7
                    self.text = canvas.create_text(150, 370, text=f'                     YOU WON!! PRESS LEFT ALT TO RESTART',
                                        font=font.Font(family='Helveca', size='15', weight='bold'))
                    self.pause()
                    self.canvas.unbind_all('<KeyPress-space>')
                
        self.canvas.after(CLOCK_RATE, self.update)

    # """def play_music(self): # optional, do not use it in the submitted version
    #     if not mixer.get_init():
    #         mixer.init()
    #     self.sound = mixer.Sound('./sound1.mp3')
    #     self.sound.play()"""
    def advance_to_next_level(self, event=None):
        subprocess.Popen([sys.executable, 'level_2.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()
class Land:
    
    def __init__(self, canvas):

        self.canvas = canvas
        self.direction = 1
        # sky
        self.canvas.create_rectangle( 0, 0, WIDTH, START_Y-100,
                                 fill='grey')
        # valley
        self.canvas.create_rectangle( 0, START_Y-120, WIDTH, START_Y,
                                 fill='cyan')
        self.platforms = []
        
        tree1 = self.make_tree(100, 355, 100, 7)
        self.start = self.canvas.create_rectangle(0,0,8,START_Y,fill ="DarkGreen")
        self.ground = self.canvas.create_rectangle(0,350,WIDTH,355,fill="DarkGreen")
        self.stop = self.canvas.create_rectangle(592,0,600,START_Y,fill ="DarkGreen")
        self.platforms.append(self.ground)
        self.make_hill( 50, 230, 250, 230, height=100, delta=3)
        self.make_hill(150, 300, 350, 300, height=100, delta=3)
        self.make_hill(250, 250, 450, 250, height=100, delta=3)
        self.make_hill(350, 300, 550, 300, height=100, delta=3)
        
        
        tree2 = self.make_tree(320,260,100,7)
        
        self.platforms.append(canvas.create_rectangle(0,START_Y-100,60,START_Y-94,fill = "DarkGreen"))
        self.platforms.append(canvas.create_rectangle(235,250,325,START_Y+5,fill="DarkGreen"))   # 3 blocks
        self.platforms.append(canvas.create_rectangle(320,250,415,290,fill="DarkGreen"))   
        self.platforms.append(canvas.create_rectangle(320,330,435,START_Y+5,fill = "DarkGreen"))
        #self.platforms.append(canvas.create_polygon(235,250,415,250,415,290,320,290,320,330,435,330,435,START_Y,235,START_Y))
        nest_egg1 = self.canvas.create_arc(295, 146, 325, 166, start=180, extent=180, outline="black", width=2, fill="brown")
        
        cloud1 = self.make_cloud(40, 90)
        cloud2 = self.make_cloud(150, 50)
        cloud3 = self.make_cloud(340, 130)
        self.clouds = [cloud1, cloud2, cloud3]
        self.platforms.append(canvas.create_rectangle(0,147,145,153,fill="DarkGreen"))
        self.moving_platform = self.canvas.create_rectangle(360,75,410,81,fill="DarkGreen")
        y = self.canvas.coords(self.moving_platform)
        
    
        
        self.platforms.append(self.moving_platform)
        self.platforms.append(canvas.create_rectangle(500,150,600,156,fill="DarkGreen"))
        nest_egg2 = self.canvas.create_arc(93, 250, 123, 270, start=180, extent=180, outline="black", width=2, fill="brown")
        
        num_curves = 4
        curve_height = 20
        curve_spacing = 10
        start_angle = 45
        end_angle = 90
        radius = 95
        for i in range(num_curves):
            curve_y = START_Y + i * (curve_height + curve_spacing)
            start_angle += 10
            end_angle += 10
            radius += 10
            curve = self.make_sky_curves(canvas, START_X+40, -80+i*20, radius, 5, 225, 270, 'DarkBlue')
        radius = 95
        for i in range(num_curves):
            curve_y = START_Y + i * (curve_height + curve_spacing)
            start_angle += 10
            end_angle += 10
            radius += 10
            curve = self.make_sky_curves(canvas, 570+40, -70+i*20, radius, 5, 225,270, 'DarkBlue')
        
    WIDTH, HEIGHT = 600, 400
    def update1(self):
        if self.direction == 1:
            dx = 1.2  # Move right by 3 pixels
        else:
            dx = -1.2 # Move left by 3 pixels

        # Move the platform
        self.canvas.move(self.moving_platform, dx, 0)
        x1, _, x2, _ = self.canvas.coords(self.moving_platform)
        if x1 <= 250 or x2 >= 510:
            # Change the direction when the boundary is reached
            self.direction *= -1
        self.canvas.after(10000000000, self.update1)
    

    def make_hill(self, x1, y1, x2, y2, height=100, delta=3):
        points = [x1,y1,(height/delta)+x1+60,y1-height,x2,y2]               #x1+height
        self.canvas.create_polygon(points,fill = "tan1")

    def make_cloud(self, x, y):
        cloud_parts = []
        
        for i in range(3):
            cloud_parts.append(self.canvas.create_oval(x + i * 12, y, x + i * 12 + 30, y + 30,
                                                    outline='black', fill='lightsteelblue'))
        for i in range(-1,4):
            cloud_parts.append(self.canvas.create_oval(x + i * 12, y+15, x + i * 12 + 30, y + 45,
                                                    outline='black', fill='lightsteelblue'))
        for i in range(3):
            cloud_parts.append(self.canvas.create_oval(x + i * 12, y+30, x + i * 12 + 30, y + 60,
                                                    outline='black', fill='lightsteelblue'))
        
        return cloud_parts

    def make_tree(self, x, y, height, width):       #tree = self.make_tree(100, 350, 90, 7)
        tree_parts = []
        
        # Draw the tree trunk
        trunk = self.canvas.create_rectangle(x - width/2, y - height, x + width/2, y,
                                            fill='DarkGreen', outline='black')
        self.platforms.append(trunk)
        tree_parts.append(trunk)

        for i in range(5):
            tree_parts.append(self.canvas.create_polygon(x,y-height+12*i,x-3.5,y-height-3.5+12*i,x-29.5,y-height+30+12*i,x-26,y-height+33.5+12*i,fill = "DarkOliveGreen3"))
            tree_parts.append(self.canvas.create_polygon(x,y-height+12*i,x+3.5,y-height-3.5+12*i,x+29.5,y-height+30+12*i,x+26,y-height+33.5+12*i,fill = "DarkOliveGreen3"))
        return tree_parts

    def make_sky_curves(self,canvas, x, y, radius, thickness, start_angle, end_angle, color):
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius
        outline_width = 2 * thickness

        curve = canvas.create_arc(x1, y1, x2, y2, start=start_angle, extent=(end_angle - start_angle),
                                style='arc', outline=color, width=outline_width)
        return curve

    def get_obstacles(self):               #obstacles
        return  self.platforms
    
    def update(self):
        # Move the clouds slowly
        for cloud in self.clouds:
            for i in cloud:
                self.canvas.move(i, 0.10, 0)
        
        self.canvas.after(100000000, self.update)
    
class Trophy:
    
    def __init__(self, canvas):
        self.canvas = canvas
        purple_egg = self.canvas.create_oval(298, 150, 318, 160, fill='yellow')
        pink_egg = self.canvas.create_oval(325, 320, 345, 330, fill='pink')
        red_egg = self.canvas.create_oval(560,140,580,150,fill="cyan")
        blue_egg = self.canvas.create_oval(17,240,37,250,fill="red")
        yellow_egg = self.canvas.create_oval(100,253,120,263,fill="orchid")
        green_egg = self.canvas.create_oval(122,137,142,147,fill="lawngreen")
        self.trophies = [purple_egg, pink_egg,red_egg,blue_egg,yellow_egg,green_egg]
    def get_trophy(self):
        return self.trophies

    
    def replace(self):
        for t in self.get_trophy():
            self.canvas.delete(t)
        
        purple_egg = self.canvas.create_oval(298, 150, 318, 160, fill='orchid')
        pink_egg = self.canvas.create_oval(325, 320, 345, 330, fill='pink')
        red_egg = self.canvas.create_oval(560,140,580,150,fill="red")
        blue_egg = self.canvas.create_oval(17,240,37,250,fill="cyan")
        yellow_egg = self.canvas.create_oval(100,253,120,263,fill="yellow")
        green_egg = self.canvas.create_oval(122,137,142,147,fill="lawngreen")
        self.trophies = [purple_egg, pink_egg,red_egg,blue_egg,yellow_egg,green_egg]
    
class AI:

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.fish = self.make_fish(x, y)
        
        self.x, self.y = 0, 0.5
        self.direction = 1
        self.move_limit = 100000
        self.current_move = 0
    def make_fish(self, x, y):
        fish_parts = []
        
        # Draw the body of the fish
        body = self.canvas.create_oval(x - 20, y - 10, x + 20, y + 10, fill='grey', outline='black')
        fish_parts.append(body)
        
        # Draw the eyes
        eye1 = self.canvas.create_oval(x - 10, y - 5, x - 4, y + 1, fill='white', outline='black')
        eye2 = self.canvas.create_oval(x + 4, y - 5, x + 10, y + 1, fill='white', outline='black')
        fish_parts.extend([eye1, eye2])
        
        # Draw the legs
        leg1 = self.canvas.create_line(x - 14, y + 5, x - 20, y + 10, fill='black', width=2)
        leg2 = self.canvas.create_line(x - 14, y - 5, x - 20, y - 10, fill='black', width=2)
        leg3 = self.canvas.create_line(x + 14, y + 5, x + 20, y + 10, fill='black', width=2)
        leg4 = self.canvas.create_line(x + 14, y - 5, x + 20, y - 10, fill='black', width=2)
        fish_parts.extend([leg1, leg2, leg3, leg4])
        
        return fish_parts

    
    def update_for_2(self, eatable):
        fish_coords = self.canvas.coords(self.fish[0])
        fish_x = fish_coords[2]

        if fish_x <= 90 or fish_x >=550:
            self.direction *= -1
            self.current_move = 0

        if self.current_move < self.move_limit:
            self.canvas.move(self.fish[0], self.direction,0 )
            self.canvas.move(self.fish[1], self.direction,0 )
            for leg in self.fish[2:]:
                self.canvas.move(leg, self.direction,0 )
            self.current_move += 1

    
    # Draw the tail of the fish
        
    def check_for_eat(self,avatar_coords,avatar_coords1):
        self.avatar_coords = avatar_coords
        self.avatar_coords1 = avatar_coords1
            #x1 >= X1 and x2 <= X2 and y1  >=Y1 and y2 <= Y2 
        trophy_coords1= self.canvas.coords(self.fish[2])
        for part in self.fish:
            trophy_coords= self.canvas.coords(part) 
            if (avatar_coords[0] < trophy_coords[2] and avatar_coords[2] > trophy_coords[0] and avatar_coords[1] < trophy_coords[3] and avatar_coords[3] > trophy_coords[1]) or (avatar_coords[0] < trophy_coords1[2] and avatar_coords[2] > trophy_coords1[0] and avatar_coords[1] < trophy_coords1[3] and avatar_coords[3] > trophy_coords1[1]) or (avatar_coords1[0] < trophy_coords[2] and avatar_coords1[2] > trophy_coords[0] and avatar_coords1[1] < trophy_coords[3] and avatar_coords1[3] > trophy_coords[1]):
                return True
    def update_for_1(self, eatable):
        fish_coords = self.canvas.coords(self.fish[0])
        fish_x = fish_coords[2]
        X1,Y1,X2,Y2 = self.canvas.coords(self.fish[3])
        
        if fish_x <= 40 or fish_x >=550:
            self.direction *= -1
            self.current_move = 0

        if self.current_move < self.move_limit:
            self.canvas.move(self.fish[0], self.direction,0 )
            self.canvas.move(self.fish[1], self.direction,0 )
            for leg in self.fish[2:]:
                self.canvas.move(leg, self.direction, 0)
            self.current_move += 1
            
            
class Avatar:
    
    def __init__(self, canvas):
        color1 = 'lime'
        color2 = 'sandybrown'
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2)
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20,
                                                  fill=color1)
        self.canvas.move(self.head, START_X, START_Y-20)
        self.canvas.move(self.torso, START_X, START_Y-20)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.is_jumping = False
        self.falling = False
        self.gravity = 0.05
        self.x = 0
        self.y = 0
    
    def update(self, Land, Trophy): # call find_trophy and hit_object, check if jumping up or falling, etc.
                                    #Land = Land() #Trophy = Trophy() in OceanLand class
        self.find_trophy(Trophy.get_trophy())
        x1, y1, x2, y2 = self.canvas.coords(self.head)
        self.hit_object(Land)
        if x1 + self.x < 0 or x2 + self.x > WIDTH:
            self.x = 0

        if y1 + self.y < 0 or y2 + self.y > HEIGHT-60:
            self.y = 0

        if self.is_jumping:
            if self.y >= 0:
                self.is_jumping = False
                self.y = 1.25
                
        if self.y > 0:
            self.falling = True
        else:
            self.falling = False

        if self.falling:
            self.y = 1.25
        else:
            self.y += self.gravity

            if y2 + self.y >= HEIGHT-60:
                self.y = 0

        self.canvas.move(self.head, self.x, self.y)
        self.canvas.move(self.torso, self.x, self.y)
        
        
    def move(self, event=None):
        if event.keysym == 'Left':
            self.x = -1
        elif event.keysym == 'Right':
            self.x = 1
        elif event.keysym == 'Up': # jumping
            self.y = -2
        elif event.keysym == 'Down':
            self.y = 1
    def hit_object(self, lands):
        torso_coords = self.canvas.coords(self.torso)
        torso_x1, torso_y1, torso_x2, torso_y2 = torso_coords
        obstacles = lands.get_obstacles()
        for obstacle in obstacles:
            object_x1, object_y1, object_x2, object_y2 = self.canvas.coords(obstacle)

        # Check if the torso collides with the object without penetration
            if torso_x2 >= object_x1 and torso_x1 <= object_x2 and torso_y2 >= object_y1 and torso_y1 <= object_y2:
                # Move the avatar's torso back to avoid penetration
                if torso_x1 < object_x1 :
                    self.canvas.move(self.torso, -(torso_x2 - object_x1), 0)
                    self.canvas.move(self.head, -(torso_x2 - object_x1), 0)
                elif torso_x2 > object_x2:
                    self.canvas.move(self.torso, object_x2 - torso_x1, 0)
                    self.canvas.move(self.head, object_x2 - torso_x1, 0)
                if torso_y1 < object_y1:
                    self.canvas.move(self.torso, 0, -(torso_y2 - object_y1))
                    self.canvas.move(self.head, 0, -(torso_y2 - object_y1))
                elif torso_y2 > object_y2:
                    self.canvas.move(self.torso, 0, object_y2 - torso_y1)
                    self.canvas.move(self.head, 0, object_y2 - torso_y1)
       

                
    def find_trophy(self, trophy):
        avatar_coords = self.canvas.coords(self.torso)
        for troph in trophy:
            trophy_coords = self.canvas.coords(troph)
            if len(avatar_coords) >= 4 and len(trophy_coords) >= 4:
                if (
                    avatar_coords[0] < trophy_coords[2] and
                    avatar_coords[2] > trophy_coords[0] and
                    avatar_coords[1] < trophy_coords[3] and
                    avatar_coords[3] > trophy_coords[1]
                ):
                    # The avatar and trophy are overlapping
                    self.canvas.delete(troph)
                    return True  # Indicate successful overlap
        return False  # No overlap
    
    def replace(self):
        self.canvas.delete(self.head)
        self.canvas.delete(self.torso)
        self_is_jumping = False
        self.falling = False
        gravity = 0.05
        color1 = 'lime'
        color2 = 'sandybrown'
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2)
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20,
                                                  fill=color1)
        self.canvas.move(self.head, START_X, START_Y-20)
        self.canvas.move(self.torso, START_X, START_Y-20)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        
        self.x = 0
        self.y = 0
            
            
if __name__ == '__main__':
    
    tk = Tk()
    tk.title('OceanLand')
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
    canvas.pack()
    game = OceanLand(canvas)
    mainloop()
