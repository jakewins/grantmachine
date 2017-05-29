# Grantmachine

A command-line tool to sort through [grants.gov](https://www.grants.gov) that remembers grants you've seen.

![Usage example](https://github.com/jakewins/grantmachine/blob/master/example.gif "Usage example")

## Usage

Clone this repo:

    git clone git@github.com:jakewins/grantmachine.git

Then, update `CATEGORIES` in `grantmachine.py` to tell it which
categories you want.

Then run the script on your command line:

    python grantmachine.py

Grants you save are stored in `saved.lst`

The script stores which grants you've seen in `./seen.lst`.
Hence, when you run it again you'll only see grants you haven't previously sorted.

## License

MIT, see LICENSE
