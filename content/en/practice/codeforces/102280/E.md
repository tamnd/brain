---
title: "CF 102280E - \u0428\u0442\u0440\u0430\u0444"
description: "We have a collection of individual banknotes. Each banknote has a denomination, and every banknote can be used at most once. Given a fine amount p, we need to choose some of the available banknotes whose total value is as small as possible while still being at least p."
date: "2026-08-13T09:48:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "E"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 189
verified: true
draft: false
---

[CF 102280E - \u0428\u0442\u0440\u0430\u0444](https://codeforces.com/problemset/problem/102280/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of individual banknotes. Each banknote has a denomination, and every banknote can be used at most once. Given a fine amount `p`, we need to choose some of the available banknotes whose total value is as small as possible while still being at least `p`.

The output must contain that minimum payable sum and the actual denominations used to obtain it. If no subset of the banknotes can reach `p`, the answer is `-1`.

The bounds shape the solution quite strongly. There are at most `1000` banknotes, while the fine is at most `100000` and a denomination can be as large as `1000000`. A conventional subset-sum dynamic program with states from `0` to `p` and a transition for every banknote costs `O(n p)`, which can reach about `10^8` state updates. With a 1.5 second limit, that is too expensive, especially in Python. We need to exploit the fact that the state set is a bitset, so many subset-sum transitions can be performed simultaneously.

The large denomination bound also matters. We cannot simply make the DP range `0..sum(q)`, because the total value can be as large as `10^9`. Fortunately, sums greater than `p` do not need to be represented during the subset-sum phase. The final banknote can be the one that pushes the total over `p`.

There are several edge cases that can silently break an otherwise plausible implementation. If `p = 0`, the empty set is already a valid payment, so the answer is `0`, with no banknotes. For example, `0 2` with denominations `5 10` must produce `0`, not `5`.

Duplicate denominations are also separate banknotes. For `p = 6` and `n = 3` with `3 3 10`, the correct answer is `6`, using both `3` banknotes. Treating the input as a set of denominations would incorrectly lose one of them.

A banknote larger than the fine may itself be the optimal answer. For `p = 7` and denominations `10 20`, the answer is `10`. A DP restricted to sums at most `p` cannot represent `10`, so the algorithm must consider a banknote as the final step separately.

Finally, reaching `p` exactly must beat every solution larger than `p`. For `p = 10` and denominations `6 4 20`, the answer is `10`, using `6 + 4`. An approach that only searches for the first sum greater than `p` would miss this optimal case.

## Approaches

The direct approach is the usual 0/1 subset-sum dynamic programming. Let `dp[s]` tell us whether some processed banknotes have total value exactly `s`. For every banknote with value `q`, we iterate over all sums and mark `s + q` as reachable. This is correct because every subset either excludes the current banknote or includes it, and iterating sums in descending order prevents using the same banknote more than once.

The problem is the number of operations. There are up to `1000` banknotes and up to `100000` relevant sums, giving roughly `100000000` transitions in the worst case. That is too much for the time limit, and Python would be particularly unsuitable for such a loop.

The key observation is that the DP state is just a set of integers. We can represent that set by the bits of one large integer. If bit `s` is set, sum `s` is reachable. Adding a banknote of value `q` then becomes a single integer shift:

`bits | (bits << q)`

The shift represents taking the current banknote, while the original `bits` represents skipping it. Python's arbitrary-precision integers perform this operation over machine words internally, so instead of processing `p` states separately, the transition processes many states in parallel.

There is one more issue because we need the actual banknotes, not merely the minimum sum. We solve reconstruction at the same time. Whenever a sum becomes reachable for the first time, we store which banknote created it. Since a sum is recorded only when it was previously unreachable, its predecessor was already reachable before the current banknote was processed. Following these stored predecessors reconstructs a valid subset.

We also need to handle the possibility that the answer is greater than `p`. Before adding each banknote to the DP, we look at all currently reachable sums that can be combined with this banknote to reach at least `p`. Because we process banknotes one by one, those sums use only earlier banknotes, so the current banknote cannot accidentally be used twice. We select the smallest such reachable sum, giving the smallest candidate involving the current banknote.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n p)` | `O(p)` | Too slow |
| Optimal bitset DP | `O(n p / W + p)` word operations | `O(p)` bits plus reconstruction data | Accepted |

Here `W` is the machine word size used internally by Python's big integers. The exact implementation cost is governed by the size of the integers involved rather than by one operation per DP state.

## Algorithm Walkthrough

1. Read `p` and the list of banknotes. If `p = 0`, immediately output `0` because paying nothing is already the minimum possible sum.
2. Represent all currently reachable subset sums by one integer `bits`. Bit `s` is set exactly when sum `s` can be formed from the banknotes processed so far. Initially only sum `0` is reachable, so `bits = 1`.
3. Create a `parent` array indexed by sums from `0` through `p`. For every newly reachable sum `s`, store the index of the banknote that created it. The predecessor of `s` is then `s - q[index]`.
4. Process the banknotes from left to right. Before adding the current banknote `q`, search the current `bits` for the smallest reachable sum `s` satisfying `s + q >= p`. If such a sum exists, `s + q` is a valid candidate answer using the current banknote and only earlier banknotes.
5. Keep the smallest candidate found. If the candidate is exactly `p`, it is globally optimal, so reconstruct it immediately. No larger sum can improve on an exact payment.
6. Update the subset-sum bitset with the current banknote using `shifted = bits << q`. Restrict the result to sums at most `p`, because larger intermediate sums are unnecessary. The newly reachable sums are `shifted & ~bits`.
7. For every newly reachable sum, store the current banknote index in `parent`. These sums are being created for the first time, so their previous state cannot already have contained them.
8. Merge the shifted states into `bits`. If bit `p` becomes set, reconstruct the exact payment from `parent[p]` because `p` itself is now reachable.
9. If all banknotes have been processed without reaching `p` and without finding a candidate above `p`, output `-1`. Otherwise reconstruct the best candidate by repeatedly taking the stored parent banknote and subtracting its denomination from the current sum.

Why it works: before processing banknote `i`, `bits` contains exactly the sums obtainable using banknotes with indices smaller than `i`. When we inspect a candidate `s + q[i]`, the banknote `i` is not part of `s`, so the resulting subset is valid. Taking the smallest such candidate for every banknote considers every possible solution according to its largest-index banknote. Exact sum `p` is handled directly by the subset-sum DP. For reconstruction, every stored parent points to a sum that was already reachable before the corresponding banknote was added, so repeatedly following parents eventually reaches sum `0` and produces a valid subset. Since every possible payment is either exactly `p` or has a last banknote whose addition crosses `p`, the minimum candidate found is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    first = input().split()
    if not first:
        return

    p, n = map(int, first)

    if n:
        q = list(map(int, input().split()))
    else:
        q = []

    if p == 0:
        print(0)
        print()
        return

    # Bit s is 1 iff sum s is reachable.
    # We only need sums from 0 through p.
    limit_mask = (1 << (p + 1)) - 1
    bits = 1  # sum 0

    # parent[s] = index of the banknote that first made s reachable.
    parent = [-1] * (p + 1)

    best_sum = None
    best_last = -1
    best_base = -1

    for i, value in enumerate(q):
        # Find the smallest currently reachable s such that
        # s + value >= p.
        threshold = max(0, p - value)

        candidates = bits >> threshold
        if candidates:
            # Position of the lowest set bit in candidates.
            offset = (candidates & -candidates).bit_length() - 1
            base = threshold + offset
            candidate = base + value

            if best_sum is None or candidate < best_sum:
                best_sum = candidate
                best_last = i
                best_base = base

        # If we already have an exact payment, it is optimal.
        if best_sum == p:
            break

        # Add this banknote to the subset-sum DP.
        shifted = (bits << value) & limit_mask
        new_bits = shifted & ~bits

        # Record reconstruction information for sums that are
        # becoming reachable for the first time.
        x = new_bits
        while x:
            low = x & -x
            s = low.bit_length() - 1
            parent[s] = i
            x -= low

        bits |= shifted

        # An exact payment is always better than every payment > p.
        if (bits >> p) & 1:
            best_sum = p
            best_last = -1
            best_base = p
            break

    if best_sum is None:
        print(-1)
        return

    answer = []

    if best_sum == p and best_last == -1:
        # Reconstruct an exact subset ending at sum p.
        cur = p
        while cur > 0:
            i = parent[cur]
            if i == -1:
                print(-1)
                return
            answer.append(q[i])
            cur -= q[i]
    else:
        # The last banknote is best_last, and the earlier banknotes
        # form best_base.
        answer.append(q[best_last])

        cur = best_base
        while cur > 0:
            i = parent[cur]
            if i == -1:
                print(-1)
                return
            answer.append(q[i])
            cur -= q[i]

    print(best_sum)
    print(*answer)

if __name__ == "__main__":
    solve()
```

The `bits` integer is the central DP structure. Bit zero is initially set because the empty subset has sum zero. For a denomination `value`, shifting `bits` left by `value` creates every sum obtainable by taking that banknote. OR-ing the shifted value with the old bitset represents both choices for the banknote.

The mask `(1 << (p + 1)) - 1` discards sums larger than `p`. Such sums are not needed as intermediate states because any optimal solution above `p` can be viewed as a reachable sum below `p` followed by its final banknote.

The expression `bits >> threshold` removes every reachable sum smaller than `threshold`. Its lowest set bit then corresponds to the smallest reachable `s >= threshold`. This gives the smallest possible total `s + value` for the current final banknote.

The reconstruction array is filled only from `new_bits`, not from every set bit in `shifted`. This is essential. A sum that was already reachable should retain its earlier parent, because that parent describes a subset formed without the current banknote. Processing only newly reachable sums also guarantees that the predecessor of every stored state is already established.

Python integers do not overflow, so denomination sums themselves are safe. The DP integer is explicitly masked to `p + 1` bits, which keeps its size bounded and prevents large denominations from creating unnecessarily large intermediate integers.

The reconstruction uses banknote indices indirectly through `parent`. Duplicate denominations cause no problem because each occurrence has a distinct index during DP, even though the output contains only the denomination values.

## Worked Examples

### Sample 1

Input:

```
15 8
20 10 5 5 3 2 1 1
```

The optimal payment is `15`, for example `10 + 5`.

| Step | Banknote | Threshold | Best crossing candidate | Reachable sums after update |
| --- | --- | --- | --- | --- |
| 1 | 20 | 0 | 20 | 0 |
| 2 | 10 | 5 | none | 0, 10 |
| 3 | 5 | 10 | 15 | 0, 5, 10, 15 |

At the third banknote, sum `10` was already reachable using the second banknote. Adding `5` gives exactly `15`, so the algorithm can stop. The stored parents reconstruct `10` and `5`.

This demonstrates why the current banknote is checked before it is inserted into the bitset. The candidate `10 + 5` uses two distinct banknotes.

### Sample 2

Input:

```
2 3
10 3 3
```

The answer is `3`, because a single `3` is the smallest available sum at least `2`.

| Step | Banknote | Threshold | Best crossing candidate | Reachable sums after update |
| --- | --- | --- | --- | --- |
| 1 | 10 | 0 | 10 | 0 |
| 2 | 3 | 0 | 3 | 0 |
| 3 | 3 | 0 | 3 | 0 |

The first banknote gives candidate `10`. The second gives candidate `3`, which is better. The third also gives `3`, but does not improve the answer.

The interesting detail is that sums above `p` are not stored in `bits`. The denomination `10` is still considered correctly as a final banknote, even though bit `10` never appears in the DP.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n p / W + p)` word operations, plus `O(p)` total reconstruction-parent assignments | Each bitset transition processes `p` bits in machine-word chunks, while every reachable sum receives a parent at most once |
| Space | `O(p)` bits for the DP and `O(p)` integers for parents | Only sums from `0` through `p` are stored |

With `p <= 100000`, the bitset itself is only about 12.5 KB when represented as raw bits. The parent array is larger because Python integers are objects, but it still stores only `p + 1` entries. The algorithm avoids the `O(n p)` Python-level nested loop that would be the main performance problem under the 1.5 second limit.

## Test Cases

The exact output can legitimately differ from the sample because the statement allows any optimal subset. For that reason, the test helper below validates the output semantically rather than requiring one particular ordering or subset.

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str):
    data = inp.split()
    p = int(data[0])
    n = int(data[1])
    bills = list(map(int, data[2:2 + n]))

    lines = out.strip().splitlines()

    if p == 0:
        assert lines[0] == "0"
        return

    if lines[0] == "-1":
        # Verify that no subset can reach p by brute force.
        reachable = {0}
        for x in bills:
            reachable |= {s + x for s in list(reachable)}
        assert all(s < p for s in reachable)
        return

    total = int(lines[0])
    used = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []

    assert total == sum(used)
    assert total >= p

    remaining = bills[:]
    for x in used:
        assert x in remaining
        remaining.remove(x)

    # Verify optimality independently for these small test cases.
    reachable = {0}
    for x in bills:
        reachable |= {s + x for s in list(reachable)}

    optimum = min((s for s in reachable if s >= p), default=None)
    assert optimum == total

def solve():
    first = input().split()
    if not first:
        return

    p, n = map(int, first)
    q = list(map(int, input().split())) if n else []

    if p == 0:
        print(0)
        print()
        return

    limit_mask = (1 << (p + 1)) - 1
    bits = 1
    parent = [-1] * (p + 1)

    best_sum = None
    best_last = -1
    best_base = -1

    for i, value in enumerate(q):
        threshold = max(0, p - value)

        candidates = bits >> threshold
        if candidates:
            offset = (candidates & -candidates).bit_length() - 1
            base = threshold + offset
            candidate = base + value

            if best_sum is None or candidate < best_sum:
                best_sum = candidate
                best_last = i
                best_base = base

        if best_sum == p:
            break

        shifted = (bits << value) & limit_mask
        new_bits = shifted & ~bits

        x = new_bits
        while x:
            low = x & -x
            s = low.bit_length() - 1
            parent[s] = i
            x -= low

        bits |= shifted

        if (bits >> p) & 1:
            best_sum = p
            best_last = -1
            best_base = p
            break

    if best_sum is None:
        print(-1)
        return

    answer = []

    if best_sum == p and best_last == -1:
        cur = p
        while cur:
            i = parent[cur]
            assert i != -1
            answer.append(q[i])
            cur -= q[i]
    else:
        answer.append(q[best_last])
        cur = best_base
        while cur:
            i = parent[cur]
            assert i != -1
            answer.append(q[i])
            cur -= q[i]

    print(best_sum)
    print(*answer)

# Provided sample 1
sample1 = """15 8
20 10 5 5 3 2 1 1
"""
out = solve_io(sample1)
validate(sample1, out)

# Provided sample 2
sample2 = """2 3
10 3 3
"""
out = solve_io(sample2)
validate(sample2, out)

# p = 0, empty payment is optimal.
case3 = """0 0
"""
out = solve_io(case3)
validate(case3, out)

# Exact boundary, requires two equal banknotes.
case4 = """6 3
3 3 10
"""
out = solve_io(case4)
validate(case4, out)

# No possible payment.
case5 = """100 3
20 30 40
"""
out = solve_io(case5)
validate(case5, out)

# Large denomination should be considered as a final banknote.
case6 = """7 2
10 20
"""
out = solve_io(case6)
validate(case6, out)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `15 8 / 20 10 5 5 3 2 1 1` | Any subset totaling `15` | Provided sample and exact-payment reconstruction |
| `2 3 / 10 3 3` | `3` with one `3` | A denomination larger than the fine and duplicate values |
| `0 0` | `0` | Minimum fine and empty subset |
| `6 3 / 3 3 10` | `6` with both `3` banknotes | Multiple copies of the same denomination |
| `100 3 / 20 30 40` | `-1` | Impossible target |
| `7 2 / 10 20` | `10` with one `10` | Answer strictly greater than `p` |

## Edge Cases

For `p = 0`, the input `0 0` is handled before the DP begins. The empty subset has sum `0`, so the algorithm prints `0` and an empty second line. Trying to force at least one banknote would produce a non-minimal answer.

For duplicate denominations, consider `6 3` with `3 3 10`. The first `3` makes sum `3` reachable, and the second `3` then makes sum `6` reachable. The parent of sum `6` points to the second banknote, while the parent of sum `3` points to the first. Following the chain gives two separate banknotes, both worth `3`.

For a denomination larger than the target, consider `7 2` with `10 20`. Before the first banknote is added, sum `0` is reachable. Since `0 >= 7 - 10`, the candidate `0 + 10 = 10` is immediately recorded. No DP state for sum `10` is required. This is exactly why the final-banknote check is performed before the bitset transition.

For an exact payment, consider `10 3` with `6 4 20`. Before processing `4`, sum `6` is already reachable. The threshold for `4` is `6`, so the algorithm finds candidate `6 + 4 = 10`. It is exact, and the algorithm stops with banknotes `6` and `4`. A solution such as `20` is never allowed to replace it because every sum equal to `p` is optimal.

For an impossible payment, consider `100 3` with `20 30 40`. Every subset has sum at most `90`, so the bitset never sets bit `100`, and no final-banknote candidate reaches `100`. The algorithm consequently prints `-1`.
