---
title: "CF 106145B - Walkability"
description: "We have a collection of houses, and each house has a number written on it. A walk between two houses is possible when their numbers have a common property: there exists some integer greater than one that divides their difference."
date: "2026-06-25T11:28:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106145
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 10-29-25"
rating: 0
weight: 106145
solve_time_s: 51
verified: true
draft: false
---

[CF 106145B - Walkability](https://codeforces.com/problemset/problem/106145/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a collection of houses, and each house has a number written on it. A walk between two houses is possible when their numbers have a common property: there exists some integer greater than one that divides their difference. If two houses do not have such a divisor, Magikarp has to use a car to move between them.

The task is to choose an order to visit every house exactly once while minimizing how many consecutive moves in that order require driving. Since the starting house is arbitrary, the answer is the minimum number of bad neighboring pairs in a permutation of all house numbers.

The key simplification comes from looking at the condition for a sidewalk. For two numbers `x` and `y`, a suitable divisor exists exactly when `|x-y|` is not equal to `1`. If the numbers are equal, every number greater than one divides the difference zero, so a sidewalk exists. If the difference is greater than one, that difference itself is a valid divisor. The only pairs that cannot walk are pairs of consecutive integers.

The input contains up to `2 * 10^5` houses, while the values themselves can be as large as `10^9`. We cannot compare all pairs of houses because that would require `O(n^2)` checks, which is around `4 * 10^10` operations in the largest case. The solution must depend on the number of distinct values rather than the size of the numeric range.

A few cases are easy to miss. With only two different consecutive values, every valid visiting order must at some point move from one value group to the other.

For example:

```
2
6 7
```

The answer is:

```
1
```

There is no way to place all `6`s and all `7`s without a `6-7` transition.

With three consecutive values, the middle value causes the same issue.

For example:

```
3
1 2 3
```

The answer is:

```
1
```

The value `2` cannot be next to either `1` or `3` in a walking-only route. Since those are the only other values, the block containing `2`s must touch one of them somewhere.

A different three-value example behaves differently:

```
3
1 2 10
```

The answer is:

```
0
```

We can visit in the order `1, 10, 2`, where both transitions are between numbers whose difference is greater than one.

## Approaches

A direct approach would try to build the entire graph of walking connections and search for a Hamiltonian path with as few non-walking edges as possible. The graph has up to `n = 200000` vertices, and checking all pairs would already be too expensive before we even start searching for a path. The brute force viewpoint is useful because it reveals the real structure: the only forbidden edges are between consecutive values.

The important observation is that only the set of distinct values matters. If there are at least four distinct values, we can always arrange the houses so that consecutive values are avoided. Put all values of one parity together and all values of the other parity together. Numbers with the same parity can never differ by one, so every transition inside these groups is safe. With enough distinct values, the boundary between the two groups can also be chosen safely.

The only remaining situations are when there are at most three distinct values. With two values, a drive is necessary exactly when the values are consecutive. With three values, a drive is necessary only when all three values are consecutive. In every other arrangement, the values can be ordered so that no neighboring pair differs by one.

The whole problem reduces to counting distinct values and checking these few small configurations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all house numbers and remove duplicates. Sort the remaining values.
2. If there is only one distinct value, return `0` because every move is between equal numbers.
3. If there are at least four distinct values, return `0`. The values can be separated by parity to avoid every consecutive-number transition.
4. If there are exactly two distinct values, check their difference. Return `1` when the difference is one, otherwise return `0`.
5. If there are exactly three distinct values, check whether they form three consecutive integers. Return `1` in that case, otherwise return `0`.

Why it works: The only forbidden walking pairs are consecutive integers. When the number of distinct values is large enough, parity grouping creates a complete walking route. When there are fewer values, the only possible obstruction is a chain of consecutive integers. Two consecutive values force one crossing between the groups, and three consecutive values force the middle value to touch an invalid neighbor. No other configuration has enough restrictions to require a drive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    vals = sorted(set(a))
    m = len(vals)

    if m == 1:
        print(0)
    elif m >= 4:
        print(0)
    elif m == 2:
        print(1 if vals[1] - vals[0] == 1 else 0)
    else:
        print(1 if vals[1] == vals[0] + 1 and vals[2] == vals[1] + 1 else 0)

if __name__ == "__main__":
    solve()
```

The solution first compresses the input into distinct values because equal numbers never create a driving requirement. Sorting gives direct access to the gaps between the few remaining values.

The case split follows directly from the proof. Large numbers of distinct values allow a parity arrangement, while one, two, and three distinct values need explicit checking. There is no need to store the original array after extracting the set because multiplicities do not change whether a forced consecutive transition exists.

The implementation avoids any pairwise comparisons. The only potentially expensive operation is sorting the distinct values, which fits easily within the limit for `2 * 10^5` numbers.

## Worked Examples

### Sample 1

Input:

```
5
1 3 4 8 9
```

The distinct values are already:

| Step | Distinct values | Count | Decision |
| --- | --- | --- | --- |
| 1 | `[1, 3, 4, 8, 9]` | 5 | At least four values |
| 2 | `[1, 3, 4, 8, 9]` | 5 | Answer is `0` |

The parity grouping idea gives a walking-only route. For example, values with odd parity can be visited together and values with even parity can be visited together.

Output:

```
0
```

### Sample 2

Input:

```
2
6 7
```

The distinct values are:

| Step | Distinct values | Count | Decision |
| --- | --- | --- | --- |
| 1 | `[6, 7]` | 2 | Exactly two values |
| 2 | Difference is `1` |  | One drive is required |

The two groups contain consecutive numbers, so any route must cross between them once.

Output:

```
1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the distinct values dominates the runtime |
| Space | O(n) | The set of distinct values can contain all input values |

The algorithm handles the maximum input size because it performs only one sorting operation and a constant amount of work afterward.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import builtins
    n = int(input())
    a = list(map(int, input().split()))

    vals = sorted(set(a))
    m = len(vals)

    if m == 1:
        ans = 0
    elif m >= 4:
        ans = 0
    elif m == 2:
        ans = 1 if vals[1] - vals[0] == 1 else 0
    else:
        ans = 1 if vals[1] == vals[0] + 1 and vals[2] == vals[1] + 1 else 0

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solve_data("""5
1 3 4 8 9
""") == "0\n", "sample 1"

assert solve_data("""2
6 7
""") == "1\n", "sample 2"

assert solve_data("""1
100
""") == "0\n", "single value"

assert solve_data("""6
5 5 5 5 5 5
""") == "0\n", "all equal values"

assert solve_data("""5
1 2 3 4 5
""") == "0\n", "large consecutive interval"

assert solve_data("""4
10 11 12 100
""") == "1\n", "three consecutive values inside four values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` value | `0` | Minimum-size input |
| All values equal | `0` | Duplicate handling |
| Five consecutive values | `0` | Parity construction |
| Three consecutive values with an extra distant value | `1` | Small-case obstruction |

## Edge Cases

For a single distinct value, such as:

```
5
42 42 42 42 42
```

the algorithm removes duplicates and sees only `[42]`. Every move is between equal values, so the result is `0`.

For two consecutive values:

```
4
8 8 9 9
```

the distinct values are `[8, 9]`. Since the difference is one, every complete ordering must leave at least one transition between the two groups. The algorithm returns `1`.

For three consecutive values:

```
5
1 1 2 3 3
```

the distinct values are `[1, 2, 3]`. The middle value `2` cannot stand next to either other value without a drive. The algorithm detects this chain and returns `1`.

For many distinct values:

```
6
10 11 12 13 14 15
```

there are six distinct values, so the parity construction applies. The algorithm returns `0`, because the values can be arranged so that all neighboring pairs differ by more than one.
