from spot_process import get_spot_info
from spot_process import get_median
from granule_process import find_border
from co_localize import get_colocalized_spots
import argparse

msg = "Path, channel1, Output are required inputs. Only input channel2 if processing co-localization data"

parser = argparse.ArgumentParser(description = msg)

parser.add_argument("-p", "--Path", help = "Path to directory containing files", required = True, default = "")
parser.add_argument("-p1", "--Path1", help = "Optional path to directory containing files for getting median intensity", required = False, default = "")
parser.add_argument("-p2", "--Path2", help = "Optional path to directory containing files for getting median intensit", required = False, default = "")
parser.add_argument("-o", "--Output", help = "Output file name prefix", required = True, default = "")
parser.add_argument("-k", "--Keyword", help = "Input file keyword to search for", required = False, default = "")
parser.add_argument("-g", "--Granule", help = "Use with argument G if there are granules", required = False, default = "")
parser.add_argument("-c1", "--Channel1", help = "Channel name 1", required = True, default = "")
parser.add_argument("-c2", "--Channel2", help = "Channel name 2", required = False, default = "")
args = parser.parse_args()

if (args.Channel2 != ""):
    get_colocalized_spots(args.Path, args.Channel1, args.Channel2, args.Output, args.Keyword)
    find_border(args.Path)
    median_int_1 = get_median(args.Path1, args.Path2, "somatic", args.Channel1)
    median_int_2 =get_median(args.Path1, args.Path2, "somatic", args.Channel2)
    get_spot_info(args.Path, f'{args.Keyword}_colocalized', args.Output, args.Granule, args.Channel1, median_int_1)
    get_spot_info(args.Path, f'{args.Keyword}_colocalized', args.Output, args.Granule, args.Channel2, median_int_2)
else:
    find_border(args.Path)
    median_int_1 = get_median(args.Path1, args.Path2, "somatic", args.Channel1)
    get_spot_info(args.Path, args.Keyword, args.Output, args.Granule, args.Channel1, median_int_1)

print("Completed")
