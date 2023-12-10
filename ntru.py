from polyutil import *
from util import * 
from CONSTANTS import *
class NTRU():
    def __init__(self, 
                 dimensions     : int,
                 bits_p         : int,
                 bits_q         : int,
                 miller_trials  : int) -> None:
        """
        TODO : add keywrd args paramater so we can use the same key over and over
        instead of generating new keys everytime 
        """
        self.N                      = dimensions
        self.p, self.q              = generate_p_and_q(bits_p, bits_q, miller_trials)
        self.f, self.f_p, self.f_q  = generate_f_keys(self.p, self.q, dimensions)
        self.g                      = generate_random_poly(dimensions)
        self.h                      = generate_public_key(self.q, dimensions, self.g, self.f_q)

    def release_public_information(self) -> [int, int, int, [int]]:
        return self.p, self.q, self.N, self.h 
    
    def encrypt_plaintext(self, message: str, **kwargs) -> [int]:
        """
        Since it would be more practical to encrypt another persons message
        using there public key infromation, if kwargs is present will encrypt 
        using the parameters there. Otherwise for testing/demonstration purpose
        will use the own public key infroation to do encryption
        """
        if kwargs:
            pass
        else:
            p = self.p 
            q = self.q
            N = self.N
            h = self.h

        m               = pad_to_fit(N, string_to_bits(message))
        encrypted_arr   = []

        for block in range(len(m) // N):
            r               = generate_random_poly(N)
            msg_block       = m[block*N:(block+1)*N]
            encrypted       = encryption(p, q, N, r, h, msg_block)
            encrypted_arr   += encrypted
        return encrypted_arr

    def decrypt_ciphertext(self, ciphertext: [int]) -> str:
        """
        Uses 
        """

        msg_arr = []
        for block in range(len(ciphertext) // self.N):
            enc_block   = ciphertext[block*self.N:(block+1)*self.N]
            msg_block   = decryption(self.p, self.q, self.N, enc_block, self.f, self.f_p)
            msg_arr     += msg_block
        return bits_to_string(msg_arr)

if __name__ == "__main__":

    
    message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor" + \
               "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud" + \
               "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis" + \
               "aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu" + \
               "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in" + \
               "culpa qui officia deserunt mollit anim id est laborum."

    ntru = NTRU(100, 3, 97, MILLER_TRIALS_DEFAULT)
    e = ntru.encrypt_plaintext(message)
    m = ntru.decrypt_ciphertext(e)
    print(m)