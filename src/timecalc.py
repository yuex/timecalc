#!/usr/bin/env python
# 20150412: 1035-1050:   /15
# 20150627: 1600-1710:  1/10
# TODO: option to control the choice of selection like '/'
# TODO: option to control TIME_UNIT
# TODO: parsing of quoted arguments '3/10 4/10 5/10'

import argparse
import yaml
import sys


TIME_UNIT = 60


def str2hm(arg):
    # hm :=
    # '1/20'  <-> (1, 20)
    # '/20'   <-> (0, 20)
    # '1/'    <-> (1, 0)
    hm = arg.split('/')
    assert len(hm) == 2
    h, m = map(lambda x: int(x) if x else 0, hm)
    assert m >= 0 and m < TIME_UNIT
    assert h >= 0
    return (h, m)


def hm2str(arg):
    assert len(arg) == 2
    hm = map(lambda x: str(x) if x else '', arg)
    return '/'.join(hm)


def sum_time(*time):
    total_hrs = sum([hrs for hrs, mte in time])
    total_mte = sum([mte for hrs, mte in time])

    hrs, mte = divmod(total_mte, TIME_UNIT)
    total_hrs += hrs
    total_mte = mte

    return total_hrs, total_mte


def sum_time_from_list(times):
    times = map(str2hm, times)
    return sum_time(*times)


def sum_time_from_str(times):
    times = map(str2hm, times.split())
    return sum_time(*times)


def avg_time(time, divisor):
    hrs, mte = time
    total_time = hrs * TIME_UNIT + mte
    ret = divmod(round(total_time * 1. / divisor), TIME_UNIT)
    return map(int, ret)


def sum_str_to_str(times):
    return hm2str(sum_time_from_str(times))


def sum_list_to_str(times):
    return hm2str(sum_time_from_list(times))


def yaml_to_dict2(lines):
    def _yaml_to_dict(lines, data):

        if isinstance(lines, list):
            for line in lines:
                _yaml_to_dict(line, data)
        elif isinstance(lines, dict):
            assert len(lines) == 1
            name, value = list(lines.items())[0]
            if isinstance(value, list):
                try:
                    the_d = data[name]
                except KeyError:
                    data[name] = {}
                    the_d = data[name]
                _yaml_to_dict(value, the_d)
            elif isinstance(value, str):
                try:
                    data[name].append(value)
                except KeyError:
                    data[name] = [value]

    data = {}
    _yaml_to_dict(lines, data)
    return data


def sum_dict(data):
    if isinstance(data, dict):
        ret = []
        for k, v in data.items():
            time = sum_dict(v)
            ret.append(time)
            if isinstance(v, dict):
                data[k] = [time, data[k]]
            elif isinstance(v, list):
                data[k] = time
        return sum_list_to_str(ret)
    elif isinstance(data, list):
        return sum_list_to_str(data)


def dict_to_yaml(data, sort=False):
    def _get_key(d):
        v = d.values()[0]
        return str2hm(v)

    def _dict_to_yaml2(data):
        lines = []

        idx = 0
        able_to_sort = True
        for k in data:
            v = data[k]
            if isinstance(v, list):
                time, subs = v
                k = '%s %s' % (k, time)
                v = _dict_to_yaml2(subs)
                if isinstance(v, list):
                    able_to_sort = False
            lines.append({k: v})
            idx += 1

        if sort and able_to_sort:
            lines.sort(key=_get_key, reverse=True)
        return lines

    lines = _dict_to_yaml2(data)
    return yaml.dump(lines, allow_unicode=True, default_flow_style=False)


def analyze_yaml(stream):
    def _analyze_yaml(lines):
        data = yaml_to_dict2(lines)
        sum_dict(data)
        return dict_to_yaml(data, True)

    return _analyze_yaml(yaml.load(stream))


def arg_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="mode", help="which calculation mode to use")

    parser_sum = subparsers.add_parser("sum", help="summarize values of time")
    parser_sum.add_argument("time", help="values to sumarize", nargs="+")

    parser_avg = subparsers.add_parser("avg", help="calculate average")
    parser_avg.add_argument("time", help="total time", type=str2hm)
    parser_avg.add_argument(
        "divisor", help="number to divide into", nargs="+", type=int)

    parser_yml = subparsers.add_parser("yml", help="analyze yaml summaries")
    parser_yml.add_argument("stream", help="where to read input", nargs="?",
                            type=open, default=sys.stdin)

    args = parser.parse_args()
    return args


def main():
    args = arg_parse()

    if args.mode == "sum":
        print(args.time)
        print(hm2str(sum_time_from_list(args.time)))

    elif args.mode == "avg":
        for d in args.divisor:
            print(hm2str(avg_time(args.time, d)))
    elif args.mode == "yml":
        print analyze_yaml(args.stream)


if __name__ == '__main__':
    main()
