#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>

#include "RSA.h"


//command: RSA.exe N public_key_int object_size src_path dst_path
int main(int argc , char** argv) {
	if (argc != 6)
		return -1;

	std::cout << argv[1] << std::endl;
	std::cout << argv[2] << std::endl;
	std::cout << argv[3] << std::endl;
	std::cout << argv[4] << std::endl;
	std::cout << argv[5] << std::endl;

	
	RSA_t N   = strtoll(argv[1], nullptr, 10);
	RSA_t key = strtoll(argv[2], nullptr, 10);
	int chunk =  strtol(argv[3], nullptr, 10);

	std::cout << sizeof(RSA_t) << std::endl;
	std::cout << sizeof(RSA_t) - chunk + 1 << std::endl;

	const char* src_path = argv[4];
	const char* dst_path = argv[5];

	std::ifstream src(src_path, std::ios::binary);
	if (!src.is_open()) {
		std::cout << "bad src file" << std::endl;
		return -1;
	}

	std::vector<char> src_bytes(
		(std::istreambuf_iterator<char>(src)),
		(std::istreambuf_iterator<char>()));

	src.close();

	std::ofstream dst(dst_path, std::ios::binary);
	if (!dst.is_open()) {
		std::cout << "bad dst file" << std::endl;
		return -1;
	}

	RSA_t tmp;
	char buff;
	int pos = 0;

	for (char c : src_bytes) {
		if (pos == 0) {
			tmp = 0;
		}
		RSA_t bits = ((RSA_t)c) << (pos * 8);
		tmp = tmp | (bits & (((RSA_t) 0xff) << (pos++ * 8)));
		if (pos == chunk) {
			pos = 0;
			RSA_t res = RSA::encrypt(tmp, N, key);
			for (int i = 0; i < sizeof(RSA_t) - chunk + 1; i++) {
				buff = res;
				res = res >> 8;
				dst.write(&buff, 1);
			}
		}
	}

	dst.close();
}