"""
Parse https://ttc.ninja-web.net/vo-para/vo-para{...} urls
"""
import requests
from bs4 import BeautifulSoup, Tag
from pathlib import Path
import time
import json
import re
from abc import abstractmethod, ABC

from typing import TypeAlias, Optional, Any
from dataclasses import dataclass, field

# =========================================================================
# Type and dataclass definitions
# =========================================================================
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

@dataclass
class VPCircleInfoABC(ABC):
    name: Optional[str] = None
    pen_name: Optional[str] = None
    position: Optional[str] = None
    block: Optional[str] = None
    circle_url: Optional[str] = None

    @abstractmethod
    def get_json(self) -> dict[str, Any]:
        """Get json representation of the circle"""
        raise NotImplementedError

@dataclass
class VPCircleInfoType1(VPCircleInfoABC): # vopara, vopara2~5
    name: Optional[str] = None
    pen_name: Optional[str] = None
    position: Optional[str] = None
    block: Optional[str] = None
    circle_url: Optional[str] = None

    def get_json(self) -> dict[str, Any]:
        """Get json representation of the circle"""
        return {
            "name": self.name,
            "pen_name": self.pen_name,
            "position": self.position,
        }

@dataclass
class VPCircleInfoType2(VPCircleInfoABC): # vopara6~...
    name: Optional[str] = None
    pen_name: Optional[str] = None
    position: Optional[str] = None
    block: Optional[str] = None
    circle_url: Optional[str] = None

    main_character: Optional[str] = None

    def get_json(self) -> dict[str, Any]:
        """Get json representation of the circle"""
        return {
            "name": self.name,
            "pen_name": self.pen_name,
            "position": self.position,
            "main_character": self.main_character,
        }

@dataclass
class VPEventInfo:
    """Info about one event"""
    name: Optional[str] = None
    header_text: Optional[str] = None
    circles: list[VPCircleInfoABC] = field(default_factory=list)

    def get_json(self) -> dict[str, Any]:
        """Get json representation of the event"""
        circle_jsons = [circle.get_json() for circle in self.circles]
        return {
            "name": self.name,
            "header_text": self.header_text,
            "circles": circle_jsons,
        }

VPEvents: TypeAlias = dict[str, dict[str, Any]] # {url (str): event_info_json (dict), ...}

# =========================================================================
# Processing related definitions
# =========================================================================

def LOG(txt: str) -> None:
    """Action to do when logging info."""
    print(txt)

class VPCrawler:
    """Class to retrieve html pages."""
    decode_error_count = 0

    def __init__(self) -> None:
        pass

    def fetch(self, url: str) -> BeautifulSoup | None:
        """Retrieve html of given url"""
        try:
            response = requests.get(url, headers=HEADERS)
            LOG(f"Successfully fetched {url}")
            try:
                return BeautifulSoup(response.content, features="lxml")
            except Exception:
                with open(Path(__file__).with_name(f"{self.decode_error_count}").with_suffix(".htm"), "wb+") as f:
                    f.write(response.content)
                self.decode_error_count += 1
        except requests.RequestException as e:
            LOG(f"Failed to fetch {url}: {e}")

class VPParser:
    """Class that will process html content."""
    RE_EVENT_DATE = re.compile(r"(\d\d\d\d)年(\d\d)月(\d\d)日 \d\d時")

    def __init__(self) -> None:
        pass
    
    def parse(self, soup: BeautifulSoup) -> VPEventInfo:
        """Parse given html content and retrieve TVMEventInfo"""
        name = self._get_event_name(soup)
        header_text = self._get_header_text(soup)
        circles = self._get_circles(soup)
        return VPEventInfo(
            name=name,
            header_text=header_text,
            circles=circles
        )
    
    def _get_event_name(self, subsoup: Tag) -> str | None:
        title_tag = subsoup.select_one("title")
        if not title_tag:
            return None
        return title_tag.get_text(strip=True)

    def _get_header_text(self, subsoup: Tag) -> str | None:
        table_0_tag = subsoup.select_one('table[border="0"]')
        if not table_0_tag:
            return None
        return table_0_tag.get_text(separator="\n", strip=True)
    
    def _get_circles(self, subsoup: Tag) -> list[VPCircleInfoABC]:
        table_1_tag = subsoup.select_one('table[border="1"]')
        if not table_1_tag:
            return []
        
        circle_info_list: list[VPCircleInfoABC]
        if "【あ】" in table_1_tag.get_text(): # type 1 (vopara, vopara1~10)
            circle_info_list = self._process_table_type1(table_1_tag)
        else: # type 2 (vopara11~...)
            circle_info_list = self._process_table_type2(table_1_tag)
        
        return circle_info_list
    
    def _process_table_type1(self, table_tag: Tag) -> list[VPCircleInfoABC]: # like 【ま】サークル名 (vopara, vopara1~10)
        table_rows = table_tag.select("tr")
        if not table_rows:
            return []

        re_block_name = re.compile(r"【([^【】]*)】")
        circle_info_list: list[VPCircleInfoABC] = []
        current_block = "" # e.g. 【ま】サークル名
        for row in table_rows:
            col_tags = row.select("td")
            if not col_tags:
                LOG(f"WARNING: invalid row {row=}")
                continue

            c0 = col_tags[0]
            c0text = c0.get_text(strip=True)
            if c0text.startswith("【"): # New block
                m = re_block_name.search(c0text)
                if not m:
                    LOG(f"WARNING: invalid row (fake new block) {row=}")
                    continue
                current_block = m.group(1)
            else: # 
                if len(col_tags) < 3 or len(col_tags) > 5:
                    LOG(f"WARNING: invalid row (wrong column count) {len(col_tags)}) {row=}")
                    continue

                circle_info = self._get_circle_info_from_row(col_tags, current_block)
                if not circle_info:
                    LOG(f"WARNING: invalid row, type 1 could not be processed {row=}")
                    continue

                circle_info_list.append(circle_info)
        return circle_info_list
    
    def _process_table_type2(self, table_tag: Tag) -> list[VPCircleInfoABC]: # like ゆかりPARADISE２(vopara, vopara11~...)
        table_rows = table_tag.select("tr")
        if not table_rows:
            return []

        circle_info_list: list[VPCircleInfoABC] = []
        current_block = "" # e.g. あ行
        for row in table_rows:
            col_tags = row.select("td")
            if not col_tags:
                LOG(f"WARNING: invalid row {row=}")
                continue

            if len(col_tags) == 1: # New block
                current_block = col_tags[0].get_text(strip=True)
            else: # Circle (or header line "サークル名 | ...")
                if col_tags[0].get_text(strip=True) == "サークル名":
                    continue # Skip header line

                circle_info = self._get_circle_info_from_row(col_tags, current_block)
                if not circle_info:
                    LOG(f"WARNING: invalid row, type 2 could not be processed {row=}")
                    continue

                circle_info_list.append(circle_info)
        return circle_info_list
    
    def _get_circle_info_from_row(self, col_tags: list[Tag], block: str) -> VPCircleInfoABC | None:
        if len(col_tags) < 3 or len(col_tags) > 5:
            LOG(f"WARNING: Invalid line detected ! {len(col_tags)=}")
            return None
        
        circle_url = None
        a_tag = col_tags[0].select_one('a')
        if a_tag and "href" in a_tag.attrs:
            circle_url = str(a_tag["href"])

        if len(col_tags) == 3:
            cn, pn, pl = [col.get_text(strip=True) for col in col_tags]
            return VPCircleInfoType1(cn, pn, pl, block, circle_url)
        elif len(col_tags) == 4:
            cn, pn, mc, pl = [col.get_text(strip=True) for col in col_tags]
            return VPCircleInfoType2(cn, pn, pl, block, circle_url, mc)
        elif len(col_tags) == 5:
            cn, pn, mc, pl1, pl2 = [col.get_text(strip=True) for col in col_tags]
            return VPCircleInfoType2(cn, pn, f"{pl2}, {pl2}", block, circle_url, mc)


# =========================================================================
# Main execution
# =========================================================================
if __name__ == "__main__":
    urls = ["https://ttc.ninja-web.net/vo-para/vo-para_list.htm"] + [f"https://ttc.ninja-web.net/vo-para/vo-para{num:02d}_list.htm" for num in range(1, 14)]
    
    crawler = VPCrawler()
    parser = VPParser()

    events: VPEvents = {}

    for url in urls:
        soup = crawler.fetch(url)
        if not soup:
            continue
        
        event_info = parser.parse(soup)
        events[url] = event_info.get_json()

    with open(Path(__file__).with_name("vopara").with_suffix(".json"), "w+", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
        