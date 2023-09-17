import toml
import sys
import click

@click.command()
@click.option('--input', nargs=1, required=True, type=click.Path)
@click.option('--blacklist_year', multiple=True, type=int)
def cli(input, blacklist):
      
    cfg = toml.load(input)
    print(cfg)
    
# import IPython; IPython.embed();

if __name__ == "__main__":
    cli()
