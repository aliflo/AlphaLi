from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
#imports all neccesary dependencies
class PongPaddle(Widget):
    score=NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0) #sets up variables for the velocities as numeric properties
    velocity = ReferenceListProperty(velocity_x, velocity_y) #allows ball.velocity to work as a shorthand

    def move(self):#When called, moves the ball one step, called in equal intervals to animate the ball 
        self.pos = Vector(*self.velocity) + self.pos 

class PongGame(Widget): #Creates the base of the program
    ball = ObjectProperty(None) #Allows the ball to reference PongBall in the kv file
    player1=ObjectProperty(None)
    player2=ObjectProperty(None)
    
    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    def update(self, dt):
        self.ball.move() #calls move
        # bounce off top and bottom
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1 #sets y velocity to opposite
        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1 #sets x velocity to opposite
        #scores a point if it goes off a side
        if self.ball.x<self.x:
            self.player2.score+=1
            self.serve_ball(vel=(4,0))
        if self.ball.x>self.width:
            self.player1.score+=1
            self.serve_ball(vel=(-4,0))
    def on_touch_move(self,touch):
        if touch.x < self.width/3:
            self.player1.center_y=touch.y
        if touch.x > self.width-self.width/3:
            self.player2.center_y=touch.y #Decides which side the touch was on and moves the paddle to that point

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball() #serves the ball as an instance of game
        Clock.schedule_interval(game.update, 1.0 / 60.0) #updates the window 60 times per second
        return game #returns the window

if __name__ == '__main__':
    PongApp().run() #runs the main app