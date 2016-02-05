# Timecalc

A tool to make the imitation of [Alexander Alexandrovich
Lyubishchev](https://zh.wikipedia.org/wiki/%E4%BA%9A%E5%8E%86%E5%B1%B1%E5%A4%A7%C2%B7%E4%BA%9A%E5%8E%86%E5%B1%B1%E5%BE%B7%E7%BD%97%E7%BB%B4%E5%A5%87%C2%B7%E6%9F%B3%E6%AF%94%E6%AD%87%E5%A4%AB)'s
[time billing](https://book.douban.com/subject/1115353/) method a lot easier.

After all, it's already half a century later. We have the great aid of
computers. We don't have to spend two days to complete the billing of the whole
year. Let our computer slaves mind those boring parts for us.

# Install

from github:

    git clone https://github.com/yuex/timecalc.git
    cd timecalc
    python setup.py install

from pypi:

    pip install timecalc


# Example

add up times

    timecalc sum 1/30 /30 2/
    4/

average time

    timecalc avg 70/ 4 28
    17/30
    2/30

analyze yml book

    cat example.yml
    ---
    - 一类:
      # Jan
      - 读书:
        - 英语:
          - 英语说文解字: 21/30
        - 技术:
          - Hacker's Guide to Git: 4/40
      - 工作: 3/
      # Feb
      - 读书:
        - 英语:
          - 英语说文解字: 26/15
        - 技术:
          - Little Book of Semaphore: 2/
      - 工作: 3/

    timecalc yml example.yml
    - 一类 60/25:
      - 工作: 6/
      - 读书 54/25:
        - 英语 47/45:
          - 英语说文解字: 47/45
        - 技术 6/40:
          - Hacker's Guide to Git: 4/40
          - Little Book of Semaphore: 2/
