import pdfplumber
import re

pat_bh = r"\d{3,4}×\d{3,4}"


def get_offer_2(pdf_path):
    rows = [
        [
            "ID",
            "Antall",
            "Bredde (mm)",
            "Høyde (mm)",
            "Utvendig",
            "Innvendig",
            "Brannprodukt",
            "Pris",
        ]
    ]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.splitlines()
            match = re.search(pat_bh, lines[3])

            if match:
                row = lines[3].split(" ")[1:3]
                if row[0].endswith("-"):
                    row[0] += lines[4].split(" ")[0]
                row[0] = "V_B" + row[0][1:]
                row[1] = int(row[1])
                row.extend(map(int, match.group().split("×")))
                for line in lines:
                    if line.startswith("Utvendig RAL"):
                        row.append(line[9:])
                    if line.startswith("Innvendig RAL"):
                        row.append(line[10:])
                    if "Passiv Brannprodukt" in line:
                        row.append(line)
                while len(row) < 7:
                    row.append("---")
                row.append(int(lines[3].split("mm")[-1].replace(" ", "")))

                rows.append(row)

    return rows
