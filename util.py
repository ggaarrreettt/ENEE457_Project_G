"""
 :: Util file
 :: 
 :: @ Author : Nicholas Mastandrea, Garrett Amos, Daniel Park 
"""
import random 

def compute_low_level_prime(number_of_bits):
    """
    First test to check that the generated number is prime uses the prime list and checks 
    that none divide the generated numeber
    """

        # Pre generated primes
    first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
                        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 
                        151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
                        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 
                        317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 
                        419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 
                        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 
                        607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661 ,673, 677, 683, 691, 
                        709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 
                        821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
                        919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009]

    def generate_random_n_bit(number_bits):
        #Generates a n bit long random number
        return random.randrange(2**(number_bits-1) + 1, 2**(number_bits) - 1)

    # First to check if it is prime efficiently we comapre it against the first few prime numbers
    while True:
        possible_prime = generate_random_n_bit(number_of_bits)
        for  divisor in first_primes_list:
            if possible_prime % divisor == 0 and divisor**2 <= possible_prime:
                break
        else:
            return possible_prime
    

def is_miller_rabin_passed(miller_rabin_candidate, number_of_trials):
        """
        The miller Rabin Test ...
        """
        max_divisin_by_two = 0
        even_component = miller_rabin_candidate - 1

        while (even_component % 2 == 0):
            even_component >>= 1
            max_divisin_by_two +=1

        assert(2**max_divisin_by_two * even_component == miller_rabin_candidate -1)

        def trial_composite(round_tester):
            if pow(round_tester, even_component, miller_rabin_candidate) == 1:
                return False
            for i in range(max_divisin_by_two):
                if (pow(round_tester, 2**i * even_component, miller_rabin_candidate) ==
                    miller_rabin_candidate - 1):
                    return False
            return True
        
        for i in range(number_of_trials):
            round_tester = random.randrange(2,miller_rabin_candidate)
            if trial_composite(round_tester):
                return False
        return True 
    

def generate_n_bit_prime(number_of_bits, numbe_of_trials):
    """
    Combines above methodology to effieciently compute a prime number
    """
    while True:
        possible_prime = compute_low_level_prime(number_of_bits)
        if not is_miller_rabin_passed(possible_prime, numbe_of_trials):
            continue 
        else:
            return possible_prime

def generate_p_and_q(number_of_bits_p: int, 
                     number_of_bits_q: int, 
                     number_of_trials: int):
    """
    Generates two prime numbers that are not equal, such that
    1 should be much larger than p for the NTRU methodology 
    """
    p = generate_n_bit_prime(number_of_bits_p, number_of_trials)
    q = generate_n_bit_prime(number_of_bits_q, number_of_trials)

    while p == q:
        # If you choose to have p and q be the same number of bits
        q = generate_n_bit_prime(number_of_bits_q, number_of_trials)
    return p, q

def string_to_bits(string:str) -> [int]: 
    bits = bin(int.from_bytes(string.encode(), 'big'))[2:]
    return list(map(int, bits.zfill(8 * ((len(bits) + 7) // 8))))

def bits_to_string(bits: [int]) -> str:
    n = int(''.join(map(str, bits)), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
