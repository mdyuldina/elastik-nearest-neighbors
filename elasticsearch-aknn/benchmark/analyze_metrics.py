import json
import matplotlib.pyplot as plt
import numpy as np


def get_metrics_path(docs, tables, bits, k1, k2):
    return "out/metrics_{}_{}_{}_{}_{}.json".format(docs, tables, bits, k1, k2)


def compare(what):
    print("\nCompare %s depending on tables" %what)
    print("Using 10000 products, 16 bits, 100 k1")
    for tables in [16, 32, 64]:
        docs_path = get_metrics_path(10000, tables, 16, 100, 10)
        for i, line in enumerate(open(docs_path)):
            metric = json.loads(line)
            results = np.array(metric[what])
            """hist, bins = np.histogram(results, bins=50)
            width = 0.7 * (bins[1] - bins[0])
            center = (bins[:-1] + bins[1:]) / 2
            plt.bar(center, hist, align='center', width=width)
            plt.show()"""

            print("Average %s with %d tables = %f" % (what, tables, np.mean(results)))

    print("\nCompare %s depending on bits" %what)
    print("Using 10000 products, 64 tables, 100 k1")
    for bits in [8, 16]:
        docs_path = get_metrics_path(10000, 64, bits, 100, 10)
        for i, line in enumerate(open(docs_path)):
            metric = json.loads(line)
            results = np.array(metric[what])
            """hist, bins = np.histogram(results, bins=50)
            width = 0.7 * (bins[1] - bins[0])
            center = (bins[:-1] + bins[1:]) / 2
            plt.bar(center, hist, align='center', width=width)
            plt.show()"""

            print("Average %s with %d bits = %f" % (what, bits, np.mean(results)))

    print("\nCompare %s depending on k1" %what)
    print("Using 10000 products, 64 tables, 16 bits")
    for k1 in [15, 100, 250]:
        docs_path = get_metrics_path(10000, 64, 16, k1, 10)
        for i, line in enumerate(open(docs_path)):
            metric = json.loads(line)
            results = np.array(metric[what])
            """hist, bins = np.histogram(results, bins=50)
            width = 0.7 * (bins[1] - bins[0])
            center = (bins[:-1] + bins[1:]) / 2
            plt.bar(center, hist, align='center', width=width)
            plt.show()"""

            print("Average %s with %d k1 = %f" % (what, k1, np.mean(results)))


def count_index_times():
    print("\nCounting index times for 64 tables and 16 bits")
    index_time_whole = 0
    index_times = list()
    for docs in [2500, 5000, 10000]:
        docs_path = get_metrics_path(docs, 64, 16, 100, 10)
        for i, line in enumerate(open(docs_path)):
            metric = json.loads(line)
            results = np.array(metric["index_times"])
            index_time_whole += np.sum(results)
            index_times.append(index_time_whole)
            print("%d docs were indexed in %d seconds" % (docs, index_time_whole))

    """f, ax = plt.subplots(1)
    ax.plot([2500, 5000, 10000], index_times, marker='s')
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.show(f)"""


def compare_index_times():
    print("\nCompare index times for 10000 docs depending on tables")
    index_times = list()
    for tables in [16, 32, 64]:
        index_time_whole = 0
        for docs in [2500, 5000, 10000]:
            docs_path = get_metrics_path(docs, tables, 16, 100, 10)
            for i, line in enumerate(open(docs_path)):
                metric = json.loads(line)
                results = np.array(metric["index_times"])
                index_time_whole += np.sum(results)

        index_times.append(index_time_whole)
        print("10000 docs with %d tables and 16 bits were indexed in %d seconds" % (tables, index_time_whole))

    """f, ax = plt.subplots(1)
    ax.plot([16, 32, 64], index_times, marker='s')
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.show(f)"""

    print("\nCompare index times for 10000 docs depending on bits")
    index_times = list()
    for bits in [8, 16]:
        index_time_whole = 0
        for docs in [2500, 5000, 10000]:
            docs_path = get_metrics_path(docs, 64, bits, 100, 10)
            for i, line in enumerate(open(docs_path)):
                metric = json.loads(line)
                results = np.array(metric["index_times"])
                index_time_whole += np.sum(results)

        index_times.append(index_time_whole)
        print("10000 docs with 64 tables and %d bits were indexed in %d seconds" % (bits, index_time_whole))

    """f, ax = plt.subplots(1)
    ax.plot([8, 16], index_times, marker='s')
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.show()"""


def compare_search_times_depending_on_docs():
    print("\nCompare search times depending on docs")
    search_times = list()
    for docs in [2500, 5000, 10000]:
        docs_path = get_metrics_path(docs, 64, 16, 100, 10)
        for i, line in enumerate(open(docs_path)):
            metric = json.loads(line)
            results = np.array(metric["search_times"])
            search_times.append(np.mean(results))
            print("Average search time  with %d docs = %d seconds" % (docs, np.mean(results)))

    """f, ax = plt.subplots(1)
    ax.plot([2500, 5000, 10000], search_times, marker='s')
    ax.set_ylim(ymin=0, ymax=70)
    ax.set_xlim(xmin=0)
    plt.show(f)"""


def compare_recall():
    compare("search_recalls")


def compare_search_times():
    compare("search_times")


if __name__ == '__main__':
    compare_recall()
    compare_search_times()
    count_index_times()
    compare_index_times()
    compare_search_times_depending_on_docs()

