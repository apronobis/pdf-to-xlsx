import pdfplumber
import re
import csv

pdf_path = "input/Window Offer 1.pdf"
csv_path = "output/offer_1.csv"
pat_bh = r"\d{3,4}x \d{3,4}"


def get_next_line(lines, field):
    iter_lines = iter(lines)
    while next(iter_lines, field) != field:
        pass
    return next(iter_lines, "---")


with pdfplumber.open(pdf_path) as pdf, open(csv_path, "w") as out:
    writer = csv.writer(out)
    writer.writerow(
        ["Rad", "Ref nr", "Antall", "Bredde (mm)", "Høyde (mm)", "Klassifisering"]
    )
    for page in pdf.pages[2:]:
        text = page.extract_text()
        lines = text.splitlines()
        row = lines[7].split(" ")[:2]
        row.extend(re.search(pat_bh, lines[7]).group().split("x "))
        row.insert(1, get_next_line(lines, "Ref nr:"))
        row.append(get_next_line(lines, "Klassifisering:"))
        writer.writerow(row)
