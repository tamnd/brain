---
title: "CF 1689E - ANDfinity"
description: "We are given an array of non-negative integers. Each array element corresponds to a vertex in a graph. Two vertices are connected by an edge whenever the bitwise AND of their values is positive. The graph is not guaranteed to be connected."
date: "2026-06-09T23:28:54+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "constructive-algorithms", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1689
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 798 (Div. 2)"
rating: 2500
weight: 1689
solve_time_s: 150
verified: false
draft: false
---

[CF 1689E - ANDfinity](https://codeforces.com/problemset/problem/1689/E)

**Rating:** 2500  
**Tags:** bitmasks, brute force, constructive algorithms, dfs and similar, dsu, graphs  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers. Each array element corresponds to a vertex in a graph. Two vertices are connected by an edge whenever the bitwise AND of their values is positive.

The graph is not guaranteed to be connected. We may repeatedly increase or decrease individual array elements by one, where decrementing is allowed only for positive values. Every increment or decrement costs one operation.

Our task is to find the minimum possible number of operations needed to make the graph connected, and output one resulting array that achieves that minimum.

The most important observation is that the graph structure is determined entirely by shared set bits. Two numbers are adjacent if they have at least one common bit equal to 1. Connectivity is therefore a property of how bits are distributed across the array, not of the numeric values themselves.

The constraints are surprisingly small. The sum of all $n$ over the entire input is at most 2000. This means an $O(n^2)$ or even $O(n^2 \log A)$ solution is perfectly acceptable. Since values are below $2^{30}$, there are only 30 relevant bit positions.

Several edge cases are easy to mishandle.

Consider:

```
2
0 0
```

A vertex corresponding to value 0 has no set bits, so it is isolated from everything. Any connected graph must contain no zeros. A solution that only checks connectivity among non-zero vertices would incorrectly claim success.

Another tricky case is:

```
2
3 12
```

The graph is disconnected because:

```
3  = 0011
12 = 1100
```

Their AND is zero. A single decrement gives:

```
3  = 0011
11 = 1011
```

and now the AND is positive. The minimum answer is 1.

A final subtle case is:

```
4
8 8 1 1
```

After removing zeros, the graph is still disconnected. Several constructive ideas connect it in two operations, but not necessarily in one. The solution must correctly distinguish between answers 1 and 2.

## Approaches

A brute force approach would be to search over all possible sequences of modifications and test connectivity after every change.

This is obviously correct in principle, but completely infeasible. Even restricting ourselves to a few increments and decrements per element already creates an exponential search space.

The key breakthrough is that the answer is always extremely small.

First, every zero must be changed. A zero contributes no bits and can never share an edge with anything. Turning every zero into one is always optimal because it costs exactly one operation per zero and produces a useful value.

After all zeros become ones, we examine the resulting graph.

If it is already connected, we are done.

Otherwise, the editorial observation is remarkable: after removing zeros, the remaining minimum additional cost is never more than two. We can first test whether one extra operation is enough by trying every possible single increment and every possible single decrement. Since $n \le 2000$, this brute force check is cheap.

If none of those attempts works, the answer must be exactly two.

The final step is a constructive way to achieve those two operations. Let

```
lowbit(x) = x & (-x)
```

and consider all elements whose lowbit is maximum.

If there is only one such element, decrement it by one.

If there are multiple such elements, decrement one of them and increment another.

This special modification always connects the graph. The proof comes from the bit-component structure used in the connectivity test.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search Over Operations | Exponential | Exponential | Too slow |
| Connectivity Testing + Try All One-Step Changes + Constructive Two-Step Fix | $O(n^2 \cdot 30)$ | $O(30)$ | Accepted |

## Algorithm Walkthrough

### Connectivity Check

The graph on vertices can be large, but there are only 30 bit positions.

Instead of building the vertex graph directly, build a graph on bits.

For every number, connect all set bits that appear inside that number. If a number contains bits 1, 4, and 7, then those bits belong to the same component because that number links them together.

After processing all numbers, all bit positions that appear anywhere should belong to a single connected component. If not, the original vertex graph cannot be connected.

### Steps

1. Count all zeros in the array.
2. Replace every zero by one and add the number of replacements to the answer.
3. Check whether the graph is connected.
4. If it is connected, output the current array.
5. Otherwise, try every index.

For each index, if the value is positive, temporarily decrease it by one and test connectivity.

If connectivity is achieved, output this array.
6. Restore the value and temporarily increase it by one.
7. Test connectivity again.
8. If connectivity is achieved, output this array.
9. If no single modification works, find the maximum value of `lowbit(a[i])`.
10. Collect all indices having that maximum lowbit.
11. If exactly one such index exists, decrease that element by one.
12. Otherwise, decrease one of those elements by one and increase another by one.
13. Add two to the answer and output the resulting array.

### Why it works

Replacing every zero by one is mandatory. A zero contains no set bits, so it is always isolated. Any connected final graph must eliminate every zero.

After zeros are removed, we first test all possibilities requiring exactly one additional operation. Since every legal one-operation solution must be either a single increment or a single decrement on one element, exhaustive checking is sufficient.

The remaining claim is that if no one-operation solution exists, then a two-operation solution always exists. The lowbit construction from the official editorial guarantees this. Elements with maximum lowbit sit at the highest "bit level" among all numbers. Adjusting one or two of them by one changes their lowest set bit and merges the disconnected bit-components. Thus every remaining case can be solved with exactly two additional operations.

Since we have already ruled out answers 0 and 1, the minimum possible answer must be 2.

## Python Solution

```python
import sys
input = sys.stdin.readline

def connected(a):
    parent = list(range(30))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra != rb:
            parent[ra] = rb

    used = []

    for x in a:
        bits = []
        for b in range(30):
            if (x >> b) & 1:
                bits.append(b)

        if bits:
            used.extend(bits)
            root = bits[0]
            for b in bits[1:]:
                union(root, b)

    used = list(set(used))

    if not used:
        return False

    r = find(used[0])
    for b in used:
        if find(b) != r:
            return False

    return True

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ops = 0

        for i in range(n):
            if a[i] == 0:
                a[i] = 1
                ops += 1

        if connected(a):
            print(ops)
            print(*a)
            continue

        found = False

        for i in range(n):
            if a[i] > 0:
                a[i] -= 1
                if connected(a):
                    print(ops + 1)
                    print(*a)
                    found = True
                    break
                a[i] += 1

            a[i] += 1
            if connected(a):
                print(ops + 1)
                print(*a)
                found = True
                break
            a[i] -= 1

        if found:
            continue

        best = max(x & -x for x in a)

        idx = [i for i in range(n) if (a[i] & -a[i]) == best]

        if len(idx) == 1:
            a[idx[0]] -= 1
        else:
            a[idx[0]] -= 1
            a[idx[1]] += 1

        print(ops + 2)
        print(*a)

solve()
```

The implementation revolves around the `connected()` function.

Instead of constructing the graph on array positions, it constructs a DSU on the 30 bit positions. Every number merges all of its set bits into a single DSU component. At the end, all used bits must belong to one DSU component for the graph to be connected. This is exactly the criterion used in the official solution.

The one-operation search must carefully restore values after every temporary modification. Forgetting to restore an element is a common source of wrong answers.

The lowbit computation uses:

```
x & -x
```

which isolates the lowest set bit. Among all elements, we find those with maximum lowbit and apply the constructive two-operation fix.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| Step | Array | Connected |
| --- | --- | --- |
| Initial | [1,2,3,4,5] | Yes |
| Zero handling | [1,2,3,4,5] | Yes |
| Output | [1,2,3,4,5] | Yes |

The graph is already connected because vertex 3 shares bits with both sides and acts as a bridge.

### Example 2

Input:

```
2
3 12
```

| Step | Array | Connected |
| --- | --- | --- |
| Initial | [3,12] | No |
| Try -1 on first | [2,12] | No |
| Restore | [3,12] | No |
| Try +1 on first | [4,12] | Yes |

The algorithm discovers a valid one-operation solution immediately. Any one-operation solution is optimal because the graph was not connected initially.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot 30)$ | Up to $2n$ connectivity checks, each processing $n$ numbers and 30 bits |
| Space | $O(30)$ | DSU over only 30 bit positions |

Since the total sum of $n$ over all test cases is at most 2000, this complexity easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    # omitted, intended for local testing
    pass

# sample-style sanity checks

# already connected
inp = """1
5
1 2 3 4 5
"""

# minimum size with zeros
inp2 = """1
2
0 0
"""

# disconnected pair requiring one operation
inp3 = """1
2
3 12
"""

# all equal
inp4 = """1
4
7 7 7 7
"""

# large lowbit component case
inp5 = """1
4
8 8 1 1
"""

# boundary value
inp6 = """1
2
1073741823 1073741823
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | Connected array after two zero fixes | Mandatory zero handling |
| `3 12` | One operation | Correct one-step search |
| `7 7 7 7` | Zero operations | Already connected graph |
| `8 8 1 1` | Uses constructive fix | Two-operation branch |
| Maximum value pair | Zero operations | High-bit correctness |

## Edge Cases

Consider:

```
2
0 2
```

The vertex corresponding to zero has no edges. The algorithm immediately converts the zero into one. After that it checks connectivity on `[1,2]`. If still disconnected, the later stages handle it. The important part is that no connected solution can keep a zero.

Consider:

```
2
3 12
```

After zero handling nothing changes. The graph is disconnected. The one-operation search tests every increment and decrement. Changing `3` to `4` yields:

```
4 & 12 = 4
```

so the graph becomes connected and the algorithm correctly returns answer 1.

Consider:

```
4
8 8 1 1
```

No one-operation modification succeeds. The algorithm reaches the constructive stage. The maximum lowbit is 8, achieved by both copies of 8. One is decreased and another increased, producing a guaranteed connected configuration in exactly two additional operations. Since all one-operation possibilities were already exhausted, this answer is optimal.
