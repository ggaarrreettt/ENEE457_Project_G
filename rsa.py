from util import *
import math 
from CONSTANTS import *
def populate_p_and_q(number_of_bits, number_of_trials):
    """
        | Generate two n/2-bit random prime numbers that are not equal
    """
    bits = int(number_of_bits / 2)

    p = generate_n_bit_prime(bits, number_of_trials)
    q = generate_n_bit_prime(bits, number_of_trials)

    while p == q:
        q = RSA.generate_n_bit_prime(number_of_bits, number_of_trials)
    return p, q

def compute_cipher_text(message     : str, 
                        public_key  : int, 
                        n           : int):
        """
         | Encrypts the message using another users public key
        """ 
        # (m ^ pub key) mod n = c
        message_encoded = [ord(c) for c in message] 
        return [pow(c, public_key, n) for c in message_encoded]

class RSA():
    def __init__(self, 
                 number_of_bits   : int,
                 number_of_trials : int,
                 display_mode     : bool):
        """
         | First generate P and Q, we know their product must be n-bits which
         | is our defined key length, therefore we can say that if the lg(p) and
         | lg(q) gives the number of bits (assuming the log result in an integer)
         | then we can use the fact that p*q -> lg(p*q) = lg(p) + lg(q) to assert
         | p and q should be half the size of n 
        """
        self.p, self.q  = populate_p_and_q(number_of_bits // 2, number_of_trials) # can make all this one line ...
        self.n          = self.p * self.q
        self.phi_n      = (self.p - 1) * (self.q - 1)

        self.pub_key = random.randrange(3, self.phi_n)
        while math.gcd(self.pub_key, self.phi_n) != 1:
            self.pub_key = random.randrange(3, self.phi_n)
        self.priv_key = self.gen_private_key()

        if display_mode:
            print('p value:', self.p)
            print('q value:', self.q)
            print('phi value:', self.phi_n)
            print('pub key:', self.pub_key)
            print('priv key:', self.priv_key)
            print('modular proof:', (self.priv_key*self.pub_key) % self.phi_n)


    def gen_private_key(self):
        """
         : Uses algebra to come up with a faster alternative to using a random
         : seed for. mod_inverse. Since the public key is picked to be coprime with
         : the phi, the mod inverse formula can be rewritten as ...
         : e*d - k*phi(N) = 1 where k is some integer value.
         : d: (1+k*phi(N))/e
         : 
         : If we want an n bit number or greater then k*phi(N) should be greater than
         : 2^n (This is done because longer private keys are more secure)
        """

        def extended_euclid_algorithim(a, b):
            """
             |
            """
            if b == 0:
                return a, 1, 0
            else:
                d2, x2, y2 = extended_euclid_algorithim(b, a % b)
                d, x, y, = d2, y2, x2 - (a // b) * y2 
                return d, x, y

        return extended_euclid_algorithim(self.pub_key, self.phi_n)[1] % self.phi_n

    def share_public_information(self):
        """
         | Exports the public key
        """
        return self.pub_key, self.n

    def compute_plaintext(self, ciphertext):
        """
         : Uses the generated private key to 
        """

        message = [pow(int(c), self.priv_key, self.n) for c in ciphertext]
        return "".join(chr(c) for c in message) 
    
        
if __name__ == "__main__":
    myRSA = RSA(2048, MILLER_TRIALS_DEFAULT, False)
    message = "my message that is secret"
    pub, n = myRSA.share_public_information()
    ctext = compute_cipher_text(message, pub, n)
    assert(message == myRSA.compute_plaintext(ctext))
    print("success")
    