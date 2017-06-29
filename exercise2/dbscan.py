from point import Point, Cluster
import data as d
import matplotlib.pyplot as plt

EPSILON = 2.2
MIN_PTS = 4

next_cluster_id = 0


def is_point_core_object(point, distances):
    neighborhood = get_neighborhood(point, distances)
    return len(neighborhood) >= MIN_PTS


def get_neighborhood(point, distances):
    neighborhood = []
    for p in d.data:
        if distances[point][p] <= EPSILON:
            neighborhood.append(p)

    return neighborhood


def plot_result(clusters, noise, core_objects, with_circle=False):
    fig, ax = plt.subplots()
    color = ['blue', 'red', 'green', 'magenta', 'cyan']
    #ax.grid()

    for i in range(len(clusters)):
        for p in clusters[i]:
            circle = plt.Circle((p.x, p.y), EPSILON, color='grey', fill=False)

            if p in core_objects:
                marker = 'x'
            else:
                marker = 'o'

            ax.scatter(p.x, p.y, color=color[i], marker=marker)
            if with_circle:
                ax.add_artist(circle)

        x = [p.x for p in clusters[i]]
        y = [p.y for p in clusters[i]]

    x = [p.x for p in noise]
    y = [p.y for p in noise]

    ax.scatter(x, y, color='grey', marker='*')

    plt.savefig('dbscan_result.pdf', format='pdf')
    plt.show()


def create_cluster(point, neighborhood, distances):
    global next_cluster_id
    point.cluster = next_cluster_id

    for p in neighborhood:
        if not p.processed:
            p.processed = True
            if is_point_core_object(p, distances):
                p.core_object = True
                neighborhood.extend(get_neighborhood(p, distances))
            if p.cluster is None:
                p.cluster = next_cluster_id

    next_cluster_id += 1


def main():
    distances = {p: {p2: p.distance_to(p2) for p2 in d.data} for p in d.data}
    clusters = {}
    noise = []
    core_objects = []

    for p in d.data:
        if not p.processed:
            p.processed = True
            if is_point_core_object(p, distances):
                p.core_object = True
                neighborhood = get_neighborhood(p, distances)
                create_cluster(p, neighborhood, distances)
            else:
                p.noise = True

    for p in d.data:
        if p.noise:
            noise.append(p)
        if p.cluster is not None:
            if p.cluster not in clusters:
                clusters[p.cluster] = []
            clusters[p.cluster].append(p)
        if p.core_object:
            core_objects.append(p)

    print(clusters)
    print(core_objects)
    print(noise)

    plot_result(clusters, noise, core_objects)

if __name__ == '__main__':
    main()