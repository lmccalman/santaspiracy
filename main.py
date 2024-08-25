import toml
import sys
import click
from glob import glob
from pathlib import Path
import numpy as np
from pathlib import Path
    

def build_blacklist(years):
    all_files = [Path(p) for p in glob("./assignments/*.toml")]
    files = [p for p in all_files if int(p.stem) in set(years)]
    people = set()
    pairs = []
    
    for fname in files:
        f = toml.load(fname)
        pairs.extend(f['assignments'])
        s_f = set([k for j in f['assignments'] for k in j]) 
        people = people.union(s_f)
        
    bl = {p: set() for p in people}
    for giver, receiver in pairs:
        bl[giver].add(receiver)
    return bl
    
def is_blacklisted(ass, bl):
    for g, r in ass:
        if g in bl:
            if r in bl[g]:
                return True
    return False
            
def extended_rep(compact_rep):        
    rec = compact_rep[1:] + [compact_rep[0]]
    res = list(zip(compact_rep, rec))
    return res

@click.command()
@click.option('--input', nargs=1, required=True, type=click.Path())
def cli(input):
      
    cfg = toml.load(input)
    bl = build_blacklist(cfg["blacklist"])
    proposal = sorted(cfg["players"])
    rng = np.random.default_rng(int(cfg["seed"]))

    found = False
    it = 0
    while not found:
        rng.shuffle(proposal)
        assignments = extended_rep(proposal)
        found = not is_blacklisted(assignments, bl)
        it += 1
    print(f"solution found after {it} iterations:\n")
    for g, r in assignments:
        print(f"{g}\t->\t{r}")
        
    yr = Path(input).stem
    out_fname = f'./assignments/{yr}.toml'
    with open(out_fname, 'w') as f:
        toml.dump({"assignments": assignments}, f)
    print(f"\nWritten assignments to {out_fname}.")

if __name__ == "__main__":
    cli()
