from sympy import Poly, symbols, GF, invert
import random

def remove_leading_zeros(polynomial: [int]) -> [int]:
    while polynomial[0] == 0:
        polynomial.pop(0)
    return polynomial

def pad_to_fit(N:int, polynomial: [int]) -> [int]:
    if len(polynomial) % N:
       polynomial = ([0] * (N - (len(polynomial)) % N)) + polynomial
    return polynomial


def generate_poly_mod(degree: int) -> [int]:
    """
    Generates a polynomial of the form X^N - 1

    Useful for perfromaing the convolution ooperator using modular arithmetic
    """
    poly_mod        = [0] * (degree + 1) 
    poly_mod[0]     = 1
    poly_mod[-1]    = -1
    return poly_mod


def poly_inverse(modular: int, N: int, poly_in: [int], poly_mod: [int]):
    """
    The poly inverse function find the multiplicative polynomial invers of a function
    defind by the ring of R_q = (Z/mZ)[X]/(poly_mod) where m in this case will either be
    p or q. For our purposes, p and q should always be prime numbers as it makes the 
    inverse simpler.

    If no poly mod function is inputted it will defualt to X^N - 1 where, N is a degree
    one higher than the maximum degree of the input function. For example

    poly_in : [-1, 0, -1, 0, -1, 0, 1, 0, 1, 1, 1] -> -X^10 + -X^8 + -X^6 +X^4 + X^2 + X + 1
    poly_mod: None -> [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1] -> X^11 - 1
    modular : 3
    output  : [1, 0, 1, 0, 1, 2, 2, 2, 1, 0] -> X^9 + X^7 + X^5 + 2*X^4 + 2*X^3 + 2*X^2 +X
    """

    if poly_mod == None:
        poly_mod = generate_poly_mod(N)
    x       = symbols('x')
    poly_m2 = Poly(poly_mod,x)

    # IMPORTANT: Assumes mod input will be a prime number since our p and q willl be prime numbers 
    try:
        inv = invert(Poly(poly_in,x).as_expr(), poly_m2.as_expr(), domain=GF(modular,symmetric=False))
        return Poly(inv,x).all_coeffs()
    except:
        return None


def generate_random_poly(max_degree: int) -> [int]:
    """
    Random polynomials should be generated with coefficents ranging in the set {-1,0,1}
    """
    random_poly = [0] * max_degree
    for i in range(max_degree):
        random_poly[i] = random.randint(-1,1)
    return random_poly


def generate_f_keys(p: int, q: int, max_degree: int)-> [[int], [int], [int]]:
    """
    The random polynomials generated in the set for the private key should be invertible
    for the circular modulation with both p and q, therefore after generating the random
    polynmial it is useful to check that the inverse exists, otherwise need to calculate a
    new random polynomial  
    """ 
    f_p, f_q = None, None 
    while f_p == None or f_q ==None:
        f   = generate_random_poly(max_degree) 
        f_p = poly_inverse(p, max_degree, f, None)
        f_q = poly_inverse(p, max_degree, f, None)
    return f, f_p, f_q


def generate_public_key(q: int, N: int, g: [int], f_q: [int]) -> [int]:
    """
    h congruent g*f_q mod q

    where we simpligy the convolution in the ring of (Z/qZ)[X]/(X^N -1)
    such that g * f_q is the same as g x f_q mod X^N - 1
    """
    x = symbols('x')
    poly_mod = generate_poly_mod(N)

    h = ((Poly(g,x)*Poly(f_q,x)) % Poly(poly_mod, x)).all_coeffs()
    s = len(h)
    for i in range(s):
        h[i] = h[i] % q
    return h 


def encryption(p: int, q:int, N:int, r: [int], h: [int], message: [int]) -> [int]:
    """
    
    """
    x               = symbols('x')
    poly_mod        = generate_poly_mod(N)
    degree_message  = len(message)

    e = ((Poly(h,x)*Poly(r,x)) % Poly(poly_mod, x)).all_coeffs()
    s = len(e)
    for i in range(s):
        if degree_message - N + i >= 0:
            m = message[degree_message - N + i] 
        else:
            m = 0 
        e[i] = (p*e[i] + m) % q
    return e


def decryption(p:int, q:int, N: int, e: [int], f: [int], f_p: [int]):
    """
    
    """
    x = symbols('x')
    poly_mod = generate_poly_mod(N)

    a = ((Poly(f,x) * Poly(e,x)) % Poly(poly_mod, x)).all_coeffs()
    s = len(a)
    for i in range(s):
        center_val  = q // 2
        temp        = a[i] % q
        a[i]        = temp if temp <= center_val else temp - q 

    m           = ((Poly(a,x) * Poly(f_p,x)) % Poly(poly_mod, x)).all_coeffs()  
    center_val  = p // 2
    s           = len(m)
    for i in range(s):
        temp        = m[i] % p
        m[i]        = temp if temp <= center_val else temp - p 
    return m 
 

if __name__ == "__main__":
    # Recretaing math in test demo to check
    f = [-1, 0, -1, 0, -1, 0, 1, 0, 1, 1, 1]
    g = [-1, -1, 0, -1, 0, 1, 0, 1, 0, 1]
    r = [-1,0,1,0,0,1,-1,0,0,1]
    m = [1,0,0,-1,1,0,1,1]
    f_p = poly_inverse(3, 11, f, None) 
    f_q = poly_inverse(61, 11, f, None)
    h   = generate_public_key(61, 11, g, f_q)
    e   = encryption(3, 61, 11, r ,h, m)
    m2  = remove_leading_zeros(decryption(3, 61, 11, e, [-1, 0, -1, 0, -1, 0, 1, 0, 1, 1, 1], f_p))
    assert (m2 == m)
    print("Test worked")
