

# Min and max are inclusive
def get_true_random_numbers(amount, min, max) -> list:
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


def generate_code_page():
    # Each page contains 150 random numbers
    random_nos = get_true_random_numbers(150, 0, 35)
    blocks = []

    list_index = 0
    for i in range(10):
        current_numbers = []
        for j in range(15):
            current_numbers.append(random_nos[list_index])
            list_index += 1

        current_numbers = [str(x) for x in current_numbers]
        block = "\t" + " & ".join(current_numbers) + " \\\\"
        block = block + """
        \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U & \\U \\\\
        \\\\
        """

        blocks.append(block)

    blocks = "\\hline \\\\\n".join(blocks)

    page = f"""
    \\begin{{flushleft}}
    \\begin{{tabular}}{{c c c c c @{{\\hskip 2em}} c c c c c @{{\\hskip 2em}} c c c c c}}
    {blocks}
    \\end{{tabular}}
    \\end{{flushleft}}
    \\newpage
    """

    return page


if __name__ == "__main__":
    number_of_pages = 20
    pages = []
    for i in range(number_of_pages):
        pages.append(generate_code_page())
        print(f"Generated {i+1}/{number_of_pages} code pages.")

    with open("codebook-template.txt", "r") as infile:
        template = infile.read()

    pages_str = "\n".join(pages)
    finished_pages = template.replace("<pageshere>", pages_str)

    with open("codepages.tex", "w") as outfile:
        outfile.write(finished_pages)