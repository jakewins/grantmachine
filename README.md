# Grantmachine

A command-line tool to rapidly sort through US Government grants.

## Usage

First, update the CATEGORIES variable in the script to tell it which
grant categories you want. Then just run the script on your command line:

    python grantmachine.py

Grants you save are stored in `saved.lst`

The script remembers which grants you've previously seen as long as
you run it in the directory that contains `seen.lst`.
Hence, you can run it again in a few months without having to go
through the same grants.

## License

MIT, see LICENSE
