#pragma once
#include <cmath>
#include <vector>
#include <string>
#include <chrono>


#define RSA_t long long
#define RSA_E_LIMIT  100

namespace RSA {

    RSA_t gcd(RSA_t a, RSA_t b);

    RSA_t phi(RSA_t n);

    //calculates : a^b % t
    RSA_t encrypt(RSA_t message, RSA_t N, RSA_t key, RSA_t phi);

    //calculates : a^b % t
    RSA_t encrypt(RSA_t message, RSA_t N, RSA_t key);

    void encrypt(std::vector<RSA_t> data, RSA_t N, RSA_t key, RSA_t phi);

    std::vector<RSA_t> encode(std::string message, RSA_t n, RSA_t key, RSA_t phi);
    std::vector<RSA_t> encode(const char* msg , int size , RSA_t n, RSA_t key, RSA_t phi);


    std::string decode(std::vector<RSA_t> data, RSA_t n, RSA_t key, RSA_t phi);

    RSA_t gcdExtended(RSA_t a, RSA_t b, RSA_t* x, RSA_t* y);

    // (k * a) % b == 1 , (b > a)
    // this function calculates the k
    RSA_t modInverse(RSA_t A, RSA_t M);


    //generates the public and the private keys
    //p , q -> prime numbers
    std::pair<RSA_t, RSA_t> generateKeys(RSA_t p, RSA_t q);
}