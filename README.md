# epp

Naive python japanese event participation parser.

## Requirements

* [python 3.10+](https://www.python.org/)
* [Beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/) for given python version

## Usage

## Known issues

**TVM**
* Issues when decoding for some pages (cannot decode in either utf-8 or shift-jis)
* The website will block incoming requests avec ~5 of them from the same IP, manual labor needed to still make progress

**vopara**
* Due to how tables are parsed, some "fake circles" like [株式会社インターネット here](https://ttc.ninja-web.net/vo-para/vo-para08_list.htm) will appear in the json file.

## License

Project under the MIT License.
