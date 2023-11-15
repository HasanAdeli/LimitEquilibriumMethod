def trapeze(a, b, h):
    return (a + b) / 2 * h


def distances(n, l, h, a, slope):
    ls = [l]
    for i in range(n+1):
        l1 = ls[i] + 2 * h[i] * slope[i] + 2 * a[i]
        ls.append(l1)
    return ls


def all_area(n, h, a, distances_):
    total_area = 0
    for i in range(n + 1):
        total_area += trapeze(distances_[i] + 2 * a[i], distances_[i+1], h[i])
    return total_area


if __name__ == '__main__':
    dist = distances(2, 5.4, [4, 5, 3], [0, 2, 3], [2.2, 2.3, 2.5])
    print(all_area(2, [4, 5, 3], [0, 2, 3], dist))
    # print(all_area(2, 5.4, [4, 5, 3], [0, 2, 3], [2.2, 2.3, 2.5]))
