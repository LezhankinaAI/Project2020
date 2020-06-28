class Sets:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, node):
        if self.parent[node] == node:
            return node
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union_sets(self, first, second):
        f_root = self.find(first)
        s_root = self.find(second)
        if f_root != s_root:
            self.parent[s_root] = f_root
        return True

    def get_item(self, index):
        return self.result()[index]

    def count_sets(self):
        return len(set(self.result()))

    def count_elems(self, node):
        return self.result().count(node)

    def result(self):
        return list(map(self.find, self.parent))


def dist_Euclid_pow(obj1, obj2, num_of_char):
    ans = 0
    for i in range(num_of_char):
        ans += (obj1[i] - obj2[i]) ** 2
    return ans


def dist_Ward(students, clusters, U, V, num_of_char):
    elems_U = clusters.count_elems(U)
    elems_V = clusters.count_elems(V)
    if elems_U == elems_V == 1:
        res = dist_Euclid_pow(students[U], students[V], num_of_char)
    else:
        obj1 = [0 for x in range(num_of_char)]
        obj2 = [0 for y in range(num_of_char)]
        for i in range(len(students)):
            if clusters.get_item(i) == U:
                for j in range(num_of_char):
                    obj1[j] += students[i][j]
            elif clusters.get_item(i) == V:
                for j in range(num_of_char):
                    obj2[j] += students[i][j]
        for i in range(num_of_char):
            obj1[i] /= elems_U
            obj2[i] /= elems_V
        res = (elems_U * elems_V) / (elems_U + elems_V)
        res *= dist_Euclid_pow(obj1, obj2, num_of_char)
    return res


def cluster_Ward(students, num_of_char, num_of_clusts):
    clusters = Sets(len(students))
    dists = list()
    while clusters.count_sets() != num_of_clusts:
        fst = clusters.get_item(0)
        n = 1
        while clusters.get_item(n) == fst:
            n += 1
        scnd = clusters.get_item(n)
        minim_dist = dist_Ward(students, clusters, fst, scnd, num_of_char) + 10
        for i in set(clusters.result()):
            for j in set(clusters.result()):
                if (i != j) & (dist_Ward(students, clusters, i, j, num_of_char) < minim_dist):
                    minim_dist = dist_Ward(students, clusters, i, j, num_of_char)
                    clust1 = i
                    clust2 = j
        dists.append(minim_dist)
        clusters.union_sets(clust1, clust2)
    if num_of_clusts == 1:
        return solution(students, num_of_char, dists)
    else:
        return clusters


def solution(students, num_of_char, dists):
    max_diff = 0
    num = 0
    for i in range(len(dists) - 1):
        if abs(dists[i] - dists[i + 1]) > max_diff:
            max_diff = abs(dists[i] - dists[i + 1])
            num = i
    num_of_clusts = len(students) - num
    return cluster_Ward(students, num_of_char, num_of_clusts)
