![pylint Score](https://mperlet.github.io/pybadge/badges/10.svg)
![PyPI - Version](https://img.shields.io/pypi/v/genpull)
![GitHub Tag](https://img.shields.io/github/v/tag/devnevins/genpull)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdevnevins%2Fgenpull%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# genpull
This creates a LaTeX file from the League of Comic Geeks export function. This LaTeX file will
generate a PDF subscription list that can be sent to your local comic book shop. There are some
stores that want both a connection to the League of Comic Geeks and a "paper" subscription list.

This is also useful for having a PDF on your phone to track your overall subscriptions. I've used
this when I need to remember if a comic that's appeared in my pull is a recommendation or not.

## Installation

Use pip to install this from PyPI.

```bash
pip install genpull
```

## How to Use genpull
Export a subscription list (in old Excel format) by going to League of Comic Geeks' Subscriptions 
page and selecting "Export Pulls" underneath the gear icon on the right side. Save that file which 
is referred to below as INFILENAME.

From the terminal, go to the directory that contains your saved INFILENAME file and run genpull 
using the command and format below. The simplest case is:
```
genpull --username "Your Name" --output "subscriptions.tex" INFILENAME
```

This will generate the LaTeX file and create the subscriptions.tex file. If you omit the output
option this will print the generated file to the terminal. You can use a redirect if you prefer.
```
genpull --username "Your Name" INFILENAME > subscriptions.tex
```

Take this LaTeX file and typeset it twice to generate the PDF. It needs to be
done twice because there are page numbers that appear.

## genpull Format
```
Usage: genpull [OPTIONS] [INFILENAME]
```

### Arguments
```
infilename      [INFILENAME]  The League of Comic Geeks Export Pulls xls filename. [default: Pulls-ComicGeeks.xls]
```

### Options
```
--debug   --no-debug          Show debugging information. (lots of output) [default: no-debug]
--output                TEXT  Name of LaTeX output file. [default: None]
--username              TEXT  Name of subscription list owner. [default: Nevins]
--install-completion          Install completion for the current shell.
--show-completion             Show completion for the current shell, to copy it or customize the installation.
--help                        Show this message and exit.        
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)