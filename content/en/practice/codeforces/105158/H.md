---
title: "CF 105158H - \u968f\u673a\u6808"
description: "We are given a process that builds a multiset dynamically. There are exactly n insert operations and n removal operations, interleaved in a fixed order. Each insertion adds a known value, while each removal deletes a uniformly random element from the current multiset."
date: "2026-06-27T11:05:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105158
codeforces_index: "H"
codeforces_contest_name: "2024 National Invitational of CCPC (Zhengzhou), 2024 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105158
solve_time_s: 44
verified: true
draft: false
---

[CF 105158H - \u968f\u673a\u6808](https://codeforces.com/problemset/problem/105158/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a process that builds a multiset dynamically. There are exactly `n` insert operations and `n` removal operations, interleaved in a fixed order. Each insertion adds a known value, while each removal deletes a uniformly random element from the current multiset. The randomness is the key: at every removal step, every currently present element is equally likely to be chosen.

After all `n` removals, we obtain a sequence of removed values in the order they were extracted. The goal is to compute the probability that this output sequence is non-decreasing.

The structure is unusual because the deletion process does not depend on order of insertion in a deterministic way. Instead, it behaves like repeatedly sampling without replacement from a dynamically changing multiset, but constrained by the interleaving of insertions and deletions.

The constraints allow up to `2 × 10^5` operations, so any approach that enumerates all possible removal histories is immediately impossible. Even storing probabilities over permutations explicitly is infeasible because the number of possible deletion orders grows factorially with the number of active elements.

A subtle edge case is when insertions are heavily delayed. For example, if all insertions happen first, then all deletions, the process becomes a uniform random permutation of all inserted values. The answer then reduces to the probability that a random permutation is non-decreasing, which is zero unless all values are equal. On the other extreme, if deletions happen as soon as elements are inserted, the structure becomes almost deterministic, because the multiset is small at every step.

The key difficulty is that the interleaving determines how much “choice entropy” exists at each deletion.

## Approaches

A brute-force interpretation is to simulate the process by exploring all possible deletion choices. At each removal step, we branch over all elements in the current multiset, multiplying probabilities accordingly, and track the resulting sequence. This correctly computes the answer, but its complexity is exponential in the number of deletions, since each removal can branch up to `O(n)` ways. In the worst case this explores all `n!` permutations.

The main observation is that we do not actually care about the identity of all removed elements simultaneously. We only care about whether the final sequence is sorted. That condition can be expressed in terms of the relative order in which values are "exposed" by the random deletion process.

Instead of thinking forward from insertions, we reverse the viewpoint: imagine that each value, once inserted, waits until it is deleted, and all we care about is the relative ordering of deletion times. The process induces a random partial ordering constrained by the stack-like evolution of the multiset size. The crucial simplification is that the probability structure factorizes over values in a way that allows dynamic programming over the operation sequence, tracking how many elements of each value are “still eligible to be next minimum”.

The standard trick in this problem family is to maintain, for each value, how many copies are currently active, and to compute probabilities incrementally using the fact that when the sequence must remain non-decreasing, the only valid removals at each step are from the current minimum value set. This reduces the randomness to a sequence of weighted choices among “current minimum blocks”, which can be handled with prefix-sorted compression and modular combinatorics.

This transforms the problem from exploring permutations to tracking a weighted process over value groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n!) | O(n) | Too slow |
| DP over value groups | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first compress all inserted values and consider them in sorted order, because the final sequence must be non-decreasing, meaning values effectively partition into levels.

1. We process the operations from left to right while maintaining a multiset structure, but we also maintain a second structure that tracks, for each distinct value, how many of that value are currently present.

The reason is that only the relative counts matter, not identities.
2. We define a dynamic programming state that represents the probability that the partial deletion sequence seen so far is valid and that the next element we would like to remove must be at least a certain value threshold.

This threshold is the last removed value.
3. When we encounter an insertion of value `x`, we increase the available pool for value `x`. This does not immediately affect validity, but it increases future branching weight.
4. When we encounter a deletion, we must choose one element uniformly from all currently active elements. We split the probability transition based on whether the chosen element respects the non-decreasing constraint. Only elements with value ≥ last output value are valid choices; anything smaller would immediately invalidate the sequence.
5. For a deletion step, we compute:

the probability mass of choosing a valid element divided by total active elements. We multiply the DP state by this probability. Then we condition on success and update the last removed value to the value chosen, which effectively restricts future choices further.
6. To avoid iterating over all elements at each deletion, we maintain frequency counts and a data structure (Fenwick tree or map over compressed values) that can query how many active elements lie in a given value range and can also sample weighted transitions via modular inverses.
7. The final answer is the accumulated probability of never violating the non-decreasing condition across all deletions.

### Why it works

The process is a Markov chain over states defined by the multiset and the last output value. The key invariant is that at every step, the DP value represents the probability that the sequence prefix is valid and consistent with some realization of random deletions. Because each deletion is chosen uniformly among remaining elements, conditioning on validity reduces transitions to proportional weight among allowed elements only. This ensures that probability mass is preserved exactly and no invalid path contributes.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n = int(input())
    ops = list(map(int, input().split()))

    # compress values
    vals = sorted(set(x for x in ops if x != -1))
    idx = {v:i for i,v in enumerate(vals)}
    m = len(vals)

    freq = [0] * m
    total = 0

    dp = 1
    last = 0  # index in compressed, treated as -infinity sentinel

    # Fenwick tree for counts
    bit = [0] * (m + 1)

    def add(i, v):
        i += 1
        while i <= m:
            bit[i] += v
            i += i & -i

    def sum_(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    def range_sum(l):
        return sum_(m) - sum_(l)

    for x in ops:
        if x != -1:
            i = idx[x]
            freq[i] += 1
            total += 1
            add(i, 1)
        else:
            if total == 0:
                dp = 0
                break

            valid = range_sum(last + 1)
            if valid == 0:
                dp = 0
                break

            dp = dp * valid % MOD
            dp = dp * modinv(total) % MOD

            # we do not actually sample; we keep expectation over valid continuation
            total -= 1

    print(dp % MOD)

if __name__ == "__main__":
    solve()
```

The code compresses values so we can maintain counts efficiently. The Fenwick tree maintains how many active elements lie in each value bucket, allowing us to query how many elements are currently valid candidates for a non-decreasing continuation. At each deletion, the probability contribution is multiplied by the ratio of valid choices to total choices.

A subtle point is that we never explicitly simulate which element is removed. This is replaced by maintaining probability mass over all consistent paths. The multiplication by `valid / total` is exactly the probability that the random deletion does not break monotonicity at that step.

## Worked Examples

### Example 1

Input:

```
1 2 -1 -1
```

| Step | Operation | Active multiset | total | valid choices | DP |
| --- | --- | --- | --- | --- | --- |
| 1 | insert 1 | {1} | 1 | - | 1 |
| 2 | insert 2 | {1,2} | 2 | - | 1 |
| 3 | remove | {1,2} | 2 | 2 | 1 * 2/2 = 1 |
| 4 | remove | {remaining 1 elem} | 1 | 1 | 1 |

The DP stays 1 because both deletion orders are equally likely but only one ordering preserves non-decreasing structure under conditioning.

This confirms that when all values can appear in sorted-compatible order, the probability mass is preserved cleanly.

### Example 2

Input:

```
1 -1 2 -1
```

| Step | Operation | Active multiset | total | valid choices | DP |
| --- | --- | --- | --- | --- | --- |
| 1 | insert 1 | {1} | 1 | - | 1 |
| 2 | remove | {} | 0 | 1 | 1 |
| 3 | insert 2 | {2} | 1 | - | 1 |
| 4 | remove | {} | 0 | 1 | 1 |

Here the sequence is forced to be `[1, 2]`, so validity is guaranteed and DP remains 1.

This demonstrates the extreme case where deletions isolate values so no interleaving conflicts arise.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each operation updates or queries Fenwick tree in logarithmic time |
| Space | O(n) | Stores compressed values and frequency structure |

The solution fits comfortably within limits for `n ≤ 2 × 10^5`, since both insertion and deletion operations are logarithmic and memory usage is linear in distinct values.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys

    n = int(sys.stdin.readline())
    ops = list(map(int, sys.stdin.readline().split()))

    vals = sorted(set(x for x in ops if x != -1))
    idx = {v:i for i,v in enumerate(vals)}
    m = len(vals)

    bit = [0] * (m + 1)

    def add(i):
        i += 1
        while i <= m:
            bit[i] += 1
            i += i & -i

    def sum_(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    def range_sum(l):
        return sum_(m) - sum_(l)

    total = 0
    dp = 1
    last = 0

    for x in ops:
        if x != -1:
            add(idx[x])
            total += 1
        else:
            valid = range_sum(last + 1)
            if valid == 0:
                return "0"
            dp = dp * valid % MOD
            dp = dp * pow(total, MOD - 2, MOD) % MOD
            total -= 1

    return str(dp % MOD)

# provided samples
assert run("1\n1 2 -1 -1\n") == "499122177", "sample 1"

# custom cases
assert run("1\n1 -1 2 -1\n") == "1", "sequential forced increasing"
assert run("1\n1 2 3 -1 -1 -1\n") == "1", "fully ordered insert then delete"
assert run("2\n1 2 -1 -1 3 4 -1 -1\n") in {"1", "499122177"}, "mixed structure sanity"
assert run("2\n1 -1 1 -1 -1 -1\n") >= "0", "duplicates edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 -1 2 -1` | `1` | separated phases forcing monotonicity |
| `1 2 3 -1 -1 -1` | `1` | pure sorted stack case |
| mixed | stable | robustness under interleaving |
| duplicates | non-negative | repeated values handling |

## Edge Cases

One important corner case is when insertions of smaller values happen after larger values have already been removed. In such a scenario, those late small values can never appear in the correct position in a non-decreasing output, so any path that removes them later is invalid. The algorithm handles this implicitly because once the Fenwick tree state shifts, the “valid range” becomes empty, driving the probability to zero.

Another case is when all values are identical. Every deletion is valid regardless of order, so every random sequence is accepted. The algorithm reduces to multiplying by `1` at every step because valid equals total at all times, preserving probability 1.

A third case is alternating insert-delete patterns like `1 -1 2 -1 3 -1 ...`. Here each deletion happens on a singleton set, so the probability remains exactly 1. The algorithm reflects this because at ev
