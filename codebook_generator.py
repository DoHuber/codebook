

# Min and max are inclusive
def get_true_random_numbers(amount, min, max):
    numbers = []
    while len(numbers) < amount:
        # Get fresh randomness and process
        with open("/dev/hwrng", "rb") as rng:
            bytes = rng.read(64)

        for byte in bytes:
            # Rejection sampling to avoid modulo bias
            if min <= byte <= max:
                numbers.append(byte)

            if len(numbers) == amount:
                break

    return numbers


if __name__ == "__main__":
    numbers = get_true_random_numbers(256, 0, 35)
    print(numbers)
    print(f"Length/Min/Max: {len(numbers)}/{min(numbers)}/{max(numbers)}")
    print(f"Average: {sum(numbers)/len(numbers)}")