import sys, pygame, math, myLib

def checkKeys():

    k = pygame.key.get_pressed();
    # W A S D ; E P N L
    key_list = [[0,0,0,0],[0,0,0,0],[0,0,0,0]];
    if(k[pygame.K_w]):
       key_list[0][0] = 1;
    if(k[pygame.K_a]):
       key_list[0][1] = 1;
    if(k[pygame.K_s]):
       key_list[0][2] = 1;
    if(k[pygame.K_d]):
       key_list[0][3] = 1;

    if(k[pygame.K_UP]):
        key_list[1][0] = 1;
    if(k[pygame.K_DOWN]):
        key_list[1][1] = 1;
    if(k[pygame.K_RIGHT]):
        key_list[1][2] = 1;
    if(k[pygame.K_LEFT]):
        key_list[1][3] = 1;

    return key_list;

def main():

    pygame.font.init();

    ####################
    #For Sprite Creation

    atp_speed = 5;
    prot_speed = 3;
    rna_speed = .1;
    bact_speed = 1;
    virus_speed = 1;

    rna_turn = math.pi / 8;

    atp_rad = 5;
    rna_leng = 10;

    bact_rad = 100;
    virus_rad = 100;

    WHITE = (255,255,255);
    BLUE = (0,0,255);
    RED = (255,0,0);
    GREEN = (0,255,0);
    BLACK = (0,0,0);

    cell_color = (150,250,150);
    atp_color = (50,50,200);
    prot_color = (200,50,50);
    rna_color = GREEN;
    bact_color = (20,155,20);
    virus_color = (150,150,0);
    menu_color = (250,150,150);

    prot_evil_color = (0,0,0);
       
    
    
    pygame.init()
    time = 0;
    fps = 150;

    #Screen
    size = width, height = 1000, 800
    wid_menu = 200;
    screen = pygame.display.set_mode(size);
    
    running = True;

    ###############


    num_atp = 100;
    num_prot = 100;
    num_rna = 50;
    num_bact = 100;
    num_virus = 100;
    

    #Sprite Creation
    cell = myLib.Cell();
    
    atp = [ myLib.Atp() for i in range(num_atp) ]
    prot = [ myLib.Prot() for i in range(num_prot) ]
    rna = [ myLib.Rna() for i in range(num_rna) ]
    bact = [ myLib.Bact() for i in range(num_bact) ]
    virus = [ myLib.Virus() for i in range(num_virus) ]

    menu = myLib.Rect();
    
    for i in range(num_atp):
        atp[i].setPosition(500,500);
        atp[i].setDim(5);
        atp[i].setvo(atp_speed);
        atp[i].setColor(atp_color);
        atp[i].setBoundType(0);
        atp[i].kill();  
        atp[i].setBorder(0,width - wid_menu,height,0);
        atp[i].setScreen(screen);
        atp[i].birth();

    for i in range(num_prot):
        prot[i].setPosition(200,200);
        prot[i].setDim(5);
        prot[i].setvo(prot_speed);
        prot[i].setColor(prot_color);
        prot[i].setBoundType(0);
        prot[i].kill();  
        prot[i].setBorder(0,width - wid_menu,height,0);
        prot[i].setScreen(screen);
        prot[i].birth();

    for i in range(num_rna):
        rna[i].setInitPos(100,500);
        rna[i].setLeng(rna_leng);
        rna[i].setAng(0);
        rna[i].calcPos();
        rna[i].setvo(rna_speed);
        rna[i].setColor(rna_color);
        rna[i].setTurn(rna_turn);
        rna[i].setBoundType(0);
        rna[i].kill();  
        rna[i].setBorder(0,width - wid_menu,height,0);
        rna[i].setScreen(screen);
        rna[i].birth();

    menu.initialize(width - wid_menu / 2, height / 2,wid_menu,height,False,menu_color,screen,True);

    clock = pygame.time.Clock();

    text = "Text";

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;


        #Input Check
        k = checkKeys();

        

        #Main code

        
            
                    
        #Update the screen and B-field
        screen.fill( BLACK );

        cell.update();

        #Update
        for i in range(num_atp):
            atp[i].update();
        for i in range(num_prot):
            prot[i].update();
        for i in range(num_rna):
            rna[i].update();

        #Show the Menu
        #menu.draw();

        
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
    
