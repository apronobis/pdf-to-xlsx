import pdfplumber
import re
import csv

pdf_path = "input/Window Offer 3.PDF"
csv_path = "output/offer_3.csv"
pat_bh = r"\d{3,4}x\d{3,4}"


with pdfplumber.open(pdf_path) as pdf, open(csv_path, "w") as out:
    writer = csv.writer(out)
    writer.writerow(["Tegning", "Ant", "Bredde (mm)", "Høyde (mm)", "Brannsikret"])
    tegnings = []
    row = []
    for page in pdf.pages:
        text = page.extract_text()
        pre_line = ""
        for line in text.splitlines():
            if line.startswith("V_"):
                tegning = line.split(" ")[0]
                if tegning not in tegnings:
                    if row:
                        row.append(brannsikret)
                        writer.writerow(row)
                    brannsikret = "---"
                    row = [tegning]
                    tegnings.append(tegning)
            match = re.search(pat_bh, line)
            if match:
                ant = line.split("x")[1].split(" ")[1].split(",")[0]
                row.append(ant)
                row.extend(match.group().split("x"))
            if line == "BRANNSIKRET":
                brannsikret = pre_line.split(" ")[1]
            pre_line = line
