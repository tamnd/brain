---
title: "CF 102331K - K-pop Strings"
description: "We need to count strings of length (n) over an alphabet of 35 characters, namely the digits 1 through 9 and the lowercase letters. A string is valid if it contains no tandem repeat whose length is at least (n-k)."
date: "2026-08-13T03:55:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "K"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 262
verified: true
draft: false
---

[CF 102331K - K-pop Strings](https://codeforces.com/problemset/problem/102331/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count strings of length (n) over an alphabet of 35 characters, namely the digits `1` through `9` and the lowercase letters. A string is valid if it contains no tandem repeat whose length is at least (n-k).

A tandem repeat is an even-length substring made from two identical consecutive halves. For example, `abab` is a tandem repeat because its two halves are both `ab`, while `abca` is not. The output is the number of length-(n) strings that avoid every such sufficiently long tandem repeat, modulo (998244353).

The useful part of the constraints is the small value of (k). Although (n) can be 100, every forbidden repeat has length at least (n-k), so there are only a small number of possible intervals that can be forbidden. In fact, the number of candidate tandem repeats is (O(k^2)), at most a few dozen for the given bounds. This makes an inclusion-exclusion search over the candidate repeats viable after a much stronger pruning observation.

A naive enumeration of all strings is completely impossible. For (n=100), there are (35^{100}), about (2.5\cdot10^{154}), strings. Even if checking one string took only (O(n^2)), the total would already be around (10^{158}) operations. A direct check of every candidate substring and every character comparison is closer to (O(35^n n^3)).

There are several boundary cases where an implementation can silently use the wrong set of forbidden intervals. For `1 16`, there cannot be any tandem repeat because every tandem repeat has positive even length, while the string has only one character. The correct answer is `35`.

For `4 0`, only a tandem repeat of length 4 qualifies. The only forbidden condition is (s_0=s_2) and (s_1=s_3), so the answer is (35^4-35^2=1499400). A solution that also forbids length-2 repeats here would be wrong.

For `2 16`, the threshold is (2-16=-14), so every tandem repeat qualifies. The only possible tandem repeat is the whole string, which means the two characters must not be equal. The answer is (35\cdot34=1190). A careless implementation that clamps the threshold to 2 or assumes (k<n) can mishandle this case.

For `3 0`, the threshold is 3, but tandem repeats must have even length. Consequently there are no forbidden substrings at all, and every string is valid. The answer is (35^3=42875). This catches code that treats the threshold itself as a possible repeat length without checking parity.

## Approaches

The brute-force approach is straightforward. Generate every one of the (35^n) strings and check whether it contains a forbidden tandem repeat. For each even interval of length at least (n-k), compare its first half with its second half. The test is correct because the definition of a K-pop string is exactly the absence of those intervals. The problem is the number of strings: at (n=100), the search space is roughly (2.5\cdot10^{154}), so even an unrealistically cheap test cannot make this approach useful.

The key change is to stop enumerating strings and instead enumerate the forbidden patterns. A particular tandem repeat does not require us to know the characters themselves. It only imposes equality constraints between positions. For example, the event that `abab` occurs at positions (0\ldots3) imposes (s_0=s_2) and (s_1=s_3).

Suppose we select several tandem-repeat events and require all of them to occur simultaneously. Every equality constraint connects two string positions. We can represent the constraints with a disjoint-set union structure. If the resulting equality graph has (c) connected components, then every component can independently choose one of the 35 characters, so exactly (35^c) strings satisfy all selected events.

This gives inclusion-exclusion. If the forbidden events are (E_1,E_2,\ldots,E_m), the number of valid strings is

[
35^n-\sum_i |E_i|+\sum_{i<j}|E_i\cap E_j|-\cdots.
]

The apparent problem is that there can be around 80 events, so (2^m) subsets are too many. The crucial observation is that many branches of this inclusion-exclusion are completely redundant. Suppose the already selected events force every equality required by the current event (E_i). Then adding (E_i) does not change the connected components at all. Every intersection containing (E_i) is identical to the corresponding intersection without (E_i), but has the opposite inclusion-exclusion sign. Those two contributions cancel, including all possible choices of later events. The whole branch can be discarded immediately.

We maintain the connected components with a rollback DSU. When an event is added, we record every successful union, recurse, and then undo exactly those unions. We process longer tandem repeats first. This ordering makes strong constraints appear early and causes later events to become redundant more often. The official editorial describes the same inclusion-exclusion and component-cancellation idea, and recommends decreasing repeat length as one of the effective orders.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(35^n n^3)) | (O(n)) | Too slow |
| Inclusion-exclusion with rollback DSU | (O(Bn\log n)) | (O(nk^2)) | Accepted |

Here (B) is the number of recursion nodes that survive the redundancy pruning. The search is still exponential in the theoretical worst case, but the whole point of the construction is that (k\le16), there are only (O(k^2)) events, and most inclusion-exclusion branches terminate as soon as their current event is already implied.

## Algorithm Walkthrough

1. Generate every possible forbidden tandem repeat. For an even length (L) with (L\ge n-k), choose its starting position (l) from (0) through (n-L). If (h=L/2), the event requires (s_{l+j}=s_{l+h+j}) for every (0\le j<h). We store those position pairs rather than the substring itself.
2. Sort the events by decreasing length. Longer repeats impose more equality constraints, so they tend to make later events redundant. The exact ordering is not part of the correctness proof, but it has a major effect on the practical size of the search tree.
3. Initialize a rollback DSU with one component for every string position. Initially there are (n) components, corresponding to (35^n) completely unrestricted strings.
4. Process the events recursively. First take the branch where the current event is not selected for inclusion-exclusion. Then temporarily add all equality constraints of the current event to the DSU and count how many unions actually changed the partition.
5. If adding the event performs no successful union, the event was already implied by the selected events. Its inclusion and exclusion branches cancel exactly, so return zero from this recursion state without examining later events.
6. If the event does introduce at least one new equality, recurse with the event included. Its inclusion-exclusion sign is negative relative to the branch where it was excluded, so subtract the result of the included branch from the excluded branch.
7. When all events have been processed, the current DSU contains exactly the equalities required by the selected subset of events. If it has (c) connected components, there are (35^c) compatible strings. Return that value.
8. After every included branch, roll the DSU back to the saved snapshot. This restores precisely the partition that existed before the current event was considered, so sibling recursion branches never affect one another.

Why it works: at every recursion state, the DSU represents exactly the equalities imposed by the events selected on the current inclusion-exclusion path. A connected component is one set of positions forced to carry the same character, and different components are independent, giving (35^c) assignments at a leaf. If the current event creates no new component merge, its constraint is already implied by the selected events. For every subset of later events, the intersection with the current event is then identical to the intersection without it, while the two inclusion-exclusion signs are opposite. Their contributions cancel, so returning zero is mathematically exact. Every non-redundant event is considered in both possible inclusion-exclusion choices, which means every subset is represented with its correct sign.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
ALPHABET = 35

def count_kpop(n, k):
    threshold = n - k

    events = []

    # An event is a forbidden tandem repeat.
    # For length L = 2*h starting at l, impose
    # s[l+j] == s[l+h+j] for 0 <= j < h.
    for L in range(max(2, threshold), n + 1):
        if L & 1:
            continue

        h = L // 2
        for l in range(n - L + 1):
            pairs = [(l + j, l + h + j) for j in range(h)]
            events.append((L, l, pairs))

    # Longer repeats first give much better pruning.
    events.sort(key=lambda x: (-x[0], x[1]))

    m = len(events)

    # powers[c] = 35^c mod MOD
    powers = [1] * (n + 1)
    for i in range(1, n + 1):
        powers[i] = powers[i - 1] * ALPHABET % MOD

    parent = list(range(n))
    size = [1] * n
    history = []
    components = n

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def unite(a, b):
        nonlocal components

        a = find(a)
        b = find(b)

        if a == b:
            return False

        if size[a] < size[b]:
            a, b = b, a

        # Store enough information to undo this union.
        history.append((b, a, size[a]))

        parent[b] = a
        size[a] += size[b]
        components -= 1
        return True

    def rollback(snapshot):
        nonlocal components

        while len(history) > snapshot:
            b, a, old_size_a = history.pop()
            parent[b] = b
            size[a] = old_size_a
            components += 1

    sys.setrecursionlimit(1000000)

    def dfs(idx):
        # All selected events have now been fixed.
        if idx == m:
            return powers[components]

        # If all positions are already equal, every remaining event
        # is implied, so all inclusion-exclusion contributions cancel.
        if components == 1:
            return 0

        # Exclude the current event.
        result = dfs(idx + 1)

        # Include the current event.
        snapshot = len(history)
        changed = False

        for a, b in events[idx][2]:
            if unite(a, b):
                changed = True

        # The event was already implied by the current constraints.
        # Including or excluding it gives identical intersections,
        # so their contributions cancel completely.
        if not changed:
            rollback(snapshot)
            return 0

        result -= dfs(idx + 1)
        result %= MOD

        rollback(snapshot)
        return result

    return dfs(0)

def main():
    n, k = map(int, input().split())
    print(count_kpop(n, k))

if __name__ == "__main__":
    main()
```

The first part of `count_kpop` constructs exactly the events that matter. The lower bound is `max(2, threshold)` because tandem repeats have positive even length. We still test parity separately, since an odd interval cannot be a tandem repeat.

Each event stores the equal-position pairs directly. This avoids doing any string manipulation during the recursion. For a repeat of length (2h), there are exactly (h) equality constraints.

The powers array is precomputed because a leaf of the recursion only needs the current number of DSU components. Looking up (35^c) is then constant time instead of performing modular exponentiation at every leaf.

The DSU deliberately does not use path compression. Path compression makes rollback complicated because one `find` operation can modify many parent pointers. Union by size is enough here because there are only (n\le100) positions, and it keeps every find operation logarithmic.

The `history` stack contains the exact information needed to undo a successful union. A failed union does not modify the DSU and therefore does not need to be recorded.

The most subtle part is the `changed` test. It is not enough to ask whether the event has any equality pairs. Every event does. What matters is whether at least one of its equalities connects two currently different components. If none does, the event adds no new information and its entire inclusion-exclusion subtree cancels.

The subtraction in `result -= dfs(idx + 1)` is the inclusion-exclusion sign. The branch without the event contributes positively relative to the current state, while the branch with the event contributes negatively. The final modulo operation keeps the result in the required range.

Python integers do not overflow, so all arithmetic is safe. The modulo is applied to the recursive result because inclusion-exclusion can produce negative intermediate values and very large positive values.

## Worked Examples

For Sample 1, the input is `1 16`. No even interval fits inside a string of length one, so the event list is empty.

| Event index | Components | Action | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | No events exist | (35^1=35) |

The recursion immediately reaches the leaf and returns (35). This demonstrates the boundary case where a very small string cannot contain any tandem repeat, regardless of the value of (k).

For Sample 2, the input is `4 0`. The threshold is 4, so the only forbidden event is the entire string. Its two halves have length 2, giving the equality constraints (s_0=s_2) and (s_1=s_3).

| Event index | Components | Action | Contribution |
| --- | --- | --- | --- |
| 0 | 4 | Exclude the event | (35^4=1500625) |
| 0 | 2 | Include the event | (-35^2=-1225) |
| 1 | 2 | Leaf | (35^2=1225) |

The final value is (1500625-1225=1499400). The DSU has two components after the event is included because positions 0 and 2 are tied together, and positions 1 and 3 are tied together. This exactly matches the (35^2) strings containing the length-4 tandem repeat.

For Sample 3, the input is `15 5`. The threshold is 10, so only even lengths 10, 12, and 14 are considered. Each possible starting position creates one event, giving a small collection of long equality patterns. The decreasing-length order lets the DSU accumulate strong constraints before shorter events are tested.

| Repeat length | Possible starts | Equality pairs per event |
| --- | --- | --- |
| 14 | 0, 1 | 7 |
| 12 | 0, 1, 2, 3 | 6 |
| 10 | 0, 1, 2, 3, 4, 5 | 5 |

The inclusion-exclusion recursion evaluates the compatible assignments for every non-redundant intersection and cancels every redundant branch. The resulting value is `911125634`, matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(Bn\log n)) | (B) is the number of recursion states that survive pruning; processing one event uses at most (O(n)) DSU operations |
| Space | (O(nk^2)) | There are (O(k^2)) events, each containing (O(n)) equality pairs, plus the rollback DSU |

The important practical parameter is (B), not the theoretical (2^m). Since (k\le16), there are only (O(k^2)) candidate repeats, and processing them from longest to shortest causes a large fraction of branches to terminate as soon as the current event is already implied. This is the intended approach for the given limits. The official tutorial explicitly describes the inclusion-exclusion pruning and the useful decreasing-length ordering.

## Test Cases

The following tests use the `count_kpop` function from the solution above. The helper redirects standard input so the assertions exercise the same input format as the submitted program.

```python
import sys
import io

MOD = 998244353

# Paste the solution's count_kpop function here,
# or import it from the submitted solution module.
from solution import count_kpop

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n, k = map(int, input().split())
        return str(count_kpop(n, k)) + "\n"
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("1 16\n") == "35\n", "sample 1"
assert run("4 0\n") == "1499400\n", "sample 2"
assert run("15 5\n") == "911125634\n", "sample 3"

# Minimum size. No tandem repeat can exist.
assert run("1 0\n") == "35\n", "minimum size"

# All length-2 strings are tandem repeats exactly when both characters
# are equal. The answer is 35 * 34.
assert run("2 16\n") == "1190\n", "all-equal boundary"

# Odd n with k = 0. No even substring can reach length 3.
assert run("3 0\n") == "42875\n", "odd-length boundary"

# For n = 100, k = 0, only the complete length-100 string can be
# a forbidden tandem repeat.
expected = (pow(35, 100, MOD) - pow(35, 50, MOD)) % MOD
assert run("100 0\n") == f"{expected}\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `35` | Minimum length and empty event set |
| `2 16` | `1190` | Very large (k), where the threshold becomes negative |
| `3 0` | `42875` | Odd threshold and the requirement that tandem lengths are even |
| `100 0` | (35^{100}-35^{50}\pmod{998244353}) | Maximum (n) and the single full-length event case |

## Edge Cases

For `1 16`, the event-generation loop starts at length 2, which is already larger than (n). The event list is empty, so the DSU starts with one component and the recursion returns (35^1=35). No artificial repeat of length one is introduced.

For `4 0`, the threshold is exactly 4. The only generated event has length 4 and two equality pairs. The include branch reduces the DSU from four components to two, contributing (35^2) bad strings. Inclusion-exclusion subtracts those from all (35^4) strings and gives `1499400`.

For `2 16`, the threshold is negative, but the implementation does not accidentally generate intervals of length zero or one. It starts from length 2 and therefore finds exactly one event, requiring the two positions to be equal. The included event leaves one DSU component, so its contribution is (35), and the result is (35^2-35=1190).

For `3 0`, the threshold is 3. The loop considers lengths from 3 to 3, but rejects 3 because it is odd. No events remain, so all (35^3=42875) strings are counted. This is why checking parity during event construction is essential.

For the maximum-size case `100 0`, the threshold is 100. Only the complete string can be a forbidden tandem repeat. Its two halves have length 50, so its equality constraints leave exactly 50 independent character choices. The result is (35^{100}-35^{50}) modulo (998244353), and the recursion contains only one event, making this case essentially the simplest possible inclusion-exclusion instance despite the maximum string length.
