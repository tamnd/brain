---
title: "CF 3B - Lorry"
description: "We have a lorry with capacity v. There are two kinds of boats. A kayak occupies 1 unit of space. A catamaran occupies 2"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 3
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 3"
rating: 1900
weight: 3
solve_time_s: 245
verified: true
draft: false
---

[CF 3B - Lorry](https://codeforces.com/problemset/problem/3/B)

**Rating:** 1900  
**Tags:** greedy, sortings  
**Solve time:** 4m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a lorry with capacity `v`. There are two kinds of boats.

A kayak occupies 1 unit of space.

A catamaran occupies 2 units of space.

Every boat also has a value, its carrying capacity. The goal is to load a subset of boats whose total occupied space does not exceed the lorry volume, while maximizing the sum of carrying capacities.

The input gives all boats one by one. For each boat we know its type and value. We must print the maximum total value and one optimal set of indices.

The constraints completely shape the solution. There can be up to `10^5` boats, which immediately rules out any subset-based dynamic programming over total volume. The volume itself can be as large as `10^9`, so even `O(n * v)` is impossible both in time and memory.

A quadratic solution is also too slow. With `10^5` items, even `O(n^2)` means around `10^10` operations, far beyond what fits in 2 seconds. We need something around `O(n log n)`.

The tricky part is that items have only two possible weights, 1 and 2. That special structure is the entire reason the problem is solvable greedily.

There are several edge cases that break naive reasoning.

Suppose we always take the boat with highest value first.

Input:

```
3 2
2 100
1 60
1 60
```

The greedy-by-value choice takes the catamaran with value 100.

The optimal answer is both kayaks, total value 120.

The issue is that choosing a size-2 item can block two very strong size-1 items.

Another dangerous case appears when the remaining volume becomes odd.

Input:

```
4 3
2 100
2 99
1 60
1 50
```

Taking the two best catamarans is impossible because total size becomes 4.

Taking one catamaran and one kayak gives 160.

Taking three kayaks is impossible because only two exist.

A careless implementation that separately optimizes each type can miss the mixed solution.

One more subtle case is when many boats have equal values.

Input:

```
5 4
1 10
1 10
2 20
2 20
1 10
```

Several optimal answers exist. The algorithm must still output a valid set of original indices. Forgetting to preserve indices during sorting is a common mistake here.

## Approaches

The brute-force idea is straightforward. Every boat can either be taken or skipped, so we could iterate through all subsets, compute total occupied volume and total carrying capacity, then keep the best feasible subset.

This works logically because it checks every possible answer. The problem is the number of subsets. With `n = 10^5`, we would need to inspect `2^100000` combinations, which is astronomically impossible.

A more realistic brute-force direction is to decide how many catamarans we take. Once that number is fixed, the remaining space is determined, and we can fill it with kayaks.

Suppose we sort all catamarans by value descending and all kayaks by value descending. Then for every possible number of catamarans `k`, we take the best `k` catamarans and the best possible number of kayaks that fit in the remaining space.

This already feels promising because once the lists are sorted, the best choice for a fixed count is always the prefix with largest values.

The key observation is that item weights are only 1 and 2. Because of that, every feasible solution can be represented as:

`some prefix of the sorted size-1 list + some prefix of the sorted size-2 list`

There is never a reason to skip a stronger item while taking a weaker item of the same size.

After sorting, we can precompute prefix sums for both groups. Then trying every possible count of catamarans becomes efficient. For each `k`, we know:

Space used = `2 * k`

Remaining space = `v - 2 * k`

Best kayak contribution = prefix sum of the first `remaining space` kayaks

The total value is computed in `O(1)` after preprocessing.

We then reconstruct the indices corresponding to the best split.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all boats and separate them into two arrays:

`ones` for kayaks and `twos` for catamarans.

Each entry stores both the value and the original index because the output requires original numbering.
2. Sort both arrays in descending order of carrying capacity.

After sorting, the best way to take `k` boats of the same type is simply taking the first `k`.
3. Build prefix sums for both arrays.

Let:

`pref1[i]` = total value of the best `i` kayaks

`pref2[i]` = total value of the best `i` catamarans

This lets us evaluate any candidate solution in constant time.
4. Iterate over the number of catamarans taken.

Suppose we take `k` catamarans. Their occupied space is `2 * k`.

If this already exceeds the lorry volume, stop considering larger `k`.
5. Compute remaining capacity.

Remaining space becomes:

`rem = v - 2 * k`

Since kayaks occupy size 1, we can take at most `rem` kayaks.

We also cannot exceed the number of available kayaks, so:

`take1 = min(rem, len(ones))`
6. Compute the total carrying capacity for this split.

Total value becomes:

`pref2[k] + pref1[take1]`

Compare it with the best answer seen so far.
7. Store the best configuration.

Save:

`best_twos = k`

`best_ones = take1`
8. Reconstruct the answer.

Output the indices of:

the first `best_ones` kayaks and

the first `best_twos` catamarans from the sorted arrays.

### Why it works

The correctness comes from an exchange argument.

Consider any optimal solution. Among all chosen kayaks, if there exists an unchosen kayak with larger value, swapping them increases the total carrying capacity without changing occupied space. So in an optimal solution, the chosen kayaks must be the highest-valued kayaks among all kayaks.

The same argument applies independently to catamarans.

That means every optimal solution is fully determined by only two numbers:

how many kayaks are chosen and how many catamarans are chosen.

Once we fix the number of catamarans, the remaining capacity uniquely determines the maximum possible number of kayaks. Prefix sums then give the best achievable value for that split.

Since we try every feasible count of catamarans, one of the iterations matches the optimal configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, v = map(int, input().split())

ones = []
twos = []

for i in range(1, n + 1):
    t, p = map(int, input().split())

    if t == 1:
        ones.append((p, i))
    else:
        twos.append((p, i))

ones.sort(reverse=True)
twos.sort(reverse=True)

pref1 = [0]
for val, _ in ones:
    pref1.append(pref1[-1] + val)

pref2 = [0]
for val, _ in twos:
    pref2.append(pref2[-1] + val)

best = 0
best_ones = 0
best_twos = 0

for k in range(len(twos) + 1):
    used = 2 * k

    if used > v:
        break

    rem = v - used
    take1 = min(rem, len(ones))

    total = pref2[k] + pref1[take1]

    if total > best:
        best = total
        best_twos = k
        best_ones = take1

answer = []

for i in range(best_ones):
    answer.append(str(ones[i][1]))

for i in range(best_twos):
    answer.append(str(twos[i][1]))

print(best)
print(" ".join(answer))
```

The first part separates boats by type while preserving original indices. Keeping indices during sorting is essential because the output requires positions from the original input order.

Sorting both groups descending guarantees that prefixes are always optimal for fixed counts.

The prefix sum arrays are built with an extra leading zero. This makes expressions like `pref1[0]` valid naturally and removes boundary-condition checks.

The main loop iterates over the number of chosen catamarans. Since each catamaran consumes 2 units, the occupied volume is `2 * k`. As soon as this exceeds `v`, larger values of `k` are also impossible, so the loop stops immediately.

The expression:

```
take1 = min(rem, len(ones))
```

is subtle. The remaining volume may be larger than the number of available kayaks. Forgetting the `min` causes out-of-bounds access.

The reconstruction phase simply takes the corresponding prefixes from the sorted arrays. Because the proof established that optimal solutions always use prefixes, this reconstruction exactly matches the computed optimum.

Python integers safely handle all sums here. The largest possible total value is at most `10^5 * 10^4 = 10^9`.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 7
1 3
```

Sorted groups:

`ones = [(3, 3), (2, 1)]`

`twos = [(7, 2)]`

Prefix sums:

`pref1 = [0, 3, 5]`

`pref2 = [0, 7]`

| k | Used Space | Remaining | take1 | Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 5 |
| 1 | 2 | 0 | 0 | 7 |

Best value is 7.

Chosen indices:

```
2
```

This trace shows why blindly maximizing the number of boats is wrong. Two kayaks fit, but the single catamaran has larger total value.

### Example 2

Input:

```
5 4
1 8
1 7
2 15
2 14
1 6
```

Sorted groups:

`ones = [(8,1), (7,2), (6,5)]`

`twos = [(15,3), (14,4)]`

Prefix sums:

`pref1 = [0, 8, 15, 21]`

`pref2 = [0, 15, 29]`

| k | Used Space | Remaining | take1 | Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | 4 | 3 | 21 |
| 1 | 2 | 2 | 2 | 30 |
| 2 | 4 | 0 | 0 | 29 |

Best answer is 30.

Chosen boats:

catamaran 3 and kayaks 1, 2.

This example demonstrates that the optimal solution can mix both types. Taking only the strongest type globally is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(n) | Arrays and prefix sums store all boats |

With `n = 10^5`, `O(n log n)` is easily fast enough in Python. The memory usage is linear and comfortably fits inside 64 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, v = map(int, input().split())

    ones = []
    twos = []

    for i in range(1, n + 1):
        t, p = map(int, input().split())

        if t == 1:
            ones.append((p, i))
        else:
            twos.append((p, i))

    ones.sort(reverse=True)
    twos.sort(reverse=True)

    pref1 = [0]
    for val, _ in ones:
        pref1.append(pref1[-1] + val)

    pref2 = [0]
    for val, _ in twos:
        pref2.append(pref2[-1] + val)

    best = 0
    best_ones = 0
    best_twos = 0

    for k in range(len(twos) + 1):
        used = 2 * k

        if used > v:
            break

        rem = v - used
        take1 = min(rem, len(ones))

        total = pref2[k] + pref1[take1]

        if total > best:
            best = total
            best_twos = k
            best_ones = take1

    ans = []

    for i in range(best_ones):
        ans.append(str(ones[i][1]))

    for i in range(best_twos):
        ans.append(str(twos[i][1]))

    print(best)
    print(" ".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run(
"""3 2
1 2
2 7
1 3
"""
).splitlines()[0] == "7", "sample 1"

# minimum case
assert run(
"""1 1
1 5
"""
).splitlines()[0] == "5", "single kayak"

# only catamarans fit
assert run(
"""3 2
2 10
2 20
1 1
"""
).splitlines()[0] == "20", "best catamaran"

# mixed optimal answer
assert run(
"""5 4
1 8
1 7
2 15
2 14
1 6
"""
).splitlines()[0] == "30", "mixed choice"

# equal values
assert run(
"""4 4
1 10
1 10
2 20
2 20
"""
).splitlines()[0] == "40", "multiple optimal answers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single kayak | 5 | Minimum-size input |
| Strong catamaran | 20 | Choosing one size-2 item over weaker combinations |
| Mixed optimal | 30 | Correct interaction between both types |
| Equal values | 40 | Multiple optimal solutions and stable reconstruction |

## Edge Cases

Consider the earlier counterexample against greedy-by-value.

Input:

```
3 2
2 100
1 60
1 60
```

Sorted groups:

`ones = [60, 60]`

`twos = [100]`

The algorithm evaluates:

For `k = 0`:

take two kayaks, total = 120

For `k = 1`:

take one catamaran, total = 100

The algorithm correctly chooses 120. A naive greedy strategy that picks the largest single value first would fail here.

Now consider the mixed-capacity case.

Input:

```
4 3
2 100
2 99
1 60
1 50
```

The iterations are:

For `k = 0`:

take two kayaks, total = 110

For `k = 1`:

remaining space = 1

take one kayak, total = 160

For `k = 2`:

occupied space = 4, impossible

The algorithm outputs the catamaran with value 100 and the kayak with value 60. This confirms that trying every feasible number of size-2 items correctly handles odd remaining capacity.

Finally, consider equal-valued items.

Input:

```
5 4
1 10
1 10
2 20
2 20
1 10
```

Any combination of two catamarans or four total kayak-value units gives the same answer. The algorithm sorts while preserving indices and simply outputs one valid optimal prefix configuration. Since the problem accepts any optimal set, this is correct.
