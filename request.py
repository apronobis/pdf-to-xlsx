import pdfplumber


def get_request(pdf_path):
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                while len(table) and table[0][0] != "ID":
                    table.pop(0)

                if not len(table):
                    continue

                table[2][0], table[3][0] = "Bredde (mm)", "Høyde (mm)"
                table = list(zip(*table[:15]))

                if not rows:
                    rows.append(table[0])

                for row in table[1:]:
                    if not row[0]:
                        continue

                    row = list(row)
                    row[1] = int(row[1])

                    if row[3] == "---":
                        row[2] = row[3]
                    else:
                        row[2], row[3] = map(int, row[3].replace(" ", "").split("×"))

                    rows.append(row)

    return rows
