import sys
from markov import identify_speaker
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def run_performance_test(speech1, speech2, speech3, max_k, runs, use_hashtable):
    '''
    record timings in a list of dictionaries
    '''
    records = []
    for k in range(1, max_k + 1):
        for run in range(1, runs + 1):
            start = time.perf_counter()
            identify_speaker(speech1, speech2, speech3, k, use_hashtable)
            elapsed = time.perf_counter() - start
            records.append({
                "Implementation": "hashtable" if use_hashtable else "dict",
                "K": k,
                "Run": run,
                "Time": elapsed
            })
    return records


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # open files & read text
    with open(filenameA, 'r') as file:
        speech1 = file.read()
    with open(filenameB, 'r') as file:
        speech2 = file.read()
    with open(filenameC, 'r') as file:
        speech3 = file.read()

    # run performance tests as outlined in README.md
    records = []
    records += run_performance_test(speech1, speech2, speech3, max_k, runs, True)
    records += run_performance_test(speech1, speech2, speech3, max_k, runs, False)

    # create a DataFrame from the records
    df = pd.DataFrame(records)
    df_average = df.groupby(["Implementation", "K"])["Time"].mean()

    # write execution_graph.png
    sns.pointplot(data=df, x="K", y="Time", hue="Implementation", linestyle="-", marker="o")
    plt.xlabel("K")
    plt.ylabel(f"Average Time (Runs={runs})")
    plt.title("HashTable vs Python dict")
    plt.savefig('execution_graph.png')
    plt.show()
