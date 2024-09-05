from collections import defaultdict
from request import get_request
from offer_1 import get_offer_1
from offer_2 import get_offer_2
from offer_3 import get_offer_3
from xlsx_utils import write_to_xlsx


PDF_PATH = "input/Request of windows.pdf"
XLSX_PATH = "output/request.xlsx"

windows = defaultdict(lambda: defaultdict(list))

for row in get_request(PDF_PATH):
    windows[row[0]]["Request windows"] = row[1:]

for row in get_offer_1("input/Window Offer 1.pdf"):
    windows[row[0]]["Offer 1"].append(row[1:])

for row in get_offer_2("input/Window Offer 2.pdf"):
    windows[row[0]]["Offer 2"].append(row[1:])

for row in get_offer_3("input/Window Offer 3.PDF"):
    windows[row[0]]["Offer 3"].append(row[1:])


def is_similar(request, offer):
    return abs(request[1] + request[2] - offer[1] - offer[2]) < 10


for i, (_id, window) in enumerate(windows.items()):
    for k, v in window.items():
        if k == "Request windows":
            continue

        if len(v) > 1:
            if len(v) == 3 and v[2][-1] < 1000:
                v[2][-1] = v[0][-1] + v[1][-1]
                row = v[2]
            else:
                next_id, next_window = list(windows.items())[i + 1]
                if "Request windows" in next_window and is_similar(
                    next_window["Request windows"], v[-1]
                ):
                    windows[next_id][k].append(v.pop())
                else:
                    row = [v[0][0], "", "=MAX(", *v[0][3:-1], ""]
                    for item in v:
                        row[1] += f"+{item[1]}"
                        row[2] += f"{item[2]},"
                        row[-1] += f"+{item[-1]}"
                    row[1] = "=" + row[1][1:]
                    row[2] = row[2][:-1] + ")"
                    row[-1] = "=" + row[-1][1:]
                    v = [row]

        window[k] = v[0]

write_to_xlsx(windows)
