---
title: "CF 102896K - Kate's 2021 Celebration"
description: "We are given several packages of balloons sold by a store. Each package has a price and a multiset of digits written on its balloons."
date: "2026-07-04T11:30:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102896
codeforces_index: "K"
codeforces_contest_name: "Northern Eurasia Finals Online 2020"
rating: 0
weight: 102896
solve_time_s: 37
verified: true
draft: false
---

[CF 102896K - Kate's 2021 Celebration](https://codeforces.com/problemset/problem/102896/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several packages of balloons sold by a store. Each package has a price and a multiset of digits written on its balloons. Kate wants to buy exactly one package such that, using the digits inside that package, she can form the year “2021”, meaning she needs at least two zeros, two ones, and one two, one two, one one is already counted, so in total the requirement reduces to two copies of digit 2, two copies of digit 0, and one copy of digit 1 is insufficient because the target is specifically “2 0 2 1”, so the exact requirement is digit counts: 2 appears twice, 0 appears once, and 1 appears once.

Each package is usable as a bag of digits, and we can freely pick digits from it as long as they exist. The task is to find the cheapest package index that satisfies these digit requirements, or report that no package can satisfy them.

The input size is small enough that checking every package independently is feasible. With at most about a thousand packages and each digit string of length up to one hundred, even a straightforward frequency scan per package is easily fast enough. Any approach worse than roughly 10^8 primitive operations would still be safe, but we are far below that.

The main edge cases come from misunderstanding multiplicity. A common mistake is to assume that seeing “2021” as a substring is required, but digits can be rearranged arbitrarily. Another subtle issue is forgetting that multiple zeros or ones may appear and only counts matter. Finally, a package might contain all required digits but in insufficient quantity, for example having only one ‘2’.

Example of a failing naive idea: if we check only whether the string contains characters '2', '0', '1' at least once, we would incorrectly accept a package like “201” which lacks the second ‘2’.

Another edge case is when multiple packages satisfy the condition and we must choose the minimum price, not the first valid one.

## Approaches

A brute-force approach is almost already optimal. For each package, we count occurrences of digits 0 to 9 and verify whether counts meet the requirement for forming “2021”. This is correct because digit positions do not matter, only frequencies.

The brute-force cost is simple: for each of n packages, we scan a string of length up to 100, so the total work is about 100,000 character inspections. This is negligible.

There is no deeper combinatorial structure to exploit because each package is independent and the check is constant-time once frequencies are computed. The only “optimization” is to stop early if counts already exceed required thresholds, but even that is not necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (count digits per package) | O(n · L) | O(1) | Accepted |
| Optimal (same as brute force) | O(n · L) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of packages and initialize a variable to store the best answer as “not found” and a best price as infinity. This ensures we can compare all candidates uniformly.
2. For each package, read its price and digit string, then compute a frequency array of size 10 by scanning the string once. This step is necessary because we need exact multiplicities, not just presence.
3. Check whether the package contains at least two ‘2’ digits, at least one ‘0’, and at least one ‘1’. This directly encodes whether we can construct “2021” from the multiset.
4. If the condition is satisfied and the price is smaller than the best seen so far, update the best answer to this package index. This maintains a running minimum over valid candidates.
5. After processing all packages, output the best index if it exists, otherwise output 0.

### Why it works

Each package is independent, so the problem reduces to a filter-and-minimize pattern over a set of candidates. The frequency check is both necessary and sufficient because any permutation of digits is allowed. Maintaining the minimum index among valid packages correctly captures the required output since we always compare against the best known valid solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(cnt):
    return cnt[2] >= 2 and cnt[0] >= 1 and cnt[1] >= 1

n = int(input())
best_price = float('inf')
best_idx = 0

for i in range(1, n + 1):
    parts = input().split()
    p = int(parts[0])
    s = parts[1]

    cnt = [0] * 10
    for ch in s:
        cnt[ord(ch) - 48] += 1

    if ok(cnt):
        if p < best_price:
            best_price = p
            best_idx = i

print(best_idx)
```

The solution is structured around a direct digit frequency table. The helper check isolates the condition for forming “2021”, which avoids repeating logic inside the loop. The index tracking is done carefully to respect 1-based indexing from the problem statement.

A common implementation mistake is forgetting to reset the frequency array per test case or mixing up ASCII conversion. Using `ord(ch) - 48` ensures correct mapping from characters to digit values.

## Worked Examples

Consider an input with three packages:

```
3
150 2021
200 220011
100 012345
```

The first package already contains exactly the needed digits.

| Package | Price | Digit counts (0,1,2) | Valid | Best index |
| --- | --- | --- | --- | --- |
| 1 | 150 | (0:1, 1:1, 2:1) | No | 0 |
| 2 | 200 | (0:2, 1:2, 2:2) | Yes | 2 |
| 3 | 100 | (0:1, 1:1, 2:0) | No | 2 |

This trace shows how validity depends strictly on counts rather than ordering.

Now consider a second example:

```
4
300 2220011
250 2020
400 221100
100 000211
```

| Package | Price | (0,1,2 counts) | Valid | Best index |
| --- | --- | --- | --- | --- |
| 1 | 300 | (2,2,3) | Yes | 1 |
| 2 | 250 | (2,0,1) | No | 1 |
| 3 | 400 | (1,2,2) | Yes | 1 |
| 4 | 100 | (2,1,1) | No | 1 |

Here the key observation is that even though package 4 is cheapest, it fails the requirement because it lacks enough ‘2’s. Package 1 remains optimal among valid ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each package string is scanned once to build digit frequencies |
| Space | O(1) | Only a fixed-size array of 10 digits is used |

With n ≤ 1000 and L ≤ 100, the total operations are about 100,000, which is far below the time limit threshold for typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline()

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    best_price = float('inf')
    best_idx = 0

    for i in range(1, n + 1):
        p, s = input().split()
        p = int(p)

        cnt = [0] * 10
        for ch in s:
            cnt[ord(ch) - 48] += 1

        if cnt[2] >= 2 and cnt[0] >= 1 and cnt[1] >= 1:
            if p < best_price:
                best_price = p
                best_idx = i

    return str(best_idx)

# provided samples
assert solve("""4
100 9876543210
200 00112233445566778899
160 012345678924568
150 000000123456789
""") == "3"

assert solve("""5
100 0123456789
120 0022446688
200 00224466883456789
10 0
10 1
""") == "0"

# custom cases
assert solve("""1
10 2021
""") == "1", "minimum valid single package"

assert solve("""2
5 000211
3 22100
""") == "2", "cheapest valid chosen"

assert solve("""3
10 222
20 001
30 11
""") == "0", "no valid package"

assert solve("""3
10 2021
5 2021
7 2021
""") == "2", "tie-breaking by price"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single valid | 1 | minimal input correctness |
| multiple candidates | 2 | correct minimum selection |
| all invalid | 0 | failure handling |
| identical valid | 2 | tie-breaking by price |

## Edge Cases

A package like “202” fails even though it visually resembles the target, because it only contains one ‘1’. The algorithm correctly rejects it since the frequency check enforces all required counts strictly.

A package like “2220011” contains sufficient digits but in excess. The algorithm accepts it because surplus digits do not affect feasibility, only minimum thresholds matter.

A case with multiple valid packages having identical prices is handled naturally because the algorithm keeps the first encountered minimum, and the problem allows any valid index in ties.
