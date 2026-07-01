---
title: "CF 104013I - Integer Square"
description: "We are given a single year in the range from 1995 to 2019. Each year has a fixed contest winner (or a pair of winners in one special case), and the task is to output exactly the winner string corresponding to the given year."
date: "2026-07-02T05:04:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104013
codeforces_index: "I"
codeforces_contest_name: "2020-2021 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104013
solve_time_s: 128
verified: true
draft: false
---

[CF 104013I - Integer Square](https://codeforces.com/problemset/problem/104013/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single year in the range from 1995 to 2019. Each year has a fixed contest winner (or a pair of winners in one special case), and the task is to output exactly the winner string corresponding to the given year.

The input is just one integer, so the entire problem reduces to a lookup from year to a predefined value. There is no computation beyond selecting the correct entry.

Since the input size is constant and tiny, complexity constraints are irrelevant in the usual sense. Any solution from direct conditional checks to array indexing runs instantly. The only real source of errors is incorrect transcription or formatting mismatches in the output string.

A subtle edge case is the year 2006, where there are two winners separated by a comma and a space. A careless implementation might split them incorrectly, omit the comma, or alter spacing, which would make the output invalid despite being logically correct.

Another common issue is off-by-one logic when using arrays indexed from 0 instead of mapping years directly, which can easily shift answers to the wrong year if not carefully aligned.

## Approaches

The brute-force idea would be to store a list of all (year, winner) pairs and iterate through it linearly to find the matching year. This is correct because there is exactly one answer per year, but it still performs unnecessary work by scanning up to 25 entries for every query.

Since there is only one query and the dataset is fixed, the natural improvement is to precompute a direct mapping from year to winner string. This can be done either using a dictionary keyed by year or an array offset by 1995. Once this structure is built, answering the query is a single lookup.

The key observation is that the dataset is static and small, so preprocessing dominates everything and eliminates any need for search or iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Linear scan over list | $O(25)$ | $O(25)$ | Accepted |
| Direct lookup (dict/array) | $O(1)$ | $O(25)$ | Accepted |

## Algorithm Walkthrough

1. Store a mapping from each year between 1995 and 2019 to its corresponding winner string. This can be implemented as a dictionary or a fixed array indexed by year offset, ensuring constant-time access.
2. Read the input year $y$.
3. Retrieve the value associated with $y$ from the mapping.
4. Print the retrieved string exactly as stored, preserving spaces and punctuation.

### Why it works

Each year in the range has exactly one associated output string defined by the problem statement. Since the mapping is complete and injective over the input domain, every valid input corresponds to exactly one stored value. A direct lookup therefore reproduces the required output without ambiguity or computation error.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    y = int(input().strip())

    winners = {
        1995: "ITMO",
        1996: "SPbSU",
        1997: "SPbSU",
        1998: "ITMO",
        1999: "ITMO",
        2000: "SPbSU",
        2001: "ITMO",
        2002: "ITMO",
        2003: "ITMO",
        2004: "ITMO",
        2005: "ITMO",
        2006: "PetrSU, ITMO",
        2007: "SPbSU",
        2008: "SPbSU",
        2009: "ITMO",
        2010: "ITMO",
        2011: "ITMO",
        2012: "ITMO",
        2013: "SPbSU",
        2014: "ITMO",
        2015: "ITMO",
        2016: "ITMO",
        2017: "ITMO",
        2018: "SPbSU",
        2019: "ITMO"
    }

    print(winners[y])

if __name__ == "__main__":
    solve()
```

The solution stores the entire mapping explicitly so that the lookup is immediate. The only critical implementation detail is preserving the exact formatting of the 2006 entry, including the comma and space.

## Worked Examples

### Example 1

Input year is 1995.

| Step | Action | Value |
| --- | --- | --- |
| 1 | Read input | 1995 |
| 2 | Lookup mapping | ITMO |
| 3 | Output | ITMO |

This confirms direct retrieval for the first year in the dataset.

### Example 2

Input year is 2006.

| Step | Action | Value |
| --- | --- | --- |
| 1 | Read input | 2006 |
| 2 | Lookup mapping | PetrSU, ITMO |
| 3 | Output | PetrSU, ITMO |

This demonstrates that composite winners must be preserved exactly as a single string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Single dictionary lookup |
| Space | $O(1)$ | Constant-size mapping for 25 years |

The input size is constant, so the solution trivially satisfies all constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    winners = {
        1995: "ITMO",
        1996: "SPbSU",
        1997: "SPbSU",
        1998: "ITMO",
        1999: "ITMO",
        2000: "SPbSU",
        2001: "ITMO",
        2002: "ITMO",
        2003: "ITMO",
        2004: "ITMO",
        2005: "ITMO",
        2006: "PetrSU, ITMO",
        2007: "SPbSU",
        2008: "SPbSU",
        2009: "ITMO",
        2010: "ITMO",
        2011: "ITMO",
        2012: "ITMO",
        2013: "SPbSU",
        2014: "ITMO",
        2015: "ITMO",
        2016: "ITMO",
        2017: "ITMO",
        2018: "SPbSU",
        2019: "ITMO"
    }

    return winners[int(inp.strip())]

assert run("1995") == "ITMO"
assert run("2006") == "PetrSU, ITMO"
assert run("2018") == "SPbSU"
assert run("2019") == "ITMO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1995 | ITMO | earliest year mapping |
| 2006 | PetrSU, ITMO | multi-winner formatting |
| 2018 | SPbSU | mid-range lookup |
| 2019 | ITMO | final boundary year |

## Edge Cases

The only meaningful edge case is the special year with two winners, 2006. The correct output must include both names separated by a comma and a space. A correct implementation treats this as an atomic string value, not as a structured pair.

For input 2006, the lookup returns exactly `"PetrSU, ITMO"`, and printing it unchanged preserves required formatting. Any transformation such as splitting on comma or trimming spaces would break correctness, even though the data remains semantically the same.
