#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load Modules:{{{
import os,subprocess
import argparse,textwrap
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import scipy
from itertools import product, combinations
# Sympy:
from sympy import *
import sympy as sp
from sympy.functions.special.error_functions import *
#from sympy import lambdify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
# ipyvolume
import ipyvolume as ipv
import numpy as np
import ipyvolume.embed as embed
import ipyvolume.pylab as p3
from ipywidgets import jslink, VBox
# }}}

# Control:{{{
TESTING = False
def run_cmd(cmd, testing=TESTING):
    """Execute command-line command."""
    if testing:
        print('>>', cmd)
    else:
        subprocess.Popen(cmd, shell=True)
#}}}

# class Plot:{{{

class Plot(object):

    def __init__(self,axis_labels=["x","y","z"],xlim=[-10,10],ylim=[-10,10],zlim=[None,None]):
        var = 'x,y,z'
        x,y,z = sp.symbols(var)
        self.axis_labels = axis_labels
        self.xlim,self.ylim,self.zlim = xlim,ylim,zlim
        integrate = sp.integrate

    def plot_expr(self, Fn, outPath):


        ipv.figure(width=500, height=500, lighting=True, controls=True)
        Fns = [i for i in Fn.split(";")]
        for Fn in Fns:
            f = parse_expr(Fn)
            f_ = f.as_expr()
            latex = sp.latex(f)
            # Generate combnations of x,y,z and pick the correct variables given
            #.. the user input.
            _symbols = sp.symbols('x,y,z')
            for var1,var2 in combinations(_symbols,2):
                func = lambdify([_symbols[0],_symbols[1]], f_, modules=['numpy', 'scipy',
                    {'erf': scipy.special.erf}])
                if (str(var1) and str(var2)) in Fn:
                    func = lambdify([var1,var2], f_, modules=['numpy', 'scipy',
                        {'erf': scipy.special.erf}])
                    break
            X,Y = np.linspace(self.xlim[0], self.xlim[1]),np.linspace(self.ylim[0], self.ylim[1])
            xplot,yplot = np.meshgrid(X,Y)

            #zplot1 = float(100/n)*func(xplot, yplot) # 100/n is a normalization const.
            zplot1 = func(xplot, yplot) # 100/n is a normalization const.

            # only x is a sequence of arrays
            x,y,z = xplot, yplot, zplot1
            #TODO: marker control
            #s = ipv.scatter(x, y, z, marker='sphere', size=10)
            #p3.clear()
            #ipv.pylab.volshow(np.array([x,y,z]), lighting=False, data_min=None,
            #    data_max=None, max_shape=256, tf=None, stereo=False,
            #    ambient_coefficient=0.5, diffuse_coefficient=0.8,
            #    specular_coefficient=0.5, specular_exponent=5, downscale=1,
            #    level=[0.1, 0.5, 0.9], opacity=[0.01, 0.05, 0.1], level_width=0.1,
            #    controls=True, max_opacity=0.2, memorder='C', extent=None)
            ipv.plot_surface(x,y,z, color="orange")
            ipv.plot_wireframe(x,y,z, color="red")
            del X,Y,xplot,yplot,zplot1

        ipv.pylab.xlim(self.xlim[0],self.xlim[1])
        ipv.pylab.ylim(self.ylim[0],self.ylim[1])
        if self.zlim != [None,None]:
            ipv.pylab.zlim(self.zlim[0],self.zlim[1])
        ipv.style.use(['seaborn-darkgrid', {'axes.x.color':'orange'}])
        ipv.pylab.view(azimuth=-45, elevation=25, distance=4)
        ipv.pylab.xyzlabel(labelx=self.axis_labels[0],
                labely=self.axis_labels[1],labelz=self.axis_labels[2])
        ipv.pylab.save("%s.html"%outPath,title=r"%s"%(latex), offline=None,
                template_options=(('extra_script_head', ''),
                    ('body_pre', ''), ('body_post', '')))
        #ipv.xyzlim(self.xlim, ylim)
        #hbox = p3.current.container#VBox([p3.current.container, ipv.figure()])
        #embed.embed_html("%s.html"%outPath, hbox, offline=True, devmode=False)


    def plot_data(self, data, outPath="3-D_figure", marker='sphere',size=2,inline=False):


        ipv.figure(width=400, height=500, lighting=True, controls=True)
        #x,y,z = data[0],data[1],data[2]
        #TODO: marker control
        ipv.quickscatter(data[0], data[1], data[2], marker=marker, size=size)#, size=10)
        #ipv.plot_surface(data[0], data[1], data[2], color="orange")
        #ipv.plot_wireframe(data[0], data[1], data[2], color="red")

        ipv.pylab.xlim(self.xlim[0],self.xlim[1])
        ipv.pylab.ylim(self.ylim[0],self.ylim[1])
        if self.zlim != [None,None]:
            ipv.pylab.zlim(self.zlim[0],self.zlim[1])
        ipv.style.use(['seaborn-darkgrid', {'axes.x.color':'orange'}])
        ipv.pylab.view(azimuth=-45, elevation=25, distance=5)
        ipv.pylab.xlabel("%s"%self.axis_labels[0])
        ipv.pylab.ylabel("%s"%self.axis_labels[1])
        ipv.pylab.zlabel("%s"%self.axis_labels[2])
        if inline:
            ipv.show()
        else:
            ipv.pylab.save("%s.html"%outPath,title=r"%s"%(latex), offline=None,
                    template_options=(('extra_script_head', ''),
                        ('body_pre', ''), ('body_post', '')))
            run_cmd('open %s.html'%(str(outPath)))

#:}}}

# MAIN:{{{
""" Main function for the plotting program."""

# Paser:{{{
if __name__=="__main__":

    parser = argparse.ArgumentParser(prog='3-D Plot',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                            description=textwrap.dedent('''\
    -------------------------------------------------------------------------------
    This program allows the user to input various mathematical functions and recive
    a 3-D plot (similar to Wolfram Alpha).

    Please remember to use variables x,y,z.
    -------------------------------------------------------------------------------
                                    '''),
                                    epilog=" ")

    parser.add_argument("--Fn",help="Function with variables x,y,z",
            required=False,type=str,metavar=str)
    parser.add_argument("--x", help="x-axis limits", type=str,
            metavar=None,required=False)
    parser.add_argument("--y", help="y-axis limits", type=str,
            metavar=None,required=False)
    parser.add_argument("--z", help="z-axis limits", type=str,
            metavar=None,required=False)
    parser.add_argument("--axis-labels", help="axis labels for plot",type=None,
            default=str("[x,y,z]"),metavar=None,required=False)
    parser.add_argument("--data", help="input data file",type=str,
            default=None,metavar=None,required=False)
    #parser.add_argument("--", help="",type=str,
    #        default=None,metavar=None,required=False)

    args = parser.parse_args()

    # Instantiate Plot class.
    m = Plot()
    Fn = args.Fn
    x,y,z = args.x,args.y,args.z
    labels = str(args.axis_labels).replace("[","").replace("]","")
    m.axis_labels = [ str(i) for i in labels.split(",")]
    data = args.data
    #:}}}

    # Check the x-axis limits
    if x:
        lim = x.replace("[","").replace("]","")
        m.xlim = [float(lim.split(",")[0]),float(lim.split(",")[1])]
    if y:
        lim = y.replace("[","").replace("]","")
        m.ylim = [float(lim.split(",")[0]),float(lim.split(",")[1])]
    if z:
        lim = z.replace("[","").replace("]","")
        m.zlim = [float(lim.split(",")[0]),float(lim.split(",")[1])]

    # Is there a directory for trash? If not, create it.
    trash = str(os.path.expanduser('~')+'/.trash')
    if not os.path.isdir('%s'%(trash)):
        run_cmd('mkdir %s'%(trash))

    if Fn:
        # Change the name for the output using markdown conventions
        name = str(Fn).replace('**','^').replace('/','Frac').replace('*','dot').replace('(','{').replace(')','}').replace(',','¿').replace(";","_and_")
        outPath = str(trash)+str('/')+str(name)
        debug=0 #1
        if debug:
            print('trash = %s'%trash)
            print('Fn = %s'%Fn)
            print('name = %s'%name)
            print('outPath = %s'%outPath)
        m.plot_expr(Fn,outPath)
        run_cmd('open %s.html'%(str(outPath)))

    if data:
        m.plot_expr(Fn,outPath)
        run_cmd('open %s.html'%(str(outPath)))


#:}}}




