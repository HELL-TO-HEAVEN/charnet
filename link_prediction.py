#!/usr/bin/env python3
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/')

import matplotlib.pyplot as plt

import networkx as nx

from random import seed
from random import randint

from books import *

def choose_link(G):
        r = randint(0, 1000)
        
        seed(r)

        r = randint(0, G.number_of_edges()-1)
        
        i = 0
        for e in G.edges():
                if i == r:
                        l = e
                        G.remove_edge(*e)
                        break
                i += 1

        assert l != None
        return l
                        
def count_all_neighbors(G, e):
        '''Return the number all neighbors of nodes u and v in the graph G.'''
        tdeg = G.degree(e[0])
        wdeg = G.degree(e[1])

        return tdeg + wdeg
        
def how_many_neighbors_intersect(G, e):
        '''Return how many neighbors u and v have in common in the graph G.'''
        ts = G.neighbors(e[0])
        ws = G.neighbors(e[1])

        inter = 0
        for t in ts:
                for w in ws:
                        if (t == w):
                                inter += 1
        return inter

def jaccard_coeff(G, e):
        '''Return the Jaccard coefficient between nodes u and v in the graph G.'''
        union = count_all_neighbors(G, e)
        inter = how_many_neighbors_intersect(G, e)

        if (union == 0) or (inter == 0):
                return 0.0
        else:
                return float(inter) / float(union)
        
def create_graph_of_missing_links(G, H):
        '''Return a dictionary with the existing edges in the form u-v, e.g
1-2, as keys and a boolean as value.
        '''
        logger.info('Creating graph of missing links')
        
        I = nx.Graph()
        for e in G.edges():
                if not H.has_edge(*e):
                     I.add_edge(*e)

        return I

def create_graph_of_non_existing_links(G):
        '''Return a dictionary with the existing edges in the form u-v, e.g
1-2, as keys and a boolean as value.
        '''
        logger.info('creating non existing links')
        N = G.number_of_nodes()
        J = nx.Graph()
        
        for u in range(N):
                for v in range(N):
                        if not G.has_edge(u, v):
                                J.add_edge(u, v)

        return J

def create_missing_links(G, H, p):
        assert p > 0.0
        assert p < 1.0
        M = G.number_of_edges()
        N = H.number_of_edges()

        logger.info('Creating missing links from the copy of G')
        # seed random number generator
        seed(1)
        
        # remove links from graph H to simulate missing links in a to
        # desired percentage p
        while ( float( H.number_of_edges() ) / float( M ) > p ):
                # the interval to pick a link
                r = randint(0, N-1)
                
                # traverse the edges and remove the rth
                i = 0
                for e in H.edges():
                     if i == r:
                             H.remove_edge(*e)
                             break
                     i += 1

                N = H.number_of_edges()

        return H

def calc_auc(G, p):
        n = 0
        np = 0
        npp = 0

        H = G.copy()

        H = create_missing_links(G, H, p)
        
        ML = create_graph_of_missing_links(G, H)
        NE = create_graph_of_non_existing_links(G)
        
        N = G.number_of_nodes()
        while(True):
                if ML.number_of_edges() == 0:
                        break
                
                em = choose_link(ML)
                en = choose_link(NE)

                sm = jaccard_coeff(H, em)
                sn = jaccard_coeff(H, en)

                if sm > sn:
                        np += 1
                elif sm == sn:
                        npp += 1
                else:
                        pass

                n += 1


        assert n > 0
        return (np + (0.5*float(npp))) / float(n)


if __name__ == '__main__':
        books = Books()
        books.read()
        p = 0.5


        fn = '/tmp/' + 'auc' + '-plot.png'
        plt.figure()
        plt.xlabel('%')
        plt.ylabel('AUC')
        plt.title('ROC')
        
        for b in books.get_books():
                (xs, ys) = ([], [])
                for x=0.5; x<1.0; x += 0.1:
                        xs.append(x)
                        G = b.get_graph()
                        auc = calc_auc(G, x)
                        ys.append(auc)
                        print(str(b.get_name()) + ',' + str(auc))
                        plot(xs, ys, 'bv')
                        

        plt.savefig(fn)
        logger.info('Wrote %s', fn)
