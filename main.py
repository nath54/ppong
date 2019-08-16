#coding:utf-8
import random,pygame,time
from pygame.locals import *

pygame.init()
mtx,mty=1280,1024
btex,btey=1000,800
io=pygame.display.Info()
atx,aty=io.current_w,io.current_h
tex,tey=int(atx/mtx*btex),int(aty/mty*btey)

fenetre=pygame.display.set_mode([tex,tey])

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)
def rxx(x): return float(x/btex*tex)
def ryy(y): return float(y/btey*tey)

font=pygame.font.SysFont("Arial",rx(20))
font2=pygame.font.SysFont("Arial",rx(30))
font3=pygame.font.SysFont("Arial",rx(40))
font4=pygame.font.SysFont("Arial",rx(60))

b1x=pygame.Rect(-10,-10,10,tey+20)
b2x=pygame.Rect(tex,-10,10,tey+20)
b1y=pygame.Rect(0,-10,tex,10)
b2y=pygame.Rect(0,tey,tex,10)

def chcl(cl):
    cl=list(cl)
    lim1,lim2=0,120
    cl[0]+=random.randint(-1,1)
    cl[1]+=random.randint(-1,1)
    cl[2]+=random.randint(-1,1)
    if cl[0]<lim1: cl[0]=lim1
    if cl[0]>lim2: cl[0]=lim2
    if cl[1]<lim1: cl[1]=lim1
    if cl[1]>lim2: cl[1]=lim2
    if cl[2]<lim1: cl[2]=lim1
    if cl[2]>lim2: cl[2]=lim2
    return tuple(cl)

class Mis:
    def __init__(self,x,y,pos,vitx):
        self.px=x
        self.py=y
        self.tx=rxx(10)
        self.ty=ryy(4)
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.pos=pos
        self.vitx=vitx
        self.dgts=33
        self.dbg=time.time()
        self.tbg=0.01
        self.destroy=False
    def update(self,bts):
        self.px+=self.vitx
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        for b in bts:
            if b!=self.pos and b.rect.colliderect(self.rect):
                b.vie-=self.dgts
                self.destroy=True
                

class Baton:
    def __init__(self,p,isbot):
        self.p=p
        self.tx=rxx(10)
        self.ty=ryy(100)
        if p==1: self.px=rxx(50)
        else: self.px=tex-rxx(50)-self.tx
        self.py=ryy(tey/2-self.ty/2)
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.vie_tot=100
        self.vie=self.vie_tot
        self.vity=0.
        self.vitmax=rxx(4)
        self.acc=rxx(0.5)
        self.decc=rxx(0.15)
        self.dbg=time.time()
        self.t=0.01
        self.dkup=time.time()
        self.dkdown=time.time()
        self.points=0
        self.bot=isbot
        self.tppbg=0
        self.dppbg=0
        self.dtir=time.time()
        self.ttir=1
    def bouger(self,aa,projs):
        if time.time()-self.dppbg>=self.tppbg:
            if aa=="Up":
                if time.time()-self.dkup>=self.t:
                    self.dkup=time.time()
                    self.vity-=self.acc
            elif aa=="Down":
                if time.time()-self.dkdown>=self.t:
                    self.dkdown=time.time()
                    self.vity+=self.acc
            elif aa=="Tir":
                if time.time()-self.dtir>=self.ttir:
                    self.dtir=time.time()
                    if self.p==1: vt=rxx(5)
                    else: vt=rxx(-5)
                    projs.append( Mis(self.px+self.tx,self.py+self.ty/2,self,vt) )
        return projs
            
    def update(self):
        if time.time()-self.dbg>=self.t:
            self.dbg=time.time()
            if self.vity > 0 and self.vity >= self.decc: self.vity-=self.decc
            elif self.vity > 0: self.vity=0
            if self.vity < 0 and self.vity <= -self.decc: self.vity+=self.decc
            elif self.vity < 0: self.vity=0
            self.py+=self.vity
            if self.py < 0: self.py,self.vity=0,0
            if self.py > tey-self.ty: self.py,self.vity=tey-self.ty,0
            self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)

v=6
vv=4
class Ball:
    def __init__(self):
        self.px=tex/2
        self.py=tey/2
        self.t=rxx(5)
        self.vitx=random.choice([rxx(-v),rxx(v)])
        self.vity=random.choice([rxx(-vv),rxx(vv)])
        self.dbg=time.time()
        self.tbg=0.01
        self.tppbg=3
        self.dppbg=time.time()
    def update(self,bts,clf):
        if time.time()-self.dppbg >= self.tppbg and time.time()-self.dbg>=self.tbg:
            self.dbg=time.time()
            self.px+=self.vitx
            self.py+=self.vity
            self.rect=pygame.Rect(int(self.px-self.t/2),int(self.py-self.t/2),int(self.t),int(self.t))
            cbt=False
            for b in bts:
                if self.rect.colliderect(b.rect): cbt=True
            if cbt:
                self.vitx=-self.vitx
                self.px+=self.vitx
                self.py+=self.vity
                for x in range(10): clf=chcl(clf)
            if self.rect.colliderect(b1y) or self.rect.colliderect(b2y):
                self.vity=-self.vity
                self.px+=self.vitx
                self.py+=self.vity
                for x in range(10): clf=chcl(clf)
            if self.rect.colliderect(b1x):
                self.px,self.py,bts[1].points,self.vity,self.vitx,self.dppbg,self.tppbg=tex/2,tey/2,bts[1].points+1,random.choice([rxx(-vv),rxx(vv)]),-self.vitx,time.time(),1
            if self.rect.colliderect(b2x):
                self.px,self.py,bts[0].points,self.vity,self.vitx,self.dppbg,self.tppbg=tex/2,tey/2,bts[0].points+1,random.choice([rxx(-vv),rxx(vv)]),-self.vitx,time.time(),1
        return clf

def aff_j(bts,ball,pause,fps,clf,projs):
    fenetre.fill(clf)
    for b in bts: b.rect=pygame.draw.rect(fenetre,(255,int(b.vie/b.vie_tot*255.),int(b.vie/b.vie_tot*255.)),(int(b.px),int(b.py),int(b.tx),int(b.ty)),0)
    for p in projs: p.rect=pygame.draw.rect(fenetre,(255-clf[0],255-clf[1],255-clf[2]),(p.px,p.py,p.tx,p.ty),0)
    ball.rect=pygame.draw.circle(fenetre,(255-clf[0],255-clf[1],255-clf[2]),(int(ball.px),int(ball.py)),int(ball.t),0)
    fenetre.blit( font2.render(str(bts[0].points),True,(250,250,250)) , [rx(150),ry(15)])
    fenetre.blit( font2.render(str(bts[1].points),True,(250,250,250)) , [rx(tex-150),ry(15)])
    fenetre.blit( font.render("fps : "+str(fps),True,(200,200,200)) , [rx(15),ry(15)])
    pygame.display.update()

def verif_keys(bt1,bt2,ball,projs):
    keys=pygame.key.get_pressed()
    if not bt2.bot:
        if keys[K_UP]: projs=bt2.bouger("Up",projs)
        if keys[K_DOWN]: projs=bt2.bouger("Down",projs)
        if keys[K_KP0]: projs=bt2.bouger("Tir",projs)
    elif ball.vitx > 0:
        if ball.py > bt2.py+bt2.ty/2: projs=bt2.bouger("Down",projs)
        if ball.py < bt2.py+bt2.ty/2: projs=bt2.bouger("Up",projs)
        if bt1.py+bt1.ty/2 >= bt2.py-bt2.ty and  bt1.py+bt1.ty/2 <= bt2.py+bt2.ty/2: projs=bt2.bouger("Tir",projs)
    if not bt1.bot:
        if keys[K_e]: projs=bt1.bouger("Up",projs)
        if keys[K_d]: projs=bt1.bouger("Down",projs)
        if keys[K_SPACE]: projs=bt1.bouger("Tir",projs)
    elif ball.vitx < 0:
        if ball.py > bt1.py+bt1.ty/2: projs=bt1.bouger("Down",projs)
        if ball.py < bt1.py+bt1.ty/2: projs=bt1.bouger("Up",projs)
        if bt2.py+bt2.ty/2 >= bt1.py-bt1.ty and  bt2.py+bt2.ty/2 <= bt1.py+bt1.ty/2: projs=bt1.bouger("Tir",projs)
    return bt1,bt2,projs

def main_j(b1b,b2b):
    ppg=20
    clf=(0,0,0)
    bt1=Baton(1,b1b)
    bt2=Baton(2,b2b)
    bts=[bt1,bt2]
    ball=Ball()
    projs=[]
    fps=0
    fini=False
    pause=False
    encour=True
    aff_j(bts,ball,pause,fps,clf,projs)
    while encour:
        t1=time.time()
        if not pause:
            b1t,bt2,projs=verif_keys(bt1,bt2,ball,projs)
            for p in projs:
                p.update(bts)
                if p.destroy and p in projs: del( projs[projs.index(p)] )
            for b in bts:
                if b.vie<0:
                    b.vie=b.vie_tot
                    b.tppbg=1
                    b.dppbg=time.time()
                b.update()
            clf=ball.update([bt1,bt2],clf)
        aff_j(bts,ball,pause,fps,clf,projs)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                elif event.key==K_p: pause=not pause
        if bt1.points>=ppg or bt2.points>=ppg: encour,fini=False,True
        tt=time.time()-t1
        if tt!=0: fps=int(1./tt)
    fenetre.fill((0,0,0))
    if bt1.points>=ppg: fenetre.blit( font2.render("player1 à gagné",True,(255,255,255)) , [rx(200),ry(100)])
    if bt2.points>=ppg: fenetre.blit( font2.render("player2 à gagné",True,(255,255,255)) , [rx(200),ry(100)])
    fenetre.blit( font2.render("Appuyez sur espace pour continuer",True,(255,255,255)) , [rx(200),ry(600)])
    pygame.display.update()
    while fini:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_SPACE: fini=False

def main():
    b1r=pygame.Rect(rx(400),ry(500),rx(200),ry(100))
    b2r=pygame.Rect(rx(150),ry(200),rx(100),ry(50))
    b3r=pygame.Rect(rx(700),ry(200),rx(100),ry(50))
    b4r=pygame.Rect(rx(450),ry(650),rx(100),ry(50))
    pxp,pyp=rx(450),ry(50)
    txp,typ=rx(180),ry(65)
    vitxp,vityp=random.choice([rxx(-3),rxx(3)]),random.choice([ryy(-3),ryy(3)])
    pr=pygame.Rect(pxp,pyp,txp,typ)
    val=10
    dbgp=time.time()
    tbgp=0.01
    p1b,p2b=False,False
    encour=True
    while encour:
        #pos
        pos=pygame.mouse.get_pos()
        #animation
        if time.time()-dbgp >= tbgp:
            dbgp=time.time()
            pr=pygame.Rect(pxp,pyp,txp,typ)
            prhaut=pygame.Rect(pxp+rx(val),pyp,txp-rx(val*2),ry(val))
            prbas=pygame.Rect(pxp+rx(val),pyp+typ-ry(val),txp-rx(val*2),ry(val))
            prgauche=pygame.Rect(pxp,pyp+ry(val),rx(val),pyp-ry(val*2))
            prdroite=pygame.Rect(pxp+txp-rx(val),pyp+ry(val),rx(val),typ-ry(val*2))
            if pr.colliderect(b1x) or pr.colliderect(b2x): vitxp=-vitxp
            if pr.colliderect(b1y) or pr.colliderect(b2y): vityp=-vityp
            if prhaut.colliderect(b1r) or prhaut.colliderect(b2r) or prhaut.colliderect(b3r) or prhaut.colliderect(b4r) or prbas.colliderect(b1r) or prbas.colliderect(b2r) or prbas.colliderect(b3r) or prbas.colliderect(b4r): vityp=-vityp
            if prgauche.colliderect(b1r) or prgauche.colliderect(b2r) or prgauche.colliderect(b3r) or prgauche.colliderect(b4r) or prdroite.colliderect(b1r) or prdroite.colliderect(b2r) or prdroite.colliderect(b3r) or prdroite.colliderect(b4r): vitxp=-vitxp
            pxp+=vitxp
            pyp+=vityp
        #aff
        fenetre.fill((10,10,10))
        pygame.draw.rect(fenetre,(255,255,255),(tex/2-rx(5),0,rx(10),tey),0)
        fenetre.blit( font4.render("Ppong",True,(150,150,150)) , [pxp,pyp])
        #b1
        if b1r.collidepoint(pos): cl1,cl2=(255,255,255),(0,0,0)
        else: cl1,cl2=(0,0,0),(255,255,255)
        pygame.draw.rect(fenetre,cl1,b1r,0)
        pygame.draw.rect(fenetre,cl2,b1r,rx(2))
        fenetre.blit( font3.render("Jouer",True,cl2) , [rx(430),ry(520)])
        #b2
        if b2r.collidepoint(pos): cl1,cl2=(255,255,255),(0,0,0)
        else: cl1,cl2=(0,0,0),(255,255,255)
        if p1b: txt="bot"
        else: txt="humain"
        pygame.draw.rect(fenetre,cl1,b2r,0)
        pygame.draw.rect(fenetre,cl2,b2r,rx(2))
        fenetre.blit( font.render(txt,True,cl2) , [rx(160),ry(210)])
        fenetre.blit( font.render("haut : e",True,(255,255,255)) , [rx(150),ry(300)])
        fenetre.blit( font.render("bas : d",True,(255,255,255)) , [rx(150),ry(340)])
        fenetre.blit( font.render("tir : espace",True,(255,255,255)) , [rx(150),ry(380)])
        #b3
        if b3r.collidepoint(pos): cl1,cl2=(255,255,255),(0,0,0)
        else: cl1,cl2=(0,0,0),(255,255,255)
        if p2b: txt="bot"
        else: txt="humain"
        pygame.draw.rect(fenetre,cl1,b3r,0)
        pygame.draw.rect(fenetre,cl2,b3r,rx(2))
        fenetre.blit( font.render(txt,True,cl2) , [rx(710),ry(210)])
        fenetre.blit( font.render("haut : fleche haut",True,(255,255,255)) , [rx(700),ry(300)])
        fenetre.blit( font.render("bas : fleche bas",True,(255,255,255)) , [rx(700),ry(340)])
        fenetre.blit( font.render("tir : NUM0",True,(255,255,255)) , [rx(700),ry(380)])
        #b4
        if b4r.collidepoint(pos): cl1,cl2=(255,255,255),(0,0,0)
        else: cl1,cl2=(0,0,0),(255,255,255)
        pygame.draw.rect(fenetre,cl1,b4r,0)
        pygame.draw.rect(fenetre,cl2,b4r,rx(2))
        fenetre.blit( font.render("quitter",True,cl2) , [rx(460),ry(660)])
        #update
        pygame.display.update()
        #events
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key==K_ESCAPE: encour=False
            elif event.type==MOUSEBUTTONUP:
                if b1r.collidepoint(pos): main_j(p1b,p2b)
                elif b2r.collidepoint(pos): p1b=not p1b
                elif b3r.collidepoint(pos): p2b=not p2b
                elif b4r.collidepoint(pos): exit()
                
main()
                



