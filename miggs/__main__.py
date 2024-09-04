import argparse
from os import path, makedirs
from shutil import rmtree
import sys
from miggs import pggb, dbg


def parse_args():
    parser = argparse.ArgumentParser(description="Miggs")
    parser.add_argument('command', choices=['construct', 'coordinates'], help="The command to run")
    parser.add_argument('--graph-type', '-g', choices=['pggb', 'dbg', 'all'], default='all', help='The graph type to use')
    parser.add_argument('--dataset', '-d', required=True, help='A file containing the paths to all the haplotypes')
    parser.add_argument('--tmp-dir', '-t', default='/tmp', help='The directory to store temporary files')
    parser.add_argument('--output', '-o', default='output', help='The output directory')
    parser.add_argument('--force-overwrite', '-f', action='store_true', help='Force overwrite of the output directory. Previous data will be lost')
    
    parser.add_argument('--bindir', '-b', default='/home/yoann/Projects/bioinfo/pangenome_coordinates/bin', help='The directory containing the executables')
    
    return parser.parse_args()


def create_coordinates(args):
    raise NotImplementedError


def main():
    args = parse_args()
    
    # Force rewrite of the output directory
    if args.force_overwrite and path.exists(args.output):
        rmtree(args.output)
    
    # Cancel exec if the outpath already exists
    if path.exists(args.output):
        print("Output directory already exists", file=sys.stderr)
        sys.exit(1)
    makedirs(args.output)
    
    # Determine the graph type
    pggb_obj = None if args.graph_type == "dbg" else pggb.PGGB(args.tmp_dir, args.output, args.bindir)
    dbg_obj = None if args.graph_type == "pggb" else dbg.DBG(args.tmp_dir, args.output, args.bindir)
    
    graphs = [x for x in [pggb_obj, dbg_obj] if x is not None]
    
    # Run the right command
    for graph in graphs:
        match args.command:
            case "construct":
                print("Constructing graph")
                graph.construct(args.dataset)
            case "coordinates":
                print("Getting coordinates")
                graph.get_coordinates()
            case _:
                print("Invalid command", file=sys.stderr)
    
    
    
if __name__ == "__main__":
    main()
    