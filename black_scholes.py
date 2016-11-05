from scipy.stats import norm
import math

def black_scholes(call_or_put, S, K, sig, t):
    d1 = (math.log(S/float(K)) + (sig**2)/2 * t)/(sig * t**0.5)
    d2 = d1 - sig * (t**0.5)
    C = norm.cdf(d1)*S - norm.cdf(d2)*K
    if call_or_put == 'C':
        return C
    else:
        return C + K - S

def black_scholes_derivative(S, K, sig, t):
    d1 = (math.log(S/float(K)) + (sig**2)/2 * t)/(sig * t**0.5)
    d2 = d1 - sig * (t**0.5)
    d1_derivative = (t**0.5)/2 - (math.log(S/float(K))/(t**0.5)) * (1/sig**2)
    d2_derivative = d1_derivative - t**0.5
    return norm.pdf(d1) * S * d1_derivative - norm.pdf(d2) * K * d2_derivative

def newton_estimation(call_or_put, S, K, t, C, sig=10.0, eps=0.001):
    delta = 100
    f = 100
    while (abs(delta) > eps):
        f = black_scholes(call_or_put, S, K, sig, t) - C
        f_prime = black_scholes_derivative(S, K, sig, t)
        delta = f/f_prime
        sig = sig - delta
    return sig

def rough_estimation(call_or_put, S, K, t, C, sig=0.5, inc=0.001):
    iters = 0
    f = 100
    while (abs(f - C) > 0.01 and iters < 100):
        f = black_scholes(call_or_put, S, K, sig, t)
        if f < C:
            sig += inc
        elif f > C:
            sig -= inc
    return sig

if __name__ == '__main__':
    call_or_put = 'C'
    S = 98.19
    K = 95
    t = .61
    C = 3.5
    print(rough_estimation(call_or_put, S, K, t, C))
