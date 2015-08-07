#!/usr/bin/env python
# 20150412: 1035-1050:   /15
# 20150627: 1600-1710:  1/10
# TODO: option to control the choice of selection like '/'
# TODO: option to control TIME_UNIT
# TODO: parsing of quoted arguments '3/10 4/10 5/10'

import argparse

TIME_UNIT = 60


def sum_time(*time):
    total_hrs = sum([hrs for hrs, mte in time])
    total_mte = sum([mte for hrs, mte in time])

    hrs, mte = divmod(total_mte, TIME_UNIT)
    total_hrs += hrs
    total_mte = mte

    return total_hrs, total_mte


def avg_time(time, divisor):
    hrs, mte = time
    total_time = hrs * TIME_UNIT + mte
    ret = divmod( round(total_time * 1. / divisor), TIME_UNIT )
    return map(int, ret)

# hm :=
    # '1/20'  <-> (1, 20)
    # '/20'   <-> (0, 20)
    # '1/'    <-> (1, 0)

def str2hm(arg):
    hm = arg.split('/')
    assert len(hm) == 2
    h,m = map(lambda x: int(x) if x else 0, hm)
    assert m >= 0 and m < TIME_UNIT
    assert h >= 0
    return (h,m)

def hm2str(arg):
    assert len(arg) == 2
    hm = map(lambda x: str(x) if x else '', arg)
    return '/'.join(hm)

def arg_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode",
            help="which calculation mode to use")

    parser_sum = subparsers.add_parser("sum", help="summarize values of time")
    parser_sum.add_argument("time", help="values of time to sumarize",
            nargs="+", type=str2hm)

    parser_avg = subparsers.add_parser("avg", help="calculate average")
    parser_avg.add_argument("time", help="total time", type=str2hm)
    parser_avg.add_argument("divisor", help="number to divide into",
            nargs="+", type=int)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = arg_parse()

    if args.mode == "sum":
        print hm2str( sum_time(*args.time) )

    elif args.mode == "avg":
        for d in args.divisor:
            print hm2str( avg_time(args.time, d) )
