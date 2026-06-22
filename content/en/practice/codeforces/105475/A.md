---
title: "CF 105475A - Pizzas"
description: "Each attendee requests a number of pizza slices, and every requested slice has a specified topping. A pizza shop sells pizzas in only one topping per pizza, and each pizza is always cut into exactly 8 equal slices."
date: "2026-06-23T02:12:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105475
codeforces_index: "A"
codeforces_contest_name: "XXII Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 105475
solve_time_s: 93
verified: true
draft: false
---

[CF 105475A - Pizzas](https://codeforces.com/problemset/problem/105475/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Each attendee requests a number of pizza slices, and every requested slice has a specified topping. A pizza shop sells pizzas in only one topping per pizza, and each pizza is always cut into exactly 8 equal slices.

The task is to decide whether it is possible to purchase some number of pizzas for each topping so that every requested slice is exactly satisfied and no slice is left unused. A key restriction is that leftover slices are not allowed, so every bought slice must be consumed by someone.

This turns the problem into a question about whether the demand for each topping can be exactly packed into groups of size 8, since each pizza contributes exactly 8 identical slices of one topping.

The input consists of multiple test cases. For each case, we are given the number of people and the number of available toppings. Then for each person we are given how many slices they want, followed by the list of toppings for those slices. The output for each case is a decision: whether a perfect purchase plan exists.

The constraints allow up to 1000 people per test case and a total of 100000 slice requests per case. This means we need a linear or near-linear solution in the total number of slice requests. Anything quadratic over people or slices would be too slow.

A subtle edge case is when distribution looks “balanced per person” but not globally divisible per topping. For example, if one person requests 3 slices of topping 0 and another requests 5 slices of topping 0, everything looks locally fine, but the total is 8 so it works. However, if the totals were 10 and 6 across different people, a naive per-person check might incorrectly accept or reject depending on implementation, even though the correct decision depends only on the aggregate sum per topping.

Another edge case arises when toppings are sparse in the input. A naive solution might ignore toppings with zero requests, but those are irrelevant since they do not affect feasibility.

## Approaches

A direct approach is to think in terms of assignment. Each slice request must be assigned to a pizza, and each pizza contributes exactly 8 identical slices. One could try to simulate grouping slices into sets of 8 per topping, but that quickly becomes unnecessary bookkeeping.

The crucial observation is that pizzas are independent across toppings. A pizza of topping t can only serve slices of topping t, and it always contributes exactly 8 slices. Therefore, for each topping independently, the total number of requested slices of that topping must be divisible by 8. If this holds, we can simply buy total_sum[t] / 8 pizzas of topping t.

This reduces the entire problem to computing sums per topping and checking a divisibility condition. The structure of the input guarantees that counting is sufficient, since there is no cross-topping interaction and no ordering constraint.

The brute-force interpretation would attempt to simulate filling pizzas slice by slice, which would require maintaining a multiset of partially filled pizzas per topping. In the worst case, with up to 100000 slices, that simulation would still be linear per insertion but unnecessarily complex and error-prone, especially when handling partial fills.

The simplified sum-based method removes all state tracking and replaces it with a single pass aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate filling pizzas) | O(total slices) but with heavy overhead | O(number of partial pizzas) | Too complex |
| Optimal (sum per topping) | O(total slices) | O(M) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `cnt` of size M with zeros to store total requested slices per topping. This array represents how many slices we must supply for each topping.
2. For each person, read their list of requested toppings and increment the corresponding entries in `cnt`. Each entry in this array accumulates global demand, not per-person structure.
3. After processing all people, iterate over all toppings from 0 to M − 1 and check whether `cnt[t]` is divisible by 8. This condition ensures that the demand can be exactly partitioned into full pizzas for that topping.
4. If any topping has a remainder when divided by 8, immediately conclude that it is impossible to satisfy all requests without waste.
5. If all toppings satisfy the divisibility condition, conclude that a valid selection of pizzas exists.

The key reasoning step is that each pizza contributes exactly 8 identical slices, so feasibility reduces to partitioning the total demand per topping into groups of size 8.

### Why it works

For each topping, we only interact with identical units, slices of the same flavor. Any valid solution must assign these slices into disjoint groups of 8, because each group corresponds exactly to one purchased pizza. If the total count is not divisible by 8, at least one slice would remain ungrouped or force an incomplete pizza, which is forbidden. Conversely, if divisibility holds, constructing the solution is trivial by taking exactly cnt[t] / 8 pizzas of each topping, and assigning their slices arbitrarily to match requests.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, m):
    cnt = [0] * m

    for _ in range(n):
        data = list(map(int, input().split()))
        p = data[0]
        toppings = data[1:]
        for t in toppings:
            cnt[t] += 1

    for x in cnt:
        if x % 8 != 0:
            return "NO"
    return "SI"

def main():
    out = []
    data = sys.stdin.read().strip().split()
    it = iter(data)

    while True:
        try:
            n = int(next(it))
            m = int(next(it))
        except StopIteration:
            break

        cnt = [0] * m
        for _ in range(n):
            p = int(next(it))
            for _ in range(p):
                t = int(next(it))
                cnt[t] += 1

        ok = True
        for x in cnt:
            if x % 8 != 0:
                ok = False
                break

        out.append("SI" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution reads input in a streaming fashion because the total number of integers can be large. Each slice request is processed exactly once, incrementing the corresponding topping counter.

The only subtlety is ensuring that all tokens are consumed correctly across multiple test cases. Using an iterator over the full input avoids repeated I/O overhead and simplifies parsing.

## Worked Examples

We use the provided sample input to illustrate behavior.

### Example 1

Input:

```
1 1
8 0 0 0 0 0 0 0 0
```

| Step | Topping 0 count | Check |
| --- | --- | --- |
| After reading person 1 | 8 | pending |

Final check: 8 % 8 = 0, so output is SI.

This confirms that exact grouping into one pizza works.

### Example 2

Input:

```
3 3
3 0 1 2
3 2 2 0
3 1 1 1
```

| Step | cnt[0] | cnt[1] | cnt[2] | Check |
| --- | --- | --- | --- | --- |
| After all input | 2 | 4 | 2 | final |

None of these values are divisible by 8, so the answer is NO.

This shows a case where even though demand is distributed, no topping forms a complete set of 8.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total slices + M) | Each slice is processed once, then each topping is checked once |
| Space | O(M) | Only the count array per topping is stored |

The constraints allow up to 100000 total slice requests per test case, so a linear pass over all requests is easily fast enough. Memory usage stays small because M is at most 100.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    data = sys.stdin.read().strip().split()
    it = iter(data)

    out = []
    while True:
        try:
            n = int(next(it))
            m = int(next(it))
        except StopIteration:
            break

        cnt = [0] * m
        for _ in range(n):
            p = int(next(it))
            for _ in range(p):
                cnt[int(next(it))] += 1

        out.append("SI" if all(x % 8 == 0 for x in cnt) else "NO")

    return "\n".join(out)

# provided sample
assert run("""1 1
8 0 0 0 0 0 0 0 0
""") == "SI"

# sample 2
assert run("""3 3
3 0 1 2
3 2 2 0
3 1 1 1
""") == "NO"

# all zeros but valid multiples of 8
assert run("""1 2
8 0 0 0 0 0 0 0 0
""") == "SI"

# impossible single topping
assert run("""1 1
1 0
""") == "NO"

# multiple test cases
assert run("""1 1
8 0 0 0 0 0 0 0 0
2 1
4 0 0 0 0
4 0 0 0 0
""") == "SI
NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single valid full pizza | SI | basic correctness |
| mixed toppings invalid | NO | aggregation logic |
| multiple test cases | SI NO | multi-case parsing |
| small impossible case | NO | divisibility failure |

## Edge Cases

A case with a single topping and a single slice request exposes the divisibility rule directly. If the input is `1 1` followed by `1 0`, the counter for topping 0 becomes 1, and since 1 % 8 is not zero, the algorithm correctly rejects it immediately.

A case where all demands are exactly multiples of 8 per topping confirms the positive scenario. If topping 0 has 16 requests and topping 1 has 8 requests, both are divisible by 8, so the algorithm accepts, matching the fact that we can buy 2 pizzas of topping 0 and 1 pizza of topping 1.

A case with many people but small per-person requests confirms that per-person structure is irrelevant. Even if each person requests a mix of toppings, only the final totals matter, and the algorithm correctly aggregates everything before checking divisibility.
