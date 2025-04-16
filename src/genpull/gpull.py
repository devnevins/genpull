"""Creates a LaTeX subscription file from LoCG export.

  The League of Comic Geeks has a subscription export function which
  can be converted into a LaTeX file and from there a PDF can be
  created.
"""
import logging
import sys
from datetime import date

import typer
import xlrd

from xlrd import XLRDError
from typing_extensions import Annotated
from jinja2 import Environment, PackageLoader, select_autoescape
from .tex_escape import tex_escape
from .__about__ import __version__

env = Environment(
    loader=PackageLoader("genpull"),
    autoescape=select_autoescape(),
    block_start_string='<BSTART>',
    block_end_string='<BEND>',
    variable_start_string='<VSTART>',
    variable_end_string='<VEND>',
)

def strip_dates(date_str: str) -> str:
    """Strips off the comic dates from the input string.

    The comic title has a date range appended to it (e.g. (2020 -
    Present)). That needs to be extraced to get just the title.
    This algorithm is looking for the conditions in both the title
    and the parts that are removed. If all checks out the modified
    title is shown, otherwise the original input is returned.

    Args:
      date_str:
        The comics run range (e.g. (2020 - present))

    Returns:
      The processed string if it checks out, otherwise the original input.
    """
    date_str_parts = date_str.split(" (")

    if date_str_parts[1][-1] == ")":
        return date_str_parts[0]

    return date_str

def gpull(
    debug: Annotated[bool, typer.Option(help=
        "Show debugging information. (lots of output)")] = False,
    version: Annotated[bool, typer.Option(help=
        f"Shows the version of {__name__.split(".", maxsplit=1)[0]}")] = False,
    infilename: Annotated[str, typer.Argument(help=
        "The League of Comic Geeks Export Pulls xls filename.")] = 
        "Pulls-ComicGeeks.xls",
    output: Annotated[str, typer.Option(help=
        "Name of LaTeX output file.")] = None,
    username: Annotated[str, typer.Option(help=
        "Name of subscription list owner.")] = "Nevins"
    ):
    """Creates a LaTeX file for a subscription list from the League of
    Comic Geeks Export Pull list.

    The League of Comic Geeks has a function where you can export your
    subscriptions along with that week's pulls. My LCS wants a PDF
    which has all of the current subscritions listed. This code creates
    a LaTeX file that gives a nice printed version once processed.

    Raises:
        FileNotFoundError:
        No input file name found.
        XLRDError:
        Error trying to read the "Subscriptions" sheet.
    """
    if debug:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("%s Version: %s", __name__.split(".", maxsplit=1)[0], __version__)

    if version and not debug:
        print(f"{__name__.split(".", maxsplit=1)[0]} Version: {__version__}")
        sys.exit()

    try:
        subscriptions = {}
        num_comics = 0
        book = xlrd.open_workbook(infilename,
            ignore_workbook_corruption = True)
        sheet = book.sheet_by_name("Subscriptions")

        if book.nsheets == 1:
            logging.debug("Workbook has one sheet.")
        else:
            logging.debug("Workbook has %d sheets.", book.nsheets)

        rows = sheet.get_rows()
        for index, row in enumerate(rows):
            # Skip header
            if index == 0:
                continue

            logging.debug("%s, %s", strip_dates(row[0].value), row[1].value)
            if row[1].value not in subscriptions:
                subscriptions[tex_escape(row[1].value)] = []
            subscriptions[tex_escape(row[1].value)].append(tex_escape(strip_dates(row[0].value)))
            num_comics += 1

        # Sort the Company names
        companies = list(subscriptions)
        logging.debug("\nRaw Company Names\n %s", companies)
        companies.sort(key=str.casefold)
        logging.debug("\nSorted Company Names\n %s", companies)

        for s in companies:
            subscriptions[s].sort(key=str.casefold)

        logging.debug("RENDERING")
        template = env.get_template("subscriptions.jinja")

        if not output:
            print(template.render(
                    num_comics=num_comics,
                    date=date.today().strftime("%Y %m %d"),
                    username=username,
                    sorted_subscriptions=companies,
                    subscriptions=subscriptions))
        else:
            with open(output, 'w', encoding="utf-8") as subscription_tex:
                subscription_tex.write(template.render(
                        num_comics=num_comics,
                        date=date.today().strftime("%Y %m %d"),
                        username=username,
                        sorted_subscriptions=companies,
                        subscriptions=subscriptions))

    except FileNotFoundError as e:
        print(f"genpull error: {e}")
    except XLRDError as e:
        print(f"genpull error: {e} in the xls file.")
