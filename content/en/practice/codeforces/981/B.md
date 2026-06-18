---
problem: 981B
contest_id: 981
problem_index: B
name: "Businessmen Problems"
contest_name: "Avito Code Challenge 2018"
rating: 1000
tags: ["sortings"]
answer: passed_samples
verified: true
solve_time_s: 72
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a328490-05a4-83ec-983e-9f0d55973968
---

# CF 981B - Businessmen Problems

**Rating:** 1000  
**Tags:** sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 12s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a328490-05a4-83ec-983e-9f0d55973968  

---

## Solution

## Problem Understanding

Two companies each own a collection of chemical elements, where every element is identified by a large integer key. Each occurrence of an element also carries a profit value that the company earns if it decides to present that element at the exhibition. The companies want to choose subsets of their own elements to maximize total profit, but they are forbidden from presenting the same element key in both chosen subsets.

From a more structural point of view, every element key may appear in one company, the other company, or both. If it appears in both, the conflict forces us to decide at most one side that is allowed to use it. If it appears in only one company, that company may freely include it or exclude it depending on whether it is beneficial.

The goal is to resolve all conflicts across shared keys in a way that maximizes the sum of chosen profits.

The constraints go up to 200,000 total elements, which rules out any solution that compares every element of one set against every element of the other. A quadratic pairing approach would require on the order of 10¹⁰ operations in the worst case, which is far beyond the time limit. The key structural hint is that the interaction between the two sets only happens through equality of keys, so all reasoning can be localized per unique element index.

A naive greedy idea that always picks the higher of two conflicting values per key seems promising but can be misapplied if implemented without grouping by key first. For example, if duplicates of the same key were treated independently instead of aggregated, one might incorrectly choose multiple contributions for the same element identity, which violates the problem condition.

Another subtle failure case occurs when a key appears in only one company. A careless implementation that only processes intersecting keys might forget to include those unique elements entirely, losing guaranteed profit.

## Approaches

A brute-force approach would attempt to consider each element key independently and decide for every possible assignment whether it goes to ChemForces, TopChemist, or neither. If we imagine k shared keys, this becomes a ternary decision per key, leading to 3ᵏ possibilities. Even at moderate k this explodes combinatorially and is infeasible.

The key observation is that the only coupling between decisions is per identical element index. Once we group all occurrences by key, each key becomes an independent decision unit. For a given key, we either take ChemForces’ contribution, or TopChemist’s contribution, or the maximum of the two if both exist.

This reduces the entire problem into a simple aggregation task: for every distinct key, compute the best achievable contribution and sum it.

The brute-force fails because it treats interactions globally, while the problem actually decomposes perfectly into independent per-key choices. The optimal solution exploits this decomposition directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^k) | O(k) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read all elements from both companies and group them by their index value. For each key, store the best profit seen from ChemForces and the best profit seen from TopChemist. This is necessary because each company guarantees distinct keys internally, so at most one value per key per company exists.
2. For every key in the union of both companies’ keys, determine its contribution to the final answer. If a key exists only in one company, take its value directly. If it exists in both, take the larger of the two values.
3. Sum these chosen contributions over all keys.

The crucial decision is the per-key maximum, which ensures that no conflicting key is counted twice while still preserving the best possible choice.

### Why it works

Each key is independent of all others because the only constraint is that the same key cannot be selected from both companies simultaneously. There are no cross-key restrictions. Once we isolate a key, the optimal decision for that key does not influence any other key, which guarantees that locally optimal choices combine into a globally optimal solution. This is a classic separability property: the objective function is additive over keys and constraints do not couple different keys.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
best = {}

for _ in range(n):
    a, x = map(int, input().split())
    best[a] = x  # ChemForces values

m = int(input())
for _ in range(m):
    b, y = map(int, input().split())
    if b in best:
        best[b] = max(best[b], y)
    else:
        best[b] = y

print(sum(best.values()))
```

The first loop initializes a dictionary with ChemForces’ values. The second loop either inserts new keys for TopChemist-only elements or updates existing ones by taking the maximum value, which correctly resolves conflicts.

The final sum aggregates the optimal contribution per key.

A common implementation pitfall is forgetting that each company’s input already guarantees uniqueness of keys within itself. That allows us to store a single value per key per company without further aggregation. Another subtle point is ensuring that we never double count a shared key by adding both values; instead we overwrite or compare.

## Worked Examples

### Example 1

Input:

```
3
1 2
7 2
3 10
4
1 4
2 4
3 4
4 4
```

We track values per key:

| Key | Chem | Top | Chosen |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 4 |
| 7 | 2 | - | 2 |
| 3 | 10 | 4 | 10 |
| 2 | - | 4 | 4 |
| 4 | - | 4 | 4 |

Final sum is 4 + 2 + 10 + 4 + 4 = 24.

This confirms that shared keys correctly select the maximum contribution while unique keys are always included.

### Example 2

Input:

```
2
5 100
10 1
3
5 50
7 20
10 10
```

| Key | Chem | Top | Chosen |
| --- | --- | --- | --- |
| 5 | 100 | 50 | 100 |
| 10 | 1 | 10 | 10 |
| 7 | - | 20 | 20 |

Final answer is 100 + 10 + 20 = 130.

This shows how the algorithm handles asymmetric overlaps where one side dominates or where only one side exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each element is processed once and dictionary operations are average O(1) |
| Space | O(n + m) | Dictionary stores one entry per distinct element key |

The linear scan matches the input size constraints directly, which ensures the solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    best = {}

    for _ in range(n):
        a, x = map(int, input().split())
        best[a] = x

    m = int(input())
    for _ in range(m):
        b, y = map(int, input().split())
        if b in best:
            best[b] = max(best[b], y)
        else:
            best[b] = y

    return str(sum(best.values()))

# provided sample
assert run("""3
1 2
7 2
3 10
4
1 4
2 4
3 4
4 4
""") == "24"

# single overlap
assert run("""1
1 5
1
1 10
""") == "10"

# disjoint sets
assert run("""2
1 1
2 2
2
3 3
4 4
""") == "10"

# all overlap, alternating dominance
assert run("""3
1 5
2 7
3 1
3
1 6
2 3
3 10
""") == "21"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single overlap | 10 | correct max choice on one key |
| disjoint sets | 10 | inclusion of all unique elements |
| alternating dominance | 21 | correct per-key max across multiple overlaps |

## Edge Cases

A key edge case is when one company has no elements. In that case, the answer is simply the sum of the other company’s values. The algorithm handles this naturally because all keys come only from one side and are added directly.

Another case is when all keys overlap. For input:

```
2
1 5
2 3
2
1 4
2 10
```

the dictionary evolves as key 1 becomes max(5,4)=5 and key 2 becomes max(3,10)=10, yielding 15. This confirms that updates never accumulate both values.

A final edge case is very large values of n and m up to 100,000 each. The dictionary-based aggregation ensures constant-time handling per element, so even full overlap inputs remain linear time and do not degrade.