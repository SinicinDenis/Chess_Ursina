from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.radial_menu import RadialMenu, RadialMenuButton
import os
from threading import Thread





class Music_player(Audio):

    def __init__(self, player, editor):
        super().__init__()
        self.player = player
        self.editor = editor
        self.sp = []
        Thread(target=self.sp_in).start()
        self.ukazatel = 0
        self.volume_ = 1
        self.text_vol = []
        self.rm = RadialMenu(buttons=(RadialMenuButton(text='Play', on_click=self.play_),
                                      RadialMenuButton(text='Stop', on_click=self.stop_),
                                      RadialMenuButton(text='Next', on_click=self.next_),
                                      RadialMenuButton(text='Prev', on_click=self.prev_),
                                      RadialMenuButton(text='Vol-', on_click=self.vol_minus),
                                      RadialMenuButton(text='Vol+', on_click=self.vol_plus)), enabled=False)

    def play_(self):
        print('play')
        self.sp[self.ukazatel].volume = self.volume_
        self.sp[self.ukazatel].play()
        

    def stop_(self):
        self.sp[self.ukazatel].stop()
    
    def next_(self):
        self.sp[self.ukazatel].stop()
        self.ukazatel = (self.ukazatel + 1) % len(self.sp)
        self.sp[self.ukazatel].volume = self.volume_
        self.sp[self.ukazatel].play()

    def prev_(self):
        self.sp[self.ukazatel].stop()
        self.ukazatel = (self.ukazatel - 1) % len(self.sp)
        self.sp[self.ukazatel].volume = self.volume_
        self.sp[self.ukazatel].play()

    def vol_plus(self):
        self.volume_ += 0.1
        if self.volume_> 1:
            self.volume_ = 1
        self.sp[self.ukazatel].volume = self.volume_
        

    def vol_minus(self):
        self.volume_ -= 0.1
        if self.volume_ < 0.1:
            self.volume_ = 0.1
        self.sp[self.ukazatel].volume = self.volume_


    def sp_in(self):
        for root, dirs, files in os.walk('music_bg/'):
            for i in files:
                self.sp += [Audio(f'{root}{i}', autoplay=False)]
        print(self.sp)
    
    def input(self, key):
        if key == 'm':
            self.rm.enabled = True
            self.text_vol += [Text(name='t',text=f'{round(self.volume_, 1)}',position=self.rm.position)]
            self.player.disable()
            
            
            self.editor.enable()
            self.editor.position = self.player.position + Vec3(0,2,0)
            self.editor.look_at((0,0,0))
            camera.fov = 60

            mouse.visible = True
            #print(scene.entities)


    def update(self):
        
        if self.rm.enabled == False:
            if self.text_vol:
                for i in self.text_vol:
                    destroy(i)
                self.text_vol.clear()
                
                self.editor.disable()
                self.player.enable()
                camera.fov = 90
                

'''
app = Ursina()
player = FirstPersonController(gravity=0)
mp = Music_player()
app.run()

'''
