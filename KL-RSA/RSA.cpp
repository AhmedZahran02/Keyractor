#include "RSA.h"

//your good old gcd function
RSA_t RSA::gcd(RSA_t a, RSA_t b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}


//calculate the number of co-prime numbers to n
//never used , but is a good to have XD
RSA_t RSA::phi(RSA_t n) {
    RSA_t result = n;
    for (RSA_t i = 2; i <= sqrt(n) + 1; i++) {
        if (n % i == 0) {
            while (n % i == 0) {
                n /= i;
            }
            result -= result / i;
        }
    }
    if (n > 1) {
        result -= result / n;
    }
    return result;
}

//checks if a * b will overflow
static bool isOverflow(RSA_t a, RSA_t b) {
    if (a == 0 || b == 0)
        return false;

    long long result = a * b;
    if (a == result / b)
        return false;
    else
        return true;
}

//calculates (a * b) % k , while avoiding overflowing
// if k is big enough , it WILL overflow , so keep this
// in mind while using it 
static RSA_t mulMod(RSA_t a, RSA_t b, RSA_t k) {
    a = a % k;
    b = b % k;
    if (isOverflow(a , b)) {
        RSA_t mi = std::min(a, b);
        RSA_t ma = std::max(a, b);
        RSA_t m = mulMod(mi , ma / 2 , k);
        m = (m + m) % k;
        if (ma % 2 == 1) m = (m + mi) % k;
        return m;
    }
    return (a * b) % k;
}

//calculates : a^b % t , with the help of phi (it makes things alot faster)
RSA_t RSA::encrypt(RSA_t message, RSA_t N, RSA_t key, RSA_t phi) {
    if (phi < 1) {
        return encrypt(message, N, key);
    }
    return encrypt(message, N, key % phi);
}

//calculates : a^b % t but without phi
// O(log(n)) --> 64 at most
RSA_t RSA::encrypt(RSA_t message, RSA_t N, RSA_t key) {
    if (key == 0)
        return 1;
    if (key == 1)
        return message % N;

    RSA_t hM = encrypt(message, N, key / 2);
    hM = mulMod(hM, hM, N);
    if (key % 2 == 1) {
        hM = mulMod(hM , message % N , N);
    }

    return hM;
}

//encrypts/decrypts a stream of data
void RSA::encrypt(std::vector<RSA_t> data, RSA_t N, RSA_t key, RSA_t phi) {
    for (int i = 0; i < data.size(); i++) {
        data[i] = encrypt(data[i], N, key, phi);
    }
}

//encodes a string message
std::vector<RSA_t> RSA::encode(std::string message, RSA_t n, RSA_t key, RSA_t phi) {
    std::vector<RSA_t> data(message.length());
    for (int i = 0; i < message.length(); i++) {
        data[i] = encrypt(message.c_str()[i], n, key, phi);
    }
    return data;
}

//encodes a message
std::vector<RSA_t> RSA::encode(const char* message , int size , RSA_t n, RSA_t key, RSA_t phi) {
    std::vector<RSA_t> data(size);
    for (int i = 0; i < size; i++) {
        data[i] = encrypt(message[i], n, key, phi);
    }
    return data;
}

//decodes a message from data
std::string RSA::decode(std::vector<RSA_t> data, RSA_t n, RSA_t key, RSA_t phi) {
    std::string str;
    RSA_t t;
    for (int i = 0; i < data.size(); i++) {
        t = encrypt(data[i], n, key, phi);
        str += ((char)(t));
    }
    return str;
}


//calculates the mod invers
RSA_t RSA::modInverse(RSA_t A, RSA_t M){
    RSA_t x, y;
    RSA_t g = gcdExtended(A, M, &x, &y);
    if (g != 1)
        return -1;
    else {
        return (x % M + M) % M;
    }
}

//gcd , but it memorizes the steps , to calculate the mod inverse
RSA_t RSA::gcdExtended(RSA_t a, RSA_t b, RSA_t* x, RSA_t* y){
    if (a == 0) {
        *x = 0, * y = 1;
        return b;
    }
    RSA_t x1, y1;
    RSA_t gcd = gcdExtended(b % a, a, &x1, &y1);
    *x = y1 - (b / a) * x1;
    *y = x1;

    return gcd;
}

//generates a pair of keys
// first --> public key
// second --> private key (but its interchangable)
std::pair<RSA_t, RSA_t> RSA::generateKeys(RSA_t p, RSA_t q) {
    RSA_t pN = (p - 1) * (q - 1);

    //calculate the e variable
    //I select a random one between the avaiable ones to make the algorethm extra spicy
    std::vector<RSA_t> possiable_e;
    for (RSA_t i = 2; i < pN; i++) {
        if (gcd(i, pN) == 1) {
            possiable_e.push_back(i);
            if (possiable_e.size() == RSA_E_LIMIT)
                break;
        }
    }

    //some spicy randomness to the equation cuz why not
    srand(time(0));

    //public key
    RSA_t e = possiable_e[rand() % possiable_e.size()];

    //private key
    // { (e * d) % pN == 1 } , we need to get d thru inverse modular
    RSA_t d = modInverse(e, pN);

    return { e , d };
}