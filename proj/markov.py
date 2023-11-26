import math
from hashtable import Hashtable


HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2


class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.use_hashtable = use_hashtable
        self.model = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO) if use_hashtable else {}
        self.build_model(text)
        self.uni_chars = set(text)

    def get_strs(self, text, pointer):
        '''
        Get the two required strings in the text
        '''
        k_str = text[pointer:pointer + self.k]
        k_str_plus1 = text[pointer:pointer + self.k + 1]

        # deal with the situation that the length of string is not enough 
        if len(k_str) < self.k:
            k_str += text[:self.k-len(k_str)]
        if len(k_str_plus1) < self.k+1:
            k_str_plus1 += text[:self.k+1-len(k_str_plus1)]

        return k_str, k_str_plus1

    def build_model(self, text):
        '''
        Build the markov model with text based on README.md
        '''
        for i in range(len(text)):
            model_str, model_str_plus1 = self.get_strs(text, i)
            for string in (model_str, model_str_plus1):
                self.model[string] = self.model.get(string, 0) + 1


    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        total_log_prob = 0
        for i in range(len(s)):
            s_str, s_str_plus1 = self.get_strs(s, i)
            num_observed_string_kplus1 = self.model.get(s_str_plus1, 0)
            num_observed_string_k = self.model.get(s_str, 0)
            num_uni_chars = len(self.uni_chars)
            total_log_prob += math.log((num_observed_string_kplus1 + 1) / (num_observed_string_k + num_uni_chars))
        return total_log_prob


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    speaker1_model = Markov(k, speech1, use_hashtable)
    speaker2_model = Markov(k, speech2, use_hashtable)

    prob_speaker1 = speaker1_model.log_probability(speech3) / len(speech3)
    prob_speaker2 = speaker2_model.log_probability(speech3) / len(speech3)

    res = "A" if prob_speaker1 > prob_speaker2 else "B"
    return prob_speaker1, prob_speaker2, res