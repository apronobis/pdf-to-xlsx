import pdfplumber
import csv

pdf_path = "input/Request of windows.pdf"
csv_path = "output/request.csv"


def filter_none(input_list):
    return [x for x in input_list if x is not None]


with pdfplumber.open(pdf_path) as pdf, open(csv_path, "w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID", "Antall", "Bredde (mm)", "Høyde (mm)", "Brannkrav", "Pris"])
    for page in pdf.pages:
        for table in page.extract_tables():
            while len(table) and table[0][0] != "ID":
                table.pop(0)
            if len(table):
                _id = filter_none(table[0])[1:]
                antall = filter_none(table[1])[1:]
                bxh = filter_none(table[3])[1:]
                b = [item.replace(" ", "").split("×")[0] for item in bxh]
                h = [item.replace(" ", "").split("×")[-1] for item in bxh]
                brannkrav = [item or "---" for item in filter_none(table[10])[1:]]
                for row in zip(_id, antall, b, h, brannkrav):
                    writer.writerow(row)
