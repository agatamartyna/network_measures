from flask import render_template, request
from app import app
from app.forms import NeighboursForm, CoefficientForm
from app.neighbourhood_density import neighbourhood_density
from app.coefficient import coefficient_cluster
from app.dictionary_process import words_segmentised
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')


@app.route('/', methods=["GET", "POST"])
def index():
    form = NeighboursForm()
    form_co = CoefficientForm()
    if request.method == "POST":
        if form.data["word"] != '':
            word = form.data["word"]
            words_for_density = words_segmentised
            neighbours = neighbourhood_density(word, words_for_density)
            neighbours_cut = []
            for neighbour in neighbours:
                if neighbour.lower() not in neighbours_cut:
                    neighbours_cut.append(neighbour.lower())
            density = len(neighbours_cut)

            return render_template("homepage.html",
                                   form=form, word=word, density=density)

        elif form_co.data["word_co"]:
            word_co = form_co.data['word_co']
            words_for_cluster = words_segmentised
            neighbours_in_cluster = coefficient_cluster(
                word_co, words_for_cluster)
            e = len(neighbours_in_cluster)

            neighbours = neighbourhood_density(word_co, words_for_cluster)
            neighbours_cut = []
            for neighbour in neighbours:
                if neighbour.lower() not in neighbours_cut:
                    neighbours_cut.append(neighbour.lower())
            density = len(neighbours_cut)

            if density == 1:
                c = 0
            elif density == 0:
                c = 0
            else:
                c = 2 * e / (density * (density - 1))
                c = round(c, 2)

            return render_template("homepage.html",
                                   form_co=form_co, word_co=word_co,
                                   density=density, c=c)

    return render_template("homepage.html", form=form)


@app.route('/coefficient', methods=["GET", "POST"])
def coefficient():
    form_co = CoefficientForm()
    form = NeighboursForm()
    if request.method == "POST":
        if form_co.data['word_co'] != '':
            word_co = form_co.data['word_co']
            words_for_cluster = words_segmentised
            neighbours_in_cluster = coefficient_cluster(
                word_co, words_for_cluster)
            e = len(neighbours_in_cluster)

            neighbours = neighbourhood_density(word_co, words_for_cluster)
            neighbours_cut = []
            for neighbour in neighbours:
                if neighbour.lower() not in neighbours_cut:
                    neighbours_cut.append(neighbour.lower())
            density = len(neighbours_cut)

            if density == 1:
                c = 0
            elif density == 0:
                c = 0
            else:
                c = 2 * e / (density * (density - 1))
                c = round(c, 2)

            img = io.BytesIO()

            neighbours = neighbours_cut
            nneighbours = neighbours_in_cluster
            pairs = []

            G = nx.Graph()

            for neighbour in neighbours:
                pairs.append((word_co, neighbour))

            for pair in pairs:
                G.add_edge(pair[0], pair[1], color='b')
            for nneighbour in nneighbours:
                G.add_edge(nneighbour[0], nneighbour[1], color='r')

            colors = nx.get_edge_attributes(G, 'color').values()
            weights = nx.get_edge_attributes(G, 'weight').values()

            nx.draw(G,
                    edge_color=colors,
                    width=list(weights),
                    with_labels=True,
                    node_color='lightblue')

            plt.savefig(img, format='png')
            plt.clf()
            plt.cla()
            plt.close()
            img.seek(0)

            plot_url = base64.b64encode(img.getvalue()).decode()

            return render_template("coefficient.html", form_co=form_co,
                                   word_co=word_co, density=density,
                                   neighbours_in_cluster=neighbours_in_cluster,
                                   c=c, plot_url=plot_url)

        if form.data["word"] != '':
            word = form.data["word"]
            words_for_cluster = words_segmentised
            neighbours = neighbourhood_density(word, words_for_cluster)
            neighbours_cut = []
            for neighbour in neighbours:
                if neighbour.lower() not in neighbours_cut:
                    neighbours_cut.append(neighbour.lower())
            density = len(neighbours_cut)

            return render_template("coefficient.html", form=form,
                                   form_co=form_co, word=word, density=density)

    return render_template("coefficient.html", form_co=form_co)


@app.route("/neighbours", methods=["GET", "POST"])
def neighbours():
    form = NeighboursForm()
    form_co = CoefficientForm()
    if request.method == "POST":

        if form.data["word"] != '':
            word = form.data["word"]
            words_for_density = words_segmentised
            neighbours = neighbourhood_density(word, words_for_density)
            neighbours_cut = []
            for neighbour in neighbours:
                if neighbour.lower() not in neighbours_cut:
                    neighbours_cut.append(neighbour.lower())
            density = len(neighbours_cut)

            img = io.BytesIO()

            pairs = []

            G = nx.Graph()

            for neighbour in neighbours:
                pairs.append((word, neighbour))

            for pair in pairs:
                G.add_edge(pair[0], pair[1])

            for pair in pairs:
                G.add_edge(pair[0], pair[1], color='b')

            colors = nx.get_edge_attributes(G, 'color').values()
            weights = nx.get_edge_attributes(G, 'weight').values()

            nx.draw(G,
                    edge_color=colors,
                    width=list(weights),
                    with_labels=True,
                    node_color='lightblue')

            plt.savefig(img, format='png')
            plt.clf()
            plt.cla()
            plt.close()
            img.seek(0)

            plot_url = base64.b64encode(img.getvalue()).decode()

            return render_template("neighbours.html",
                                   neighbours=neighbours_cut,
                                   form=form,
                                   word=word,
                                   density=density,
                                   plot_url=plot_url)

        if form_co.data["word_co"] != '':
            word_co = form_co.data["word_co"]
            words_for_cluster = words_segmentised
            neighbours_in_cluster = coefficient_cluster(
                word_co, words_for_cluster)
            e = len(neighbours_in_cluster)

            neighbours = neighbourhood_density(word_co, words_for_cluster)
            neighbours_cut = []
            for neighbour in neighbours:
                if neighbour.lower() not in neighbours_cut:
                    neighbours_cut.append(neighbour.lower())
            density = len(neighbours_cut)

            if density == 1:
                c = 0
            elif density == 0:
                c = 0
            else:
                c = 2 * e / (density * (density - 1))
                c = round(c, 2)

            return render_template("neighbours.html", form=form,
                                   form_co=form_co, word_co=word_co,
                                   density=density, c=c)

    return render_template("neighbours.html", form=form)
