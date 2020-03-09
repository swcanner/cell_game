import sys, pygame, math, myLib

def checkKeys():

    k = pygame.key.get_pressed();

    s = 0;
    e = 0;

    esc = 0;

    knmi = [0,0,0,0,0,0];
    

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
        knmi[0] = 1;
    if(k[pygame.K_DOWN]):
        key_list[1][1] = 1;
        knmi[1] = 1;
    if(k[pygame.K_RIGHT]):
        key_list[1][2] = 1;
        knmi[3] = 1;
    if(k[pygame.K_LEFT]):
        key_list[1][3] = 1;
        knmi[2] = 1;

    if(k[pygame.K_b]):
        knmi[5] = 1;
    if(k[pygame.K_a]):
        knmi[4] = 1;

    if(k[pygame.K_e]):
        key_list[1][3] = 1;

    if(k[pygame.K_SPACE]):
        s = 1;
    if(k[pygame.K_KP_ENTER] or k[pygame.K_RETURN]):
        e = 1;

    if(k[pygame.K_ESCAPE]):
        esc = 1;

    return key_list,s,e,esc,knmi;

def parser(arr,true_arr,pos):
    #Determines if the konami code was inputted
    for i in range(len(true_arr)):
        if (arr[pos] != true_arr[i]):
            return False;
        pos += 1;
        pos %= len(arr);
    return True;

def getMaxMol(r):
    #Outputs the maximum NA and ATP possible for given radius

    na = ((r - 100) /  10) * 2000;
    atp = ((r - 100) /  10) * 4;
    res = 2 * na / 3;

    return na, atp,res;

def moveAtpCons(mxr,r,o,fps):

    #Speed
    m = (mxr + 25 - r) * 5 / (.75 + o / 2);
    m /= fps;

    return m;

def isInBound(c,w,h):
    b = [0,0]

    x = c.getX();
    y = c.getY();

    if (x > w * 2 / 3):
        b[0] = 1;
    if (x < w /3 ):
        b[0] = -1;
    if (y > h * 2 / 3):
        b[1] = 1;
    if (y < h /3 ):
        b[1] = -1;

    return b;



#PER SECOND
def calcAtpRate(p,ind,atpPerProtRate,mitoRate,fps):
    n = 0;
    for i in p:
        if (i.isAlive()):
            if (i.getType() == ind):
                n += 1;
    r = atpPerProtRate * n + mitoRate;
    return r;

def countOnOff(c,w,h):
    n = 0;
    j = 0;
    for i in c:
        if i.isAlive():
            if i.getX() < 0:
                n += 1;
            elif i.getX() > w:
                n += 1;
            elif i.getY() < 0:
                n += 1;
            elif i.getY() > h:
                n += 1;
            else:
                j += 1;
    return j,n;

def isOnScreen(c,w,h):
    if c.isAlive():
        if c.getX() + c.getRadius() > 0:
            if c.getX() - c.getRadius() < w:
                if c.getY() + c.getRadius() > 0:
                    if c.getY() - c.getRadius() < h:
                        return True;

    return False;

def main():

    pygame.font.init();

    pygame.mixer.init();

    #Initial Conditions
    fps = 30;
    cell_na = 8000;
    cell_residue = cell_na / 2;
    cell_prot = 0;
    cell_atp = 10;
    atpPerProtRate = .5;
    mitoRate = 2.5;
    rna_per = 1000;
    rna_rate = fps * 1.75;
    res_per = 300;
    prot_rate = fps * 2.15;
    atpreq_list = [[1,1,3],
                   [1,1,1],
                   [2,2,2]];
    prot_refPeriod = fps * .5;
    coefRest = .5;
    nMakeAtp = 5;
    move_atp_rate = fps * .75;

    minr = 130;
    maxr = 250;
    vesc_r = 30;
    resPerVesc = 50;
    vir_nRna = 3

    evil_time = 30 * fps;
    evil_prob = 0.05/fps;

    spawnRate_vesc = fps * 0.45;
    spawnRate_vir = fps * 1.15;
    spawnRate_bact = fps * 2.15;
    old_rate = spawnRate_bact;
    lastTime_vesc = 0;
    lastTime_vir = 5 * fps;
    lastTime_bact = 25 * fps;

    medium_time = 60 * fps;
    hard_time = 120 * fps;

    explode_maxR = 250;
    explode_dr = 750 / fps;

    evil_str = 8;

    bact_dSurr = math.pi * 2 / (fps * 3);
    regen = 1;

    ####################
    #For Sprite Creation

    atp_speed = 7;
    prot_speed = 4;
    rna_speed = 5;
    nuc_speed = .25;
    mito_speed = .5;
    endo_speed = .33;
    vesc_speed = 1.5;

    bact_speed = 1;
    virus_speed = 1;

    atp_rad = 3;
    prot_rad = 10;
    rna_leng = 10;
    rna_turn = math.pi / 12;

    cell_rad = 150;
    bact_rad = 100;
    virus_rad = 75;

    nuc_rad = 50;
    endo_rad = 35;
    mito_rad = 35;

    WHITE = (255,255,255);
    BLUE = (0,0,255);
    RED = (255,0,0);
    GREEN = (0,255,0);
    BLACK = (0,0,0);

    cell_color = (100,200,100);
    atp_color = (50,50,200);
    prot_color = (200,50,50);
    rna_color = (0,0,0);
    bact_color = (200,155,20);
    virus_color = (150,150,0);
    menu_color = (250,150,150);
    outer_color = (100,200,100);
    nuc_color = (200,175,175);
    vesc_color = (150,200,150);
    explode_color = (100,100,250);


    prot_evil_color = (0,0,0);

    pygame.init()
    time = 0;

    #Screen
    size = width, height = 1000, 800
    wid_menu = 200;
    screen = pygame.display.set_mode(size);

    running = True;

    ###############


    num_atp = 200;
    num_prot = 100;
    num_rna = 125;
    num_bact = 35;
    num_vir = 35;
    num_vesc = 50;

    if (3*num_vir < num_rna):
        num_rna = 3*num_vir  + 50;

    num_dna = 3;
    num_protDna = 3;


    #Sprite Creation
    cell = myLib.Cell();
    cell.setPosition(400,400);
    cell.makeCell();
    cell.setMinR(minr);
    cell.setMaxR(maxr);
    cell.setRegen(regen);
    cell.setHP(10000);
    cell.setNa(cell_na);
    cell.setnRes(cell_residue);
    cell.setResCost(res_per);
    cell.setDim(cell_rad);
    cell.setCoef(coefRest);
    cell.setColor(cell_color);
    cell.resetBactKill();
    cell.setFps(fps);
    cell.setnAtp(1);
    cell.setBoundType(0);
    cell.resetVirKill();
    cell.setBorder(0,width - wid_menu,height,0);
    cell.setScreen(screen);
    cell.birth();

    atp = [ myLib.Atp() for i in range(num_atp) ]
    prot = [ myLib.Prot() for i in range(num_prot) ]
    rna = [ myLib.Rna() for i in range(num_rna) ]
    bact = [ myLib.Bact() for i in range(num_bact) ]
    vir = [ myLib.Virus() for i in range(num_vir) ]
    vesc = [ myLib.Cell() for i in range(num_vesc) ]
    explode = [myLib.Explosion() for i in range(num_prot)]

    atp_pos = 0;
    prot_pos = 0;
    rna_pos = 0;
    bact_pos = 0;
    vir_pos = 0;

    menu = myLib.Rect();



    for i in range(num_atp):
        atp[i].setPosition(500,500);
        atp[i].setDim(atp_rad);
        atp[i].setvo(atp_speed);
        atp[i].setColor(atp_color);
        atp[i].setBoundType(0);
        atp[i].kill();
        atp[i].setCell(cell);
        atp[i].setBorder(0,width - wid_menu,height,0);
        atp[i].setScreen(screen);

    for i in range(num_prot):
        explode[i].setPosition(401,401);
        explode[i].setCell(cell);
        explode[i].setMaxR(explode_maxR);
        explode[i].setDr(explode_dr);
        explode[i].setColor(explode_color);
        explode[i].setScreen(screen);
        explode[i].setBorder(0,width - wid_menu,height,0);
        explode[i].kill();

    for i in range(num_prot):
        prot[i].setPosition(401,401);
        prot[i].setIntra();
        prot[i].setDim(prot_rad);
        prot[i].setCell(cell);
        prot[i].setvo(prot_speed);
        prot[i].setPointTemp( [ [0,0],[0,1],[1,1],[1,0] ] )
        prot[i].setAtpReqList(atpreq_list);
        prot[i].setNumAtp(4);
        prot[i].setNMakeAtp(nMakeAtp);
        prot[i].setRefPer(prot_refPeriod);
        prot[i].setStr(evil_str);
        prot[i].setEvilTime(evil_time);
        prot[i].setEvilProb(evil_prob);
        prot[i].setColor(prot_color);
        prot[i].setBoundType(-2);
        prot[i].setExplode(explode[i]);
        prot[i].setLineWidth(0);
        prot[i].kill();
        #prot[i].birth();
        prot[i].setBorder(0,width - wid_menu,height,0);
        prot[i].setScreen(screen);

    for i in range(num_rna):
        rna[i].setInitPos(-500,-500);
        rna[i].setLeng(rna_leng);
        rna[i].setCell(cell);
        rna[i].setvo(rna_speed);
        rna[i].setColor(rna_color);
        rna[i].setTurn(rna_turn);
        rna[i].setBoundType(-2);
        rna[i].kill();
        rna[i].setBorder(0,width - wid_menu,height,0);
        rna[i].setScreen(screen);

    for i in range(num_vir):
        vir[i].setPosition(400,400);
        vir[i].setvo(virus_speed);
        vir[i].setCell(cell);
        vir[i].setLineWidth(0);
        vir[i].setDim(virus_rad);
        vir[i].setNRna(vir_nRna);
        vir[i].setColor(virus_color);
        vir[i].setBoundType(-2);
        vir[i].setBorder(0,width - wid_menu,height,0);
        vir[i].setScreen(screen);
        vir[i].kill();

    for i in range(num_vir):
        bact[i].setPosition(400,400);
        bact[i].setvo(bact_speed);
        bact[i].setCell(cell);
        bact[i].setDim(bact_rad);
        bact[i].setColor(bact_color);
        bact[i].setBoundType(-2);
        bact[i].setBorder(0,width - wid_menu,height,0);
        bact[i].setScreen(screen);
        bact[i].setDSurr(bact_dSurr);
        bact[i].kill();

    for i in range(num_vesc):
        vesc[i].setPosition(400,400);
        vesc[i].makeVesc();
        vesc[i].setvo(vesc_speed);
        vesc[i].setMinR(vesc_r);
        vesc[i].setMaxR(vesc_r);
        vesc[i].setRegen(regen);
        vesc[i].setCell(cell);
        vesc[i].setHP(10);
        vesc[i].setNa(0);
        vesc[i].setnRes(0);
        vesc[i].setResCost(0);
        vesc[i].setResPerVesc(resPerVesc);
        vesc[i].setDim(vesc_r);
        vesc[i].setCoef(0);
        vesc[i].setColor(vesc_color);
        vesc[i].setFps(fps);
        vesc[i].setBoundType(-2);
        vesc[i].setBorder(0,width - wid_menu,height,0);
        vesc[i].setScreen(screen);
        vesc[i].kill();

    cell.setAtp(atp);
    cell.setProt(prot);
    cell.setRna(rna);

    cell.setVesc(vesc);
    cell.setVir(vir);
    cell.setBact(bact);


    #Nucleus
    dna = myLib.MySprite();
    dna.setScreen(screen);
    dna.setImage("./org/dna_00.png");
    dna.scale((75,47));
    dna.setDim(75,45,False);
    dna.setPosition(width - wid_menu + 100,100);
    dna.setBoundType(-2);
    dna.birth();

    ppos = [0,0];
    dpos = [0,0];


    nuc = myLib.Nucleus();
    nuc.setPosition(400,400);
    nuc.setDim(nuc_rad);
    nuc.setvo(nuc_speed);
    nuc.setCell(cell);
    nuc.setColor(nuc_color);
    nuc.setNaCost(rna_per);
    nuc.setProdRate(rna_rate);
    nuc.setBoundType(0);
    nuc.setBorder(0,width - wid_menu,height,0);
    nuc.setScreen(screen);
    nuc.setDna(dna);
    nuc.birth();

    cell.setNuc(nuc);

    endo = myLib.Endo();
    endo.setPosition(300,400);
    endo.setImage("./org/endo.png");
    endo.setDim(endo_rad);
    endo.setvo(endo_speed);
    endo.setResCost(res_per);
    endo.scale((2*endo_rad,2*endo_rad));
    endo.setCell(cell);
    endo.setBoundType(0);
    endo.setBorder(0,width - wid_menu,height,0);
    endo.setScreen(screen);
    endo.birth();

    cell.setEndo(endo);

    mito = myLib.Mito();
    mito.setPosition(400,350);
    mito.setImage("./org/mito.png");
    mito.setDim(mito_rad);
    mito.setvo(mito_speed);
    mito.scale((2*mito_rad,2*mito_rad));
    atpRate = calcAtpRate(prot,[1,2],atpPerProtRate,mitoRate,fps);
    mito.setProdRate(fps / atpRate);
    mito.setCell(cell);
    mito.setBoundType(0);
    mito.setBorder(0,width - wid_menu,height,0);
    mito.setScreen(screen);
    mito.birth();

    cell.setMito(mito);


    #Menu options
    menu.initialize(width - wid_menu / 2, height / 2,wid_menu,height,False,menu_color,screen,True);

    prot_list = [["./pdb/memb0.png","./pdb/memb1.png","./pdb/memb2.png"],
                 ["./pdb/intra0.png","./pdb/intra1.png","./pdb/intra2.png"],
                 ["./pdb/mab0.png","./pdb/mab1.png","./pdb/mab2.png"]];

    dna_to_rna_time =  [[3,3,5],
                        [2,2,5],
                        [4,4,4]]

    na_cost = [[rna_per,rna_per,rna_per],
               [rna_per,rna_per,rna_per],
               [rna_per,rna_per,rna_per]]
    resPerProt = 300;
    rna_to_prot_time =  [[3,3,3],
                         [3,3,3],
                         [3,3,3]]
    menu_list = [["./pdb/menu00.png","./pdb/menu01.png","./pdb/menu02.png"],
                 ["./pdb/menu10.png","./pdb/menu11.png","./pdb/menu12.png"],
                 ["./pdb/menu20.png","./pdb/menu21.png","./pdb/menu22.png"]];
    dna_list = [["./org/dna_00.png","./org/dna_01.png","./org/dna_02.png"],
                ["./org/dna_10.png","./org/dna_11.png","./org/dna_12.png"],
                ["./org/dna_20.png","./org/dna_21.png","./org/dna_22.png"]]

    prot_type = [["Flippase","Floppase","Signalling"],
                 ["Protein Enzyme","RNA Enzyme","Lipid Enzyme"],
                 ["mAb A","mAb B","mAb C"]]

    prot_im = myLib.MySprite();
    prot_im.setScreen(screen);
    prot_im.setImage(prot_list[0][0]);
    prot_im.scale((190,190));
    prot_im.setDim(190,190,False);
    prot_im.setPosition(width - wid_menu + 100,100);
    prot_im.setBoundType(-2);
    prot_im.birth();

    back_im = myLib.MySprite();
    back_im.setScreen(screen);
    back_im.setImage("./pdb/bg.png");
    back_im.scale( (3*(width-wid_menu),3*height) );
    back_im.setDim(3*(width-wid_menu),3*height,False);
    back_im.setPosition((width-wid_menu / 2),height/2);
    back_im.setBoundType(-2);
    back_im.birth();

    menu_im = myLib.MySprite();
    menu_im.setScreen(screen);
    menu_im.setImage(menu_list[0][0]);
    menu_im.scale((wid_menu,height));
    menu_im.setDim(wid_menu,height,False);
    menu_im.setPosition(width - wid_menu / 2,height / 2);
    menu_im.setBoundType(-2);
    menu_im.birth();

    enter_im = myLib.MySprite();
    enter_im.setScreen(screen);
    enter_im.setImage("./pdb/enter.png");
    enter_im.scale((wid_menu / 5,wid_menu / 5));
    enter_im.setDim(wid_menu / 5,wid_menu / 5,False);
    enter_im.setPosition(width - wid_menu + 30,height / 2  + 35);
    enter_im.setBoundType(-2);
    enter_im.birth();

    #Produce Text
    currProd = [-1,-1];
    prevProdTime = 0;

    pygame.font.init();
    font = pygame.font.SysFont('Courier New', 20)

    atpreq_text = "ATP Required: " + str(atpreq_list[0][0]);
    atpobj_text = font.render(atpreq_text, True, (250,250,250))
    begin_stop_text = "Begin"
    prod_text = "Production"
    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
    prodobj_text = font.render(prod_text, True, (250,250,250))

    maxNa, maxAtp, maxRes = getMaxMol(cell.getRadius());

    atpRate = calcAtpRate(prot,[1,2],atpPerProtRate,mitoRate,fps);
    mito.setProdRate(atpRate);

    currNa_text = "Nucleic Acids: " + str(cell_na) +" / " + str(maxNa);
    freeNa_text = "Free NAs: " + str( (cell_na - resPerProt * num_prot));
    currRes_text = "Residues: " + str(cell.getnRes()) + " / " + str(maxRes);
    currAtp_text = "ATP: " + str(cell.getnAtp()) + " / " + str(maxAtp);
    atpRate_text = "ATP Rate: " + str(atpRate) + "/s"
    currOuter_text = "Outer Protection: " + str( (cell.getOuter() * 10) ) + "%";
    currProd_text = "Current Production: ";
    prod_text = "";
    if(currProd == [-1,-1]):
        prod_text = "None";
    else:
        prod_text = prot_type[currProd[0]][currProd[1]];
    dnaHP_text = "DNA Health: " + str(cell.getHP());

    currNaObj = font.render(currNa_text,True, (250,250,250));
    freeNaObj = font.render(freeNa_text,True, (250,250,250));
    currAtpObj = font.render(currAtp_text,True, (250,250,250));
    atpRateObj = font.render(atpRate_text,True, (250,250,250));
    currOuterObj = font.render(currOuter_text,True, (250,250,250));
    currProdObj = font.render(currProd_text,True, (250,250,250));
    prodObj = font.render(prod_text,True, (250,250,250));
    dnaHPObj = font.render(dnaHP_text,True, (250,250,250));


    pause_screen = myLib.MySprite();
    pause_screen.setScreen(screen);
    pause_screen.kill();
    pause_screen.setPosition(0,0);
    pause_screen.setImage("./menu/pause.png");
    pause_screen.setBoundType(-2);
    pause_screen.scale((width,height));

    death_screen = myLib.MySprite();
    death_screen.setScreen(screen);
    death_screen.kill();
    death_screen.setPosition(0,0);
    death_screen.setImage("./menu/gameOver.png");
    death_screen.setBoundType(-2);
    death_screen.scale((width,height));

    intro_images = ["./menu/0.png","./menu/1.png","./menu/2.png",
                    "./menu/3.png","./menu/4.png","./menu/5.png"]

    intro_screen = myLib.MySprite();
    intro_screen.setScreen(screen);
    intro_screen.kill();
    intro_screen.setPosition(0,0);
    intro_screen.setImage(intro_images[0]);
    intro_screen.setBoundType(-2);
    intro_screen.scale((width,height));
    intro_screen.birth();

    score_font = pygame.font.SysFont('Courier New', 15)
    hScore = 1000;

    try:
        f = open("./.score.txt", "r")
        j = f.readline();
        hScore = int(j);
        f.close();
    except IOError:
        hScore = 1000;

    cScore = 0;
    cScore_text = " Score: " + str(cScore);
    hScore_text = "HScore: " + str(hScore);

    cScoreObj = score_font.render(cScore_text,True, (250,250,250));
    hScoreObj = score_font.render(hScore_text,True, (250,250,250));

    #Sounds

    boom = pygame.mixer.Sound("./sounds/boom.ogg");
    ee = pygame.mixer.Sound("./sounds/ee.ogg");
    kah = pygame.mixer.Sound("./sounds/kah.ogg");
    oo = pygame.mixer.Sound("./sounds/oo.ogg");
    over = pygame.mixer.Sound("./sounds/over.ogg");
    bip = pygame.mixer.Sound("./sounds/bip.ogg");
    ttt = pygame.mixer.Sound("./sounds/ttt.ogg");
    
    #Just some stuffs
    clock = pygame.time.Clock();

    ko, so, eo, esco, knmio = checkKeys();

    epo = endo.getLenQ();

    moveTime = 0;
    gTime = 0;

    pause = False;
    isIntro = True;
    ipos = 0;

    ritten = False;

    crackerBarrell = 0;

    konami_input = [0,0,0,0,0,0,0,0,0,0];
    konami_pos = 0;
    konami_code = [0,0,1,1,2,3,2,3,5,4];
    dknmi = [0,0,0,0,0,0];
    triggered = False;

    
    konami_screen = myLib.MySprite();
    konami_screen.setScreen(screen);
    konami_screen.kill();
    konami_screen.setPosition(0,0);
    konami_screen.setImage("./menu/meem.jpg");
    konami_screen.setBoundType(-2);
    konami_screen.scale((width,height));
    konami_screen.kill();
        

    #Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;

         #Input Check
        k, s, e, esc, knmi = checkKeys();

        ds = s - so;
        de = e - eo;
        desc = esc - esco;

        for i in range(len(dknmi)):
            dknmi[i] = knmi[i] - knmio[i];
            
        #Inputs
        try:
            nInp = dknmi.index(1);
        except ValueError:
            nInp = -1;
        
        if nInp > -1:
            konami_input[konami_pos] = nInp;
            konami_pos += 1;
            konami_pos %= len(konami_input);
        triggered = parser(konami_input,konami_code,konami_pos);
        

        if (triggered):
            konami_screen.birth();
        else:
            konami_screen.kill();


        dk = [0,0,0,0];
        for i in range(4):
            dk[i] = k[1][i] - ko[1][i];

        if (desc == 1):
           pause = not pause;

        if (isIntro):
            if (ds > 0):
                ipos += 1;
                if (ipos < len(intro_images)):
                    intro_screen.setImage(intro_images[ipos]);
                    intro_screen.scale((width,height));
                else:
                    isIntro = False;
                    intro_screen.kill();
            intro_screen.update();

        elif (cell.isAlive() and not pause):
            gTime += 1;

            #UDRL
            if(dk[0] == 1):
                dpos[1] -= 1;
            if(dk[1] == 1):
                dpos[1] += 1;
            if(dk[2] == 1):
                dpos[0] += 1;
            if(dk[3] == 1):
                dpos[0] -= 1;

            dpos[0] %= num_dna;
            dpos[1] %= num_protDna;


            maxNa, maxAtp, maxRes = getMaxMol(cell.getRadius());

            if (maxRes < cell.getnRes()):
                cell.setnRes(maxRes);
            
            atpRate = calcAtpRate(prot,[1,2],atpPerProtRate,mitoRate,fps);

            if(ppos[0] != dpos[0] or ppos[1] != dpos[1]):
                dna.setImage(dna_list[dpos[0]][dpos[1]])
                dna.scale((75,47));
                prot_im.setImage(prot_list[dpos[0]][dpos[1]])
                prot_im.scale((190,190));
                menu_im.setImage(menu_list[dpos[0]][dpos[1]])
                menu_im.scale((wid_menu,height));
                atpreq_text = "ATP Required: " + str(atpreq_list[dpos[0]][dpos[1]]);
                atpobj_text = font.render(atpreq_text, True, (250,250,250))
                if(dpos == currProd):
                    begin_stop_text = "Stop"
                    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                else:
                    begin_stop_text = "Begin"
                    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                prod_text = "Production"
                prodobj_text = font.render(prod_text, True, (250,250,250))


            ppos[0] = dpos[0];
            ppos[1] = dpos[1];


            #Explosions

            #Movement

            #WASD positions

            mvNow = False;
            for i in k[0][:]:
                if i > 0:
                    mvNow = True;

            m = moveAtpCons(cell.getMaxR(),cell.getRadius(),cell.getOuter(),fps);

            if mvNow:
                if cell.isFreeAtp():
                    b = isInBound(cell,width-wid_menu,height);
                    #Get the positions to move

                    #W
                    if k[0][0] == 1:
                        moveTime += 1;
                        if b[1] == -1:
                            #Move the bg
                            back_im.dpos(0,m);
                            #Move virus, bact, and more
                            for i in explode:
                                i.dpos(0,m);
                            for i in vir:
                                i.dpos(0,m);
                            for i in bact:
                                i.dpos(0,m);
                            for i in vesc:
                                i.dpos(0,m);
                            for i in rna:
                                if i.getVir() != []:
                                    if i.getVir().getLatch() == False:
                                        i.dpos(0,m)

                        else:
                            #Move the cell and organelles
                            cell.dpos(0,-m);
                            nuc.dpos(0,-m);
                            endo.dpos(0,-m);
                            mito.dpos(0,-m);
                            #Move virus, bact, and more
                            for i in atp:
                                i.dpos(0,-m);
                            for i in prot:
                                i.dpos(0,-m);
                            for i in rna:
                                if i.getVir() == []:
                                    i.dpos(0,-m);
                                elif i.getVir().getLatch():
                                    i.dpos(0,-m);

                    #A
                    if k[0][1] == 1:
                        moveTime += 1;
                        if b[0] == -1:
                            #Move the bg
                            back_im.dpos(m,0);
                            #Move virus, bact, and more
                            for i in explode:
                                i.dpos(m,0);
                            for i in vir:
                                i.dpos(m,0);
                            for i in bact:
                                i.dpos(m,0);
                            for i in vesc:
                                i.dpos(m,0);
                            for i in rna:
                                if i.getVir() != []:
                                    if i.getVir().getLatch() == False:
                                        i.dpos(m,0)
                        else:
                            #Move the cell and organelles
                            cell.dpos(-m,0);
                            nuc.dpos(-m,0);
                            endo.dpos(-m,0);
                            mito.dpos(-m,0);
                            #Move virus, bact, and more
                            for i in atp:
                                i.dpos(-m,0);
                            for i in prot:
                                i.dpos(-m,0);
                            for i in rna:
                                if i.getVir() == []:
                                    i.dpos(-m,0);
                                elif i.getVir().getLatch():
                                    i.dpos(-m,0);

                    #S
                    if k[0][2] == 1:
                        moveTime += 1;
                        if b[1] == 1:
                            #Move the bg
                            back_im.dpos(0,-m);
                            #Move virus, bact, and more
                            for i in explode:
                                i.dpos(0,-m);
                            for i in vir:
                                i.dpos(0,-m);
                            for i in bact:
                                i.dpos(0,-m);
                            for i in vesc:
                                i.dpos(0,-m);
                            for i in rna:
                                if i.getVir() != []:
                                    if i.getVir().getLatch() == False:
                                        i.dpos(0,-m)

                        else:
                            #Move the cell and organelles
                            cell.dpos(0,m);
                            nuc.dpos(0,m);
                            endo.dpos(0,m);
                            mito.dpos(0,m);
                            #Move virus, bact, and more
                            for i in atp:
                                i.dpos(0,m);
                            for i in prot:
                                i.dpos(0,m);
                            for i in rna:
                                if i.getVir() == []:
                                    i.dpos(0,m);
                                elif i.getVir().getLatch():
                                    i.dpos(0,m);


                    #D
                    if k[0][3] == 1:
                        moveTime += 1;
                        if b[0] == 1:
                            #Move the bg
                            back_im.dpos(-m,0);
                            #Move virus, bact, and more
                            for i in explode:
                                i.dpos(-m,0);
                            for i in vir:
                                i.dpos(-m,0);
                            for i in bact:
                                i.dpos(-m,0);
                            for i in vesc:
                                i.dpos(-m,0);
                            for i in rna:
                                if i.getVir() != []:
                                    if i.getVir().getLatch() == False:
                                        i.dpos(-m,0)
                        else:
                            #Move the cell and organelles
                            cell.dpos(m,0);
                            nuc.dpos(m,0);
                            endo.dpos(m,0);
                            mito.dpos(m,0);

                            #Move virus, bact, and more
                            for i in atp:
                                i.dpos(m,0);
                            for i in prot:
                                i.dpos(m,0);
                            for i in rna:
                                if i.getVir() == []:
                                    i.dpos(m,0);
                                elif i.getVir().getLatch():
                                    i.dpos(m,0);


            if (moveTime >= move_atp_rate):
                moveTime = 0;
                cell.killFreeAtp();









            ##############################################
            #Main code
            cell.setMaxAtp(maxAtp);
            cell.setMaxNa(maxNa);
            mito.setProdRate(fps / atpRate);
            cell_na = cell.getNa();


            ########################
            #Production business

            #rna
            if(de == 1):
                #check if we can produce
                if(currProd != dpos and cell.getFreeNa() >= nuc.getNaCost() ):
                    #We can produce
                    prevPosTime = time;
                    currProd[0] = dpos[0];
                    currProd[1] = dpos[1];
                    nuc.setCurrProd(currProd);
                    nuc.setProdTime(time);
                    begin_stop_text = "Stop"
                    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                elif(dpos == currProd):
                    currProd = [-1,-1]
                    nuc.setCurrProd(currProd);
                    nuc.setProdTime(time);
                    begin_stop_text = "Start"
                    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                elif(cell.getFreeNa() < nuc.getNaCost() ):
                    begin_stop_text = "Resources"
                    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                    prod_text = "Required"
                    prodobj_text = font.render(prod_text, True, (250,250,250))


            #Check if we can produce
            t = nuc.produceRna(time,bip);
            if (nuc.isAlive()):
                if(t):
                    currProd = [-1,-1];
                    nuc.setCurrProd(currProd);
                    nuc.setProdTime(time);
                    begin_stop_text = "Begin"
                    beginobj_text = font.render(begin_stop_text, True, (250,250,250))
            else:
                currProd = [-1,-1];
                nuc.setCurrProd(currProd);
                nuc.setProdTime(time);
                begin_stop_text = "Cannot"
                beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                prod_text = "Produce"
                prodobj_text = font.render(prod_text, True, (250,250,250))

            #Prot

            #########################

            #Explosions!?!?!??!?!?!

            #Only if space happens
            if (ds == 1):
                #Run through all prots
                for i in prot:
                    if i.isAlive():
                        if i.getType() == [0,2]:
                            if i.isAtpFull():
                                if i.canFire(time):
                                    i.explode(time);
                                    boom.play();


            ##############################################


            #Update the screen and B-field
            screen.fill( BLACK );

            iw = width - wid_menu;

            if (back_im.getX() < -iw/2) :
                back_im.setX(iw/2);
            if (back_im.getX() > 3*iw/2) :
                back_im.setX(iw/2);
            if (back_im.getY() < -height/2) :
                back_im.setY(height/2);
            if (back_im.getY() > 3*height/2) :
                back_im.setY(height/2);


            back_im.update();

            #Spawning
            #Vesicles
            if (time - lastTime_vesc >= spawnRate_vesc):
                vAlive = False;
                for i in range(num_vesc):
                    if (vesc[i].isAlive() == False):
                        vAlive = True;
                        vesc[i].spawn();
                        i = 10000000
                        lastTime_vesc = time;
                        break;
                if (vAlive == False):
                    for i in range(num_vesc):
                        if (isOnScreen(vesc[i],width-wid_menu,height) == False):
                            vesc[i].spawn();
                            i = 10000000
                            lastTime_vesc = time;
                            break;
            #Viruses
            if (time - lastTime_vir >= spawnRate_vir):
                vAlive = False;
                for i in range(num_vir):
                    if (vir[i].isAlive() == False):
                        vAlive = True;
                        vir[i].spawn();
                        vir[i].makeSelf();
                        i = 10000000
                        lastTime_vir = time;
                        break;
                if (vAlive == False):
                    for i in range(num_vir):
                        if (isOnScreen(vir[i],width-wid_menu,height) == False):
                            vir[i].destroy();
                            vir[i].spawn();
                            vir[i].makeSelf();
                            i = 10000000
                            lastTime_vir = time;
                            break;
            #Bacteria
            if (time - lastTime_bact >= spawnRate_bact):
                vAlive = False;
                for i in range(num_bact):
                    if (bact[i].isAlive() == False):
                        vAlive = True;
                        bact[i].spawn();
                        bact[i].makeSelf();
                        i = 10000000
                        lastTime_bact = time;
                        break;
                if (vAlive == False):
                    for i in range(num_bact):
                        if (isOnScreen(bact[i],width-wid_menu,height) == False):
                            bact[i].destroy();
                            bact[i].spawn();
                            bact[i].makeSelf();
                            i = 10000000
                            lastTime_bact = time;
                            break;
            #If we have no DNA left or no ATP left
            #Welcome to Bacterial Hell

            if (cell.getNuc().isAlive() == False or cell.isFreeAtp() == False):

                for i in range(num_vir):
                    if (vir[i].isAlive()):
                        if (vir[i].isOnScreen() == False):
                            vir[i].destroy();
                for i in range(num_vesc):
                    if (vesc[i].isAlive()):
                        if (vesc[i].isOnScreen() == False):
                            vesc[i].kill();
                spawnRate_bact = .15 * fps;
            else:
                spawnRate_bact = old_rate;

            if (cell.getNuc().isAlive() == False):
                spawnRate_vir = 5.0;
                spawnRate_vesc = 1.0;
                spawnRate_bact = .35;


            if (time > medium_time):
                spawnRate_bact = old_rate / 2;
                old_rate = spawnRate_bact;
                spawnRate_vir = spawnRate_vir / 2;
            if (time > hard_time):
                spawnRate_bact = old_rate / 2;
                old_rate = spawnRate_bact;
                spawnRate_vir = spawnRate_vir / 2;



            for i in range(num_prot):
                explode[i].update();
            for i in range(num_bact):
                bact[i].update(oo);
            for i in range(num_vir):
                vir[i].update(kah);
            for i in range(num_vesc):
                vesc[i].update(ee);

            cell.update(ee);

            #Organelles
            nuc.update();
            endo.update();
            endo.selProd(time);
            if(endo.produceProt(time,ttt)):
                endo.setCurrProd([-1,-1]);
                endo.setProdTime(time);
            if(epo != endo.getLenQ()):
                epo = endo.getLenQ();
            mito.produce(time);
            mito.update();

            #Update
            for i in range(num_prot):
                prot[i].update(time);
            for i in range(num_atp):
                atp[i].update();
            for i in range(num_rna):
                rna[i].update();

            #nuc.update();
            #mito.update();









            #Show the Menu
            menu.draw();
            menu_im.update();
            prot_im.update();
            pygame.draw.rect(screen,BLUE,(width - wid_menu + 5, height/2, 185, 85))
            enter_im.update();

            screen.blit(atpobj_text, (width - wid_menu + 10,height/2 - 25))
            screen.blit(beginobj_text, (width - wid_menu + 85,height/2 + 10))
            screen.blit(prodobj_text, (width - wid_menu + 60,height/2 + 35))



            currNa_text = "NA: " + str(cell.getNa() / 1000) +"k";
            freeNa_text = "Free NA: " + str( cell.getFreeNa() / 1000) + "k";
            currRes_text = "Res's: " + str(int(cell.getnRes() / 1000)) + "k";
            freeRes_text = "Free Res: " + str(int(cell.getnRes() - cell.getnProt() * resPerProt)/1000) + "k";
            currAtp_text = "ATP: " + str(cell.getnAtp()) + " / " + str(maxAtp);
            atpRate_text = "ATP Rate: " + str((atpRate)) + "/s"
            currOuter_text = "Outer Protect: ";
            currOutPer_text  = str(cell.getOuter() * 10)  + "%";
            currProd_text = "Current Product: ";
            prod_text = "";
            if(currProd == [-1,-1]):
                prod_text = "None";
            else:
                prod_text = str(int(nuc.getTimeTill(time) + 1)) + "s  " + prot_type[currProd[0]][currProd[1]];

            hpp = cell.getHP();
            if (hpp < 0):
                hpp = 0;
            dnaHP_text = "DNA Health: " + str(int(hpp / 100));

            currNaObj = font.render(currNa_text,True, (250,250,250));
            freeNaObj = font.render(freeNa_text,True, (250,250,250));
            currResObj = font.render(currRes_text,True, (250,250,250));
            freeResObj = font.render(freeRes_text,True, (250,250,250));
            currAtpObj = font.render(currAtp_text,True, (250,250,250));
            atpRateObj = font.render(atpRate_text,True, (250,250,250));
            currOuterObj = font.render(currOuter_text,True, (250,250,250));
            currOutPerObj = font.render(currOutPer_text,True, (250,250,250));
            currProdObj = font.render(currProd_text,True, (250,250,250));
            prodObj = font.render(prod_text,True, (250,250,250));
            dnaHPObj = font.render(dnaHP_text,True, (250,250,250));

            screen.blit(currNaObj, (width - wid_menu + 5,height/2 + 100))
            screen.blit(freeNaObj, (width - wid_menu + 5,height/2 + 130))
            screen.blit(currResObj, (width - wid_menu + 5,height/2 + 160))
            screen.blit(freeResObj, (width - wid_menu + 5,height/2 + 190))
            screen.blit(currAtpObj, (width - wid_menu + 5,height/2 + 220))
            screen.blit(atpRateObj, (width - wid_menu + 5,height/2 + 250))
            screen.blit(currOuterObj, (width - wid_menu + 5,height/2 + 280))
            screen.blit(currOutPerObj, (width - wid_menu + 100,height/2 + 300))
            screen.blit(currProdObj, (width - wid_menu + 5,height/2 + 325))
            screen.blit(prodObj, (width - wid_menu + 15,height/2 + 345))
            screen.blit(dnaHPObj, (width - wid_menu + 5,height/2 + 375))

            #Score
            cScore = int( 20* time / fps + 2000 * cell.getBactKill() + 200 * cell.getVirKill());
            cScore_text = " Score: " + str(cScore);

            cScoreObj = score_font.render(cScore_text,True, (250,250,250));
            pygame.draw.rect(screen, (0,0,0), [0,0,150,30]);
            screen.blit(cScoreObj, (5,2))
            screen.blit(hScoreObj, (5,13))


            time += 1;


        elif (pause):
            pause_screen.birth();
            pause_screen.update();
            pause_screen.kill();


        else:
            #Dead
            screen.fill(BLACK);
            death_screen.birth();
            death_screen.update();
            death_screen.kill();

            crackerBarrell += 1;

            screen.blit(cScoreObj, (5,2))
            screen.blit(hScoreObj, (5,13))

            if ritten == False:
                over.play();
                f = open("./.score.txt", "w")
                if (cScore > hScore):
                    hScore = cScore;
                f.write(str(hScore));
                f.close();
                ritten = True;

            if (ds == 1 and ritten == True and crackerBarrell > 15):
                #Initial Conditions
                fps = 30;
                cell_na = 8000;
                cell_residue = cell_na / 2;
                cell_prot = 0;
                cell_atp = 10;
                atpPerProtRate = .5;
                mitoRate = 2.5;
                rna_per = 1000;
                rna_rate = fps * 1.75;
                res_per = 300;
                prot_rate = fps * 2.15;
                atpreq_list = [[1,1,3],
                               [1,1,1],
                               [2,2,2]];
                prot_refPeriod = fps * .5;
                coefRest = .5;
                nMakeAtp = 5;
                move_atp_rate = fps * .75;

                minr = 130;
                maxr = 250;
                vesc_r = 30;
                resPerVesc = 50;
                vir_nRna = 3

                evil_time = 30 * fps;
                evil_prob = 0.05/fps;

                spawnRate_vesc = fps * 0.45;
                spawnRate_vir = fps * 1.15;
                spawnRate_bact = fps * 2.15;
                old_rate = spawnRate_bact;
                lastTime_vesc = 0;
                lastTime_vir = 5 * fps;
                lastTime_bact = 25 * fps;

                medium_time = 60 * fps;
                hard_time = 120 * fps;

                explode_maxR = 250;
                explode_dr = 750 / fps;

                evil_str = 8;

                bact_dSurr = math.pi * 2 / (fps * 3);
                regen = 1;

                ####################
                #For Sprite Creation

                atp_speed = 7;
                prot_speed = 4;
                rna_speed = 5;
                nuc_speed = .25;
                mito_speed = .5;
                endo_speed = .33;
                vesc_speed = 1.5;

                bact_speed = 1;
                virus_speed = 1;

                atp_rad = 3;
                prot_rad = 10;
                rna_leng = 10;
                rna_turn = math.pi / 12;

                cell_rad = 150;
                bact_rad = 100;
                virus_rad = 75;

                nuc_rad = 50;
                endo_rad = 35;
                mito_rad = 35;

                WHITE = (255,255,255);
                BLUE = (0,0,255);
                RED = (255,0,0);
                GREEN = (0,255,0);
                BLACK = (0,0,0);

                cell_color = (100,200,100);
                atp_color = (50,50,200);
                prot_color = (200,50,50);
                rna_color = (0,0,0);
                bact_color = (200,155,20);
                virus_color = (150,150,0);
                menu_color = (250,150,150);
                outer_color = (100,200,100);
                nuc_color = (200,175,175);
                vesc_color = (150,200,150);
                explode_color = (100,100,250);


                prot_evil_color = (0,0,0);

                pygame.init()
                time = 0;

                #Screen
                size = width, height = 1000, 800
                wid_menu = 200;
                screen = pygame.display.set_mode(size);

                running = True;

                ###############


                num_atp = 200;
                num_prot = 100;
                num_rna = 125;
                num_bact = 35;
                num_vir = 35;
                num_vesc = 50;

                if (3*num_vir < num_rna):
                    num_rna = 3*num_vir  + 50;

                num_dna = 3;
                num_protDna = 3;


                #Sprite Creation
                cell = myLib.Cell();
                cell.setPosition(400,400);
                cell.makeCell();
                cell.setMinR(minr);
                cell.setMaxR(maxr);
                cell.setRegen(regen);
                cell.setHP(10000);
                cell.setNa(cell_na);
                cell.setnRes(cell_residue);
                cell.setResCost(res_per);
                cell.setDim(cell_rad);
                cell.setCoef(coefRest);
                cell.setColor(cell_color);
                cell.resetBactKill();
                cell.setFps(fps);
                cell.setnAtp(1);
                cell.setBoundType(0);
                cell.resetVirKill();
                cell.setBorder(0,width - wid_menu,height,0);
                cell.setScreen(screen);
                cell.birth();

                atp = [ myLib.Atp() for i in range(num_atp) ]
                prot = [ myLib.Prot() for i in range(num_prot) ]
                rna = [ myLib.Rna() for i in range(num_rna) ]
                bact = [ myLib.Bact() for i in range(num_bact) ]
                vir = [ myLib.Virus() for i in range(num_vir) ]
                vesc = [ myLib.Cell() for i in range(num_vesc) ]
                explode = [myLib.Explosion() for i in range(num_prot)]

                atp_pos = 0;
                prot_pos = 0;
                rna_pos = 0;
                bact_pos = 0;
                vir_pos = 0;

                menu = myLib.Rect();



                for i in range(num_atp):
                    atp[i].setPosition(500,500);
                    atp[i].setDim(atp_rad);
                    atp[i].setvo(atp_speed);
                    atp[i].setColor(atp_color);
                    atp[i].setBoundType(0);
                    atp[i].kill();
                    atp[i].setCell(cell);
                    atp[i].setBorder(0,width - wid_menu,height,0);
                    atp[i].setScreen(screen);

                for i in range(num_prot):
                    explode[i].setPosition(401,401);
                    explode[i].setCell(cell);
                    explode[i].setMaxR(explode_maxR);
                    explode[i].setDr(explode_dr);
                    explode[i].setColor(explode_color);
                    explode[i].setScreen(screen);
                    explode[i].setBorder(0,width - wid_menu,height,0);
                    explode[i].kill();

                for i in range(num_prot):
                    prot[i].setPosition(401,401);
                    prot[i].setIntra();
                    prot[i].setDim(prot_rad);
                    prot[i].setCell(cell);
                    prot[i].setvo(prot_speed);
                    prot[i].setPointTemp( [ [0,0],[0,1],[1,1],[1,0] ] )
                    prot[i].setAtpReqList(atpreq_list);
                    prot[i].setNumAtp(4);
                    prot[i].setNMakeAtp(nMakeAtp);
                    prot[i].setRefPer(prot_refPeriod);
                    prot[i].setStr(evil_str);
                    prot[i].setEvilTime(evil_time);
                    prot[i].setEvilProb(evil_prob);
                    prot[i].setColor(prot_color);
                    prot[i].setBoundType(-2);
                    prot[i].setExplode(explode[i]);
                    prot[i].setLineWidth(0);
                    prot[i].kill();
                    #prot[i].birth();
                    prot[i].setBorder(0,width - wid_menu,height,0);
                    prot[i].setScreen(screen);

                for i in range(num_rna):
                    rna[i].setInitPos(-500,-500);
                    rna[i].setLeng(rna_leng);
                    rna[i].setCell(cell);
                    rna[i].setvo(rna_speed);
                    rna[i].setColor(rna_color);
                    rna[i].setTurn(rna_turn);
                    rna[i].setBoundType(-2);
                    rna[i].kill();
                    rna[i].setBorder(0,width - wid_menu,height,0);
                    rna[i].setScreen(screen);

                for i in range(num_vir):
                    vir[i].setPosition(400,400);
                    vir[i].setvo(virus_speed);
                    vir[i].setCell(cell);
                    vir[i].setLineWidth(0);
                    vir[i].setDim(virus_rad);
                    vir[i].setNRna(vir_nRna);
                    vir[i].setColor(virus_color);
                    vir[i].setBoundType(-2);
                    vir[i].setBorder(0,width - wid_menu,height,0);
                    vir[i].setScreen(screen);
                    vir[i].kill();

                for i in range(num_vir):
                    bact[i].setPosition(400,400);
                    bact[i].setvo(bact_speed);
                    bact[i].setCell(cell);
                    bact[i].setDim(bact_rad);
                    bact[i].setColor(bact_color);
                    bact[i].setBoundType(-2);
                    bact[i].setBorder(0,width - wid_menu,height,0);
                    bact[i].setScreen(screen);
                    bact[i].setDSurr(bact_dSurr);
                    bact[i].kill();

                for i in range(num_vesc):
                    vesc[i].setPosition(400,400);
                    vesc[i].makeVesc();
                    vesc[i].setvo(vesc_speed);
                    vesc[i].setMinR(vesc_r);
                    vesc[i].setMaxR(vesc_r);
                    vesc[i].setRegen(regen);
                    vesc[i].setCell(cell);
                    vesc[i].setHP(10);
                    vesc[i].setNa(0);
                    vesc[i].setnRes(0);
                    vesc[i].setResCost(0);
                    vesc[i].setResPerVesc(resPerVesc);
                    vesc[i].setDim(vesc_r);
                    vesc[i].setCoef(0);
                    vesc[i].setColor(vesc_color);
                    vesc[i].setFps(fps);
                    vesc[i].setBoundType(-2);
                    vesc[i].setBorder(0,width - wid_menu,height,0);
                    vesc[i].setScreen(screen);
                    vesc[i].kill();

                cell.setAtp(atp);
                cell.setProt(prot);
                cell.setRna(rna);

                cell.setVesc(vesc);
                cell.setVir(vir);
                cell.setBact(bact);


                #Nucleus
                dna = myLib.MySprite();
                dna.setScreen(screen);
                dna.setImage("./org/dna_00.png");
                dna.scale((75,47));
                dna.setDim(75,45,False);
                dna.setPosition(width - wid_menu + 100,100);
                dna.setBoundType(-2);
                dna.birth();

                ppos = [0,0];
                dpos = [0,0];


                nuc = myLib.Nucleus();
                nuc.setPosition(400,400);
                nuc.setDim(nuc_rad);
                nuc.setvo(nuc_speed);
                nuc.setCell(cell);
                nuc.setColor(nuc_color);
                nuc.setNaCost(rna_per);
                nuc.setProdRate(rna_rate);
                nuc.setBoundType(0);
                nuc.setBorder(0,width - wid_menu,height,0);
                nuc.setScreen(screen);
                nuc.setDna(dna);
                nuc.birth();

                cell.setNuc(nuc);

                endo = myLib.Endo();
                endo.setPosition(300,400);
                endo.setImage("./org/endo.png");
                endo.setDim(endo_rad);
                endo.setvo(endo_speed);
                endo.setResCost(res_per);
                endo.scale((2*endo_rad,2*endo_rad));
                endo.setCell(cell);
                endo.setBoundType(0);
                endo.setBorder(0,width - wid_menu,height,0);
                endo.setScreen(screen);
                endo.birth();

                cell.setEndo(endo);

                mito = myLib.Mito();
                mito.setPosition(400,350);
                mito.setImage("./org/mito.png");
                mito.setDim(mito_rad);
                mito.setvo(mito_speed);
                mito.scale((2*mito_rad,2*mito_rad));
                atpRate = calcAtpRate(prot,[1,2],atpPerProtRate,mitoRate,fps);
                mito.setProdRate(fps / atpRate);
                mito.setCell(cell);
                mito.setBoundType(0);
                mito.setBorder(0,width - wid_menu,height,0);
                mito.setScreen(screen);
                mito.birth();

                cell.setMito(mito);


                #Menu options
                menu.initialize(width - wid_menu / 2, height / 2,wid_menu,height,False,menu_color,screen,True);

                prot_list = [["./pdb/memb0.png","./pdb/memb1.png","./pdb/memb2.png"],
                             ["./pdb/intra0.png","./pdb/intra1.png","./pdb/intra2.png"],
                             ["./pdb/mab0.png","./pdb/mab1.png","./pdb/mab2.png"]];

                dna_to_rna_time =  [[3,3,5],
                                    [2,2,5],
                                    [4,4,4]]

                na_cost = [[rna_per,rna_per,rna_per],
                           [rna_per,rna_per,rna_per],
                           [rna_per,rna_per,rna_per]]
                resPerProt = 300;
                rna_to_prot_time =  [[3,3,3],
                                     [3,3,3],
                                     [3,3,3]]
                menu_list = [["./pdb/menu00.png","./pdb/menu01.png","./pdb/menu02.png"],
                             ["./pdb/menu10.png","./pdb/menu11.png","./pdb/menu12.png"],
                             ["./pdb/menu20.png","./pdb/menu21.png","./pdb/menu22.png"]];
                dna_list = [["./org/dna_00.png","./org/dna_01.png","./org/dna_02.png"],
                            ["./org/dna_10.png","./org/dna_11.png","./org/dna_12.png"],
                            ["./org/dna_20.png","./org/dna_21.png","./org/dna_22.png"]]

                prot_type = [["Flippase","Floppase","Signalling"],
                             ["Protein Enzyme","RNA Enzyme","Lipid Enzyme"],
                             ["mAb A","mAb B","mAb C"]]

                prot_im = myLib.MySprite();
                prot_im.setScreen(screen);
                prot_im.setImage(prot_list[0][0]);
                prot_im.scale((190,190));
                prot_im.setDim(190,190,False);
                prot_im.setPosition(width - wid_menu + 100,100);
                prot_im.setBoundType(-2);
                prot_im.birth();

                back_im = myLib.MySprite();
                back_im.setScreen(screen);
                back_im.setImage("./pdb/bg.png");
                back_im.scale( (3*(width-wid_menu),3*height) );
                back_im.setDim(3*(width-wid_menu),3*height,False);
                back_im.setPosition((width-wid_menu / 2),height/2);
                back_im.setBoundType(-2);
                back_im.birth();

                menu_im = myLib.MySprite();
                menu_im.setScreen(screen);
                menu_im.setImage(menu_list[0][0]);
                menu_im.scale((wid_menu,height));
                menu_im.setDim(wid_menu,height,False);
                menu_im.setPosition(width - wid_menu / 2,height / 2);
                menu_im.setBoundType(-2);
                menu_im.birth();

                enter_im = myLib.MySprite();
                enter_im.setScreen(screen);
                enter_im.setImage("./pdb/enter.png");
                enter_im.scale((wid_menu / 5,wid_menu / 5));
                enter_im.setDim(wid_menu / 5,wid_menu / 5,False);
                enter_im.setPosition(width - wid_menu + 30,height / 2  + 35);
                enter_im.setBoundType(-2);
                enter_im.birth();

                #Produce Text
                currProd = [-1,-1];
                prevProdTime = 0;

                pygame.font.init();
                font = pygame.font.SysFont('Courier New', 20)

                atpreq_text = "ATP Required: " + str(atpreq_list[0][0]);
                atpobj_text = font.render(atpreq_text, True, (250,250,250))
                begin_stop_text = "Begin"
                prod_text = "Production"
                beginobj_text = font.render(begin_stop_text, True, (250,250,250))
                prodobj_text = font.render(prod_text, True, (250,250,250))

                maxNa, maxAtp, maxRes = getMaxMol(cell.getRadius());

                atpRate = calcAtpRate(prot,[1,2],atpPerProtRate,mitoRate,fps);
                mito.setProdRate(atpRate);

                currNa_text = "Nucleic Acids: " + str(cell_na) +" / " + str(maxNa);
                freeNa_text = "Free NAs: " + str( (cell_na - resPerProt * num_prot));
                currRes_text = "Residues: " + str(cell.getnRes()) + " / " + str(maxRes);
                currAtp_text = "ATP: " + str(cell.getnAtp()) + " / " + str(maxAtp);
                atpRate_text = "ATP Rate: " + str(atpRate) + "/s"
                currOuter_text = "Outer Protection: " + str( (cell.getOuter() * 10) ) + "%";
                currProd_text = "Current Production: ";
                prod_text = "";
                if(currProd == [-1,-1]):
                    prod_text = "None";
                else:
                    prod_text = prot_type[currProd[0]][currProd[1]];
                dnaHP_text = "DNA Health: " + str(cell.getHP());

                currNaObj = font.render(currNa_text,True, (250,250,250));
                freeNaObj = font.render(freeNa_text,True, (250,250,250));
                currAtpObj = font.render(currAtp_text,True, (250,250,250));
                atpRateObj = font.render(atpRate_text,True, (250,250,250));
                currOuterObj = font.render(currOuter_text,True, (250,250,250));
                currProdObj = font.render(currProd_text,True, (250,250,250));
                prodObj = font.render(prod_text,True, (250,250,250));
                dnaHPObj = font.render(dnaHP_text,True, (250,250,250));


                pause_screen = myLib.MySprite();
                pause_screen.setScreen(screen);
                pause_screen.kill();
                pause_screen.setPosition(0,0);
                pause_screen.setImage("./menu/pause.png");
                pause_screen.setBoundType(-2);
                pause_screen.scale((width,height));

                death_screen = myLib.MySprite();
                death_screen.setScreen(screen);
                death_screen.kill();
                death_screen.setPosition(0,0);
                death_screen.setImage("./menu/gameOver.png");
                death_screen.setBoundType(-2);
                death_screen.scale((width,height));

                intro_images = ["./menu/0.png","./menu/1.png","./menu/2.png",
                                "./menu/3.png","./menu/4.png","./menu/5.png"]

                intro_screen = myLib.MySprite();
                intro_screen.setScreen(screen);
                intro_screen.kill();
                intro_screen.setPosition(0,0);
                intro_screen.setImage(intro_images[0]);
                intro_screen.setBoundType(-2);
                intro_screen.scale((width,height));
                intro_screen.birth();

                score_font = pygame.font.SysFont('Courier New', 15)
                hScore = 1000;

                try:
                    f = open("./.score.txt", "r")
                    j = f.readline();
                    hScore = int(j);
                    f.close();
                except IOError:
                    hScore = 1000;

                cScore = 0;
                cScore_text = " Score: " + str(cScore);
                hScore_text = "HScore: " + str(hScore);

                cScoreObj = score_font.render(cScore_text,True, (250,250,250));
                hScoreObj = score_font.render(hScore_text,True, (250,250,250));

                #Sounds

                boom = pygame.mixer.Sound("./sounds/boom.ogg");
                ee = pygame.mixer.Sound("./sounds/ee.ogg");
                kah = pygame.mixer.Sound("./sounds/kah.ogg");
                oo = pygame.mixer.Sound("./sounds/oo.ogg");
                over = pygame.mixer.Sound("./sounds/over.ogg");
                bip = pygame.mixer.Sound("./sounds/bip.ogg");
                ttt = pygame.mixer.Sound("./sounds/ttt.ogg");
                
                #Just some stuffs
                clock = pygame.time.Clock();

                ko, so, eo, esco, knmio = checkKeys();

                epo = endo.getLenQ();

                moveTime = 0;
                gTime = 0;

                pause = False;
                isIntro = True;
                ipos = 0;

                ritten = False;

                crackerBarrell = 0;

                konami_input = [0,0,0,0,0,0,0,0,0,0];
                konami_pos = 0;
                konami_code = [0,0,1,1,2,3,2,3,5,4];
                dknmi = [0,0,0,0,0,0];
                triggered = False;

                
                konami_screen = myLib.MySprite();
                konami_screen.setScreen(screen);
                konami_screen.kill();
                konami_screen.setPosition(0,0);
                konami_screen.setImage("./menu/meem.jpg");
                konami_screen.setBoundType(-2);
                konami_screen.scale((width,height));
                konami_screen.kill();




        ko = k;
        so = s;
        eo = e;
        knmio = knmi;
        esco = esc;
        konami_screen.update();

        pygame.display.flip();

        clock.tick(fps);




if __name__=="__main__":
    main();
