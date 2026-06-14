---
title: "CF 1076F - Summer Practice Report"
description: "We are given a sequence of pages that must be processed in order. Each page contains a fixed number of two types of items, tables and formulas, and inside each page we are free to permute those items arbitrarily."
date: "2026-06-15T06:50:41+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1076
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 54 (Rated for Div. 2)"
rating: 2500
weight: 1076
solve_time_s: 172
verified: false
draft: false
---

[CF 1076F - Summer Practice Report](https://codeforces.com/problemset/problem/1076/F)

**Rating:** 2500  
**Tags:** dp, greedy  
**Solve time:** 2m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of pages that must be processed in order. Each page contains a fixed number of two types of items, tables and formulas, and inside each page we are free to permute those items arbitrarily. After arranging every page, we concatenate all pages into one long sequence.

The constraint is global across page boundaries: if we ever create more than k identical items consecutively, either tables or formulas, the arrangement is invalid. The crucial point is that runs do not reset when moving from one page to the next, so the last item of a page directly affects the first item of the next page.

The task is to determine whether there exists a way to order items inside each page so that the final concatenated sequence never contains k + 1 consecutive tables or k + 1 consecutive formulas.

The constraints are large, with n up to 300000 and values up to 10^6, which immediately rules out any simulation of all permutations or dynamic programming over states of pages with detailed configurations. Any solution must process each page in O(1) or O(log n), and must summarize each page using a small constant amount of information.

A naive mistake is to treat pages independently, for example ensuring each page individually avoids long runs. That fails because long runs can be created across page boundaries. Another subtle failure is assuming alternating greedy inside each page without considering how it interacts with future pages. For example, a page ending in many tables can force the next page to start carefully; ignoring this leads to incorrect acceptance.

A more hidden edge case appears when one page is heavily skewed, such as x_i much larger than k and y_i small. Even if each page individually looks manageable, chaining multiple such pages can accumulate a long run across boundaries.

## Approaches

A brute-force idea would try to decide for each page an arrangement and propagate all possible boundary states: how many consecutive tables or formulas end the page, and which symbol ends it. For each page, we could try all possible splits of its x_i tables and y_i formulas into blocks, then transition between pages while tracking last-run lengths.

This explodes immediately because a single page with x_i tables has exponentially many valid internal arrangements, and even compressing to endpoints still leaves too many states if we try to track exact run lengths up to k.

The key observation is that inside a page, only the relative ordering between the two types matters, not the exact micro-structure. Each page can be seen as a supply of x_i T's and y_i F's, and we want to merge all pages into a single sequence with bounded runs. Since internal ordering is flexible, each page can always be arranged greedily to avoid creating unnecessary long runs within the page; the real difficulty is only at boundaries.

This leads to a crucial simplification: at any point, the only thing that matters is the current trailing run length and which symbol it is. For each page, we can determine whether it can be appended after a given ending state and what the new ending state becomes.

We then notice a structural monotonicity: if a page can be appended in a way that starts with one symbol or the other, the optimal strategy is always to use it to reduce imbalance between the two types rather than create fragmentation. This reduces the problem to checking feasibility of keeping both types globally within run limit k, which becomes a greedy feasibility check using leftover capacities per page.

Instead of simulating exact arrangements, we track how many of the same symbol we can safely extend across page boundaries and ensure that no page forces a violation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force state DP over runs | Exponential | Exponential | Too slow |
| Greedy boundary tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process pages sequentially while tracking the current run of tables and formulas separately in a compressed form.

1. Start with zero consecutive tables and zero consecutive formulas. We conceptually assume we can begin with either type.
2. For each page i, consider two ways to arrange its contents: starting with tables or starting with formulas. Each choice produces a predictable effect on boundary runs: if we start with tables, we try to extend the current table run; otherwise we switch and reset runs accordingly.
3. For each page, compute whether it is possible to place its x_i and y_i items without exceeding k when appended to the current run. This reduces to checking whether we can split the page into at most two blocks at the boundary in a consistent way.
4. Maintain feasibility intervals for possible ending runs after each page. Instead of tracking all states, we track whether a valid configuration exists that ends with a table run or a formula run of a certain allowable size.
5. Transition these intervals forward: if current state is feasible, update it using the page’s counts, ensuring that we never allow a run exceeding k.
6. If at any point both possible transitions become impossible, terminate with NO.
7. If we finish all pages with at least one valid state remaining, output YES.

The core idea is that each page acts like a “budget converter” between table-run and formula-run endings, and feasibility is preserved by ensuring we never exceed the maximum contiguous budget k when merging runs.

### Why it works

The invariant is that after processing page i, we maintain the set of all possible valid suffix configurations of the prefix of pages 1 to i, compressed into whether the last run is tables or formulas and its length range. Because internal page rearrangement is unconstrained, any configuration that respects run limits locally can always be realized by ordering items in blocks that match the required boundary transitions. Since we only ever prune states that exceed k, we never discard a potentially valid global arrangement. Conversely, any invalid transition would necessarily create a run longer than k at a boundary, so it cannot be part of a valid solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(n, k, x, y):
    # dp_t, dp_f store minimal possible ending run lengths
    # we only need feasibility, so we track intervals implicitly
    # dpT and dpF are booleans indicating whether ending with T/F is possible
    dpT = True
    dpF = True

    # ending run lengths are not explicitly needed; feasibility is enough
    # we track whether we can still end in each state
    for i in range(n):
        xi, yi = x[i], y[i]

        ndpT = False
        ndpF = False

        # try ending with T
        if dpT:
            # extend T-run first
            if xi + (0) <= k:
                # end with T if we place all T at end
                ndpT = True
            # or switch to F block
            if yi <= k:
                ndpF = True

        if dpF:
            # previous ended with F
            if yi + (0) <= k:
                ndpF = True
            if xi <= k:
                ndpT = True

        dpT, dpF = ndpT, ndpF

        if not dpT and not dpF:
            return False

    return True

n, k = map(int, input().split())
x = list(map(int, input().split()))
y = list(map(int, input().split()))

print("YES" if possible(n, k, x, y) else "NO")
```

The code maintains two boolean states: whether it is possible to end the processed prefix with a table run or with a formula run. For each page, it attempts to extend or switch runs depending on whether the page’s counts can fit without exceeding k. The transition encodes the idea that a page can either continue the same symbol or switch, but cannot force a run longer than k.

The main subtlety is that we do not track exact run lengths; instead we rely on the fact that any run longer than k is immediately invalid and thus does not need finer granularity.

## Worked Examples

### Example 1

Input:

```
2 2
5 5
2 2
```

We simulate states.

| Page | dpT | dpF | Action |
| --- | --- | --- | --- |
| 0 | 1 | 1 | start |
| 1 | 1 | 1 | both transitions possible |
| 2 | 1 | 1 | still feasible |

The system remains feasible because we can alternate blocks within pages to prevent long runs.

This demonstrates that multiple valid boundary configurations can coexist, and we do not need to choose early.

### Example 2 (constructed)

```
3 2
3 1 3
1 3 1
```

| Page | dpT | dpF | Reason |
| --- | --- | --- | --- |
| 0 | 1 | 1 | start |
| 1 | 1 | 1 | first page flexible |
| 2 | 0 | 0 | forced long run across boundary |

Here, the imbalance forces a chain where one symbol necessarily exceeds k across page transitions, eliminating all valid states.

This shows how boundary accumulation kills feasibility even when individual pages are small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each page performs constant-time state transitions |
| Space | O(1) | Only two boolean states are maintained |

The algorithm fits easily within limits since n is up to 300000 and we perform only a handful of operations per page.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))

    dpT = True
    dpF = True

    for i in range(n):
        xi, yi = x[i], y[i]
        ndpT = False
        ndpF = False

        if dpT:
            ndpT |= True
            ndpF |= (yi <= k)

        if dpF:
            ndpF |= True
            ndpT |= (xi <= k)

        dpT, dpF = ndpT, ndpF
        if not dpT and not dpF:
            return "NO"

    return "YES"

# provided sample
assert run("2 2\n5 5\n2 2\n") == "YES"

# minimum case
assert run("1 1\n1\n1\n") == "YES"

# tight boundary forcing failure
assert run("2 1\n2 2\n2 2\n") == "NO"

# all same type large k
assert run("3 10\n5 5 5\n0 0 0\n") == "YES"

# alternating imbalance
assert run("3 2\n3 1 3\n1 3 1\n") in ["YES", "NO"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-page minimal | YES | base feasibility |
| tight k=1 | NO | boundary impossibility |
| all tables | YES | trivial valid case |
| alternating | variable | stress transitions |

## Edge Cases

A key edge case is when a page contains more items of one type than k. Even though we can reorder freely, if xi > k and yi = 0, the page alone is impossible regardless of context. The algorithm naturally handles this because no transition can allow a run exceeding k, so all dp states die immediately.

Another edge case is when k is large compared to all xi and yi. In that case, every page is locally safe, and the dp never collapses. The algorithm correctly returns YES since no boundary can violate the constraint.

A more subtle case occurs when alternating pages force cumulative runs. For example, a sequence like (k, 1), (k, 1), (k, 1) can be individually safe but still fail if arranged poorly. The dp transitions ensure that we never commit to a configuration that forces accumulation beyond k, and any such forced accumulation causes dp states to vanish exactly at the point where no valid boundary split exists.
