---
problem: 1320A
contest_id: 1320
problem_index: A
name: "Journey Planning"
contest_name: "Codeforces Round 625 (Div. 1, based on Technocup 2020 Final Round)"
rating: 1400
tags: ["data structures", "dp", "greedy", "math", "sortings"]
answer: passed_samples
verified: true
solve_time_s: 267
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2de6ec-99fc-83ec-9276-106005ae8eca
---

# CF 1320A - Journey Planning

**Rating:** 1400  
**Tags:** data structures, dp, greedy, math, sortings  
**Model:** gpt-5-5  
**Solve time:** 4m 27s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2de6ec-99fc-83ec-9276-106005ae8eca  

---

## Solution

## Problem Understanding

We are given a line of cities, each with an index from left to right and an associated beauty value. We need to choose a sequence of cities to visit such that indices strictly increase. The key restriction is that consecutive chosen cities are not arbitrary: the increase in position must match the increase in beauty. Formally, if we move from city $i$ to city $j$, then the difference in indices must equal the difference in their beauty values.

This condition can be rewritten in a more structural way. Rearranging

$$j - i = b_j - b_i$$

gives

$$b_j - j = b_i - i$$

So all cities in a valid journey must share the same value of $b_i - i$. That single observation turns the problem into grouping by a derived key.

The goal is to pick a valid group of cities (same key) and maximize the sum of their beauty values. A group may consist of one city, which is always valid.

The constraint $n \le 2 \cdot 10^5$ rules out any quadratic pairing of cities. Any solution that tries all pairs or builds transitions between all valid edges would degrade to $O(n^2)$ in the worst case, which is far too slow. We need a linear or near-linear grouping strategy.

A subtle edge case appears when all cities have distinct $b_i - i$ values. In that case, every valid journey has length one, so the answer is simply the maximum $b_i$. A naive approach that assumes at least one valid transition could incorrectly try to extend nonexistent chains.

Another edge case is when many cities share the same $b_i - i$ but are not contiguous. The condition does not require adjacency in the array, only equality of the derived key, so skipping indices is valid as long as order is preserved.

## Approaches

A brute-force strategy would attempt to start from every city and extend to all valid next cities. From a city $i$, we could try every $j > i$ and check whether the transition condition holds. Each successful transition leads to a recursive or DP extension. This works logically because it directly enforces the constraint, but for each city we may scan all later cities, leading to about $O(n^2)$ transitions. With $2 \cdot 10^5$ cities, this is on the order of $4 \cdot 10^{10}$ checks, which is not feasible.

The key structural simplification comes from rewriting the constraint. The condition on consecutive cities depends only on equality of $b_i - i$. This means the entire problem decomposes into independent groups indexed by this value. Once grouped, there is no interaction between different groups, and within a group every subset respecting increasing indices is valid.

This turns the problem into a simple accumulation task: for each key $b_i - i$, sum all corresponding $b_i$ values and take the maximum over all groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (pair checking / DP over transitions) | $O(n^2)$ | $O(n)$ | Too slow |
| Group by $b_i - i$ | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each city $i$, compute the value $key = b_i - i$. This transforms the constraint into a grouping rule. The reason this works is that the original condition between adjacent cities becomes equality of this expression.
2. Maintain a hash map from each key to the sum of beauty values of all cities with that key. Each city contributes independently to its group.
3. Iterate over all cities, adding $b_i$ to the sum corresponding to $b_i - i$. This builds the total contribution of every valid journey group.
4. Track the maximum sum across all keys. This represents choosing the best possible valid journey, since any valid journey must lie entirely inside one key group.
5. Output the maximum value found.

### Why it works

The transformation $j - i = b_j - b_i$ implies invariance of $b_i - i$ across all consecutive steps, and therefore across the entire sequence. This partitions cities into disjoint classes where transitions are always valid internally and impossible externally. Any valid journey is exactly a subsequence inside one such class, and its total beauty is simply the sum of its elements. Since we are free to choose any subset within a class, taking all elements in that class maximizes the sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    b = list(map(int, input().split()))
    
    mp = {}
    ans = 0
    
    for i, val in enumerate(b, start=1):
        key = val - i
        if key in mp:
            mp[key] += val
        else:
            mp[key] = val
        if mp[key] > ans:
            ans = mp[key]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the grouping idea. The enumeration starts from 1 to match the problem’s city indexing. The dictionary stores cumulative sums per key, and the answer is updated on the fly to avoid a second pass.

A common pitfall is forgetting that indices are 1-based in the key computation. Using 0-based indexing would shift all groups and produce incorrect merging of unrelated cities.

## Worked Examples

### Example 1

Input:

```
6
10 7 1 9 10 15
```

We compute $b_i - i$ for each position.

| i | b[i] | key = b[i] - i | running sum per key |
| --- | --- | --- | --- |
| 1 | 10 | 9 | 9 → 10 |
| 2 | 7 | 5 | 5 → 7 |
| 3 | 1 | -2 | -2 → 1 |
| 4 | 9 | 5 | 5 → 16 |
| 5 | 10 | 5 | 5 → 26 |
| 6 | 15 | 9 | 9 → 25 |

The best group is key = 5, giving sum 26.

This shows that cities with non-adjacent indices can still combine if their transformed value matches, and that we should not look for contiguous segments.

### Example 2

Input:

```
5
1 2 3 4 5
```

| i | b[i] | key | running sum |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 2 | 0 | 3 |
| 3 | 3 | 0 | 6 |
| 4 | 4 | 0 | 10 |
| 5 | 5 | 0 | 15 |

All cities share the same key, so the optimal journey includes all of them.

This confirms that the solution naturally handles fully compatible sequences without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each city is processed once and dictionary updates are constant average time |
| Space | $O(n)$ | In the worst case, all keys are distinct |

This complexity comfortably fits within limits for $n \le 2 \cdot 10^5$, since both operations and memory usage scale linearly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp):
    import sys
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.strip()

# provided sample
assert capture("6\n10 7 1 9 10 15\n") == "26"

# single element
assert capture("1\n100\n") == "100"

# all same key structure
assert capture("3\n1 2 3\n") == "6"

# no useful merging
assert capture("4\n10 1 10 1\n") == "20"

# decreasing values
assert capture("5\n5 4 3 2 1\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 100 | minimal case |
| 1 2 3 | 6 | full merging |
| 10 1 10 1 | 20 | non-contiguous grouping |
| 5 4 3 2 1 | 5 | no beneficial transitions |

## Edge Cases

When $n = 1$, the algorithm assigns a single key and returns that single value, since there is nothing to combine. For input `[100]`, the key is $100 - 1 = 99$, and the answer is 100 directly.

When all $b_i - i$ values differ, each group has size one. For example, `[10, 1, 100]` produces keys `9, -1, 97`, so no merging happens and the maximum single value is returned. The algorithm naturally avoids incorrect aggregation because each key is isolated in the dictionary.

When all cities share the same key, such as `[1,2,3,4]`, every city contributes to one accumulator, and the algorithm effectively sums the entire array. This demonstrates that long valid chains are fully captured without explicitly building sequences.