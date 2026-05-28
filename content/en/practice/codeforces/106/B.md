---
title: "CF 106B - Choosing Laptop"
description: "Each laptop has four values: processor speed, RAM size, HDD size, and price. A laptop is considered outdated if there exists another laptop that is strictly better in all three technical characteristics at the same time."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 106
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 82 (Div. 2)"
rating: 1000
weight: 106
solve_time_s: 123
verified: true
draft: false
---

[CF 106B - Choosing Laptop](https://codeforces.com/problemset/problem/106/B)

**Rating:** 1000  
**Tags:** brute force, implementation  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each laptop has four values: processor speed, RAM size, HDD size, and price. A laptop is considered outdated if there exists another laptop that is strictly better in all three technical characteristics at the same time. Price does not matter for deciding whether a laptop is outdated.

After removing all outdated laptops, we must choose the remaining laptop with the minimum cost and print its original index.

The constraints are tiny. There are at most 100 laptops, so even an algorithm that compares every pair of laptops is completely safe. A full pairwise comparison performs at most $100^2 = 10{,}000$ checks, which is trivial within a 2 second time limit.

The main difficulty is not performance, it is interpreting the dominance condition correctly. A laptop becomes outdated only if another laptop is strictly larger in speed, strictly larger in RAM, and strictly larger in HDD simultaneously.

One easy mistake is treating "greater or equal" as sufficient. Consider this input:

```
2
2000 1024 100 300
2000 2048 200 250
```

The second laptop is better in RAM and HDD, but processor speed is equal, not strictly greater. Neither laptop is outdated. The correct answer is:

```
2
```

A careless implementation using `>=` would incorrectly remove the first laptop.

Another common bug is forgetting that price is irrelevant while checking outdated laptops. Consider:

```
2
3000 2048 300 900
2500 1024 200 100
```

The second laptop is outdated even though it is much cheaper. The correct answer is:

```
1
```

Some implementations mistakenly keep cheaper laptops regardless of specifications.

There is also a subtle case where several laptops are incomparable. For example:

```
3
3000 1024 500 400
2500 4096 300 350
3200 2048 200 300
```

None dominates another because each loses in at least one attribute. All three remain candidates, so we simply choose the cheapest one, which is laptop 3.

## Approaches

The most direct approach is to examine every laptop and ask whether some other laptop dominates it. For laptop `i`, we iterate over all laptops `j`. If laptop `j` has strictly greater speed, RAM, and HDD, then laptop `i` is outdated and can be discarded.

After identifying all non-outdated laptops, we scan them and select the one with the minimum price.

This brute-force method is already fast enough. With at most 100 laptops, the total number of comparisons is only 10,000. Each comparison checks three integers, so the runtime is effectively instantaneous.

There is no need for sorting, advanced data structures, or optimization tricks because the constraint is intentionally small. The key observation is that the problem asks about pairwise dominance across exactly three attributes. Since every laptop may potentially interact with every other laptop, a complete comparison is the simplest and clearest solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(1) | Accepted |

For this problem, the brute-force solution is also the optimal practical solution.

## Algorithm Walkthrough

1. Read all laptops and store their attributes together with their original 1-based index.
2. For every laptop `i`, assume initially that it is not outdated.
3. Compare laptop `i` against every other laptop `j`.
4. If laptop `j` has strictly greater speed, strictly greater RAM, and strictly greater HDD, mark laptop `i` as outdated.

This matches the exact definition from the problem statement. Equal values do not count.
5. After all comparisons, keep only the laptops that were never marked outdated.
6. Among the remaining laptops, choose the one with the minimum cost.
7. Print its original index.

### Why it works

A laptop is valid if and only if no other laptop dominates it in all three technical specifications. The algorithm checks this condition exhaustively for every laptop. Since every possible dominating pair is tested, no outdated laptop can survive the filtering step.

After filtering, the problem reduces to selecting the minimum-cost laptop among all valid candidates. Since the algorithm scans every surviving laptop exactly once, it always finds the correct minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    laptops = []

    for i in range(n):
        speed, ram, hdd, cost = map(int, input().split())
        laptops.append((speed, ram, hdd, cost, i + 1))

    best_cost = float('inf')
    best_index = -1

    for i in range(n):
        s1, r1, h1, c1, idx1 = laptops[i]

        outdated = False

        for j in range(n):
            if i == j:
                continue

            s2, r2, h2, c2, idx2 = laptops[j]

            if s2 > s1 and r2 > r1 and h2 > h1:
                outdated = True
                break

        if not outdated and c1 < best_cost:
            best_cost = c1
            best_index = idx1

    print(best_index)

if __name__ == "__main__":
    solve()
```

The solution stores every laptop together with its original index because the output requires the position in the input, not the laptop data itself.

The nested loops implement the dominance check directly. For each laptop, we search for another laptop that is strictly better in all three characteristics. The `break` is important because once a laptop is known to be outdated, further comparisons are unnecessary.

The strict comparison operators are the most important implementation detail. Replacing `>` with `>=` changes the meaning of the problem and produces incorrect results when attributes are equal.

The final selection step only considers laptops that survived the outdated test. Since all prices are distinct, the minimum-cost laptop is unique.

## Worked Examples

### Example 1

Input:

```
5
2100 512 150 200
2000 2048 240 350
2300 1024 200 320
2500 2048 80 300
2000 512 180 150
```

| Laptop | Dominated? | Reason | Candidate Cost |
| --- | --- | --- | --- |
| 1 | Yes | Laptop 3 is better in all three specs | Removed |
| 2 | No | No laptop beats it everywhere | 350 |
| 3 | No | No laptop beats it everywhere | 320 |
| 4 | No | HDD is low, but no laptop exceeds all three | 300 |
| 5 | Yes | Laptop 3 dominates it | Removed |

Among the remaining laptops, the cheapest is laptop 4 with cost 300.

Output:

```
4
```

This example shows that a laptop with a weaker HDD can still survive if nobody is strictly better in every category simultaneously.

### Example 2

Input:

```
3
3000 1024 500 400
2500 4096 300 350
3200 2048 200 300
```

| Laptop | Dominated? | Why Not Dominated | Candidate Cost |
| --- | --- | --- | --- |
| 1 | No | Highest HDD | 400 |
| 2 | No | Highest RAM | 350 |
| 3 | No | Highest speed | 300 |

No laptop dominates another because each one wins in some category.

The cheapest valid laptop is laptop 3.

Output:

```
3
```

This trace demonstrates that dominance requires superiority in all three specifications simultaneously, not just two out of three.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every laptop is compared against every other laptop |
| Space | O(1) | Only a few variables besides the input array are used |

With $n \le 100$, the quadratic solution performs at most 10,000 comparisons, which is tiny for modern hardware. The memory usage is also negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    laptops = []

    for i in range(n):
        speed, ram, hdd, cost = map(int, input().split())
        laptops.append((speed, ram, hdd, cost, i + 1))

    best_cost = float('inf')
    best_index = -1

    for i in range(n):
        s1, r1, h1, c1, idx1 = laptops[i]

        outdated = False

        for j in range(n):
            if i == j:
                continue

            s2, r2, h2, c2, idx2 = laptops[j]

            if s2 > s1 and r2 > r1 and h2 > h1:
                outdated = True
                break

        if not outdated and c1 < best_cost:
            best_cost = c1
            best_index = idx1

    print(best_index)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run(
    "5\n"
    "2100 512 150 200\n"
    "2000 2048 240 350\n"
    "2300 1024 200 320\n"
    "2500 2048 80 300\n"
    "2000 512 180 150\n"
) == "4", "sample 1"

# minimum size
assert run(
    "1\n"
    "3000 2048 500 700\n"
) == "1", "single laptop"

# equal attribute edge case
assert run(
    "2\n"
    "2000 1024 100 300\n"
    "2000 2048 200 250\n"
) == "2", "equal speed should not dominate"

# cheaper outdated laptop
assert run(
    "2\n"
    "3000 2048 300 900\n"
    "2500 1024 200 100\n"
) == "1", "price does not affect dominance"

# incomparable laptops
assert run(
    "3\n"
    "3000 1024 500 400\n"
    "2500 4096 300 350\n"
    "3200 2048 200 300\n"
) == "3", "choose cheapest among non-dominated"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single laptop | 1 | Minimum-size input |
| Equal speed case | 2 | Strict inequality handling |
| Cheap outdated laptop | 1 | Price ignored during dominance checks |
| Incomparable laptops | 3 | Correct handling of partial superiority |

## Edge Cases

Consider the equality case again:

```
2
2000 1024 100 300
2000 2048 200 250
```

Laptop 2 has better RAM and HDD, but processor speed is equal. The algorithm checks:

```
2000 > 2000
```

This is false, so laptop 1 is not marked outdated. Both laptops survive, and the cheaper one, laptop 2, is selected. The output is:

```
2
```

Now consider a cheap but outdated laptop:

```
2
3000 2048 300 900
2500 1024 200 100
```

When comparing laptop 2 against laptop 1:

```
3000 > 2500
2048 > 1024
300 > 200
```

All three conditions are true, so laptop 2 is outdated despite being cheaper. Only laptop 1 remains valid, so the answer is:

```
1
```

Finally, consider incomparable laptops:

```
3
3000 1024 500 400
2500 4096 300 350
3200 2048 200 300
```

Each laptop loses in at least one category during every comparison. None gets marked outdated. The algorithm then simply chooses the minimum price among all three candidates, which is laptop 3.
