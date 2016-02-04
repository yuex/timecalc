#!/usr/bin/env python
import sys
import yaml
from timecalc import sum_time_from_str
from timecalc import sum_time_from_list
from timecalc import hm2str, str2hm


def sum_str_to_str(times):
    return hm2str(sum_time_from_str(times))


def sum_list_to_str(times):
    return hm2str(sum_time_from_list(times))


def yaml_to_dict2(stream):
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
    lines = yaml.load(stream)
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


if __name__ == "__main__":

    with open(sys.argv[1]) as stream:
        data = yaml_to_dict2(stream)

    sum_dict(data)

    print dict_to_yaml(data, True)
