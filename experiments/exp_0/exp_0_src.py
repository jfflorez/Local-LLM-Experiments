
import os
import sys

project_dir = os.path.normpath(os.path.join(os.path.abspath(__file__),'..','..'))
if not project_dir in sys.path:
    sys.path.append(project_dir)

import math
from collections import Counter
import re
import time
import requests
import subprocess
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Entropy calculation
# -----------------------------

def compute_entropy(counter : Counter):
    """ Computes the entropy of a discrete random variable with a
    histogram described by key value pairs (counter), where
    key is a categorical value and value stores its frequency or counts.    
    
    """
    total = sum(counter.values())
    if total == 0:
        return 0

    entropy = 0
    for count in counter.values():
        p = count / total
        entropy -= p * math.log2(p)
    # Miller–Madow
    k = len(counter)  # number of observed categories
    correction = (k - 1) / (2 * total * math.log(2))

    return entropy + correction

# -----------------------------
# Helper: Extract animal word
# -----------------------------

def extract_first_word(text):
    text = text.lower()
    words = re.findall(r"[a-z]+", text)
    if words:
        return words[0]
    return None
    #for word in words:
    #    if word in animal_dictionary:
    #        return word
    #return None




def generate_figures(prompt, results : dict):
    """ process a dictionary of results, associated with each parameters variant in exp_0/paramters.
    Each key, value are such that kay is a hash of the parameters and value
    is a dict  {"temperature" : temperature, "counter" : counter, "entropy" : entropy}

    """
    "".split()
    models = []
    # Collect all unique animals across temperatures
    #temps = set()
    models =  set()
    #aggr_counter = Counter()
    for key in results.keys():
        key_parts = key.split('_')
        param_hash = key_parts.pop(-1)
        model_name = '_'.join(key_parts)
        #aggr_counter.update(result['counter'])
        #temps.add(result['temperature'])
        models.add(model_name)

    #all_categories = [category_name for category_name, counts in aggr_counter.most_common()]

    #all_animals = sorted({
    #    animal
    #    for result in results.values()
    #    for animal in result['counter'].keys()
    #})
    #Counter().most_common()
    #temps = sorted(results.keys())
    output_dict = {}
    for model_name in models:
        model_results = {key:value for key,value in results.items() if model_name in key}

        temps = set()
        aggr_counter = Counter()
        for key, result in model_results.items():
            #key_parts = key.split('_')
            #param_hash = key_parts.pop(-1)
            #model_name = '_'.join(key_parts)
            aggr_counter.update(result['counter'])
            temps.add(result['temperature'])
            #models.add(model_name)
            
        all_categories = [category_name for category_name, counts in aggr_counter.most_common()]
        num_temps = len(temps)

        x = np.arange(len(all_categories))
        width = 0.8 / num_temps  # total bar width divided among temperatures
        colors = plt.cm.viridis(np.linspace(0.2, 1, len(temps)))
        plt.figure(figsize=(10,5))
        for i, result in enumerate(model_results.values()):
            temperature = result['temperature']
            n_samples = result['n_samples']
            counter = result['counter']
            entropy = result['entropy']
            counts = [counter.get(animal, 0) for animal in all_categories]

            offset = (i - (num_temps - 1) / 2) * width
            plt.bar(x + offset, [i/sum(counts) for i in counts], width=width, 
                    label=f'Temperature={temperature}, Entropy={entropy:0.2f}', 
                    color=colors[i], edgecolor='black')


        plt.xticks(x, all_categories, rotation=45, fontsize=14)
        plt.yscale('log')
        plt.yticks(fontsize=14)
        plt.suptitle(f'Empirical PMF of the First Generated Word Given a Fixed Prompt', fontsize=16, fontweight='bold')
        #plt.suptitle(f'Empirical Probability Mass Function of the First Word over \n{n_samples} independent text respones to a fixed prompt', fontsize=16, fontweight='bold')
        plt.title(f'Prompt: {prompt}', fontsize=14, color='gray') # Subtitle

        plt.xlabel('The First Generated Word (animal name)', fontsize=16)
        plt.ylabel("Probability (in log scale)", fontsize=16)
        plt.legend(fontsize=14)#, loc='upper right')
        plt.tight_layout(pad=2)
        fig = plt.gcf()
        plt.show()

        name = f"bar_plot_of_first_word_by_{model_name}"
        output_dict[model_name] = (name, fig)

    return output_dict