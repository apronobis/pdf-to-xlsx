import re
import pdfplumber

pat_bh = r"\d{3,4}x \d{3,4}"
pat_pris = r"\d+ \d{3}"


def get_next_line(lines, field):
    iter_lines = iter(lines)
    while next(iter_lines, field) != field:
        pass
    return next(iter_lines, "---")


def get_offer_1(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        rows = [
            [
                "ID",
                "Antall",
                "Bredde (mm)",
                "Høyde (mm)",
                "Type",
                "Maling",
                "Alu. bekledning",
                "Pris",
            ]
        ]

        for page in pdf.pages[2:]:
            text = page.extract_text()
            lines = text.splitlines()

            match = re.search(pat_bh, lines[7])
            row = [get_next_line(lines, "Ref nr:"), int(lines[7].split(" ")[1])]
            row.extend(map(int, match.group().split("x ")))
            row.append(" ".join(lines[7][: match.start()].split(" ")[2:-1]))
            row.append(get_next_line(lines, "Maling:").split(": ")[1])
            row.append(get_next_line(lines, "Alu. bekledning:"))
            row.append(int(lines[7].split("N")[-1].replace(" ", "")))

            rows.append(row)

    return rows
