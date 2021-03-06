from app.density import neighbourhood_density
from app.segmentise import segmentise


def coefficient_cluster(word, words):
    # prepare words for generating neighbourhood density
    words_segmentised = words

    # get neighbours of a given word
    neighbours = neighbourhood_density(word, words_segmentised)

    # prepare the neighbours for other neighbour-search
    neighbours_segmentised = []
    for neighbour in neighbours:
        neighbours_segmentised.append((segmentise(neighbour), neighbour))
    # get neighbours of neighbours
    neighbours_neighbours = []
    for neighbour in neighbours:
        neighbour_neighbour = neighbourhood_density(
            neighbour, neighbours_segmentised)
        for n_n in neighbour_neighbour:
            neighbours_neighbours.append((neighbour, n_n))

    # remove reccurring pairs
    tuples = []
    for tupl in neighbours_neighbours:
        if (tupl[1], tupl[0]) not in tuples:
            tuples.append(tupl)

    return tuples
