# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import argparse

import argparse
from CONSTANTS import *
from rsa import RSA
from ntru import NTRU
import time
import sys


# Given an RSA bit length (x), returns the equivalent security-level dimension in NTRU
# The data for the linear interpolation is from this paper https://ijarcce.com/upload/2017/february-17/IJARCCE%2062.pdf
def rsa_to_ntru(x):
    # Given data points from https://ijarcce.com/upload/2017/february-17/IJARCCE%2062.pdf
    x_values = [1024, 2048, 3072, 7680, 15360]
    y_values = [251, 347, 397, 587, 787]

    # Perform linear interpolation
    if x <= x_values[0]:
        return y_values[0]
    elif x >= x_values[-1]:
        return y_values[-1]
    else:
        # Find the two nearest data points
        for i in range(len(x_values) - 1):
            if x_values[i] <= x <= x_values[i + 1]:
                # Perform linear interpolation
                x0, x1 = x_values[i], x_values[i + 1]
                y0, y1 = y_values[i], y_values[i + 1]
                return int(y0 + (y1 - y0) * (x - x0) / (x1 - x0))


# Maps an RSA bit size to NTRU dimension level
RSA_TO_NTRU = {1024: 251, 2028: 347, 3072: 397, 7680: 587, 15360: 787}

def key_test(repititions, num_bits, num_dims, miller_trials):
    print(f"Running key generation test with {num_bits} bits and {miller_trials} Miller Trials...")

    rsa_avg = 0
    ntru_avg = 0
    for i in range(repititions):
        # Do RSA
        start_time = time.time()
        rsa_ = RSA(num_bits, miller_trials, False)
        rsa_avg += time.time() - start_time

        # Do NTRU
        start_time = time.time()
        ntru = NTRU(num_dims, 3, 97, miller_trials)
        ntru_avg += time.time() - start_time

    rsa_avg /= repititions
    ntru_avg /= repititions

    print(f"RSA Key-gen took on average, {rsa_avg} seconds.")
    print(f"NTRU Key-gen took on average, {ntru_avg} seconds.")


def encrypt_test(num_bits):
    print(f"Number of bits for encryption test: {num_bits}")


def parse():
    ### Adding Parser Args ###
    parser = argparse.ArgumentParser()

    # Add key test argument
    parser.add_argument("-key_test", help="Runs comparison test for generating keys", action='store_true')

    # Add encryption test argument
    parser.add_argument("-encrypt_test", help="Runs comparison test for encryption", action='store_true')

    # Add Miller Trial param
    parser.add_argument("-miller", help="Number of Miller Trials to use (default 20)", type=int)

    # Number of times to repeat test
    parser.add_argument("Repetitions", help="Number of times to repeat the experiment", type=int)

    # Number of bits RSA should use
    parser.add_argument("RSA_bits", help=f"Number of bits RSA should use for key "
                                         f"generation ({MIN_RSA_BITS}-{MAX_RSA_BITS}). A security-equivilent"
                                         " NTRU dimension will be calculated and used.", type=int)

    return parser.parse_args()




def compute_keys():
    for i in range(1024,10360, 16):
        print(f"Ca")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(3000)
    print(sys.getrecursionlimit())

    # Define command line arguments
    args = parse()

    # Get the desired RSA key bit size and truncate it accordingly
    rsa_bits = args.RSA_bits
    if (rsa_bits < MIN_RSA_BITS):
        rsa_bits = MIN_RSA_BITS
    if (rsa_bits > MAX_RSA_BITS):
        rsa_bits = MAX_RSA_BITS

    # Function auto-limits dimension size between 251-787
    ntru_dim = rsa_to_ntru(args.RSA_bits)

    print(f"Repeating experiment(s) {args.Repetitions} times. "
          f"RSA using {args.RSA_bits} bits and NTRU using {ntru_dim} dimensions.")

    # Determine # of Miller Trials
    miller_trials = MILLER_TRIALS_DEFAULT
    if (args.miller):
        miller_trials = args.miller

    if (args.key_test):
        key_test(args.Repetitions, args.RSA_bits, ntru_dim, miller_trials)

    if (args.encrypt_test):
        encrypt_test(args.encrypt_test)
