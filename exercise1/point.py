class Point:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return "{0}:={1}".format(self.name, self.value)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (other.value == self.value) and (other.name == self.name)

    def __hash__(self):
        return hash((self.value, self.name))


class Omega:
    def __init__(self, mixing_coefficients, mean, variance):
        self.mixing_coefficients = mixing_coefficients
        self.mean = mean
        self.variance = variance

    def __str__(self):
        return "Omega Component: " + self.__repr__()

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.mixing_coefficients, self.mean, self.variance)


class Cluster:
    def __init__(self, index, points, all_points):
        self.all_points = all_points
        self.points = set(points)
        self.omega = self.calculate_omega()
        self.index = index

    def add_point(self, point):
        self.points.add(point)

    def calculate_omega(self):
        mean = self.get_mean()
        variance = self.get_variance()
        mixing_coefficients = self.get_mixing_coefficients()
        return Omega(mixing_coefficients, mean, variance)

    def remove_point(self, point):
        self.points.remove(point)

    def get_all_points(self):
        return set(self.points)

    def is_omega_set(self):
        if self.omega is None:
            return False
        return True

    def get_point_by_name(self, name):
        for p in self.points:
            if p.name == name:
                return p

        return None

    def get_mean(self):
        sum = 0
        for point in self.points:
            sum = sum + point.value

        return sum / len(self.points)

    def get_variance(self):
        mean = self.get_mean()
        sum = 0;
        for point in self.points:
            sum = sum + (point.value - mean) ** 2

        return (1 / (len(self.points) - 1)) * sum

    def get_mixing_coefficients(self):
        return len(self.points) / len(self.all_points)

    def calculate_new_mean(self, responsibility):
        enumerator = 0
        denominator = 0
        for p in self.all_points:
            enumerator += responsibility[p] * p.value
            denominator += responsibility[p]

        return enumerator / denominator

    def calculate_new_variance(self, responsibility):
        mean_new = self.calculate_new_mean(responsibility)
        enumerator = 0
        denominator = 0
        for p in self.all_points:
            enumerator += responsibility[p] * ((p.value - mean_new) ** 2)
            denominator += responsibility[p]

        return enumerator / denominator

    def calculate_new_mixing_coefficients(self, responsibilities, clusters):
        enumerator = 0
        for p in self.all_points:
            enumerator += responsibilities[self.index - 1][p]

        denominator = 0
        for c in clusters:
            for p in self.all_points:
                denominator += responsibilities[c.index - 1][p]

        return enumerator / denominator

    def do_m_step(self, responsibilities, clusters):
        new_mean = self.calculate_new_mean(responsibilities[self.index - 1])
        new_variance = self.calculate_new_variance(responsibilities[self.index - 1])
        new_mixing_coefficients = self.calculate_new_mixing_coefficients(responsibilities, clusters)

        self.omega = Omega(new_mixing_coefficients, new_mean, new_variance)

    def update_points(self, responsibilities):
        self.remove_all_points()

        for p in self.all_points:
            decision = True
            for r in responsibilities:
                if responsibilities[self.index - 1][p] < r[p]:
                    decision = False

            if decision:
                self.points.add(p)


    def remove_all_points(self):
        self.points = set()

    def __str__(self):
        return "Cluster: " + self.points.__str__()

    def __contains__(self, point):
        for p in self.points:
            if p == point:
                return True
        return False

    def __eq__(self, other):
        if isinstance(other, Cluster):
            return self.points == other.points
        return False
