import pdfplumber
import re
import csv

pdf_path = "input/Window Offer 2.pdf"
csv_path = "output/offer_2.csv"
pat_bh = r"\d{3,4}×\d{3,4}"


with pdfplumber.open(pdf_path) as pdf, open(csv_path, "w") as out:
    writer = csv.writer(out)
    writer.writerow(["Lnr", "Mrk", "Ant", "Bredde (mm)", "Høyde (mm)", "Brannprodukt"])
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.splitlines()
        match = re.search(pat_bh, lines[3])
        if match:
            row = lines[3].split(" ")[:3]
            if row[1].endswith("-"):
                row[1] += lines[4].split(" ")[0]
            row.extend(match.group().split("×"))
            brannprodukt = "---"
            for line in lines:
                if "Passiv Brannprodukt" in line:
                    brannprodukt = line.split(" ")[0]
            row.append(brannprodukt)
            writer.writerow(row)
