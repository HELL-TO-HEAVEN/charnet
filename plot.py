import matplotlib.pyplot as plt

# LOCAL
from books import *
from graphs import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Plot:
        # set of markers to be used in the plot
        markers = ['+', '^', 'v', 'o', 'p', 's', '.', '*', 'd']

        @staticmethod
        def get_color(book):
                if (book.get_category() == BookCategory.FICTION):
                        return 'gray'
                elif (book.get_category() == BookCategory.BIOGRAPHY):
                        return 'black'
                elif (book.get_category() == BookCategory.CANONICAL):
                        return 'black'
                else:
                        logger.error('Non categorized book ', book.get_name())
                        exit()

        @staticmethod
        def do_density_versus_clustering_coefficient(books):
                fn = 'figure1.pdf'
                xs = []
                ys = []
        
                f = open(fn, "w")

                for book in books.get_books():
                        nms = 0 # counter for markers
                        G = book.get_graph()

                        x = nx.density(G)
                        y = nx.average_clustering(G)

                        marker_style = dict(linestyle=':', color=Plot.get_color(book), markersize=8)
                        plt.plot(x, y, c=Plot.get_color(book),
                                 marker=Plot.markers[nms % len(Plot.markers)],
                                 label=book.get_raw_book_label(),
                                 alpha=0.3, 
                                 **marker_style)

                        nms += 1 # increment no. of markers counter

                plt.ylim(-0.1,0.8)
                plt.xlabel('Density')
                plt.ylabel('Clustering coefficient')
                plt.grid()
                plt.title('')
                plt.legend(fontsize=7, loc='center right')
                plt.savefig(fn)

                logger.info('Wrote %s', fn)

        @staticmethod
        def do_centralities(books):
                """Centralities Lobby index centrality is calculated using function
                defined in lobby.py.  Degree, betweenness and closeness centralities
                are calculated using NetworkX. All measures are normalized.
                """
                offset_fig_nr = 1 # figure number starts after 1
                centrs = Graphs.get_centrality_names()

        
                fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8), (ax9, ax10, ax11)) = plt.subplots(nrows=4, ncols=3)
                axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]

                # Calculate the centralities
                lobbyf = open('lobby.centr.csv', 'w')
                for b in books.get_books():
                        G = b.get_graph()
                        b.avg['Assortativity'] = nx.degree_assortativity_coefficient(G)
                        for centr in centrs:
                                b.avg[centr] = Graphs.get_avg_centrality(G, centr)

                centrs.append('Assortativity')
                k = 0
                for c in centrs:
                        if c == 'Lobby': # Lobby is y in all 
                                continue
                        
                        fn = 'Figure-' + c + '.pdf'
                        
                        nms = 0 # counter for markers

                        marker_style = dict(linestyle='', markersize=6)
                        for b in books.get_books():
                                x = b.avg[c]
                                y = b.avg['Lobby']
                                axes[k].plot(x, y, c = Plot.get_color(b),
				             marker = Plot.markers[nms % len(Plot.markers)],
				             label=b.get_name(),
               			             alpha=0.3,
				             **marker_style)
                                axes[k].grid(True)
                                print(k)
                                axes[k].set_xlabel(c)
                                axes[k].set_ylabel('Lobby')

                                axes[k].text(0.5, 1.1, '' ,
                                             style='italic',
                                             horizontalalignment='center',
                                             verticalalignment='center',
                                             fontsize=8, color='gray',
                                             transform=axes[k].transAxes)

                        if k==0:
                                axes[k].legend(loc='upper right', fontsize=4)
                        
                        # fix number colision problems
                        if c == 'Assortativity':
                                start, end = axes[k].get_xlim()
                                axes[k].xaxis.set_ticks(np.arange(start, end, 0.1))
                        elif c == 'Betweenness':
                                start, end = axes[k].get_xlim()
                                axes[k].xaxis.set_ticks(np.arange(start, end, 0.02))
                        elif c == 'Closeness':
                                start, end = axes[k].get_xlim()
                                axes[k].xaxis.set_ticks(np.arange(start, end, 0.1))
                        else: # Degree
                                start, end = axes[k].get_xlim()
                                axes[k].xaxis.set_ticks(np.arange(start, end, 0.05))
                        # calculate Pearson correlation
                        #  (r_row, p_value) = pearsonr(xs, ys)
                        #  print name, r_row, p_value
                        # write Pearson correlation in the plot
                        # axes[i].text(.675, .875, '$r=$'+'{0:.3f}'.format(r_row),
                        # horizontalalignment='center',
                        # verticalalignment='center',
                        # fontsize=10, color='black',
                        # transform=axes[i].transAxes)
                        k = k + 1
                        if k == 8:
                                break
		        #plt.xscale('log')   			       			       
                        #plt.yscale('log')
                        #plt.legend()
                        nms += 1 # increment no. of markers counter
                        
                        fig.subplots_adjust(hspace=0)
                        plt.tight_layout()
                        plt.savefig(fn)
                        logger.info('Wrote plot %s', fn)
                        lobbyf.close()

