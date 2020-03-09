import sys, pygame, math, myLib

def main():

    pygame.font.init();

    WHITE = (255,255,255);
    BLUE = (0,0,255);
    RED = (255,0,0);
    GREEN = (0,255,0);
    BLACK = (0,0,0);

    elec_color = (0,145,0);
    prot_color = (20,20,165);
    neut_color = (150,150,150);
    
    pygame.init()
    time = 0;
    fps = 50;

    #Screen
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size);
    
    running = True;

    ###############

    elec = [];
    prot = [];

    num_elec = 200;

    #Sprite Creation
    elec = [ myLib.Particle() for i in range(num_elec) ]
    
    for i in range(num_elec):
        elec[i].setPosition(300,400);
        elec[i].setVel(1,2);
        elec[i].resetAcc();
        elec[i].setDim(10);
        elec[i].setvo(10);
        #elec[i].setColor( ((i%10)*25,100,(i%10)*25 ) );
        elec[i].setColor(elec_color);
        elec[i].setM(1);
        elec[i].setBoundType(1);
        elec[i].kill();  
        elec[i].setBorder(0,width,height,0);
        elec[i].setScreen(screen);
        elec[i].birth();

    elec[0].setPosition(400,400);

    elec[0].birth();


    clock = pygame.time.Clock();

    text = "Electron";

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;

               

                
        

        #Update the screen and B-field
        screen.fill( BLACK );


        for i in range(num_elec):
            elec[i].brownian();
                                    

        #Update
        for i in range(num_elec):
            elec[i].update();

        
        time += 1;
        #if(time % 100 == 0):
            #elec[0].printPos();
            #print(k);
            #print(m);
            #print(x,y);

        pygame.display.flip();

        clock.tick(fps);
        



if __name__=="__main__":
    main();
    
