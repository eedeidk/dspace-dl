# dspace-dl
Parses each level of dspace like websites for convenience downloading.

## setup

- configure poetry for containerised work `pip install poetry`
- clone the repo `git clone git@github.com:eedeidk/dspace-dl.git`
- inside the dir create a venv using poetry & install dependencies `poetry install`

## usage

currently supports `egyankosh.ac.in` but should work with similar `dspace`  websites. all it does is parses each level of page (e.g. chapter of a course/ thesis) for all pdfs listed on that topic handler and lists the links to a timestamp generated text file. you can use the generated text file with any downloaders.

```shell
poetry run python ndl.py
input format # https://egyankosh.ac.in/handle/000000/00
```

e.g. to use with `wget` use `wget -i genfile.txt` currently, the egyankosh library has certain certificate issue so use `--no-check-certificate` when using `wget`

## bugs - fix

currently has some bugs. to be addressed later.

- next page load functionality

## Contributions

anyone is welcome to fix & upgrade - provided the contributor uses commenting etc for better readability
