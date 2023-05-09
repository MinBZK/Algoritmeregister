import random


def find_new_upc(avoid_upc_list: list[str]) -> str:
    upc = "0"
    attempt_limiter = 0
    while True:
        upc = generate_upc()
        if upc not in avoid_upc_list:
            break

        attempt_limiter += 1
        if attempt_limiter > 1000:
            raise RuntimeError("Unable to generate valid UPC")
    return upc


def generate_upc() -> str:
    """Generates a UPC Code.

    The code is eight numbers. The first seven are generated randomly, the last one is a control number based on the
    first seven.

    The control value is calculated as: (even entries)*3 + (odd entries) mod 10. The resulting code does not have any
    near neighbours; changing a single number, or swapping two numbers will result in an invalid UPC code.

    This can be used to generate ID's for distinct objects. It then reduces the chance of accidentally accessing another
    entry due to typing errors.
    """
    rl: list[int] = [random.randint(1, 9) for each in range(0, 7)]

    e: int = rl[0] + rl[2] + rl[4] + rl[6]
    o: int = rl[1] + rl[3] + rl[5]
    control_value: int = (e * 3 + o) % 10
    rl.append(control_value)

    upc_string: str = "".join(list(map(str, rl)))
    return upc_string


def validate_upc(code: str) -> bool:
    """Validates a UPC code.

    See generate_upc() on how the code is built up. This function checks if the code complies
    with the generation logic."""
    try:
        int(code)
    except (ValueError, TypeError):
        return False

    if len(code) != 8:
        return False

    r: str = code
    e: int = int(r[0]) + int(r[2]) + int(r[4]) + int(r[6])
    o: int = int(r[1]) + int(r[3]) + int(r[5])
    c: int = (e * 3 + o) % 10
    return True if c == int(r[7]) else False
