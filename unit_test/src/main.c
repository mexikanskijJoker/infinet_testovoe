#include "testy/func.h"
#include "testy/func_cust.h"

int main() {
	if (func_ok(1, 1)) {
		return customer_check(5);
	}

	return 0;
}
