import typer
import xlrd
import logging

from xlrd import XLRDError
from typing_extensions import Annotated
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import date

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
    return(date_str_parts[0])
  else:
    return(date_str)

def gpull(
  debug: Annotated[bool, typer.Option(help="Show debugging information. (lots of output)")] = False,
  infilename: Annotated[str, typer.Argument(help="The League of Comic Geeks Export Pulls xls filename.")] = "Pulls-ComicGeeks.xls",
  outfilename: Annotated[str, typer.Option(help="Name of LaTeX output file.")] = None,
  username: Annotated[str, typer.Option(help="Name of subscription list owner.")] = "Nevins"
):
  """Creates a LaTeX file for a subscription list from the League of
    Comic Geeks Export Pull list.

    The League of Comic Geeks has a function where you can export your
    subscriptions along with that week's pulls. My LCS wants a PDF
    which has all of the current subscritions listed. This code creates
    a LaTeX file that gives a nice printed version once processed.

    Args:
      infilename:
        Name of the League of Comic Geeks export file.

    Raises:
      FileNotFoundError:
        No input file name found.
      XLRDError:
        Error trying to read the "Subscriptions" sheet.
  """
  if debug:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  try:
      subscriptions = {}
      num_comics = 0
      book = xlrd.open_workbook(infilename, ignore_workbook_corruption = True)
      sheet = book.sheet_by_name("Subscriptions")

      if book.nsheets == 1:
        logging.debug(f"Workbook has one sheet.")
      else:
        logging.debug(f"Workbook has {book.nsheets} sheets.")

      rows = sheet.get_rows()
      for index, row in enumerate(rows):
          # Skip header
          if index == 0:
              continue

          logging.debug(f"{strip_dates(row[0].value), row[1].value}")
          if row[1].value not in subscriptions:
            subscriptions[row[1].value] = []
          subscriptions[row[1].value].append(strip_dates(row[0].value))
          num_comics += 1

  
  except FileNotFoundError as e:
      print(f"genpull error: {e}")
  except XLRDError as e:
      print(f"genpull error: {e} in the xls file.")

  subscription_keys = list(subscriptions)
  logging.debug(f"\nRaw Subscription Keys\n{subscription_keys}")
  subscription_keys.sort(key=str.casefold)
  for s in subscription_keys:
    subscriptions[s].sort(key=str.casefold)  
  logging.debug(f"\nSorted Subscription Keys\n{subscription_keys}")
  logging.debug("RENDERING")
  template = env.get_template("subscriptions.jinja")

  print(template.render(num_comics=num_comics, 
                        date=date.today().strftime("%Y %m %d"),
                        username=username, 
                        sorted_subscriptions=subscription_keys, 
                        subscriptions=subscriptions))