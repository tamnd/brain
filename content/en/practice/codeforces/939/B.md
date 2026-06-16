---
title: "CF 939B - Hamster Farm"
description: "Dima has a fixed number of hamsters that will be ready for transport, and a collection of box types, each with a different capacity. Every box used must be completely filled, and all chosen boxes must be of a single type because buying mixed types removes a discount."
date: "2026-06-17T02:35:46+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 939
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 464 (Div. 2)"
rating: 1000
weight: 939
solve_time_s: 66
verified: true
draft: false
---

[CF 939B - Hamster Farm](https://codeforces.com/problemset/problem/939/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

Dima has a fixed number of hamsters that will be ready for transport, and a collection of box types, each with a different capacity. Every box used must be completely filled, and all chosen boxes must be of a single type because buying mixed types removes a discount.

So the decision is: pick one capacity value from the list, say it holds `a` hamsters per box, then pack as many full boxes of that size as possible using the available `N` hamsters. Any leftover hamsters that do not fit into a full box are left behind and do not contribute to the result.

For a chosen capacity `a`, the number of usable boxes is `N // a`, and the number of transported hamsters is `a * (N // a)`. The goal is to pick the index that maximizes this transported total.

The constraints are extremely large: `N` can be up to 10^18 and each capacity can also be up to 10^18, while the number of types can reach 100,000. This immediately rules out any approach that tries to simulate packing or iterates over hamsters or boxes individually. Even quadratic reasoning over capacities is impossible. The only feasible direction is to evaluate each type independently in constant time.

A few edge cases deserve attention. When `N = 0`, no hamsters exist, so every capacity produces zero transported hamsters and any type is valid, but the number of boxes must also be zero. When a box capacity is larger than `N`, that type contributes zero transported hamsters as well, since no full box can be formed. These cases can silently break incorrect greedy logic that assumes at least one full box always exists.

## Approaches

A brute-force interpretation would try to reason about how many hamsters remain after choosing each type and how many full boxes can be formed. For each capacity `a_i`, we compute how many complete boxes fit and multiply back to get the transported total. This is already close to optimal, because each type can be evaluated independently without interaction.

A naive mistake would be attempting to enumerate how many boxes to take for each type from `1` up to `N / a_i`, computing a best choice per type. That would lead to a total complexity proportional to the sum of all possible box counts, which in the worst case reaches 10^18 and is completely infeasible.

The key observation is that the structure of the problem removes all combinatorial interaction. Once a capacity is fixed, the best strategy is forced: take as many full boxes as possible. There is no benefit in taking fewer boxes because unused hamsters cannot improve anything later. This reduces the problem to evaluating a single formula per type and choosing the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over box counts per type | O(NK) | O(1) | Too slow |
| Evaluate each type once | O(K) | O(1) | Accepted |

## Algorithm Walkthrough

We process each box type independently and compute the best outcome achievable if that type is chosen.

1. Read `N` and the list of capacities. These define the total available hamsters and all possible box sizes.
2. Initialize variables to store the best answer found so far, including the best index and the best transported value.
3. For each type `i`, compute how many full boxes can be formed, which is `N // a[i]`. This directly enforces the requirement that boxes must be completely filled.
4. Compute the transported hamsters as `a[i] * (N // a[i])`. This measures the total usable output for that choice.
5. If this value is larger than the best seen so far, update the best index and store both the index and number of boxes.
6. After scanning all types, output the stored best index and corresponding box count.

The central idea is that each candidate type induces a deterministic outcome, so the problem becomes a linear scan over independent options.

### Why it works

For any fixed capacity, the optimal strategy is fully determined because partial boxes are forbidden and unused hamsters cannot be redistributed across types. Therefore each type defines a single possible outcome. Since there is no coupling between choices, comparing these outcomes independently is sufficient to guarantee that the global maximum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    best_idx = 1
    best_val = -1
    best_boxes = 0

    for i, x in enumerate(a, start=1):
        boxes = n // x
        total = boxes * x

        if total > best_val:
            best_val = total
            best_idx = i
            best_boxes = boxes

    print(best_idx, best_boxes)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived formula for each type. Integer division safely handles all large values because Python integers do not overflow. The comparison uses the transported total as the primary metric, while the number of boxes is stored only for output once the best type is identified. The index is tracked in 1-based form to match the input specification.

A subtle point is initialization: setting `best_val` to `-1` ensures that even when `N = 0`, the first type is still selected, producing a valid answer with zero boxes.

## Worked Examples

### Example 1

Input:

```
19 3
5 4 10
```

We evaluate each type independently.

| Type | Capacity | Boxes = 19 // a | Transported |
| --- | --- | --- | --- |
| 1 | 5 | 3 | 15 |
| 2 | 4 | 4 | 16 |
| 3 | 10 | 1 | 10 |

The maximum transported value is 16 from type 2, with 4 boxes.

This confirms that even though type 1 has a decent capacity, type 2 produces more full utilization under the constraint of integer packing.

### Example 2

Input:

```
7 3
8 3 2
```

| Type | Capacity | Boxes = 7 // a | Transported |
| --- | --- | --- | --- |
| 1 | 8 | 0 | 0 |
| 2 | 3 | 2 | 6 |
| 3 | 2 | 3 | 6 |

Both type 2 and type 3 achieve the same maximum transported value. Either is valid.

This demonstrates that capacities larger than `N` naturally become irrelevant, and ties are acceptable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K) | Each of the K capacities is evaluated exactly once using constant-time arithmetic |
| Space | O(1) | Only a few variables are maintained beyond the input array |

The constraints allow up to 100,000 types, so a single linear scan is well within limits. Each iteration performs only integer division and multiplication, which are constant-time operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    best_idx = 1
    best_val = -1
    best_boxes = 0

    for i, x in enumerate(a, start=1):
        boxes = n // x
        total = boxes * x
        if total > best_val:
            best_val = total
            best_idx = i
            best_boxes = boxes

    return f"{best_idx} {best_boxes}"

# provided sample
assert run("19 3\n5 4 10\n") == "2 4"

# minimum N = 0
assert run("0 3\n5 4 10\n") in ["1 0", "2 0", "3 0"]

# all capacities larger than N
assert run("3 3\n10 11 12\n") in ["1 0", "2 0", "3 0"]

# all equal capacities
assert run("20 3\n5 5 5\n") in ["1 4", "2 4", "3 4"]

# mixed case
assert run("17 4\n3 4 5 6\n") == "2 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| N=0 case | any index 0 | zero-hamster edge behavior |
| all ai > N | any index 0 | no valid full boxes |
| equal capacities | any max index | tie handling |
| mixed case | best selection | correct maximization |

## Edge Cases

When `N = 0`, the computation `N // a[i]` is always zero, so every type yields zero transported hamsters. The algorithm still selects the first type because the comparison uses a strict greater-than check starting from `-1`, and all candidates tie at zero. The output correctly reports zero boxes.

When all capacities exceed `N`, each candidate produces zero boxes. The algorithm does not attempt to discard these types prematurely, which avoids incorrect behavior from filtering logic. The first type is returned as a valid answer.

When multiple types achieve the same maximum transported value, the algorithm preserves the first encountered maximum. Since the problem allows any correct answer, this tie-breaking is valid and consistent.
