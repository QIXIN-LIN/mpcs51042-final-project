import sys
from markov import identify_speaker


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # open and read the files
    with open(filenameA, 'r') as file:
        speech1 = file.read()
    with open(filenameB, 'r') as file:
        speech2 = file.read()
    with open(filenameC, 'r') as file:
        speech3 = file.read()

    # call identify_speaker
    use_hashtable = (hashtable_or_dict == "hashtable")
    prob_speaker_a, prob_speaker_b, most_likely_speaker = identify_speaker(speech1, speech2, speech3, k, use_hashtable)

    # print results
    print(f"Speaker A: {prob_speaker_a}")
    print(f"Speaker B: {prob_speaker_b}")
    print(f"\nConclusion: Speaker {most_likely_speaker} is most likely")


    # Output should resemble (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely
