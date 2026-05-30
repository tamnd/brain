---
title: "CF 474B - Worms"
description: "We are given several piles of worms arranged in order. The worms are numbered consecutively across all piles. If the pile sizes are: then the first pile contains worms numbered 1 through 2, the second pile contains worms numbered 3 through 9, and the third pile contains worms…"
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 474
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 271 (Div. 2)"
rating: 1200
weight: 474
solve_time_s: 96
verified: true
draft: false
---

[CF 474B - Worms](https://codeforces.com/problemset/problem/474/B)

**Rating:** 1200  
**Tags:** binary search, implementation  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several piles of worms arranged in order. The worms are numbered consecutively across all piles.

If the pile sizes are:

```
2 7 3
```

then the first pile contains worms numbered 1 through 2, the second pile contains worms numbered 3 through 9, and the third pile contains worms numbered 10 through 12.

For each query, we are given a worm label and must determine which pile contains that worm.

The key challenge is that both the number of piles and the number of queries can be as large as $10^5$. A solution that scans through all piles for every query would perform up to $10^{10}$ operations in the worst case, which is far beyond what a 1-second time limit allows. We need something closer to $O(n \log n)$ or $O((n+m)\log n)$.

A subtle detail is that worm labels often lie exactly on pile boundaries. Consider:

```
2
2 3
2
2 3
```

The piles cover ranges:

```
Pile 1: [1, 2]
Pile 2: [3, 5]
```

The correct answers are:

```
1
2
```

A careless binary search implementation may incorrectly place worm 2 into pile 2 if it searches for the first prefix sum strictly greater than the query instead of greater than or equal to it.

Another common source of mistakes is the first worm of a pile.

```
3
2 2 2
1
3
```

The ranges are:

```
Pile 1: [1, 2]
Pile 2: [3, 4]
Pile 3: [5, 6]
```

Worm 3 belongs to pile 2. Any off-by-one error in the range construction will produce the wrong result.

## Approaches

A straightforward solution is to reconstruct the range covered by every pile and then, for each query, scan piles one by one until the correct range is found.

For example, after building:

```
Pile 1: [1, 2]
Pile 2: [3, 9]
Pile 3: [10, 12]
...
```

we could check each interval sequentially. This works because every worm belongs to exactly one pile. The problem is performance. With $10^5$ piles and $10^5$ queries, we may perform $10^{10}$ interval checks.

The structure of the numbering gives us a much better option. If we compute prefix sums of pile sizes, we obtain:

```
a = [2, 7, 3, 4, 9]

prefix = [2, 9, 12, 16, 25]
```

Each prefix sum represents the largest worm label contained in that pile.

A worm belongs to the first pile whose ending label is at least the worm number. For example, worm 11 belongs to pile 3 because:

```
2  < 11
9  < 11
12 >= 11
```

The prefix sum array is sorted in increasing order, which makes binary search applicable. Instead of scanning all piles, we find the first prefix sum greater than or equal to the query in $O(\log n)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of piles and their sizes.
2. Build a prefix sum array where `prefix[i]` equals the total number of worms in piles `1..i+1`.

This converts pile sizes into pile ending positions.
3. For each query worm label `q`, perform a binary search on the prefix sum array.
4. Find the first position whose prefix sum is greater than or equal to `q`.

This identifies the first pile whose ending label reaches or passes the queried worm.
5. Output the pile index using 1-based numbering.

### Why it works

The prefix sum array partitions all worm labels into consecutive ranges.

If:

```
prefix[i-1] < q <= prefix[i]
```

then all labels up to `prefix[i-1]` belong to earlier piles, while pile `i+1` contains labels beginning at `prefix[i-1] + 1` and ending at `prefix[i]`. Finding the first prefix sum that is at least `q` therefore uniquely determines the correct pile. Binary search simply locates this boundary efficiently.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())
    piles = list(map(int, input().split()))

    prefix = []
    total = 0

    for x in piles:
        total += x
        prefix.append(total)

    m = int(input())
    queries = list(map(int, input().split()))

    ans = []

    for q in queries:
        pile = bisect_left(prefix, q) + 1
        ans.append(str(pile))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part of the code constructs the prefix sum array. Each element stores the largest worm label belonging to that pile.

The crucial operation is:

```
bisect_left(prefix, q)
```

`bisect_left` returns the first position whose value is greater than or equal to `q`. That matches the mathematical condition needed for this problem.

The `+1` converts the zero-based array position into the one-based pile numbering required by the statement.

Using Python's built-in binary search avoids many boundary mistakes. In particular, it correctly handles queries equal to a pile endpoint, which is the most common off-by-one trap in this problem.

## Worked Examples

### Example 1

Input:

```
5
2 7 3 4 9
3
1 25 11
```

Prefix sums:

```
[2, 9, 12, 16, 25]
```

| Query | First Prefix ≥ Query | Array Position | Pile |
| --- | --- | --- | --- |
| 1 | 2 | 0 | 1 |
| 25 | 25 | 4 | 5 |
| 11 | 12 | 2 | 3 |

Output:

```
1
5
3
```

This example demonstrates the central observation. We never need to know the exact interval of every pile. The first prefix sum reaching the queried label already identifies the answer.

### Example 2

Input:

```
3
2 2 2
4
2 3 4 5
```

Prefix sums:

```
[2, 4, 6]
```

| Query | First Prefix ≥ Query | Array Position | Pile |
| --- | --- | --- | --- |
| 2 | 2 | 0 | 1 |
| 3 | 4 | 1 | 2 |
| 4 | 4 | 1 | 2 |
| 5 | 6 | 2 | 3 |

Output:

```
1
2
2
3
```

This trace exercises boundary values. Queries 2 and 4 are exactly equal to pile endpoints, and `bisect_left` still returns the correct pile.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | Building prefix sums takes O(n), each query uses binary search in O(log n) |
| Space | O(n) | The prefix sum array stores one value per pile |

With $n,m \le 10^5$, the solution performs roughly $10^5$ prefix-sum operations and $10^5$ binary searches. This easily fits within the time limit, and storing $10^5$ integers is well within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    piles = list(map(int, input().split()))

    prefix = []
    total = 0

    for x in piles:
        total += x
        prefix.append(total)

    m = int(input())
    queries = list(map(int, input().split()))

    ans = []
    for q in queries:
        ans.append(str(bisect_left(prefix, q) + 1))

    return "\n".join(ans)

# provided sample
assert run(
"""5
2 7 3 4 9
3
1 25 11
"""
) == "1\n5\n3", "sample 1"

# minimum size
assert run(
"""1
1
1
1
"""
) == "1", "single pile single worm"

# all piles equal
assert run(
"""4
5 5 5 5
4
5 10 15 20
"""
) == "1\n2\n3\n4", "boundary endpoints"

# off-by-one at pile starts
assert run(
"""3
2 2 2
3
3 5 6
"""
) == "2\n3\n3", "pile beginnings"

# large boundary transitions
assert run(
"""2
1000 1000
4
1 1000 1001 2000
"""
) == "1\n1\n2\n2", "range transitions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pile containing one worm | 1 | Minimum constraints |
| Four equal piles with endpoint queries | 1,2,3,4 | Exact boundary handling |
| Queries at pile starts | 2,3,3 | Off-by-one correctness |
| Two large piles with transition queries | 1,1,2,2 | Switching between adjacent piles |

## Edge Cases

Consider a query exactly equal to a pile endpoint.

```
2
2 3
1
2
```

Prefix sums:

```
[2, 5]
```

Binary search for `2` returns position `0` because `prefix[0] = 2`. The answer is pile `1`, which is correct. Searching for the first prefix sum strictly greater than the query would incorrectly return pile `2`.

Consider a query that is the first worm of a new pile.

```
2
2 3
1
3
```

Prefix sums:

```
[2, 5]
```

Binary search for `3` returns position `1` because `2 < 3 <= 5`. The answer becomes pile `2`. This confirms that pile beginnings are handled correctly without explicitly storing interval starts.

Consider the smallest possible input.

```
1
1
1
1
```

Prefix sums:

```
[1]
```

Binary search for `1` returns position `0`, giving pile `1`. The algorithm works even when only a single pile and a single worm exist.

Consider the final worm in the entire collection.

```
3
2 2 2
1
6
```

Prefix sums:

```
[2, 4, 6]
```

Binary search finds the first prefix sum at least `6`, which is the last element. The answer is pile `3`, confirming that the upper boundary of the numbering scheme is handled correctly.
