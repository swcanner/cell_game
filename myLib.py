import sys, pygame, math, random, copy

class MySprite:

    def __init__(self):
        self.img = [];
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.v_o = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.energy = 0;
        self.visible = False;
        self.boundType = 0;
        self.lborder = 0;
        self.rborder = 400;
        self.bborder = 400;
        self.uborder = 0;
        self.lineWidth = 0;

    def setLineWidth(self,w):
        self.lineWidth = w;
    def getLineWidth(self):
        return self.lineWidth;

    def initialize(self,screen,img,wid,hei,circle,x,y,vx,vy,ax,ay,m,vis,bt):
        self.setScreen(screen);
        self.setImage(img);
        self.setDim(wid,hei,circle);
        self.setPosition(x,y);
        self.setVel(vx,vy);
        self.setAcc(ax,ay);
        self.m = m;
        self.doVecs();
        self.visible = vis;
        self.boundType = bt;

    def dist(self,xa,ya):
        r = (self.x - xa )**2 + (self.y - ya) ** 2;
        r = math.sqrt(r);
        return r;

    def dpos(self,ex,ey):
        self.x += ex;
        self.y += ey;

    def setScreen(self,screena):
        self.screen = screena;

    def setImage(self,image):
        self.im = pygame.image.load(image);

    def scale(self,x):
        self.im = pygame.transform.scale(self.im, x);

    def setPosition(self,xa,ya):
        self.x = xa;
        self.y = ya;
        self.px = xa + .0000001;
        self.py = ya + .0000001;

    def getM(self):
        return self.m;

    def setM(self,m):
        self.m = m;

    def getPosition(self):
        return self.x,self.y

    def isOnScreen(self):
        if self.visible:
            if self.x + self.radius > self.lborder:
                if self.x - self.radius < self.rborder:
                    if self.x + self.radius > self.uborder:
                        if self.y - self.radius < self.bborder:
                            return True;
        return False;


    def getX(self):
        return self.x;
    def getY(self):
        return self.y;
    def setX(self,xo):
        self.x = xo;
    def setY(self,yo):
        self.y = yo;

    def getPx(self):
        return self.px;

    def getPy(self):
        return self.py;

    def setVel(self,vx,vy):
        self.dx = vx;
        self.dy = vy;

    def getVel(self):
        return self.dx, self.dy

    def getVelMag(self):
        return self.vel;

    def getVelAngle(self):
        return self.velAngle;

    def getVx(self):
        return self.dx;

    def getVy(self):
        return self.dy;

    def setAcc(self,ax,ay):
        self.ddx = ax;
        self.ddy = ay;

    def getAcc(self):
        return self.ddx,self.ddy;

    def spawn(self):
        self.birth();

        r = random.random();
        if r < .5:
            r = random.uniform(self.lborder - 1.75 * self.width, self.rborder + 1.75 * self.width);
            self.x = r;
            r = random.random();
            if (r < .5):
                self.y = self.bborder + 1.75 * self.height + random.uniform(0,400);
            else:
                self.y = self.uborder - 1.75 * self.height - random.uniform(0,400);
        else:
            r = random.uniform(1.75 * self.height + self.lborder, self.bborder + 1.75 * self.height);
            self.y = r;
            r = random.random();
            if (r < .5):
                self.x = self.rborder + 1.75 * self.width + random.uniform(0,400);
            else:
                self.x = self.lborder - 1.75 * self.width - random.uniform(0,400);

    def doVecs(self):
        self.vel = math.sqrt(self.dx*self.dx + self.dy*self.dy);
        self.acc = math.sqrt(self.ddx*self.ddx + self.ddy*self.ddy);
        self.velAngle = math.atan2(self.dy,self.dx);
        self.accAngle = math.atan2(self.ddy,self.ddy);
        self.energy = .5 * self.m * self.vel * self.vel;

    def setDim(self,width,height,circle):
        self.width = width;
        self.height = height;
        self.radius = (width + height) / 4;
        self.circle = circle;

    def setBorder(self,lborder,rborder,bborder,uborder):
        self.lborder = lborder;
        self.rborder = rborder;
        self.bborder = bborder;
        self.uborder = uborder;

    def birth(self):
        self.visible = True;

    def revive(self):
        self.visible = True;

    def kill(self):
        self.visible = False;

    def isVisible(self):
        return self.visible;
    def isAlive(self):
        return self.visible;

    def printPos(self):
        print(str(self.x) + " " + str(self.x));

    def move(self):
        cx = self.x;
        cy = self.y;
        #Verlet method ; dt = 1
        #self.x = 2*cx - self.px + self.ddx
        #self.y = 2*cy - self.py + self.ddy

        self.px = cx;
        self.py = cy;

        self.x += self.dx
        self.y += self.dy

        self.dx += self.ddx
        self.dy += self.ddy


    def setvo(self, v):
        self.v_o =  v;

    def brownian(self):
        self.px = self.x;
        self.py = self.y;

        r = random.random();
        r = r * math.pi * 2;

        self.dx = self.v_o * math.cos(r);
        self.dy = self.v_o * math.sin(r);

        self.x += self.dx
        self.y += self.dy


    def setBoundType(self, bt):
        self.boundType = bt;

    def draw(self):
        self.screen.blit(self.im,(self.x - self.width/2,self.y - self.height/2));

    def checkbounds(self):
        #-1 - Die
        #0 - bounce Acc
        #1 - bounce No Acc
        #2 - wrap

        right = self.x + self.width/2;
        left = self.x - self.width/2;
        up = self.y - self.height/2;
        down = self.y + self.height/2;

        r = False;
        l = False;
        t = False;
        b = False;

        if(right > self.rborder):
            r = True;
        if(left < self.lborder):
            l = True;
        if(up < self.uborder):
            t = True;
        if(down > self.bborder):
            b = True;

        if (self.boundType == -1):
            if(r | l | b | t):
                self.visible = False;

        if (self.boundType == 0):

            if(r):
                self.x = self.rborder - self.width/2 -1;
                self.dx = -self.dx;
                self.ddx = -self.ddx;
            if(l):
                self.x = self.lborder + self.width/2 +1
                self.dx = -self.dx;
                self.ddx = -self.ddx;
            if(b):
                self.y = self.bborder - self.height/2 -1
                self.dy = -self.dy;
                self.ddy = -self.ddy;
            if(t):
                self.y = self.uborder + self.height/2 +1
                self.dy = -self.dy;
                self.ddy = -self.ddy;

        if (self.boundType == 1):

            if(r):
                self.x = self.rborder - self.width/2 -1;
                self.dx = -self.dx;
            if(l):
                self.x = self.lborder + self.width/2 +1
                self.dx = -self.dx;
            if(b):
                self.y = self.bborder - self.height/2 -1
                self.dy = -self.dy;
            if(t):
                self.y = self.uborder + self.height/2 +1
                self.dy = -self.dy;

        #Wrap
        if (self.boundType == 2):
            if(r):
                self.x = self.lborder + self.width;
            if(l):
                self.x = self.rborder - self.width;
            if(t):
                self.y = self.bborder + self.height;
            if(b):
                self.y = self.uborder - self.height;

    #Checks if the x y is inside another guy. VERY SIMPLE
    def simpleCollision(self,other):
        right = other.x + other.width/2;
        left = other.x - other.width/2;
        up = other.y - other.height/2;
        down = other.y + other.height/2;

        r = False;
        l = False;
        t = False;
        b = False;

        if(self.x < right):
            r = True;
        if(self.x > left):
            l = True;
        if(self.y > up):
            t = True;
        if(self.y < down):
            b = True;

        if(r & l & t & b):
            return True;

        return False;


    def update(self):
        if(self.visible):
            self.doVecs();
            self.checkbounds();
            self.move();
            self.draw();
            self.doVecs();



class Circle(MySprite):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.energy = 0;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.cell = [];

    def setCell(self,c):
        self.cell = c;
    def getCell(self):
        return self.cell;

    def closeToCell(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = (cx - self.x) ** 2 + (cy - self.y) ** 2;
        r = math.sqrt(r);
        if (r < self.cell.getRadius() + self.radius):
            return True;
        return False;

    def checkOther(self,things):
        for o in things:
            if (o.isAlive()):
                cx = o.getX();
                cy = o.getY();

                r = (cx - self.x) ** 2 + (cy - self.y) ** 2;
                r = math.sqrt(r);
                if (r > .5):
                    if (r < o.getRadius() + self.radius * 1.5):

                        self.px = self.x;
                        self.py = self.y;
                        #Put it inside the cell
                        #get angle that atp is at wrt cell
                        y = self.y - cy;
                        x = self.x - cx;

                        scale_fact = (o.getRadius() + self.radius * 1.5 + 5) / r;

                        x *= scale_fact;
                        y *= scale_fact;

                        self.x = cx + x;
                        self.y = cy + y;
        return;

    def checkOtherSingle(self,thing):
        o =  thing;
        if (o.isAlive()):
            cx = o.getX();
            cy = o.getY();

            r = (cx - self.x) ** 2 + (cy - self.y) ** 2;
            r = math.sqrt(r);

            if (r > .5):
                if (r < o.getRadius() + self.radius * 1.5):

                    self.px = self.x;
                    self.py = self.y;
                    #Put it inside the cell
                    #get angle that atp is at wrt cell
                    y = self.y - cy;
                    x = self.x - cx;

                    scale_fact = (o.getRadius() + self.radius *1.5 + 5) / r;

                    x *= scale_fact;
                    y *= scale_fact;

                    self.x = cx + x;
                    self.y = cy + y;
        return;


    def setColor(self,c):
        self.color = c;

    def setDim(self,r):
        self.width = 2*r;
        self.height = 2*r;
        self.radius = r;
        self.circle = True;

    def getRadius(self):
        return self.radius;

    def draw(self):
        if(self.visible):
            pygame.draw.circle(self.screen,self.color,(int(self.x),int(self.y)),self.radius)



class Cell(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.energy = 0;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.outerColor = (1,1,1);

        self.naPerRna = 1000;
        self.resPerProt = 325;

        self.natp = 0;
        self.nprot = 0;
        self.nres = 0;
        self.na = 0;
        self.nrna = 0;
        self.outer = 0;
        self.coefRest = .8;

        self.atp = [];
        self.prot = [];
        self.rna = [];

        self.vesc = [];
        self.vir = [];
        self.bact = [];

        self.maxAtp = 0;
        self.maxNa = 0;
        self.maxRes = 0;

        self.resPerVesc = 300;

        self.mito = [];
        self.nuc = [];
        self.endo = []

        self.dnaHP = 100.0;
        self.regen = .005;
        self.fps = 150;

        self.isVesc = False;

        self.minRadius = 100;
        self.maxRadius = 250;

        self.bactKill = 0;
        self.virKill = 0;

    def resetBactKill(self):
        self.bactKill = 0;
    def incBactKill(self):
        self.bactKill += 1;
    def getBactKill(self):
        return self.bactKill;
    def resetVirKill(self):
        self.virKill = 0;
    def incVirKill(self):
        self.virKill += 1;
    def getVirKill(self):
        return self.virKill;


    def setResPerVesc(self,r):
        self.resPerVesc = r;
    def getResPerVesc(self):
        return self.resPerVesc;

    def setVesc(self,v):
        self.vesc = v;
    def setVir(self,v):
        self.vir = v;
    def setBact(self,b):
        self.bact = b;
    def getVesc(self):
        return self.vesc;
    def getVir(self):
        return self.vir;
    def getBact(self):
        return self.bact;

    def makeVesc(self):
        self.isVesc = True;
    def makeCell(self):
        self.isVesc = False;
    def getIsVesc(self):
        return self.isVesc;
    def getIsCell(self):
        if self.isVesc:
            return False;
        return True;

    def addRna(self):
        self.na += 1000;

    def setFps(self,f):
        self.fps = f;
    def getFps(self):
        return self.fps;
    def setHP(self,h):
        self.dnaHP = h;
    def getHP(self):
        return self.dnaHP;
    def decHP(self,d):
        if (self.dnaHP >= 0):
            self.dnaHP -=  d;
        else:
            self.nuc.kill();

    def setRegen(self,r):
        self.regen = r;
    def getRegen(self):
        return regen;
    def regener(self):
        if(self.dnaHP < 10000):
            if(self.dnaHP > 0):
                self.dnaHP += self.regen;

    def isFreeAtp(self):
        for i in self.atp:
            if i.isAlive():
                if i.getProt() == []:
                    return True;
        return False;

    def killFreeAtp(self):
        for i in self.atp:
            if i.isAlive():
                if i.getProt() == []:
                    i.kill();
                    self.selfAlive();
                    return;

    def upSuck(self,s):
        if (self.isVesc):
            if (self.closeToCell()):
                s.play();
                self.kill();
                self.cell.incSize();
                self.cell.incRes(self.resPerVesc);

    def setMaxR(self,r):
        self.maxRadius = r;
    def setMinR(self,r):
        self.minRadius = r;
    def getMaxR(self):
        return self.maxRadius;
    def getMinR(self):
        return self.minRadius;

    def getNumLipidEnz(self):
        n = 0
        for i in self.prot:
            if (i.getType() == [1,2]):
                n += 1
        return n

    def decSize(self):
        if(self.radius - 9 > self.minRadius):
            self.radius -= 10;
            return True;
        return False;
    def incSize(self):
        if(self.radius < self.maxRadius):
            self.radius += 3;
            return True;
        return False;

    def decNa(self,d):
        self.na += d;
    def incNa(self,i):
        self.na += i;
    def decRes(self,d):
        self.nres -= d;
    def incRes(self,i):
        self.nres += i;
    def setCoef(self,c):
        self.coefRest = c;

    def remNa(self):
        self.na -= self.naPerRna * (1 - self.coefRest);
        if(self.na <= 0):
            self.na = 0;
    def remRes(self):
        self.nres -= self.resPerProt * (1 - self.coefRest);
        if(self.nres <= 0):
            self.nres = 0;


    def getMito(self):
        return self.mito;
    def getNuc(self):
        return self.nuc;
    def getEndo(self):
        return self.endo;

    def setNuc(self,n):
        self.nuc = n;
    def setMito(self,m):
        self.mito = m;
    def setEndo(self,e):
        self.endo = e;
    def setMaxAtp(self,r):
        self.maxAtp = r;
    def getMaxAtp(self):
        return self.maxAtp;
    def setMaxNa(self,n):
        self.maxNa = n;
    def getMaxNa(self):
        return self.maxNa;
    def setMaxRes(self,r):
        self.maxRes = r;

    def setNaPerRna(self,r):
        self.naPerRna = r;

    def setnAtp(self,a):
        self.natp = a;
    def getnAtp(self):
        return self.natp;
    def setAtp(self,a):
        self.atp = a;
    def getAtp(self):
        return self.atp;

    def selfAlive(self):
        self.natp = self.calcAlive(self.atp);
        self.nprot = self.calcAlive(self.prot);
        self.nrna = self.calcAliveRna();

    def calcAlive(self,item):
        n = 0;
        for i in item:
            if( i.isAlive()):
                n += 1;
        return n;

    def calcAliveRna(self):
        n = 0;
        for i in self.rna:
            if( i.isAlive()):
                if (i.getVir() == []):
                    n += 1;
        return n;

    def setnProt(self,p):
        self.nprot = p;
    def setProt(self,p):
        self.prot = p;
    def getProt(self):
        return self.prot;
    def getnProt(self):
        return self.nprot;
    def setResPerProt(self,n):
        self.resPerProt = n;
    def getResPerProt(self):
        return self.resPerProt;
    def getResCost(self):
        return self.resPerProt;
    def setResCost(self,r):
        self.resPerProt = r;
    def setnRes(self,r):
        self.nres = r;
    def getnRes(self):
        return self.nres;

    def getFreeAmino(self):
        d = self.na - self.nrna * self.naPerRna;
        if(d < 0):
            return 0;
        return d;
    def getFreeNa(self):
        return self.getFreeAmino();

    def getFreeNres(self):
        d = self.nres - self.nprot * self.resPerProt;
        if (d < 0):
            return 0;
        return d;
    def getFreeRes(self):
        return self.getFreeNres();


    def setNa(self,a):
        self.na = a;
    def getNa(self):
        return self.na;
    def getNa(self):
        return self.na;
    def setRna(self,r):
        self.rna = r;
    def getRna(self):
        return self.rna;

    def incOuter(self):
        if(self.outer < 10):
            self.outer += 1;
            a = self.outer * 25;
            self.outerColor = (a,a,a);
            return True;
        else:
            return False;
    def decOuter(self):
        a = self.outer * 25;
        self.outerColor = (a,a,a);
        self.outer -= 1;
    def setOuter(self,o):
        self.outer = o;
    def getOuter(self):
        return self.outer;



    def draw(self):
        if(self.visible):
            pygame.draw.circle(self.screen,self.outerColor,(int(self.x),int(self.y)),self.radius+10)
            pygame.draw.circle(self.screen,self.color,(int(self.x),int(self.y)),self.radius)

    def update(self,s):
        if(self.visible):
            self.checkbounds();
            self.selfAlive();

            if (self.isVesc):
                self.brownian();
                self.checkOther(self.cell.getVesc());
                self.checkOther(self.cell.getVir());
                self.checkOther(self.cell.getBact());
                self.upSuck(s);

            self.regener();
            self.move();
            self.draw();
            self.doVecs();

class Bact(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.energy = 0;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.latch = False;
        self.cellDir = False;
        self.ang = 0;

        self.amount = 0;
        self.dSurr = 0;

    def setDSurr(self,d):
        self.dSurr = d;
    def getDSurr(self):
        self.dSurr = 0;

    def destroy(self):
        self.visible = False;
        self.latch = False;
        self.cellDir = False;
        self.amount = 0;

        #Create Vescicles
        n = 0;
        for i in self.cell.getVesc():
            if i.isAlive() == False:
                i.birth();
                i.setX(self.x + random.uniform(-60,60));
                i.setY(self.y + random.uniform(-60,60));
                n += 1;
            if n > 3:
                break;
        if (n <= 3):
            for i in self.cell.getVesc():
                if i.isAlive():
                    if i.isOnScreen() == False:
                        i.kill();
                        i.setX(self.x + random.uniform(-60,60));
                        i.setY(self.y + random.uniform(-60,60));
                        n += 1;
                if n > 3:
                    break;

    def makeSelf(self):
        self.visible = True;
        self.latch = False;
        self.cellDir = False;
        self.amount = 0;
        #no contents taht matter

    def calcSurr(self):
        if(self.latch):
            if(self.isAlive()):
                self.amount += self.dSurr / (1 + self.cell.getOuter() * .05 + 1.5 * self.cell.getRadius() / self.cell.getMaxR());
                if (self.amount > math.pi * 2 + .1):
                    self.cell.kill();

    def checkGuys(self):
        self.checkOther(self.cell.getBact());
        self.checkOther(self.cell.getVir());
        self.checkOther(self.cell.getVesc());

    def checkLatch(self,s):
        if (not self.latch):
            cx = self.cell.getX();
            cy = self.cell.getY();
            r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

            if(  r < (self.cell.getRadius() + self.radius + 22) ):
                #Latch it

                self.latch = True;
                s.play();
                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (self.cell.getRadius() + self.radius) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;
            else:
                #If Cell is near we  go

                if (r < self.cell.getRadius() + self.radius + 450):
                    self.cellDir = True;
                elif (self.cell.getNuc().isAlive() == False or self.cell.isFreeAtp() == False):
                    self.cellDir = True;
        else:
            cx = self.cell.getX();
            cy = self.cell.getY();

            r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

            y = self.y - cy;
            x = self.x - cx;

            scale_fact = (self.cell.getRadius() + self.radius) / r;

            x *= scale_fact;
            y *= scale_fact;

            self.x = cx + x;
            self.y = cy + y;

    def getLatch(self):
        return self.latch;

    def brownian(self):

        #If latched do nothing cuz like we got that with check latch

        x = self.cell.getX() - self.x;
        y = self.cell.getY() - self.y;

        if (self.latch == False):
            if (self.cellDir == False):

                ang = math.atan2(self.dy,self.dx);
                ang += random.uniform(-.75,.75);
                self.dx = self.v_o * math.cos(ang)
                self.dy = self.v_o * math.sin(ang)
                self.x += self.dx;
                self.y += self.dy;
            else:
                #GO TO THE CELL!
                ang = math.atan2(y,x);
                ang += random.uniform(-1.5,1.5);
                self.dx = self.v_o * math.cos(ang)
                self.dy = self.v_o * math.sin(ang)
                self.x += self.dx;
                self.y += self.dy;

        else:
            #We're latched
            r = random.uniform(0,2*math.pi)
            self.x += math.cos(r) * self.v_o;
            self.y += math.sin(r) * self.v_o;

    def draw(self):
        if(self.visible):


            pygame.draw.circle(self.screen,(0,0,0),(int(self.x),int(self.y)),self.radius+10)
            pygame.draw.circle(self.screen,self.color,(int(self.x),int(self.y)),self.radius)

            if(self.latch):
                off = 100;
                xs = self.cell.getX() - self.cell.getRadius() - off/2;
                ys = self.cell.getY() - self.cell.getRadius() - off/2;
                l = self.cell.getRadius() * 2 + off;

                x = self.x - self.cell.getX();
                y = self.y - self.cell.getY();
                ang = math.atan2(-y,x);

                pygame.draw.arc(self.screen, self.color,
                    [xs,ys,l,l],ang-self.amount/2,ang+self.amount/2,self.cell.getRadius());

    def update(self,s):
        if(self.visible):
            self.brownian();
            self.checkGuys();
            self.checkLatch(s);
            self.calcSurr();
            self.draw();

class Virus(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 3;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.lineWidth = 0;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.energy = 0;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);


        self.points = [];
        self.outline = [];
        self.point_template = [];
        self.cell = [];
        self.rna = [];
        self.nRna = 3;
        self.type = 0;

        self.latch = False;



    def makePoint(self):
        for i in range(len(self.point_template)):
            #self.points[i] = tuple(el
            self.points[i][0] = self.x + self.radius * self.point_template[i][0];
            self.points[i][1] = self.y + self.radius * self.point_template[i][1];
            self.outline[i][0] = self.x + (self.radius + 10) * self.point_template[i][0];
            self.outline[i][1] = self.y + (self.radius + 10) * self.point_template[i][1];

    def draw(self):
        self.makePoint();
        pygame.draw.polygon(self.screen,(0,0,0),self.outline,self.lineWidth);
        pygame.draw.polygon(self.screen,self.color,self.points,self.lineWidth);

    def getShape(self):

        s = [];

        if(self.type == 0):
            s = [ [-1,-1],[-1,1],[1,1],[1,-1],[-1,-1] ]
        elif(self.type == 1):
            s = [ [-.65,-1],[-1,.65],[0,1],[1,.65],[.65,-1] ]
        else:
            self.type = 2;
            s = [ [-.5,-1],[-1,0],[-.5,1],[.5,1],[1,0],[.5,-1] ]

        self.point_template = s;
        self.points = copy.deepcopy(s);
        self.outline = copy.deepcopy(s);

    def checkLatch(self,s):
        if (not self.latch):
            if (self.rna != []):
                cx = self.cell.getX();
                cy = self.cell.getY();

                r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

                if(  r < (self.cell.getRadius() + self.radius + 22) ):
                    #Latch it

                    self.latch = True;

                    s.play();

                    y = self.y - cy;
                    x = self.x - cx;

                    scale_fact = (self.cell.getRadius() + self.radius) / r;

                    x *= scale_fact;
                    y *= scale_fact;

                    self.x = cx + x;
                    self.y = cy + y;
        else:
            if (self.rna == []):
                self.latch = False;
            else:
                cx = self.cell.getX();
                cy = self.cell.getY();

                r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (self.cell.getRadius() + self.radius) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;
    def getLatch(self):
        return self.latch;

    def brownian(self):

        #If latched do nothing cuz like we got that with check latch

        #Run away from the cell
        if (self.rna == []):
            self.latch = False;
            cx = self.cell.getX();
            cy = self.cell.getY();

            y = self.y - cy;
            x = self.x - cx;

            ang = math.atan2(y,x);
            ang += random.uniform(-.5,.5);
            self.dx = self.v_o * math.cos(ang)
            self.dy = self.v_o * math.sin(ang)
            self.x += self.dx;
            self.y += self.dy;

            self.checkOtherSingle(self.cell)


        elif (self.latch == False):

            ang = math.atan2(self.dy,self.dx);
            ang += random.uniform(-.5,.5);
            self.dx = self.v_o * math.cos(ang)
            self.dy = self.v_o * math.sin(ang)
            self.x += self.dx;
            self.y += self.dy;

        else:
            #We're latched
            r = random.uniform(0,2*math.pi)
            self.x += math.cos(r) * self.v_o;
            self.y += math.sin(r) * self.v_o;

    def setNRna(self,n):
        self.nRna = n;
    def getNRna(self):
        return self.nRna;
    def setType(self,t):
        self.type = t;
    def getType(self):
        return self.type;
    def getRna(self):
        return self.rna;
    def delRna(self):
        self.rna = [];
    def remRna(self,c):
        self.rna.remove(c);
    def destroyRna(self):
        for i in self.rna:
            i.kill();
            i.unsetVir();
        self.rna = [];

    def addRna(self):
        for i in self.cell.getRna():
            if(i.isAlive() == False):
                i.birth();
                i.setType([-2,self.type]);
                self.rna.append(i);
                i.setVir(self);
                return;

    def putRna(self):
        for i in self.rna:
            r0 = random.uniform(0,self.radius);
            r1 = random.uniform(0,2*math.pi);
            r2 = random.uniform(0,2*math.pi);

            i.setXo(r0 * math.cos(r1));
            i.setYo(r1 * math.sin(r1));
            i.setAng(r2);
            i.calcPos();


    def randType(self):
        r = random.uniform(0,3);
        r = int(r);
        self.type = r;

    def makeSelf(self):
        self.randType();
        self.getShape()
        for i in range(self.nRna):
            self.addRna();
        self.birth();
        self.putRna();

    def destroy(self):
        self.kill();
        self.destroyRna();

    def update(self,s):
        if(self.visible):
            self.checkbounds();
            self.brownian();
            self.checkOther(self.cell.getVesc());
            self.checkOther(self.cell.getVir());
            self.checkLatch(s);
            self.draw();
            self.doVecs();

class Atp(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.cell = [];
        self.prot  = [];
        self.latch = False;
        self.looker = [];

    def setProt(self,p):
        self.prot = p;

    def setCell(self,c):
        self.cell = c;

    def getProt(self):
        return self.prot;

    def getCell(self):
        return self.cell;

    def latchProt(self,p):
        if(p.addAtp(self)):
            self.prot = p;
            self.latch = True;

    def clearLooker(self):
        looker = [];

    def unLatch(self):
        self.latch = False;
        self.prot = [];

    def goWithProt(self):
        if(self.latch and self.prot.isAlive()):
            self.px = self.x;
            self.py = self.y;
            self.x = self.prot.getX();
            self.y = self.prot.getY();

    def kill(self):
        self.latch = False;
        self.prot = [];
        self.visible = False;

    #Latch to protein if
    def checkLatchProt(self,p):
        if (not self.latch):
            for i in range(len(p)):
                if (p[i].isAlive()):
                    if (not p[i].getAllFull()):

                        cx = p[i].getX();
                        cy = p[i].getY();

                        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

                        if(  r < (p[i].getRadius() + self.getRadius() + 1.25) ):
                            self.latchProt(p[i]);
                            return;



    #Make sure it stays in the cell
    def checkCell(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if(  r > (self.cell.getRadius() - 8) ):
            self.px = self.x;
            self.py = self.y;
            #Put it inside the cell
            #get angle that atp is at wrt cell
            y = self.y - cy;
            x = self.x - cx;

            scale_fact = (self.cell.getRadius() - 8) / r;

            x *= scale_fact;
            y *= scale_fact;

            self.x = cx + x;
            self.y = cy + y;

    def checkSelf(self):
        #Check Cell
        self.checkCell();
        self.checkOrganelle(self.cell.getNuc() );
        self.checkOrganelle(self.cell.getEndo() );
        self.checkOrganelle(self.cell.getMito() );


    def checkOrganelle(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );
        if(org.isAlive()):
            if(  r < (org.getRadius() + 3) ):
                self.px = self.x;
                self.py = self.y;
                #Put it OUTSIDE the organelle
                #get angle that atp is at wrt cell
                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (org.getRadius() + self.getRadius() + 5) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;

    def brownian(self):
        if(self.latch == False and self.prot == []):
            if(self.looker == []):
                r = 125;
                p = [];
                for i in self.cell.getProt():
                    if(i.isAlive()):
                        if(not i.isAtpFull()):
                            cr = self.dist(i.getX(),i.getY());
                            if(cr < r):
                                r = cr;
                                p = i;
                if(p != []):
                    self.looker = p;

            if(self.looker != []):
                if(not self.looker.isAtpFull() and self.looker.isAlive()):
                    self.px = self.x
                    self.py = self.y;

                    cx = self.looker.getX();
                    cy = self.looker.getY();

                    rx = cx - self.x;
                    ry = cy - self.y;

                    ang = math.atan2(ry,rx);

                    r = random.uniform(ang-1.5,ang+1.5);

                    self.dx = self.v_o * math.cos(r);
                    self.dy = self.v_o * math.sin(r);

                    self.x += self.dx
                    self.y += self.dy
                else:
                    self.looker = [];
            else:
                self.px = self.x;
                self.py = self.y;
                r = random.uniform(0,6.28);

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy
        else:
            self.looker = [];

    def kicker(self):
        if self.px == self.x:
            if self.py == self.y:
                r = random.uniform(0,6.28);

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy

    def isIn(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if(  r < (org.getRadius() + 3) ):
            return True;
        return False;


    def badBound(self):

        for i in range(5):
            a = self.isIn(self.cell.getEndo());
            b = self.isIn(self.cell.getMito());
            c = self.isIn(self.cell.getNuc());

            if (a or b or c):
                self.px = self.x;
                self.py = self.y;
                self.kicker();
                self.checkCell();
            else:
                return;

    def checkProt(self):
        if (self.prot != []):
            if(self.prot.isAlive()):
                return;
            else:
                self.kill();

    def update(self):

        if(self.visible):
            self.checkProt();
            if(self.latch):
                self.checkSelf();
                self.goWithProt();
                self.draw();
                #if(self.px == self.x):
                #    if(self.py == self.y):
                #        self.getProt().kill();
                #        self.getProt().killAtp();
                #        self.kill();
                self.kicker();
            else:
                self.brownian();
                self.checkLatchProt(self.cell.getProt());
                #self.badBound();
                self.checkbounds();
                self.checkSelf();
                self.draw();
                #self.badBound();
                self.kicker();
        self.px = self.x;
        self.py = self.y;

        """
        pygame.font.init();
        font = pygame.font.SysFont('Courier New', 32)
        s = str(len(self.prot.atp));
        text = font.render(s, True, (250,250,250))
        self.screen.blit(text, (self.x,self.y))
        """

class Nucleus(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.cell = [];
        self.dna  = [];

        self.currProd = [-1,-1];
        self.naCost = 0;
        self.prodTime = 0;
        self.prod_rate  = 100;


    def setDna(self,p):
        self.dna = p;

    def setCell(self,c):
        self.cell = c;

    def getDna(self):
        return self.dna;

    def getCell(self):
        return self.cell;

    def setProdRate(self,r):
        self.prod_rate = r;
    def setNaCost(self,n):
        self.naCost = n;
    def getNaCost(self):
        return self.naCost;
    def setCurrProd(self,ind):
        self.currProd = ind;
    def getCurrProd(self):
        return self.currProd;
    def setProdTime(self,t):
        self.prodTime = t;
    def produceRna(self,t,s):
        #Just cuz
        if(self.currProd != [-1,-1]):
            if( self.cell.getNa() > self.naCost ):
                if(t - self.prodTime >= self.prod_rate):
                    #We produce
                    for i in self.cell.getRna():
                        if(i.isAlive() == False):
                            i.birth();
                            i.unsetVir();
                            i.setVir([]);
                            i.setPosition(self.x + random.uniform(-1,1),self.y + random.uniform(-1,1) );
                            i.setAng(math.atan2(self.y,self.x))
                            i.setType(self.currProd);
                            i.calcPos();
                            self.cell.selfAlive();
                            self.prevProd = t;
                            self.currProd = [-1,-1]
                            s.play();
                            return True;
        return False;
    def getTimeTill(self,t):
        timey = (self.prod_rate  - (t - self.prodTime)) / (self.cell.getFps())
        return timey;

    #Make sure it stays in the cell
    def checkCell(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if(  r > (self.cell.getRadius() - self.radius) ):
            #Put it inside the cell
            #get angle that atp is at wrt cell
            y = self.y - cy;
            x = self.x - cx;

            scale_fact = (self.cell.getRadius() - self.radius - 10) / r;

            x *= scale_fact;
            y *= scale_fact;

            self.x = cx + x;
            self.y = cy + y;

    def checkOrganelle(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if (org.isAlive()):
            if(  r < (org.getRadius() + self.getRadius() + 20) ):
                #Put it OUTSIDE the organelle
                #get angle that atp is at wrt cell
                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (org.getRadius() + self.radius + 25) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;

    def checkSelf(self):
        #Check Cell
        self.checkCell();
        self.checkOrganelle(self.cell.getMito() );
        self.checkOrganelle(self.cell.getEndo());



    def update(self):
        if(self.visible):
            self.brownian();
            #self.x = self.cell.getX();
            #self.y = self.cell.getY();
            self.checkbounds();
            self.checkSelf();
            self.draw();

            self.dna.setPosition(self.x,self.y);
            self.dna.update();

class Endo(Circle):

    def __init__(self):
        self.screen = [];
        self.im = []
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.cell = [];

        self.prodQueue = [];

        self.currProd = [-1,-1];
        self.prodTime = 0;
        self.prod_rate = 50;

        self.resCost = 330;

    def setProdTime(self,p):
        self.prodTime = p;
    def getProdTime(self):
        return self.prodTime;
    def setCurrProd(self,p):
        self.currProd = p;
    def getCurrProd(self):
        return self.currProd
    def setProdRate(self,p):
        self.prod_rate = p;
    def setResCost(self,r):
        self.resCost = r;
    def getProdRate(self):
        return self.prod_rate;
    def getResCost(self):
        return self.resCost;

    def getLenQ(self):
        return len(self.prodQueue);

    def setCell(self,c):
        self.cell = c;

    def getCell(self):
        return self.cell;

    #Make sure it stays in the cell
    def checkCell(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if(  r > (self.cell.getRadius() - self.radius) ):
            #Put it inside the cell
            #get angle that atp is at wrt cell
            y = self.y - cy;
            x = self.x - cx;

            scale_fact = (self.cell.getRadius() - self.radius) / r;

            x *= scale_fact;
            y *= scale_fact;

            self.x = cx + x;
            self.y = cy + y;

    def checkOrganelle(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );
        if (org.isAlive()):
            if(  r < (org.getRadius() + self.getRadius() + 20) ):
                #Put it OUTSIDE the organelle
                #get angle that atp is at wrt cell
                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (org.getRadius() + self.radius + 25) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;

    def rnaEnter(self,rna):
        self.prodQueue.append(rna);
        rna.setInEndo();

    def selProd(self,t):
        if(self.currProd == [-1,-1]):
            if( self.cell.getFreeRes() > self.resCost ):
                if (len(self.prodQueue) > 0):
                    self.currProd = self.prodQueue[0].getType();
                    self.prodTime = t;

    def produceProt(self,t,s):
        #Check if we are producing
        if(self.currProd != [-1,-1]):
            #Check if we CAN produce
            if( self.cell.getFreeAmino() > self.resCost ):
                #has time passed
                if(t - self.prodTime >= self.prod_rate):
                    #We produce
                    for i in self.cell.getProt():
                        if(i.isAlive() == False):
                            i.birth();
                            i.setPosition(self.x + random.uniform(-1,1),self.y + random.uniform(-1,1) );
                            r = self.prodQueue[0];
                            i.makeSelf(r.getType(),t);
                            self.cell.selfAlive();
                            self.prevProd = t;
                            self.CurrProd = [-1,-1];
                            i.setCreateTime(t);

                            r.setOutEndo();
                            r.kill();
                            #r.setPosition(self.x + random.uniform(-1,1),self.y + random.uniform(-1,1) );
                            #r.setAng(math.atan2(self.y,self.x))
                            #r.setType(self.currProd);
                            #r.checkOrganelle(self);
                            self.cell.remNa();

                            self.prodQueue.remove(self.prodQueue[0]);

                            s.play();

                            return True;
        return False;

    def checkSelf(self):
        #Check Cell
        self.checkCell();
        self.checkOrganelle(self.cell.getNuc() );
        self.checkOrganelle(self.cell.getMito() );

    def draw(self):
        self.screen.blit(self.im,(self.x - self.width/2,self.y - self.height/2));


    def update(self):
        if(self.visible):
            self.brownian();
            self.checkbounds();
            self.checkSelf();
            self.draw();

class Mito(Circle):

    def __init__(self):
        self.screen = [];
        self.im = []
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.cell = [];
        self.prevProd = 0; #Time previously produced an ATP
        self.prod_rate = 100; #Frames till production
        self.rna_type = [];

    def setCell(self,c):
        self.cell = c;
    def getCell(self):
        return self.cell;
    def setProdRate(self,p):
        self.prod_rate = p;
    def produce(self,t):
        if(self.cell.getMaxAtp() > self.cell.getnAtp()):
            if(t - self.prevProd >= self.prod_rate):
                #We produce
                for i in self.cell.getAtp():
                    if(i.isAlive() == False):
                        i.birth();
                        i.setPosition(self.x + random.uniform(-1,1),self.y + random.uniform(-1,1) );
                        self.cell.selfAlive();
                        self.prevProd = t;
                        return;

    def makeNAtp(self,n):
        k = 0;
        i = 0;

        while i < len(self.cell.getAtp()):
            if(self.cell.getAtp()[i].isAlive() == False):
                self.cell.getAtp()[i].birth();
                self.cell.getAtp()[i].setPosition(self.x + random.uniform(-1,1),self.y + random.uniform(-1,1) );
                self.cell.selfAlive();
                k += 1;
            i += 1;
            if(k >= n):
                i = 1000000000;

    def getCell(self):
        return self.cell;

    #Make sure it stays in the cell
    def checkCell(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if(  r > (self.cell.getRadius() - self.radius - 5) ):
            #Put it inside the cell
            #get angle that atp is at wrt cell
            y = self.y - cy;
            x = self.x - cx;

            scale_fact = (self.cell.getRadius() - self.radius - 10) / r;

            x *= scale_fact;
            y *= scale_fact;

            self.x = cx + x;
            self.y = cy + y;

    def checkOrganelle(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );
        if (org.isAlive()):
            if(  r < (org.getRadius() + self.radius + 20) ):
                #Put it OUTSIDE the organelle
                #get angle that atp is at wrt cell
                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (org.getRadius() + self.radius + 25) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;

    def checkSelf(self):
        #Check Cell
        self.checkCell();
        self.checkOrganelle(self.cell.getNuc() );
        self.checkOrganelle(self.cell.getEndo());

    def draw(self):
        self.screen.blit(self.im,(self.x - self.width/2,self.y - self.height/2));


    def update(self):
        if(self.visible):
            self.brownian();
            self.checkbounds();
            self.checkSelf();
            self.draw();

class Prot(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.cell = [];
        self.type = [-1,-1];

        self.numSides = 3;
        self.point_template = [ [0,0],[0,1],[1,1],[1,0] ];
        self.points = [ [0,0],[0,1],[1,1],[1,0] ];
        self.orientUp = True;
        self.width = 0;

        self.createTime = 0;
        self.evilTime = 0;
        self.evilProb = 0;
        self.lineWidth = 0;

        self.numAtpList = [[1,1,4],[1,1,0],[2,2,2]];

        self.numreq_atp = 0;
        self.active = False;
        self.allAtp = False;
        self.atp = [];

        self.nMakeAtp = 5;

        self.memb = False;
        self.latch = False;

        self.looker = [];

        self.time = 0;
        self.refPer = 10;
        self.prevFire = 0;

        self.evil = False;
        self.str = .05;

        self.explosion = [];

    def setLineWidth(self,l):
        self.lineWidth = l;
    def getLineWidth(self):
        return self.lineWidth;

    def setExplode(self,e):
        self.explosion = e;
        e.setProt(self);
    def getExplode(self):
        return self.explosion;

    def setCreateTime(self,s):
        self.createTime = s;
    def getCreateTime(self):
        return self.createTime;
    def setEvilTime(self,e):
        self.evilTime = e;
    def getEvilTime(self):
        return self.evilTime;
    def setEvilProb(self,e):
        self.evilProb  = e;
    def getEvilProb(self):
        return self.evilProb;

    def makeEvil(self):
        self.evil = True;
        self.color = (0,0,0);
    def isEvil(self):
        return self.evil;
    def getEvil(self):
        return self.evil;
    def makeGood(self):
        self.evil = False;
    def setStr(self,s):
        self.str = s;
    def getStr(self):
        return self.str;

    def setRefPer(self,r):
        self.refPer = r;
    def getRefPer(self):
        return self.refPer;
    def setPrevFire(self,t):
        self.prevFire = t;
    def getPrevFire(self):
        return self.prevFire;

    def setNMakeAtp(self,n):
        self.nMakeAtp = n;

    def getShape(self):

        s = [];

        if(self.type == [0,0]):
            s = [ [-1,-1],[-1,1],[1,1],[1,-1] ]
        elif(self.type == [0,1]):
            s = [ [0,0],[0,1],[1,1],[1,-1],[-1,-1],[-1,0] ]
        elif(self.type == [0,2]):
            s = [ [-.5,1],[.5,1],[.5,.5],[1,.5],[1,-.5],[.5,-.5],[.5,-1],[-.5,-1],[-.5,-.5],[-1,-.5],[-1,.5],[-.5,.5] ]
        elif(self.type == [1,0]):
            s = [ [0,-1],[1,0],[0,1],[-1,0] ]
        elif(self.type == [1,1]):
            s = [ [-1,1],[1,1],[-1,-1] ]
        elif(self.type == [1,2]):
            s = [ [-1,-1],[0,1],[1,1],[0,-1] ]
        elif(self.type == [2,0]):
            s = [ [.5,1],[.5,0],[1,-1],[.5,-1],[0,-.25],[-.5,-1],[-1,-1],[-.5,0],[-.5,1]]
        elif(self.type == [2,1]):
            s = [ [-1,1],[1,1],[0 ,-1]]
        elif(self.type == [2,2]):
            s = [ [.5,1],[.5,-1],[1,-1],[-1,-1]]
        elif(self.type == [-2,0]):
            s = [ [-1,-1],[-1,1],[1,1],[1,-1] ]
        elif(self.type == [-2,1]):
            s = [ [-1,-1],[-1,1],[1,1],[1,-1] ]
        elif(self.type == [-2,2]):
            s = [ [-1,-1],[-1,1],[1,1],[1,-1] ]


        self.points = copy.deepcopy(s);
        self.point_template = copy.deepcopy(s);

    def getCost(self):
        if  (self.evil == False):
            self.numreq_atp = self.numAtpList[self.type[0]][self.type[1]];
        else:
            self.numreq_atp = 0;

    def setAtpReqList(self,n):
        self.numAtpList = n;

    def makeSelf(self,ty,ti):
        self.birth();
        self.type = ty;
        self.latch = False;

        if (self.type == [0,0]):
            self.memb = True
        elif (self.type == [0,1]):
            self.memb = True
        elif (self.type == [0,2]):
            self.memb = True;
        elif (self.type == [1,2]):
            self.memb = True;
        else:
            self.memb = False;

        self.looker = [];
        self.time = ti;
        self.prevFire = ti;
        self.getCost();
        self.getShape();

    def canFire(self,t):
        if(t - self.prevFire > self.refPer):
            return True;
        return False;


    def doJob(self,t):
        if(self.isAtpFull()):
            if(self.canFire(t)):
                if(self.type == [0,0]):
                    #Flippase
                    if(self.latch == True):
                        if(self.cell.getOuter() < 10):
                            self.killAtp();
                            self.cell.incOuter();
                            self.setPrevFire(t);
                elif(self.type == [0,1]):
                    #Floppase
                    if(self.latch == True):
                        if(self.cell.getOuter() > 0):
                            self.killAtp();
                            self.cell.decOuter();
                            self.setPrevFire(t);
                #Cannot do [0,2] here, done thru space
                #Inside main code right before updates and spawns
                elif(self.type == [0,2]):
                    self.makeGood();
                elif(self.type == [1,0]):
                    #Protein Enzyme
                    i = self.closeToProt(self.cell.getProt());
                    if (i != []):
                        if (i.isEvil()):
                            self.cell.incVirKill();
                        i.killAtp();
                        i.kill();
                        self.looker = [];
                        self.cell.remRes();
                        self.killAtp();
                        self.setPrevFire(t);
                elif(self.type == [1,1]):
                    #Rna Enzyme
                    i = self.closeToRna(self.cell.getRna());
                    if (i != []):
                        if (i.getType()[0] == -2):
                            self.cell.incVirKill();
                        self.looker = [];
                        i.kill();
                        self.cell.remNa();
                        self.killAtp();
                        self.setPrevFire(t);
                elif(self.type == [1,2]):
                    #Lipid Enzyme
                    if(self.latch == True):
                        if(self.cell.decSize() == True):
                            self.killAtp();
                            self.setPrevFire(t);
                            self.cell.getMito().makeNAtp(self.nMakeAtp);
                elif(self.type == [2,0]):
                    #mab a
                    i = self.closeToSpecRna(self.cell.getRna(),[-2,0]);
                    if (i != []):
                        self.cell.incVirKill();
                        self.looker = [];
                        i.kill();
                        self.cell.remNa();
                        self.killAtp();
                        self.setPrevFire(t);
                elif(self.type == [2,1]):
                    #mab b
                    i = self.closeToSpecRna(self.cell.getRna(),[-2,1]);
                    if (i != []):
                        self.cell.incVirKill();
                        self.looker = [];
                        i.kill();
                        self.cell.remNa();
                        self.killAtp();
                        self.setPrevFire(t);
                elif(self.type == [2,2]):
                    #mab c
                    i = self.closeToSpecRna(self.cell.getRna(),[-2,2]);
                    if (i != []):
                        self.cell.incVirKill();
                        self.looker = [];
                        i.kill();
                        self.cell.remNa();
                        self.killAtp();
                        self.setPrevFire(t);
                else:
                    #EVIL Protein
                    self.memb = False;
                    self.latch = False;
                    self.evil = True;
                    #self.color = (0,0,0);
                    self.numreq_atp = 0;
                    if self.cell.getNuc().isAlive():
                        if self.closeToNuc():
                            self.attackDna();


    def attackDna(self):
        self.cell.decHP(self.str);

    def explode(self,t):
        if self.isAlive():
            if self.getType() == [0,2]:
                if self.isAtpFull():
                    if self.canFire(t):
                        self.looker = [];
                        self.explosion.explode(t);
                        self.killAtp();
                        self.setPrevFire(t);



    def checkEvil(self,t):
        if (self.type[0] >= -1):
            self.evil = False;
            #Now we need to check if it goes evil

            if (self.createTime + self.evilTime < t):
                #calc if become evil
                r =  random.random();
                if (r < self.evilProb):
                    #It became evil!!! Setup the evil stuff
                    self.evil = True;
                    self.type[0] = -2;
                    self.looker = [];
                    self.numreq_atp = 0;
                    self.killAtp();

        else:
            self.evil = True;

    def setMemb(self):
        self.memb = True;
    def setIntra(self):
        self.memb = False;
    def getMemb(self):
        return self.memb;

    def getAllFull(self):
        return self.allAtp;

    def checkAllFull(self):
        if(len(self.atp) >= self.numreq_atp):
            self.allAtp = True;
        else:
            self.allAtp = False;

    def addAtp(self,a):
        if(not self.allAtp):
            #We can add it
            self.atp.append(a);
            self.checkAllFull();
            return True;
        return False;

    def setNumAtp(self,n):
        self.numreq_atp = n;

    #Checks to see if its within range of another protein in the list
    #Returns the first one in the list that is seen
    def closeToProt(self,p):
        for i in range(len(p)):
            if (p[i].isAlive()):
                px = p[i].getX();
                py = p[i].getY();
                if(px != self.x and py != self.y):
                    #Make sure its not the protein itself
                    r = math.sqrt( (px - self.x)**2 + (py - self.y)**2 );
                    if(r < 2*self.radius):
                        return p[i];
        return [];

    def closeToNuc(self):

        px = self.cell.getNuc().getX();
        py = self.cell.getNuc().getY();

        r = math.sqrt( (px - self.x)**2 + (py - self.y)**2 );
        if (r < self.cell.getNuc().getRadius() + self.getRadius() + 7):
            return True;

    def closeToRna(self,r):
        for i in range(len(r)):
            if (r[i].isAlive()):
                px = r[i].getXo();
                py = r[i].getYo();

                tr = math.sqrt( (px - self.x)**2 + (py - self.y)**2 );
                if(tr < self.radius + 3):
                    return r[i];

                px = r[i].getXf();
                py = r[i].getYf();

                tr = math.sqrt( (px - self.x)**2 + (py - self.y)**2 );
                if(tr < self.radius + 3):
                    return r[i];

        return [];

    def closeToSpecRna(self,r,t):
        for i in range(len(r)):
            if  (r[i].isAlive()):
                if (r[i].getType() == t):
                    px = r[i].getXo();
                    py = r[i].getYo();

                    tr = math.sqrt( (px - self.x)**2 + (py - self.y)**2 );
                    if(tr < self.radius + 3):
                        return r[i];

                    px = r[i].getXf();
                    py = r[i].getYf();

                    tr = math.sqrt( (px - self.x)**2 + (py - self.y)**2 );
                    if(tr < self.radius + 3):
                        return r[i];

        return [];

    def killAtp(self):
        for i in range(len(self.atp)):
            self.atp[i].kill();
            self.atp[i].unLatch();
            self.atp[i].setProt([]);
            self.atp[i].setPosition(-500,-500);
        self.atp = [];
        self.allAtp = False;

    def setLatch(self):
        if(self.memb):
            self.latch = True;
        else:
            self.latch = False;
    def setUnLatch(self):
        self.latch = False;
    def getLatch(self):
        return self.latch;

    def setActive(self):
        self.active = True;
    def setPassive(self):
        self.active = False;
    def getActive(self):
        return self.active;

    def setLooker(self,l):
        self.looker = l;
    def clearLooker(self):
        self.looker = [];

    def checkLatch(self):
        if (self.memb):
            cx = self.cell.getX();
            cy = self.cell.getY();

            r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

            if(  r > (self.cell.getRadius() - 8) ):
                #Latch it

                self.setLatch();

                y = self.y - cy;
                x = self.x - cx;

                scale_fact = self.cell.getRadius() / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;
        else:
            self.latch = False;

    def keepLatch(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );
        scale_fact = self.cell.getRadius() / r;

        y = self.y - cy;
        x = self.x - cx;

        x *= scale_fact;
        y *= scale_fact;

        self.x = cx + x;
        self.y = cy + y;


    def setPointTemp(self,p):
        self.point_template = p;

    def makePoint(self):
        for i in range(len(self.point_template)):
            #self.points[i] = tuple(el
            self.points[i][0] = self.x + self.radius * self.point_template[i][0];
            self.points[i][1] = self.y + self.radius * self.point_template[i][1];


    def setCell(self,c):
        self.cell = c;

    def getCell(self):
        return self.cell;

    def setWidth(self,w):
        self.width = w;

    def fill(self):
        self.width = 0;

    def setNumSides(self,n):
        numSides = n;

    def setType(self,t):
        self.type = t;
    def getType(self):
        return self.type;

    def draw(self):
        #pygame.draw.polygon(self.screen,self.color,[[0,0],[20,20],[100,5]]);
        if (self.evil):
            pygame.draw.polygon(self.screen,(0,0,0),self.points,self.lineWidth);
        else:
            pygame.draw.polygon(self.screen,self.color,self.points,self.lineWidth);

     #Make sure it stays in the cell
    def checkCell(self):
        cx = self.cell.getX();
        cy = self.cell.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );

        if(  r > (self.cell.getRadius() - 8) ):
            #Put it inside the cell
            #get angle that atp is at wrt cell
            y = self.y - cy;
            x = self.x - cx;

            scale_fact = (self.cell.getRadius() - 8) / r;

            x *= scale_fact;
            y *= scale_fact;

            self.x = cx + x;
            self.y = cy + y;

    def checkSelf(self):
        #Check Cell
        self.checkCell();
        self.checkOrganelle(self.cell.getNuc() );
        self.checkOrganelle(self.cell.getEndo() );
        self.checkOrganelle(self.cell.getMito() );


    def checkOrganelle(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.x)**2 + (cy - self.y)**2 );
        if (org.isAlive()):
            if(  r < (org.getRadius() + self.radius) ):
                #Put it OUTSIDE the organelle
                #get angle that atp is at wrt cell
                y = self.y - cy;
                x = self.x - cx;

                scale_fact = (org.getRadius() + self.radius + 3) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.x = cx + x;
                self.y = cy + y;

    def isAtpFull(self):
        if (len(self.atp) >= self.numreq_atp):
            return True;
        else:
            return False;

    def brownian(self):
        if(not self.latch):
            if(self.memb):
                if(self.type == [0,0] or self.type == [0,1] or self.type == [0,2] or self.type == [1,2]):
                    cx = self.cell.getX();
                    cy = self.cell.getY();

                    rx =  self.x - cx;
                    ry = self.y - cy;

                    ang = math.atan2(ry,rx);

                    r = random.uniform(ang-1.5,ang+1.5);

                    self.dx = self.v_o * math.cos(r);
                    self.dy = self.v_o * math.sin(r);

                    self.x += self.dx
                    self.y += self.dy

        if(self.type == [0,2]):
            if (self.latch):
                self.px = self.x;
                self.py = self.y;

                if(self.looker == []):
                    r = self.cell.getRadius() + self.cell.getBact()[0].getRadius() + 150;
                    p = [];
                    for i in self.cell.getBact():
                        if(i.isAlive()):
                            if(i.getLatch()):
                                cr = self.dist(i.getX(),i.getY());
                                if(cr < r and cr != 0):
                                    r = cr;
                                    p = i;
                    if(p != []):
                        self.looker = p;

                if(self.looker != []):
                    if(self.isAtpFull()):
                        if(self.looker.isAlive()):

                            cx = self.looker.getX();
                            cy = self.looker.getY();

                            rx = cx - self.x;
                            ry = cy - self.y;

                            rad = rx**2 + ry**2;
                            rad = math.sqrt(rad);
                            if (rad > self.cell.getRadius() + self.cell.getBact()[0].getRadius() + 150):
                                self.looker = [];
                            else:
                                ang = math.atan2(ry,rx);

                                r = random.uniform(ang-1.5,ang+1.5);

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                        else:
                            self.looker = [];
                    else:
                        self.px = self.x;
                        self.py = self.y;

                        r = random.random();
                        r = r * math.pi * 2;

                        self.dx = self.v_o * math.cos(r);
                        self.dy = self.v_o * math.sin(r);

                        self.x += self.dx
                        self.y += self.dy

                else:
                    self.px = self.x;
                    self.py = self.y;

                    r = random.random();
                    r = r * math.pi * 2;

                    self.dx = self.v_o * math.cos(r);
                    self.dy = self.v_o * math.sin(r);

                    self.x += self.dx
                    self.y += self.dy

        #put some stuff here about the signalling and bacteria
        #Once bacteria is implemented
        if(self.type == [1,0]):
            self.px = self.x;
            self.py = self.y;

            if(self.looker == []):
                r = 150;
                p = [];
                for i in self.cell.getProt():
                    if(i.isAlive()):
                        if(i.getType() == [-2,0] or i.getType() == [-2,1] or i.getType() == [-2,2]):
                            cr = self.dist(i.getX(),i.getY());
                            if(cr < r and cr != 0):
                                r = cr;
                                p = i;
                if(p != []):
                    self.looker = p;

            if(self.looker != []):
                if(self.isAtpFull()):
                    if(self.looker.isAlive()):
                        cx = self.looker.getX();
                        cy = self.looker.getY();

                        rx = cx - self.x;
                        ry = cy - self.y;

                        ang = math.atan2(ry,rx);

                        r = random.uniform(ang-1.5,ang+1.5);

                        self.dx = self.v_o * math.cos(r);
                        self.dy = self.v_o * math.sin(r);

                        self.x += self.dx
                        self.y += self.dy
                    else:
                        self.looker = [];
                else:
                    self.px = self.x;
                    self.py = self.y;

                    r = random.random();
                    r = r * math.pi * 2;

                    self.dx = self.v_o * math.cos(r);
                    self.dy = self.v_o * math.sin(r);

                    self.x += self.dx
                    self.y += self.dy

            else:
                self.px = self.x;
                self.py = self.y;

                r = random.random();
                r = r * math.pi * 2;

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy

        if(self.type == [1,1]):
            self.px = self.x;
            self.py = self.y;

            if(self.looker == []):
                r = 150;
                p = [];
                for i in self.cell.getRna():
                    if(i.notInEndo()):
                        if(i.isAlive()):
                            cr = self.dist(i.getXf(),i.getYf());
                            if(cr < r and cr != 0):
                                r = cr;
                                p = i;
                if(p != []):
                    self.looker = p;

            if(self.looker != []):
                if(self.looker.isAlive()):
                    if(self.isAtpFull()):
                        if(self.looker.notInEndo()):
                            cx = self.looker.getXf();
                            cy = self.looker.getYf();

                            rx = cx - self.x;
                            ry = cy - self.y;

                            ang = math.atan2(ry,rx);

                            r = random.uniform(ang-1.5,ang+1.5);

                            self.dx = self.v_o * math.cos(r);
                            self.dy = self.v_o * math.sin(r);

                            self.x += self.dx
                            self.y += self.dy
                        else:
                            self.px = self.x;
                            self.py = self.y;

                            r = random.random();
                            r = r * math.pi * 2;

                            self.dx = self.v_o * math.cos(r);
                            self.dy = self.v_o * math.sin(r);

                            self.x += self.dx
                            self.y += self.dy
                    else:
                        self.px = self.x;
                        self.py = self.y;

                        r = random.random();
                        r = r * math.pi * 2;

                        self.dx = self.v_o * math.cos(r);
                        self.dy = self.v_o * math.sin(r);

                        self.x += self.dx
                        self.y += self.dy
                else:
                    self.looker = [];

            if(self.type == [2,0]):
                self.px = self.x;
                self.py = self.y;

                if(self.looker == []):
                    r = 150;
                    p = [];
                    for i in self.cell.getRna():
                        if(i.notInEndo()):
                            if(i.isAlive()):
                                if(i.getType() == [-2,0]):
                                    cr = self.dist(i.getXf(),i.getYf());
                                    if(cr < r and cr != 0):
                                        r = cr;
                                        p = i;
                    if(p != []):
                        self.looker = p;

                if(self.looker != []):
                    if(self.looker.isAlive()):
                        if(self.isAtpFull()):
                            if(self.looker.notInEndo()):
                                cx = self.looker.getXf();
                                cy = self.looker.getYf();

                                rx = cx - self.x;
                                ry = cy - self.y;

                                ang = math.atan2(ry,rx);

                                r = random.uniform(ang-1.5,ang+1.5);

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                            else:
                                self.px = self.x;
                                self.py = self.y;

                                r = random.random();
                                r = r * math.pi * 2;

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                        else:
                            self.px = self.x;
                            self.py = self.y;

                            r = random.random();
                            r = r * math.pi * 2;

                            self.dx = self.v_o * math.cos(r);
                            self.dy = self.v_o * math.sin(r);

                            self.x += self.dx
                            self.y += self.dy
                    else:
                        self.looker = [];
            else:
                self.px = self.x;
                self.py = self.y;

                r = random.random();
                r = r * math.pi * 2;

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy

            if(self.type == [2,1]):
                self.px = self.x;
                self.py = self.y;

                if(self.looker == []):
                    r = 150;
                    p = [];
                    for i in self.cell.getRna():
                        if(i.notInEndo()):
                            if(i.isAlive()):
                                if(i.getType() == [-2,1]):
                                    cr = self.dist(i.getXf(),i.getYf());
                                    if(cr < r and cr != 0):
                                        r = cr;
                                        p = i;
                    if(p != []):
                        self.looker = p;

                if(self.looker != []):
                    if(self.looker.isAlive()):
                        if(self.isAtpFull()):
                            if(self.looker.notInEndo()):
                                cx = self.looker.getXf();
                                cy = self.looker.getYf();

                                rx = cx - self.x;
                                ry = cy - self.y;

                                ang = math.atan2(ry,rx);

                                r = random.uniform(ang-1.5,ang+1.5);

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                            else:
                                self.px = self.x;
                                self.py = self.y;

                                r = random.random();
                                r = r * math.pi * 2;

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                        else:
                            self.px = self.x;
                            self.py = self.y;

                            r = random.random();
                            r = r * math.pi * 2;

                            self.dx = self.v_o * math.cos(r);
                            self.dy = self.v_o * math.sin(r);

                            self.x += self.dx
                            self.y += self.dy
                    else:
                        self.looker = [];
            else:
                self.px = self.x;
                self.py = self.y;

                r = random.random();
                r = r * math.pi * 2;

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy

            if(self.type == [2,2]):
                self.px = self.x;
                self.py = self.y;

                if(self.looker == []):
                    r = 150;
                    p = [];
                    for i in self.cell.getRna():
                        if(i.notInEndo()):
                            if(i.isAlive()):
                                if(i.getType() == [-2,2]):
                                    cr = self.dist(i.getXf(),i.getYf());
                                    if(cr < r and cr != 0):
                                        r = cr;
                                        p = i;
                    if(p != []):
                        self.looker = p;

                if(self.looker != []):
                    if(self.looker.isAlive()):
                        if(self.isAtpFull()):
                            if(self.looker.notInEndo()):
                                cx = self.looker.getXf();
                                cy = self.looker.getYf();

                                rx = cx - self.x;
                                ry = cy - self.y;

                                ang = math.atan2(ry,rx);

                                r = random.uniform(ang-1.5,ang+1.5);

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                            else:
                                self.px = self.x;
                                self.py = self.y;

                                r = random.random();
                                r = r * math.pi * 2;

                                self.dx = self.v_o * math.cos(r);
                                self.dy = self.v_o * math.sin(r);

                                self.x += self.dx
                                self.y += self.dy
                        else:
                            self.px = self.x;
                            self.py = self.y;

                            r = random.random();
                            r = r * math.pi * 2;

                            self.dx = self.v_o * math.cos(r);
                            self.dy = self.v_o * math.sin(r);

                            self.x += self.dx
                            self.y += self.dy
                    else:
                        self.looker = [];
            else:
                self.px = self.x;
                self.py = self.y;

                r = random.random();
                r = r * math.pi * 2;

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy

        if(self.type == [-2,0] or self.type == [-2,1] or self.type == [-2,2]):
            self.numreq_atp = 0;
            self.px = self.x;
            self.py = self.y;

            if(self.looker == []):
                r = 150;
                p = [];
                i = self.cell.getNuc();
                if(i.isAlive()):
                    cr = self.dist(i.getX(),i.getY());
                    if(cr < r and cr != 0):
                        r = cr;
                        p = i;
                if(p != []):
                    self.looker = p;

            if(self.looker != []):
                if(self.looker.isAlive()):
                    if(self.isAtpFull()):
                        cx = self.looker.getX();
                        cy = self.looker.getY();

                        rx = cx - self.x;
                        ry = cy - self.y;

                        ang = math.atan2(ry,rx);

                        r = random.uniform(ang-1.5,ang+1.5);

                        self.dx = self.v_o * math.cos(r);
                        self.dy = self.v_o * math.sin(r);

                        self.x += self.dx
                        self.y += self.dy
                    else:
                        self.px = self.x;
                        self.py = self.y;

                        r = random.random();
                        r = r * math.pi * 2;

                        self.dx = self.v_o * math.cos(r);
                        self.dy = self.v_o * math.sin(r);

                        self.x += self.dx
                        self.y += self.dy
                else:
                    self.looker = [];
                    self.px = self.x;
                    self.py = self.y;

                    r = random.random();
                    r = r * math.pi * 2;

                    self.dx = self.v_o * math.cos(r);
                    self.dy = self.v_o * math.sin(r);

                    self.x += self.dx
                    self.y += self.dy
            else:
                self.looker = [];
                self.px = self.x;
                self.py = self.y;

                r = random.random();
                r = r * math.pi * 2;

                self.dx = self.v_o * math.cos(r);
                self.dy = self.v_o * math.sin(r);

                self.x += self.dx
                self.y += self.dy
        else:
            self.px = self.x;
            self.py = self.y;

            r = random.random();
            r = r * math.pi * 2;

            self.dx = self.v_o * math.cos(r);
            self.dy = self.v_o * math.sin(r);

            self.x += self.dx
            self.y += self.dy




    def update(self,t):
        if(self.visible):
            self.brownian();
            self.checkAllFull();
            self.checkSelf();
            self.checkEvil(t);
            if(self.memb):
                if (not self.latch):
                    self.checkLatch();
                if (self.latch):
                    self.keepLatch();

            if(not self.latch):
                self.checkSelf();

            self.doJob(t);
            self.makePoint();
            self.checkbounds();
            self.draw();

class Explosion(Circle):

    def __init__(self):
        self.screen = [];
        self.width = 1;
        self.height = 1;
        self.radius = 1;
        self.circle = False;
        self.x = 0;
        self.y = 0;
        self.px = 0;
        self.py = 0;
        self.dx = 0;
        self.dy = 0;
        self.ddx = 0;
        self.ddy = 0;
        self.vel = 0;
        self.acc = 0;
        self.velAngle = 0;
        self.accAngle = 0;
        self.m = 1;
        self.energy = 0;
        self.visible = False;
        self.boundType = 0;
        self.color = (0,0,0);
        self.prot = [];
        self.cell = [];
        self.splodin = False;
        self.initTime = 0;
        self.maxR = 250;
        self.dr = 10;

    def setProt(self,p):
        self.prot = p;
    def getProt(self):
        return self.prot;
    def setCell(self,c):
        self.cell = c;
    def getCell(self):
        return self.cell

    def setMaxR(self,r):
        self.maxR = r;
    def setDr(self,r):
        self.dr = r;

    def explode(self,t):
        self.splodin = True;
        self.visible = True;
        self.initTime = t;
        self.radius = 0;
        self.setPosition(self.prot.getX(),self.prot.getY());

    def stillSplodin(self):
        if (self.splodin):
            self.radius += self.dr;
            self.closeToBact();
            if (self.radius > self.maxR):
                #No longer sploding
                self.splodin = False;
                self.visible = False;
                self.initTime = 0;
                self.radius = 0;
                self.x = -2000;


    def closeToBact(self):
        for i in self.cell.getBact():
            if i.isAlive():
                cx = i.getX();
                cy = i.getY();

                r = (cx - self.x) ** 2 + (cy - self.y) ** 2;
                r = math.sqrt(r);

                if (r < self.radius + 50):
                    i.destroy();
                    self.cell.incBactKill();
        #Destroy any bacteria within the radius


    def setColor(self,c):
        self.color = c;

    def setDim(self,r):
        self.width = 2*r;
        self.height = 2*r;
        self.radius = r;
        self.circle = True;

    def getRadius(self):
        return self.radius;

    def draw(self):
        if(self.visible):
            pygame.draw.circle(self.screen,self.color,(int(self.x),int(self.y)),self.radius)

    def update(self):
        if (self.visible):
            self.stillSplodin();
            self.draw();

class Rect:

    def __init__(self):
        self.x = 0;
        self.y = 0;
        self.wid = 0;
        self.hei = 0;
        self.fill = True;
        self.color = [0,0,0];
        self.screen = [];
        self.visible = False;

    def initialize(self,x,y,w,h,f,c,s,v):
        self.setPos(x,y);
        self.setDim(w,h);
        self.setFill(f);
        self.setColor(c);
        self.setScreen(s);
        self.setVisible(v);

    def printProp(self):
        print(self.x,self.y);
        print(self.wid,self.hei);
        print(self.fill,self.color);
        print(self.visible);

    def setPos(self,x,y):
        self.x = x;
        self.y = y;

    def setDim(self,w,h):
        self.wid = w;
        self.hei = h;

    def setFill(self,f):
        self.fill = f;

    def fill(self):
        self.fill = False;

    def empty(self):
        self.fill = True;

    def setColor(self, c ):
        self.color = c;

    def setScreen(self,screen):
        self.screen = screen;

    def setVisible(self,v):
        self.visible = v;

    def draw(self):
        if (self.visible):
            pygame.draw.rect(self.screen, self.color, [self.x - self.wid / 2, self.y - self.hei / 2, self.wid, self.hei], self.fill)

class Arc(Rect):

    def __init__(self):
        self.x = 0;
        self.y = 0;
        self.wid = 0;
        self.hei = 0;
        self.r = 0;
        self.fill = True;
        self.color = [0,0,0];
        self.screen = [];
        self.visible = False;
        self.startRad = 0;
        self.arcRad = 0; #Radians
        self.lineWidth = 4;

    def setRad(self,s,r):
        self.startRad = s;
        self.arcRad = r;

    def setLineWidth(self,w):
        self.lineWidth = w;

    def draw(self):
        if(self.visible):
            pygame.draw.arc(self.screen, self.color, [self.x - self.wid / 2, self.y - self.hei / 2, self.wid, self.hei],self.startRad,self.startRad+self.arcRad,self.lineWidth);



class Line:

    def __init__(self):
        self.xo = 0;
        self.yo = 0;
        self.xf = 0;
        self.yf = 0;
        self.dx = 0;
        self.dy = 0;
        self.width = 1;
        self.leng = 0;
        self.ang = 0;
        self.boundType = 0;
        self.fill = True;
        self.color = [0,0,0];
        self.screen = [];
        self.visible = False;

        self.rborder = 800;
        self.lborder = 0;
        self.uborder = 0;
        self.bborder = 800;

    def initialize(self,x,y,xf,yf,vx,vy,c,s,v):
        self.setInitPos(x,y);
        self.setFinPos(xf,yf);
        self.setvel(vx,vy);
        self.setColor(c);
        self.setScreen(s);
        self.setVisible(v);

    def printProp(self):
        print(self.xo,self.yo);
        print(self.xf,self.yf);
        print(self.fill,self.color);
        print(self.visible);

    def setBoundType(self,bt):
        self.boundType = bt;

    def setLeng(self,l):
        self.leng = l;

    def setWidth(self,w):
        self.width = w;

    def setInitPos(self,x,y):
        self.xo = x;
        self.yo = y;
    def setPosition(self,x,y):
        self.xo = x;
        self.yo = y;
    def setXo(self,a):
        self.xo = a;
    def setXf(self,a):
        self.xf = a;
    def setYo(self,a):
        self.yo = a;
    def setYf(self,a):
        self.yf = a;
    def getXo(self):
        return self.xo;
    def getXf(self):
        return self.xf;
    def getYo(self):
        return self.yo;
    def getYf(self):
        return self.yf;

    def calcPos(self):
        self.xf = self.xo + self.leng * math.cos(self.ang);
        self.yf = self.yo + self.leng * math.sin(self.ang);

    def dpos(self,ex,ey):
        self.xo += ex;
        self.xf += ex;
        self.yo += ey;
        self.yf += ey;

    def setFinPos(self,x,y):
        self.xf = x;
        self.yf = y;

    def setAng(self,a):
        self.ang = a;

    def calcAng(self):
        self.ang = math.atan2(self.yf-self.yo,self.xf-self.xo);

    def setVel(self,vel):
        self.calcAng();
        vx = vel * math.cos(self.ang);
        vy = vel * math.sin(self.ang);
        self.dx = vx;
        self.dy = vy;

    def setColor(self, c ):
        self.color = c;

    def setScreen(self,screen):
        self.screen = screen;

    def setVisible(self,v):
        self.visible = v;

    def kill(self):
        self.visible = False;
    def birth(self):
        self.visible = True;
    def getVisible(self):
        return self.visible;
    def isAlive(self):
        return self.visible;

    def move(self):
        self.xo += self.dx
        self.yo += self.dy
        self.xf += self.dx
        self.yf += self.dy

    def checkBounds(self):
        #Only Bounce
        r = False;
        l = False;
        t = False;
        b = False;


        if(self.xf > self.rborder):
            r = True;
        if(self.xf < self.lborder):
            l = True;
        if(self.yf < self.uborder):
            t = True;
        if(self.yf > self.bborder):
            b = True;

        if (self.boundType == 0):

            xo = self.xo;
            yo = self.yo;
            xf = self.xf;
            yf = self.yf;

            if(r):
                self.dx = -self.dx;
                self.xf = xo;
                self.xo = xf;
            if(l):
                self.dx = -self.dx;
                self.xf = xo;
                self.xo = xf;
            if(b):
                self.dy = -self.dy;
                self.yf = yo;
                self.yo = yf;
            if(t):
                self.dy = -self.dy;
                self.yf = yo;
                self.yo = yf;

    def setBorder(self,lborder,rborder,bborder,uborder):
        self.lborder = lborder;
        self.rborder = rborder;
        self.bborder = bborder;
        self.uborder = uborder;


    def update(self):
        self.checkBounds()
        self.move();
        self.draw();
    def draw(self):
        if (self.visible):
            pygame.draw.line(self.screen,self.color,(self.xo,self.yo),(self.xf,self.yf), self.width);

class Rna(Line):

    def __init__(self):
        self.xo = 0;
        self.yo = 0;
        self.xf = 0;
        self.yf = 0;
        self.dx = 0;
        self.dy = 0;
        self.width = 1;
        self.leng = 0;
        self.ang = 0;
        self.boundType = 0;
        self.fill = True;
        self.color = [0,0,0];
        self.screen = [];
        self.visible = False;
        self.v_o = 0;
        self.turn = 0;
        self.cell = [];

        self.rborder = 800;
        self.lborder = 0;
        self.uborder = 0;
        self.bborder = 800;
        self.type = [-1,-1];
        self.inEndo = False;
        self.vir = [];

    def setInEndo(self):
        self.inEndo = False;
    def setOutEndo(self):
        self.inEndo = False;
    def notInEndo(self):
        if (self.inEndo):
            return False;
        return True;
    def isInEndo(self):
        return self.inEndo;

    def setVir(self,v):
        self.vir = v;
    def unsetVir(self):
        self.vir = [];
    def getVir(self):
        return self.vir;

    def setType(self,t):
        self.type = t;
    def getType(self):
        return self.type;

    def setCell(self,c):
        self.cell =  c;

    def setTurn(self,t):
        self.turn = t;

    def setvo(self,v):
        self.v_o = v;

    def kill(self):
        self.vir =  [];
        self.type = [-1,-1];
        self.inEndo = False;
        self.visible = False;

    def brownian(self):
        if (self.type[0] != -2):
            self.calcAng();
            self.ang = self.ang + random.uniform(-self.turn,self.turn);
            self.xo = self.xo + (self.xf - self.xo) * self.v_o / self.leng;
            self.yo = self.yo + (self.yf - self.yo) * self.v_o / self.leng;
            self.calcPos();
        else:
            if (self.vir != []):
                if (self.getVir().getLatch == False):
                    self.calcAng();
                    self.ang = self.ang + random.uniform(-self.turn,self.turn);
                    self.xo = self.xo + (self.xf - self.xo) * self.v_o / self.leng;
                    self.yo = self.yo + (self.yf - self.yo) * self.v_o / self.leng;
                    self.calcPos();
                else:
                    #Shoot for place inside the cell
                    self.ang = self.ang + random.uniform(-self.turn,self.turn);
                    self.xo = self.xo + (self.xf - self.xo) * self.v_o / self.leng;
                    self.yo = self.yo + (self.yf - self.yo) * self.v_o / self.leng;
                    self.calcPos();
            else:
                #Just meander like  any other guy
                self.ang = self.ang + random.uniform(-self.turn,self.turn);
                self.xo = self.xo + (self.xf - self.xo) * self.v_o / self.leng;
                self.yo = self.yo + (self.yf - self.yo) * self.v_o / self.leng;
                self.calcPos();


    #Make sure it stays in the cell
    def checkCell(self):
        if (self.vir == []):
            cx = self.cell.getX();
            cy = self.cell.getY();

            r = math.sqrt( (cx - self.xf)**2 + (cy - self.yf)**2 );

            if(  r > (self.cell.getRadius() - 5) ):
                #Put it inside the cell
                #get angle that atp is at wrt cell
                y = self.yf - cy;
                x = self.xf - cx;

                scale_fact = (self.cell.getRadius() - 8) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.xo = cx + x;
                self.yo = cy + y;
                self.ang = self.ang + math.pi;
                self.calcPos();
        elif (self.vir.getLatch() == False):
            cx = self.vir.getX();
            cy = self.vir.getY();

            r = math.sqrt( (cx - self.xf)**2 + (cy - self.yf)**2 );

            if(  r > (self.vir.getRadius() / 1.25 - 5) ):
                #Put it inside the cell
                #get angle that atp is at wrt cell
                y = self.yf - cy;
                x = self.xf - cx;

                scale_fact = (self.vir.getRadius() / 1.25 - 8) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.xo = cx + x;
                self.yo = cy + y;
                self.ang = self.ang + math.pi;
                self.calcPos();

        else:

            #Check to see if it gets outside cell and virus first

            cx = self.vir.getX();
            cy = self.vir.getY();

            r = math.sqrt( (cx - self.xf)**2 + (cy - self.yf)**2 );

            if(  r > (self.vir.getRadius() * 1.75 - 5) ):
                #Put it inside the cell
                #get angle that atp is at wrt cell
                y = self.yf - cy;
                x = self.xf - cx;

                scale_fact = (self.vir.getRadius() * 1.75 - 8) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.xo = cx + x;
                self.yo = cy + y;
                self.ang = self.ang + math.pi;
                self.calcPos();

            #Send it to the  Cell!!!!

            cx = self.cell.getX();
            cy = self.cell.getY();

            vx = self.vir.getX();
            vy = self.vir.getY();

            r = math.sqrt( (cx - vx)**2 + (cy - vy)**2 );

            alfa = .33 * r;
            angy = math.atan2(vy-cy,vx-cx);

            nx = cx + alfa * math.cos(angy);
            ny = cy + alfa * math.sin(angy);

            #We have designated position - nx,ny
            #Now send Rna there

            self.ang = math.atan2(ny-self.yf,nx-self.xf);

            #Check if in cell
            bx = self.cell.getX();
            by = self.cell.getY();
            r_cell = math.sqrt( (bx-self.xf)**2 + (by - self.yf)**2 );

            if (r_cell < self.cell.getRadius() ):
                #Inside cell, remove all necessary things
                self.vir.remRna(self);
                self.vir = [];
                self.cell.addRna();




    def checkSelf(self):
        #Check Cell
        self.checkCell();
        self.checkOrganelle(self.cell.getNuc() );
        #self.checkOrganelle(self.cell.getEndo() );
        self.checkOrganelle(self.cell.getMito() );
        self.checkEndo();

    def checkEndo(self):
        cx = self.cell.getEndo().getX();
        cy = self.cell.getEndo().getY();
        r = math.sqrt( (cx - self.xf)**2 + (cy - self.yf)**2 );
        if(  r < (self.cell.getEndo().getRadius() + 3) ):
            self.cell.getEndo().rnaEnter(self);
            self.inEndo = True;


    def checkOrganelle(self,org):
        cx = org.getX();
        cy = org.getY();

        r = math.sqrt( (cx - self.xf)**2 + (cy - self.yf)**2 );

        if(org.isAlive()):
            if(  r < (org.getRadius() + 3) ):
                #Put it OUTSIDE the organelle
                #get angle that atp is at wrt cell
                y = self.yf - cy;
                x = self.xf - cx;

                scale_fact = (org.getRadius() + 10) / r;

                x *= scale_fact;
                y *= scale_fact;

                self.xo = cx + x;
                self.yo = cy + y;
                self.ang = self.ang  + math.pi;
                self.calcPos();

    def update(self):
        if(self.visible):
            if(not self.inEndo):
                if (self.vir == []):
                    self.brownian();
                    self.checkSelf();
                    self.checkBounds();
                    self.draw();
                else:
                    self.brownian()
                    self.checkCell();
                    self.draw();
