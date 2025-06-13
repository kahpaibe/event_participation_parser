"""
Small codes to help with json formatting.
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup

PATH_PAGES = Path(__file__).parent / "pages"

if __name__ == "__main__":
    # ==== process event 11 ====
    html_11 = PATH_PAGES / "11.htm"
    if html_11.exists() and False:
        with open(html_11, "rb") as f:
            content = html_11.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        table = soup.select_one("table")
        if not table:
            print("WARNING: could not find table in 11.htm")
        else:
            rows = table.select("tr")
            for row in rows:
                cols = row.select("td")

                if len(cols) == 0 or len(cols) == 1:
                    continue
                elif len(cols) == 2:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                    })
                elif len(cols) == 3:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                    })
                elif len(cols) == 4:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                        "circle_url": cols[3].get_text(strip=True),
                    })
                else:
                    print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                    continue
            with open(Path(__file__).parent / "11.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!11": circles}, f, ensure_ascii=False, indent=4)
            
    html_12 = PATH_PAGES / "12.htm"
    if html_12.exists() and False:
        with open(html_12, "rb") as f:
            content = html_12.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        table = soup.select_one("table")
        if not table:
            print("WARNING: could not find table in 12.htm")
        else:
            rows = table.select("tr")
            for row in rows:
                cols = row.select("td")

                if len(cols) == 0 or len(cols) == 1:
                    continue
                elif len(cols) == 2:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                    })
                elif len(cols) == 3:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                    })
                elif len(cols) >= 4:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                        "circle_url": cols[3].get_text(strip=True),
                    })
                else:
                    print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                    continue
            with open(Path(__file__).parent / "12.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!12": circles}, f, ensure_ascii=False, indent=4)
            
    html_14 = PATH_PAGES / "14.htm"
    if html_14.exists() and False:
        with open(html_14, "rb") as f:
            content = html_14.read_bytes()
        soup = BeautifulSoup(content, features="html.parser")

        circles = []
        table = soup.select_one("table")
        if not table:
            print("WARNING: could not find table in 12.htm")
        else:
            rows = table.select("tr")
            for row in rows:
                cols = row.select("td")

                if len(cols) == 0 or len(cols) == 1:
                    continue
                elif len(cols) == 2:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                    })
                elif len(cols) == 3:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                    })
                elif len(cols) == 4:
                    circles.append({
                        "name": cols[1].get_text(strip=True),
                        "position": cols[0].get_text(strip=True),
                        "pen_name": cols[2].get_text(strip=True),
                        "circle_url": cols[3].get_text(strip=True),
                    })
                else:
                    print(f"WARNING: too many cols, should not happen ! {len(cols)=}, {cols=}")
                    continue
            with open(Path(__file__).parent / "14.json", "w+", encoding="utf-8") as f:
                json.dump({"幺樂団カァニバル!14": circles}, f, ensure_ascii=False, indent=4)
            