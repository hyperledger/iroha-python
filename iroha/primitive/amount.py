from iroha.helper import logger
from schema.primitive_pb2 import Amount, uint256

UINT64_NUMBER = int(18446744073709551616)

def amount2int(amount):
    logger.debug("amount2int")
    res = int(0)
    res += int(amount.value.first)
    res *= UINT64_NUMBER
    logger.debug(res)
    res += int(amount.value.second)
    res *= UINT64_NUMBER
    logger.debug(res)
    res += int(amount.value.third)
    res *= UINT64_NUMBER
    logger.debug(res)
    res += int(amount.value.fourth)
    return res


def int2amount(int_num,precision=0):
    logger.debug("int2amount")
    value = uint256()
    value.fourth = int(int_num % UINT64_NUMBER)
    int_num //= UINT64_NUMBER
    value.third = int(int_num % UINT64_NUMBER)
    int_num //= UINT64_NUMBER
    value.second = int(int_num % UINT64_NUMBER)
    int_num //= UINT64_NUMBER
    value.first = int(int_num)
    return Amount(
        value = value,
        precision = precision
    )
