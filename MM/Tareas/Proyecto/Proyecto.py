import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy import constants as const
from astropy import units as unit
import scipy.optimize
import warnings

warnings.filterwarnings('ignore')
dark_matter=pd.read_csv(sys.argv[1])
d_m=dark_matter.values
gas=pd.read_csv(sys.argv[2])
g=gas.values

def Fun(delta):
    #Calculos para las masas
    dist=np.sqrt((d_m**2).sum(axis=1))
    rad=np.arange(0+delta,4+delta,delta)
    Bin=[]
    j=0
    for i in rad:
        Bin.append((dist<i).sum())
        j=j+1
    mass=d_m[0,3]*np.array(Bin)

    #Calculos para la velocidad
    norm=np.sqrt((g[:,0:2]**2).sum(axis=1))
    vecs=np.concatenate((([-g[:,1]]/norm).T,([g[:,0]]/norm).T),axis=1)
    vel_t=np.sum(vecs*g[:,3:5],axis=1)
    V=np.concatenate((np.array([norm]).T,np.array([vel_t]).T,np.array([g[:,6]]).T),axis=1)
    vel_prom=[]
    for i in rad:
        A,B,C=np.extract(V[:,0]<=i,V[:,0]),np.extract(V[:,0]<=i,V[:,1]),np.extract(V[:,0]<=i,V[:,2])
        D,E=np.extract(A>i-delta,B),np.extract(A>i-delta,C)
        vel_prom.append(np.average(D,weights=E))
    r=rad*unit.kpc
    M=(mass*1e10)*const.M_sun
    v_circ=np.sqrt((const.G*M)/r)
    v_circ=v_circ.to(unit.km/unit.s)
    vel_prom=np.array(vel_prom)*(unit.km/unit.s)
    
    #Calculos para la densidad
    def Rho(mass,rad):
        slope=[mass[0]/rad[0]]
        for i in range(1,mass.shape[0]):
            slope.append((mass[i]-mass[i-1])/(rad[i]-rad[i-1]))
        Slope=np.array(slope)*(unit.M_sun/unit.kpc)
        rho=(Slope/(4*np.pi*((rad*unit.kpc)**2))).to(unit.M_sun/unit.pc**3)
        return rho
    rho=Rho(mass,rad)*1e10
    Mass=(((vel_prom**2)*r)/const.G).to(unit.M_sun)
    rho1=Rho(Mass.value,rad)
    
    #Calculos para alfa
    def Optimize(arr,brr,i):
        p0 = [np.log10(arr)[i],np.log10(brr)[i]]
        errfunc         = lambda p: np.ravel(p[0]*np.log10(arr[i+1:])+p[1]-np.log10(brr[i+1:]))
        fitparams       = scipy.optimize.leastsq(errfunc,p0,full_output=1)[0]
        fitparams       = list(fitparams)
        return fitparams[0],fitparams[1]
    
    if delta==0.05:
        j=5
    if delta==0.1:
        j=3
    if delta==0.2:
        j=2
    if delta==0.4:
        j=1        
    m1,b1=Optimize(rad,rho.value,j)
    m2,b2=Optimize(rad,rho1.value,j)
    
    
    #Plots
    plt.figure(1,figsize=(16,12), dpi=80)
    def Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter):
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data',spine_b))
        ax.yaxis.set_ticks_position('left')
        if c==0:
            ax.spines['left'].set_position(('data',spine_l))
        ax.set_title(Title,fontsize=20)
        ax.set_xlabel(xlabel, labelpad=5,fontsize=15)
        ax.set_ylabel(ylabel, labelpad=5,fontsize=15)
        if xmin>=0:
            plt.xlim(xmin,xmax)
            plt.ylim(ymin,ymax)
        plt.grid(True)
        if scatter==1:
            if Leg==0:
                return plt.scatter(X,Y)
            else:
                return plt.scatter(X,Y,label=Leg), ax.legend(loc=Leg_loc)
        else:
            if Leg==1:
                return plt.plot(X,Y) 
            else:
                return plt.plot(X,Y,label=Leg), ax.legend(loc=Leg_loc)
            
    ##Plot de Masa
    plt.subplot(221)
    c,spine_b,spine_l,Title,xlabel,ylabel=0,0,0,'M(<R)','Radio [kpc] ($\Delta$='+str(delta)+')','Masa [$1x10^{10} M_\odot$]'
    xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter=0,rad.max()+0.025,0,mass.max()+(mass.max()/10),rad,mass,0,0,1
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    
    #Plot de velocidad
    plt.subplot(222)
    c,spine_b,spine_l,Title,xlabel,ylabel=0,0,0,'Curva de rotación','$R$ [kpc] ($\Delta$='+str(delta)+')','$V_{circ}(R)$ [km/s]'
    xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter=0,rad.max()+0.025,0,vel_prom.value.max()+(vel_prom.value.max()/10),rad,vel_prom,'Valor experimental',7,1
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    Y,Leg=v_circ,'Valor teórico'
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    
    #Plot de densidad
    plt.subplot(223)
    c,spine_b,spine_l,Title,xlabel,ylabel=1,-2.4,0,'Perfil de densidad','$\log(R)$ [kpc] ($\Delta$='+str(delta)+')',r'$\log(\rho) [M_\odot /pc^3]$'
    xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter=-1,0,-2.4,0,np.log10(rad),np.log10(rho.value),'Densidad teórica',1,1
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    Y,Leg=np.log10(rho1.value),'Densidad experimental'
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)

    #Plot de ajuste
    plt.subplot(224)
    c,spine_b,spine_l,Title,xlabel,ylabel=1,-2.4,0,'Ajuste lineal del perfil de densidad','$\log(R)$ [kpc] ($\Delta$='+str(delta)+')',r'$\log(\rho) [M_\odot /pc^3]$'
    xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter=-1,0,-2,-0.5,np.log10(rad),np.log10(rho.value),'Densidad teórica',1,1
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    Y,Leg=np.log10(rho1.value),'Densidad experimental'
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    X,Y,Leg,scatter=np.log10(rad)[3:],m1*X[3:]+b1,'Ajuste teórico',0
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)
    Y,Leg,scatter=m2*X+b2,'Ajuste experimental',0
    Plot(c,spine_b,spine_l,Title,xlabel,ylabel,xmin,xmax,ymin,ymax,X,Y,Leg,Leg_loc,scatter)    
    
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.20)
    plt.savefig('SNAPSHOTS/'+sys.argv[3]+'/Plot_delta_'+str(delta)+'.jpg')
    plt.clf()
    return m1,m2
A=np.array([['Experimental','Teórico']]).T
for i in [0.05,0.1,0.2,0.4]:
    m1,m2=Fun(i)
    B=np.array([[m2,m1]]).T
    A=np.concatenate((A,B),axis=1)
column=['Delta','0.05','0.1','0.2','0.4']
tab=pd.DataFrame(A,columns=column)
tab.to_csv('SNAPSHOTS/'+sys.argv[3]+'/Alfa.csv',columns=column,index=False)