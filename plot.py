import matplotlib.pyplot as plt
from scipy.stats import pearsonr

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
                        return 'black'
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
        def do_centrality(books):
                """Centralities Lobby index centrality is calculated using function
                defined in lobby.py.  Degree, betweenness and closeness centralities
                are calculated using NetworkX. All measures are normalized.
                """
                offset_fig_nr = 1 # figure number starts after 1
                centrs = Graphs.get_centrality_names()
                
                fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8), (ax9, ax10, ax11)) = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=True)
                axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]

                for c in Graphs.get_centrality_names():
                        (xs, ys) = ([], [])
                        k = 0
                        fn = 'Figure-' + c + '.png'
                        
                        nms = 0 # counter for markers
                        marker_style = dict(linestyle='', markersize=6)
                        for b in books.get_books():
                                G = b.get_graph()
                                cs = Graphs.get_centrality_values(G, c)
                                Graphs.get_centrality_values(G, 'Lobby')
                                for u in G.nodes:
                                        xs.append(cs[u])
                                        ys.append(G.nodes[u]['Lobby'])

                                print(xs, '\n', ys)
                                
                                axes[k].set_title(b.get_name(), fontsize=10)
                                #axes[k].set_xlim(math.floor(xmin), 1.0)
                                #axes[k].set_ylim(math.floor(ymin), 1.0)
                                axes[k].set_xscale('log')
                                axes[k].set_yscale('log')
                                axes[k].plot(xs, ys, c = Plot.get_color(b),
				             marker = Plot.markers[nms % len(Plot.markers)],
				             label=b.get_name(),
               			             alpha=0.3,
				             **marker_style)
                                axes[k].grid(True)
                                axes[k].text(0.5, 1.1, '' ,
                                             style='italic',
                                             horizontalalignment='center',
                                             verticalalignment='center',
                                             fontsize=8, color='gray',
                                             transform=axes[k].transAxes)

                                k = k + 1
                                if k==0:
                                        axes[k].legend(loc='upper right', fontsize=4)
                        
                                # calculate Pearson correlation
                                (r_row, p_value) = pearsonr(xs, ys)
                                #  print name, r_row, p_value
                                # write Pearson correlation in the plot
                                axes[k].text(.675, .875, '$r=$'+'{0:.3f}'.format(r_row),
                                             horizontalalignment='center',
                                             verticalalignment='center',
                                             fontsize=10, color='black',
                                             transform=axes[nms].transAxes)
                                nms += 1 # increment no. of markers counter
                                if k == 12:
                                        break

                        fig.subplots_adjust(hspace=0)
                        plt.tight_layout()
                        plt.savefig(fn)
                        logger.info('Wrote plot %s', fn)

        @staticmethod
        def do_assortativity(books):
                """Assortativity mixing is calculated and plotted versus average degree.
                """
                fn = 'Figure-Assortativity.png'
                xticklabels = np.arange(0, 1.1, 0.1)
                yticklabels = xticklabels

                fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8), (ax9, ax10, ax11)) = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=True)
                fig.subplots_adjust(hspace=.1, wspace=.1)
                axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]

                marker_style = dict(linestyle='', markersize=6)
                k=0
                for b in books.get_books():
                        G = b.get_graph()
                        # xs (vertices), ys (degree of neighbors of xs), xs, ys_avg (avg degree of neighbors of xs)
                        (xs, ys, xxs, yavgs) = Graphs.get_degree_avg_neighbors(G)

                        axes[k].plot(xxs, yavgs, label='avg', color='black')
                        axes[k].plot(xs, ys, '.', color='gray', label=b.get_name())
                        axes[k].set_xlim(xticklabels[0], xticklabels[len(xticklabels)-1])
                        axes[k].set_ylim(yticklabels[0], yticklabels[len(yticklabels)-1])
                        axes[k].xaxis.set_tick_params(labelsize=6)
                        axes[k].yaxis.set_tick_params(labelsize=6)
                        axes[k].legend(fontsize='x-small')
                        axes[k].grid(True)
                        
                        if k > 8: # if sharex fails
                                axes[k].set_xlabel('$k/k_{max}$', fontsize=8)
                                
                        if k % 3 == 0: # if sharey fails
                                axes[k].set_ylabel('$knn/knn_{max}$', fontsize=8)

                        k = k + 1
                        if k==0:
                                axes[k].legend(loc='upper right', fontsize=4)

                        if k == 12:
                                break
                plt.savefig(fn)
                logger.info('Wrote plot %s', fn)

        @staticmethod
        def do(books):
                Plot.do_centrality(books)
                Plot.do_assortativity(books)
