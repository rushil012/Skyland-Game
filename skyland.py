# assignment: PA 5
# author: Rushil Nagpal
# date: June 9, 2023
# file: skyland.py is a one-level game
# description of output : avatar has to collect all the trophies(eggs) to win and avoid spider attack.

from tkinter import *
import tkinter.font as font
import math
import subprocess
import sys
WIDTH, HEIGHT = 600, 400 # global variables (constants) go here
CLOCK_RATE = 15
START_X, START_Y = 20, 350
END_X, END_Y = 400, 350

class Skyland:
    
    def __init__(self, canvas):
        
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.canvas.bind_all('<KeyPress-Alt_L>', self.restart)
        self.canvas.bind_all('<KeyPress-2>', self.advance_to_next_level)
        self.land = Land(canvas)
        self.trophy = Trophy(canvas)
        
        self.spider1 = AI(canvas,50,230)
        self.spider2 = AI(canvas,500,145)
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
            self.spider1.update_for_1(self.eatable)
            self.spider2.update_for_2(self.eatable)
            if self.spider2.check_for_eat(t,a):
                self.var = True
                self.var3 = 8
                self.canvas.delete(self.text)
                self.pause()
                self.canvas.unbind_all('<KeyPress-space>')
            if self.spider1.check_for_eat(t,a):
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
                    self.text = canvas.create_text(150, 370, text=f'                                                          YOU WON!! PRESS LEFT ALT TO RESTART, Press 2 to advance to next level',
                                        font=font.Font(family='Helveca', size='11', weight='bold'))
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
                                 fill='lightblue')
        # valley
        self.canvas.create_rectangle( 0, START_Y-120, WIDTH, START_Y,
                                 fill='limegreen')
        self.platforms = []
        
        tree1 = self.make_tree(100, 355, 100, 7)
        self.start = self.canvas.create_rectangle(0,0,8,START_Y,fill ="coral")
        self.ground = self.canvas.create_rectangle(0,350,WIDTH,355,fill="coral")
        self.stop = self.canvas.create_rectangle(592,0,600,START_Y,fill ="coral")
        self.platforms.append(self.ground)
        self.make_hill( 50, 230, 250, 230, height=100, delta=3)
        self.make_hill(150, 300, 350, 300, height=100, delta=3)
        self.make_hill(250, 250, 450, 250, height=100, delta=3)
        self.make_hill(350, 300, 550, 300, height=100, delta=3)
        
        
        tree2 = self.make_tree(320,260,100,7)
        
        self.platforms.append(canvas.create_rectangle(0,START_Y-100,60,START_Y-94,fill = "coral"))
        self.platforms.append(canvas.create_rectangle(235,250,325,START_Y+5,fill="coral"))   # 3 blocks
        self.platforms.append(canvas.create_rectangle(320,250,415,290,fill="coral"))   
        self.platforms.append(canvas.create_rectangle(320,330,435,START_Y+5,fill = "coral"))
        #self.platforms.append(canvas.create_polygon(235,250,415,250,415,290,320,290,320,330,435,330,435,START_Y,235,START_Y))
        nest_egg1 = self.canvas.create_arc(295, 146, 325, 166, start=180, extent=180, outline="black", width=2, fill="brown")
        
        cloud1 = self.make_cloud(40, 90)
        cloud2 = self.make_cloud(150, 50)
        cloud3 = self.make_cloud(340, 130)
        self.clouds = [cloud1, cloud2, cloud3]
        self.platforms.append(canvas.create_rectangle(0,147,145,153,fill="coral"))
        self.moving_platform = self.canvas.create_rectangle(360,75,410,81,fill="coral")
        y = self.canvas.coords(self.moving_platform)
        

        # Schedule the next update
       
        self.platforms.append(self.moving_platform)
        self.platforms.append(canvas.create_rectangle(500,150,600,156,fill="coral"))
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
            curve = self.make_sky_curves(canvas, START_X+40, -80+i*20, radius, 5, 225, 270, 'green')
        radius = 95
        for i in range(num_curves):
            curve_y = START_Y + i * (curve_height + curve_spacing)
            start_angle += 10
            end_angle += 10
            radius += 10
            curve = self.make_sky_curves(canvas, 570+40, -70+i*20, radius, 5, 225,270, 'green')
        s1 = self.draw_spider_web(canvas,145//2,160//2)
        s2 = self.draw_spider_web(canvas,1065//2,430//2)
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
    def draw_spider_web(self, canvas, center_x, center_y):
        num_octagons = 5
        radius_outer = 140 // 2
        radius_inner = radius_outer / (num_octagons + 1)  # Radius of the inner octagons

        for octagon in range(num_octagons):
            radius = radius_inner * (octagon + 1)
            num_lines = 8

            for i in range(num_lines):
                angle = i * (360 / num_lines)
                start_x = center_x + int(radius * math.cos(math.radians(angle)))
                start_y = center_y + int(radius * math.sin(math.radians(angle)))

                angle2 = (i + 1) * (360 / num_lines)
                end_x = center_x + int(radius * math.cos(math.radians(angle2)))
                end_y = center_y + int(radius * math.sin(math.radians(angle2)))

                canvas.create_line(start_x, start_y, end_x, end_y, fill='white', width=3)
        
        angle_step = 360 / num_octagons
        angle_start = octagon * angle_step
        angle_end = angle_start + angle_step

        start_x = center_x + int(radius_outer * math.cos(math.radians(angle_start)))
        start_y = center_y + int(radius_outer * math.sin(math.radians(angle_start)))

        end_x = center_x + int(radius_outer * math.cos(math.radians(angle_end)))
        end_y = center_y + int(radius_outer * math.sin(math.radians(angle_end)))

        canvas.create_line(center_x, center_y, start_x, start_y, fill='white', width=3)
        canvas.create_line(center_x, center_y, end_x, end_y, fill='white', width=3)

        angle_step_additional = angle_step / 2
        for i in range(num_lines // 2):
                angle_additional = angle_start + (i * angle_step_additional)

                start_x_additional = center_x + int(radius_outer * math.cos(math.radians(angle_additional)))
                start_y_additional = center_y + int(radius_outer * math.sin(math.radians(angle_additional)))

                end_x_additional = center_x + int(radius_outer * math.cos(math.radians(angle_additional + 180)))
                end_y_additional = center_y + int(radius_outer * math.sin(math.radians(angle_additional + 180)))

                canvas.create_line(start_x_additional, start_y_additional, end_x_additional, end_y_additional, fill='white', width=3)

            # Draw 4 lines at 45 degrees with each other
        angle_step_45 = 45
        for i in range(4):
                angle_45 = angle_start + (i * angle_step_45)

                start_x_45 = center_x + int(radius_outer * math.cos(math.radians(angle_45)))
                start_y_45 = center_y + int(radius_outer * math.sin(math.radians(angle_45)))

                end_x_45 = center_x + int(radius_outer * math.cos(math.radians(angle_45+180)))
                end_y_45 = center_y + int(radius_outer * math.sin(math.radians(angle_45 + 180)))

                canvas.create_line(start_x_45, start_y_45, end_x_45, end_y_45, fill='white', width=3)


    def make_hill(self, x1, y1, x2, y2, height=100, delta=3):
        points = [x1,y1,(height/delta)+x1+60,y1-height,x2,y2]               #x1+height
        self.canvas.create_polygon(points,fill = "brown")

    def make_cloud(self, x, y):
        cloud_parts = []
        
        for i in range(3):
            cloud_parts.append(self.canvas.create_oval(x + i * 12, y, x + i * 12 + 30, y + 30,
                                                    outline='black', fill='white'))
        for i in range(-1,4):
            cloud_parts.append(self.canvas.create_oval(x + i * 12, y+15, x + i * 12 + 30, y + 45,
                                                    outline='black', fill='white'))
        for i in range(3):
            cloud_parts.append(self.canvas.create_oval(x + i * 12, y+30, x + i * 12 + 30, y + 60,
                                                    outline='black', fill='white'))
        
        return cloud_parts

    def make_tree(self, x, y, height, width):       #tree = self.make_tree(100, 350, 90, 7)
        tree_parts = []
        
        # Draw the tree trunk
        trunk = self.canvas.create_rectangle(x - width/2, y - height, x + width/2, y,
                                            fill='coral', outline='black')
        self.platforms.append(trunk)
        tree_parts.append(trunk)

        for i in range(5):
            tree_parts.append(self.canvas.create_polygon(x,y-height+12*i,x-3.5,y-height-3.5+12*i,x-29.5,y-height+30+12*i,x-26,y-height+33.5+12*i,fill = "green"))
            tree_parts.append(self.canvas.create_polygon(x,y-height+12*i,x+3.5,y-height-3.5+12*i,x+29.5,y-height+30+12*i,x+26,y-height+33.5+12*i,fill = "green"))
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
        purple_egg = self.canvas.create_oval(298, 150, 318, 160, fill='orchid')
        pink_egg = self.canvas.create_oval(325, 320, 345, 330, fill='pink')
        red_egg = self.canvas.create_oval(560,140,580,150,fill="red")
        blue_egg = self.canvas.create_oval(17,240,37,250,fill="cyan")
        yellow_egg = self.canvas.create_oval(100,253,120,263,fill="yellow")
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
        self.thread = self.canvas.create_line(x+10, 0, x+10, y+5,
                                          fill='ivory2', width=3)
        self.spider = self.make_spider(x, y)
        
        self.x, self.y = 0, 0.5
        self.direction = 1
        self.move_limit = 100000
        self.current_move = 0
    def make_spider(self, x, y):

        color1 = 'black'
        rectangle = canvas.create_oval(-50,-20,100,98,fill="",outline= "")
        head = canvas.create_oval(5, 5, 15, 13, fill=color1)
        torso = canvas.create_oval(0, 10, 20, 40, fill=color1)
        legs = [canvas.create_line(-5-i*5, 10*i+5, 5, 10*i+15,  \
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(15, 10*i+15, 25+i*5, 10*i+5, \
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(-10+i*5, 10*i+35, 5, 10*i+25, \
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(15, 10*i+25, 30-i*5, 10*i+35,\
                fill=color1, width=4) for i in range(2) ]     
        
        spider = [head, torso] + legs + [rectangle]
        for part in spider:
            self.canvas.move(part, x, y)
        return spider
    
    def update_for_2(self, eatable):
        spider_coords = self.canvas.coords(self.spider[0])
        spider_x = spider_coords[1]

        if spider_x <= 8 or spider_x >=150:
            self.direction *= -1
            self.current_move = 0

        if self.current_move < self.move_limit:
            self.canvas.move(self.spider[0], 0, self.direction)
            self.canvas.move(self.spider[1], 0, self.direction)
            for leg in self.spider[2:]:
                self.canvas.move(leg, 0, self.direction)
            self.current_move += 1
    def check_for_eat(self,avatar_coords,avatar_coords1):
        self.avatar_coords = avatar_coords
        self.avatar_coords1 = avatar_coords1
        
        trophy_coords= self.canvas.coords(self.spider[1])    #x1 >= X1 and x2 <= X2 and y1  >=Y1 and y2 <= Y2 
        trophy_coords1= self.canvas.coords(self.spider[2])
        if (avatar_coords[0] < trophy_coords[2] and avatar_coords[2] > trophy_coords[0] and avatar_coords[1] < trophy_coords[3] and avatar_coords[3] > trophy_coords[1]) or (avatar_coords[0] < trophy_coords1[2] and avatar_coords[2] > trophy_coords1[0] and avatar_coords[1] < trophy_coords1[3] and avatar_coords[3] > trophy_coords1[1]) or (avatar_coords1[0] < trophy_coords[2] and avatar_coords1[2] > trophy_coords[0] and avatar_coords1[1] < trophy_coords[3] and avatar_coords1[3] > trophy_coords[1]):
            return True
    def update_for_1(self, eatable):
        spider_coords = self.canvas.coords(self.spider[0])
        spider_x = spider_coords[1]
        X1,Y1,X2,Y2 = self.canvas.coords(self.spider[3])

        
        if spider_x <= 20 or spider_x >=235:
            self.direction *= -1
            self.current_move = 0

        if self.current_move < self.move_limit:
            self.canvas.move(self.spider[0], 0, self.direction)
            self.canvas.move(self.spider[1], 0, self.direction)
            for leg in self.spider[2:]:
                self.canvas.move(leg, 0, self.direction)
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
                                    #Land = Land() #Trophy = Trophy() in skyland class
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
    tk.title('Skyland')
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
    canvas.pack()
    game = Skyland(canvas)
    mainloop()
