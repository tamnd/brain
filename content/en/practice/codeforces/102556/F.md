---
title: "CF 102556F - Riana and Fiber Chatroom"
description: "Each user can be represented by their birth year, because all users born in the same year are automatically the same age. The only extra connection comes from a “fast year” birthday, a date from January 1 to February 28."
date: "2026-08-04T09:10:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102556
codeforces_index: "F"
codeforces_contest_name: "2020 Ateneo de Manila University DISCS PrO HS Division"
rating: 0
weight: 102556
solve_time_s: 63
verified: true
draft: false
---

[CF 102556F - Riana and Fiber Chatroom](https://codeforces.com/problemset/problem/102556/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each user can be represented by their birth year, because all users born in the same year are automatically the same age. The only extra connection comes from a “fast year” birthday, a date from January 1 to February 28. A fast-year user born in year `y` connects year `y` with year `y-1`.

The transitive closure of these connections defines the final age groups. Riana wants every existing user and herself to belong to one age group after adding as few new users as possible.

The input contains the existing users and Riana’s registered birthday. The output asks for the minimum number of additional birthdays that create a connected age group, followed by any valid birthdays to add.

With up to `100000` users, checking every pair of people is impossible. A quadratic solution would perform about `10^10` comparisons, which is far beyond the limit. The useful structure is that years form a line, so the problem becomes connecting missing edges on a path.

A common mistake is to compare exact birthdays. The rules only depend on year groups and fast-year connections. Another mistake is forgetting Riana herself. Her year must be included even though she is not among the existing chat members.

## Approaches

A direct approach would build a graph between all users, adding an edge whenever two users are considered the same age, then repeatedly add users until the graph becomes connected. This is correct because the definition of age is exactly connectivity under those rules. However, comparing all pairs is too expensive, and the graph can contain `100001` vertices.

The key observation is that every user year is a node on a number line. A fast-year birthday in year `y` creates only the edge between `y` and `y-1`. We only need to know which adjacent year edges already exist.

If the smallest and largest relevant years are `L` and `R`, every missing edge between `y-1` and `y` inside this interval must be created. Adding a fast-year user in year `y` is exactly the operation that creates that edge. Since every added user can create only one adjacent-year connection, every missing edge is unavoidable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N²) | Too slow |
| Optimal | O(N + range of years) | O(N) | Accepted |

## Algorithm Walkthrough

1. Parse Riana’s birthday and every existing birthday. Store the years that appear and mark every year containing at least one fast-year birthday.
2. Include Riana’s birth year among the relevant years. The final age group must contain her as well.
3. Find the minimum and maximum relevant years. Every connection needed lies between these two years.
4. For every year `y` from `min_year + 1` to `max_year`, check whether there is already a fast-year user born in year `y`. If not, add a new user born on January 1 of year `y`.
5. Output all added birthdays.

Why it works: The age graph is a path over years. The only possible edges are between consecutive years. Existing fast-year users provide some of these edges. Any missing edge splits the path into two disconnected parts, so it must be added by at least one new user. The algorithm adds exactly one user for every missing edge, which is both sufficient and necessary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_date(s):
    y, m, d = map(int, s.split("-"))
    return y, m, d

def format_date(y, m=1, d=1):
    if y < 10000:
        return f"{y:04d}-{m:02d}-{d:02d}"
    return f"{y:05d}-{m:02d}-{d:02d}"

def solve():
    n = int(input())
    ry, rm, rd = parse_date(input().strip())

    years = {ry}
    fast = set()

    for _ in range(n):
        y, m, d = parse_date(input().strip())
        years.add(y)
        if m == 1 or (m == 2 and d <= 28):
            fast.add(y)

    lo = min(years)
    hi = max(years)

    ans = []
    for y in range(lo + 1, hi + 1):
        if y not in fast:
            ans.append(format_date(y))

    print(len(ans))
    for x in ans:
        print(x)

if __name__ == "__main__":
    solve()
```

The parser ignores the exact formatting width of the year because splitting by `-` gives the numeric year directly. The fast-year condition is checked only for January and February 28 or earlier.

The loop starts at `lo + 1` because a fast-year user in year `y` connects `y` to `y - 1`. Starting from `lo` would create an unnecessary connection outside the required interval. Using January 1 is convenient because it is always a valid fast-year date.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + Y) | `N` birthdays are read and `Y` is the distance between the minimum and maximum years |
| Space | O(N) | The sets store relevant years and existing fast-year connections |

The year range is at most `99999 - 1000`, so the linear scan is small. The solution easily fits the constraints.
