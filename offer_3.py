import pdfplumber
import re

pat_bh = r"\d{3,4}x\d{3,4}"


def get_offer_3(pdf_path):
    rows = [
        [
            "ID",
            "Antall",
            "Bredde (mm)",
            "Høyde (mm)",
            "Beskrivelse",
            "Utvendig",
            "Innvendig",
            "Pris",
        ]
    ]

    with pdfplumber.open(pdf_path) as pdf:
        tegnings = []
        row = []
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.splitlines():
                if line.startswith("V_"):
                    tegning = line.split(" ")[0]
                    if tegning not in tegnings:
                        if row:
                            rows.append(row)
                        row = [tegning]
                        tegnings.append(tegning)
                if line.startswith("Utvendig"):
                    row.insert(-1, line[9:])
                if line.startswith("Innvendig"):
                    row.insert(-1, line[10:])
                if len(row) == 5:
                    row.insert(-1, line)
                match = re.search(pat_bh, line)
                if match:
                    ant = int(line.split("x")[1].split(" ")[1].split(",")[0])
                    row.append(ant)
                    row.extend(map(int, match.group().split("x")))
                    row.append(" ".join(line.split(" ")[-2:]))
    return rows
