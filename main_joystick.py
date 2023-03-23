import my_setup_class as mySetup
import time
import keyboard


def main():

    ## INITIALISE SETUP & TOOLS
    mySetup.usedTools = ["PAV", "MSA_600"]
    mySetup.initiate()
    time.sleep(1)
    mySetup.myPav.move_chuck_separation()


    # define the key event handlers
    def on_left(event):
        mySetup.myPav.move_chuck_velocity( plusMinZeroX = '+', plusMinZeroY = '0')
        print('x: +' )

    def on_right(event):
        mySetup.myPav.move_chuck_velocity(plusMinZeroX = '-', plusMinZeroY = '0')
        print('x: -')
    
    def on_home(event):
        print('moving to home' )
        mySetup.myPav.move_chuck_relative_to_home(x=0, y=0)

    def on_up(event):
        mySetup.myPav.move_chuck_velocity( plusMinZeroX = '0', plusMinZeroY = '-')
        print('y: -')

    def on_down(event):
        mySetup.myPav.move_chuck_velocity( plusMinZeroX = '0', plusMinZeroY = '+')
        print('y: +')

    def on_m(event):
        mySetup.myPav.move_chuck_relative_to_home(100, 100)
        
    def on_release(event):
        print('stop movement')
        mySetup.myPav.stop_chuck_movement()


    # add the key event listeners
    keyboard.on_press_key('left', on_left)
    keyboard.on_press_key('h', on_home)
    keyboard.on_press_key('right', on_right)
    keyboard.on_press_key('up', on_up)
    keyboard.on_press_key('down', on_down)
    keyboard.on_press_key('m', on_m)
    keyboard.on_release(on_release)
    # keyboard.wait(0.1)
    while True:
        time.sleep(0.1)


if __name__=='__main__':
    main()
    #exit()