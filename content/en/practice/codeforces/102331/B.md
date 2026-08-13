---
title: "CF 102331B - Bitwise Xor"
description: "We have an array of up to (300000) integers, each using at most 60 bits, and a threshold (x). A subsequence is considered good when every pair of selected array elements has XOR at least (x)."
date: "2026-08-14T01:11:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "B"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 367
verified: true
draft: false
---

[CF 102331B - Bitwise Xor](https://codeforces.com/problemset/problem/102331/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of up to (300000) integers, each using at most 60 bits, and a threshold (x). A subsequence is considered good when every pair of selected array elements has XOR at least (x). The task is to count all non-empty good subsequences, with the answer taken modulo (998244353). The original problem uses a 2 second time limit and 1 GiB memory limit.

The original order of the array only determines which indices form a subsequence. The condition itself depends only on the values selected. This means we can first sort the values and count valid selections from that sorted order. Sorting does not lose any subsequence: equal values remain separate elements, and after sorting each subset of positions still corresponds to exactly one subset of the original positions.

The bound (n\le300000) immediately rules out anything quadratic in (n), since (n^2) is about (9\cdot10^{10}). The 60-bit bound is much more useful: operations that inspect one bit at a time can afford roughly 60 work per element, giving an (O(60n)) algorithm. The large memory limit also makes a trie natural in C++, but a straightforward 60-level trie can contain tens of millions of nodes, which is unnecessarily expensive in Python. The implementation below uses a compressed binary trie, keeping only branching nodes, so its size is linear in the number of distinct values.

There are several edge cases that can silently break a careless implementation. When (x=0), every XOR is non-negative, so every non-empty subsequence is valid. For example, input `3 0` with values `0 1 2` has answer (2^3-1=7). A solution that treats equality as invalid would incorrectly exclude pairs with XOR zero.

When equal values occur and (x>0), two copies of the same value cannot be selected together because their XOR is zero. For example, `3 1` with values `5 5 5` has answer `3`, since only the three singleton subsequences work. A careless solution that deduplicates the array would get `1`, because the three equal positions are still three different subsequence choices.

The boundary (a_i\oplus a_j=x) is valid because the condition is greater than or equal to (x). For example, `2 2` with values `0 2` has answer `3`: both singletons and the pair are valid because (0\oplus2=2). An implementation using `>` instead of `>=` would return `2`.

Finally, sorting is essential to the reduction, but the sorted positions are not the original subsequence indices. For example, `3 2` with values `2 0 1` still has answer `5`. A solution that assumes the original array is already ordered would miss valid transitions.

## Approaches

The direct brute-force approach is to enumerate every non-empty subsequence and check all pairs inside it. For a subset of size (k), this takes (\binom{k}{2}) XOR comparisons. Summed over all subsets, the number of pair checks in the worst case is

\binom n2 2^{n-2}.
]

For (n=300000), this is beyond any practical limit. Even enumerating subsets without checking all pairs already requires (2^n) operations.

The first useful observation comes from sorting the values. Suppose (a\le b\le c). Look at the highest bit where the three numbers are not all equal. There are only two possibilities. Either (a) differs from both (b) and (c) at that bit, or (c) differs from both (a) and (b). In the first case, (a\oplus b) and (a\oplus c) have that high bit set while (b\oplus c) does not, so (b\oplus c) is smaller than both. In the second case, (a\oplus b) is smaller than both other XORs. Consequently,

[
\min(a\oplus b,b\oplus c)\le a\oplus c.
]

This property has a strong consequence. Take any selected values in sorted order,

[
b_1\le b_2\le\cdots\le b_k.
]

If every pair of consecutive selected values has XOR at least (x), then every non-consecutive pair also has XOR at least (x). For three consecutive selected values, the inequality above says that the XOR of the outer pair is at least the smaller XOR of the two neighboring pairs. Applying the same argument repeatedly extends this to arbitrary distances.

So after sorting, the original all-pairs condition becomes a local condition: a subsequence is valid exactly when every two consecutive selected values have XOR at least (x).

This changes the counting problem into a dynamic program. Let (f_i) be the number of valid subsequences whose last selected element is the (i)-th value in the sorted array. The last element can stand alone, giving one subsequence. Otherwise we append (a_i) to any valid subsequence ending at some (j<i) with

[
a_j\oplus a_i\ge x.
]

Thus

1+
\sum_{\substack{j<i\a_j\oplus a_i\ge x}}f_j.
]

The remaining problem is to calculate this weighted XOR threshold query efficiently.

A standard binary trie solves the query in (O(60)). At every bit, we compare the XOR bit with the corresponding bit of (x). If the corresponding bit of (x) is zero, taking an XOR bit of one makes the entire XOR larger regardless of lower bits, so that whole trie subtree can be added immediately. If the bit of (x) is one, the XOR bit must also be one to remain equal to (x)'s prefix, so only one branch can continue.

The usual trie has up to (60n) nodes. That is acceptable in a low-level language, but it is a poor representation in Python. Since all values are known before the DP starts, we can build a compressed binary trie containing only the branching points. A compressed trie has (O(n)) nodes, while a query still follows at most 60 branching levels.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2 2^n)) | (O(n)) | Too slow |
| Standard binary trie DP | (O(n\log A)) | (O(n\log A)) | Accepted in low-level languages |
| Compressed binary trie DP | (O(n\log A)) | (O(n)) | Accepted |

Here (\log A\le60).

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. The original all-pairs condition can now be replaced by checking only consecutive selected values, because for (a\le b\le c),

[
\min(a\oplus b,b\oplus c)\le a\oplus c.
]

Thus, if the consecutive selected pairs all satisfy the threshold, every other pair does too.

1. Group equal values into one leaf of a compressed binary trie. The DP still treats equal occurrences separately, so this is only a structural compression of the value space, not a removal of array elements.
2. Build the compressed trie recursively. For a set of at least two distinct values, find the highest bit on which the smallest and largest values differ. That bit separates the set into a zero group and a one group, both contiguous because the values are sorted. Recursively build the two groups.
3. Give every trie node a subtree sum. This sum represents the total (f_j) of already processed array elements whose values belong to that subtree. Initially every sum is zero.
4. Process the sorted array from left to right. For the current value (v), query the trie for the total DP weight of previous values (y) satisfying

[
v\oplus y\ge x.
]

Call the returned sum (q). Then

[
f=1+q.
]

The `1` represents the singleton subsequence containing only the current position.

1. Add (f) to the global answer and insert this DP weight into the leaf representing (v). The weight is also propagated through every ancestor so that future queries see the correct subtree sums.
2. To perform the compressed-trie query, keep the comparison with (x) equal so far. At an internal node, its branching bit is the next bit that can differ between values in its two children. Before using that bit, the bits skipped by compression are fixed for the whole subtree. Compare those fixed bits against (x). If the fixed XOR prefix is already greater than (x), the entire subtree can be added. If it is smaller, the entire subtree can be discarded.
3. If the fixed prefix is equal, inspect the branching bit. When the corresponding bit of (x) is zero, the child producing XOR bit one is entirely valid and can be added, while the child producing XOR bit zero continues the equality path. When the corresponding bit of (x) is one, only the child producing XOR bit one can continue.
4. At a leaf, all bits are fixed, so directly test whether its value XOR the current value is at least (x). The leaf's stored sum is then either included or ignored.
5. Take every DP value modulo (998244353). Python integers do not overflow, but reducing after additions keeps the stored subtree sums small and matches the required output modulus.

Why it works: after sorting, the key invariant is that a partial subsequence counted by (f_i) is valid exactly when its consecutive selected values satisfy the XOR threshold. The transition considers every possible previous endpoint satisfying that threshold, so every valid subsequence ending at (i) is counted exactly once. The compressed trie does not change the set of stored values. It only skips bit positions where every value in a subtree has the same bit, and those skipped bits can be compared against (x) as a fixed prefix. Hence every subtree added by the query consists entirely of valid predecessors, while every discarded subtree consists entirely of invalid predecessors.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

MOD = 998244353
TOP = 59

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    # Only distinct values need structural nodes.
    vals = []
    for v in a:
        if not vals or vals[-1] != v:
            vals.append(v)

    m = len(vals)

    # Compressed binary trie.
    #
    # bit[u]  : branching bit, -1 for a leaf
    # left[u] : child with bit 0
    # right[u]: child with bit 1
    # rep[u]  : any representative value in the subtree
    # total[u]: sum of dp values currently stored in the subtree
    # parent[u]: parent node
    bit = []
    left = []
    right = []
    rep = []
    total = []
    parent = []

    leaf_of = {}

    def new_node(b, lch, rch, representative, par):
        idx = len(bit)
        bit.append(b)
        left.append(lch)
        right.append(rch)
        rep.append(representative)
        total.append(0)
        parent.append(par)
        return idx

    def build(lo, hi, par):
        if hi - lo == 1:
            v = vals[lo]
            u = new_node(-1, -1, -1, v, par)
            leaf_of[v] = u
            return u

        diff = vals[lo] ^ vals[hi - 1]
        b = diff.bit_length() - 1
        threshold = ((vals[lo] >> (b + 1)) << (b + 1)) | (1 << b)

        mid = bisect_left(vals, threshold, lo, hi)

        u = new_node(b, -1, -1, vals[lo], par)
        lc = build(lo, mid, u)
        rc = build(mid, hi, u)
        left[u] = lc
        right[u] = rc
        return u

    root = build(0, m, -1)

    def query(v):
        """
        Return the sum of dp values stored at y such that
        y xor v >= x.
        """
        u = root
        ans = 0

        # All bits above `top` are already known to be equal
        # between (representative xor v) and x.
        top = TOP

        while True:
            b = bit[u]

            if b == -1:
                if (rep[u] ^ v) >= x:
                    ans += total[u]
                    if ans >= MOD:
                        ans -= MOD
                return ans

            z = rep[u] ^ v

            # Bits b+1 ... top are fixed for the whole subtree.
            # If they already differ from x, the whole subtree has
            # the same comparison result.
            d = (z ^ x) >> (b + 1)
            if d:
                highest = b + 1 + d.bit_length() - 1
                if (z >> highest) & 1:
                    ans += total[u]
                    if ans >= MOD:
                        ans -= MOD
                return ans

            vb = (v >> b) & 1
            xb = (x >> b) & 1

            if xb == 0:
                # XOR bit 1 is already larger than x at this bit.
                greater_child = right[u] if vb == 0 else left[u]
                if greater_child != -1:
                    ans += total[greater_child]
                    if ans >= MOD:
                        ans -= MOD

                # XOR bit 0 keeps the prefix equal.
                equal_child = left[u] if vb == 0 else right[u]
            else:
                # XOR bit 0 would make the result smaller.
                # Only XOR bit 1 can keep equality.
                equal_child = right[u] if vb == 0 else left[u]

            if equal_child == -1:
                return ans

            u = equal_child
            top = b - 1

    answer = 0

    for v in a:
        dp = query(v) + 1
        if dp >= MOD:
            dp -= MOD

        answer += dp
        if answer >= MOD:
            answer -= MOD

        u = leaf_of[v]
        while u != -1:
            total[u] += dp
            if total[u] >= MOD:
                total[u] -= MOD
            u = parent[u]

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part sorts the array and creates `vals`, the sorted list of distinct values. Duplicates are retained in `a`, because every occurrence represents a different array position and consequently a different possible subsequence. The compressed trie only stores one structural leaf per distinct value.

The `build` function finds the highest bit that differs between the smallest and largest value of a subtree. Since that is the first differing bit, all values below it have the same higher-bit prefix. The values with this bit equal to zero form one contiguous range, and the values with it equal to one form another. The resulting tree has at most (2m-1) nodes for (m) distinct values.

The `total` array stores the sum of DP values in each subtree. Updating a leaf therefore requires walking through its ancestors. A path has at most 60 branching levels, so the update costs (O(60)).

The subtle part is `query`. A normal binary trie has a node at every bit position. The compressed trie skips positions where all values agree. At a compressed node, `rep[u]` represents those skipped bits for every value in that subtree. The expression

```
d = (z ^ x) >> (b + 1)
```

checks whether the skipped prefix already differs from (x). If it does, the highest differing bit determines the comparison for every value in the subtree, so the query can terminate immediately.

When the prefixes are equal, the current branching bit is handled exactly like an ordinary XOR threshold trie. For an (x) bit of zero, the branch producing XOR bit one is completely valid. For an (x) bit of one, the branch producing XOR bit zero is completely invalid. Only the equality branch needs further inspection.

The query is performed before inserting the current DP value. This is what guarantees that (f_i) only uses (j<i). The singleton contribution is then added separately with `+1`.

The values can be as large as (2^{60}-1), so the highest relevant bit is 59. Python has arbitrary-precision integers, so no overflow handling is needed. The modulus is applied to every stored sum and to the answer after each addition.

## Worked Examples

### Sample 1

The input is `n=3`, `x=0`, and the sorted values are `0,1,2`. Since every non-negative XOR is at least zero, every subsequence is valid.

| Step | Value (v) | Query result | (dp) | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 1 |
| 2 | 1 | 1 | 2 | 3 |
| 3 | 2 | 3 | 4 | 7 |

At the first element there are no previous values, so only the singleton is counted. At the second element, the singleton and the subsequence `[0,1]` are valid. At the third element, all four subsequences ending in `2` are valid. The final answer is (7), matching (2^3-1).

### Sample 2

Now (x=2), with sorted values `0,1,2`.

| Step | Value (v) | Valid previous DP sum | (dp) | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 1 |
| 2 | 1 | 0 | 1 | 2 |
| 3 | 2 | 2 | 3 | 5 |

For `v=1`, the only previous value is `0`, and (0\oplus1=1<2), so the pair cannot be formed. For `v=2`, both previous values work because (0\oplus2=2) and (1\oplus2=3). Thus the three valid subsequences ending at `2` are `[2]`, `[0,2]`, and `[1,2]`. The answer is `5`.

The second trace also exercises the equality boundary: XOR exactly equal to (x) is accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n+n\cdot60)) | Sorting costs (O(n\log n)), while each trie query and update follows at most 60 branching bits |
| Space | (O(n)) | The compressed trie has at most (2m-1) nodes for (m\le n) distinct values |

The largest input contains (300000) values, so the (O(n\log n)) sorting step and the constant 60-bit factor are both practical. The compressed representation is especially useful in Python because it avoids the roughly (60n) node explosion of an uncompressed binary trie. The original problem provides 1024 MiB of memory, and the compressed implementation uses linear space.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io
import random

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    "3 0\n"
    "0 1 2\n"
) == "7", "sample 1"

assert run(
    "3 2\n"
    "0 1 2\n"
) == "5", "sample 2"

assert run(
    "3 3\n"
    "0 1 2\n"
) == "4", "sample 3"

assert run(
    "7 4\n"
    "11 5 5 8 3 1 3\n"
) == "35", "sample 4"

# Minimum-size input
assert run(
    "1 123456789\n"
    "42\n"
) == "1", "single element"

# x = 0: every non-empty subsequence is valid
assert run(
    "4 0\n"
    "7 7 7 7\n"
) == "15", "x = 0"

# Equal values with positive x: only singletons are valid
assert run(
    "4 1\n"
    "5 5 5 5\n"
) == "4", "all equal values"

# Equality boundary: XOR exactly x must be accepted
assert run(
    "2 2\n"
    "0 2\n"
) == "3", "xor exactly x"

# Maximum 60-bit values
M = (1 << 60) - 1
assert run(
    f"3 {M}\n"
    f"0 {M} {M - 1}\n"
) == "4", "60-bit boundary"

# Maximum-size input, x = 0.
# Every one of the 2^n - 1 non-empty subsequences is valid.
n = 300000
big_input = f"{n} 0\n" + ("0 " * n) + "\n"
expected = (pow(2, n, 998244353) - 1) % 998244353
assert run(big_input) == str(expected), "maximum n"

# Small randomized cross-check against brute force.
def brute(a, x):
    n = len(a)
    ans = 0

    for mask in range(1, 1 << n):
        chosen = [a[i] for i in range(n) if mask >> i & 1]
        ok = True

        for i in range(len(chosen)):
            for j in range(i + 1, len(chosen)):
                if (chosen[i] ^ chosen[j]) < x:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            ans += 1

    return ans % 998244353

rng = random.Random(0)

for n in range(1, 8):
    for _ in range(50):
        a = [rng.randrange(16) for _ in range(n)]
        x = rng.randrange(16)

        inp = f"{n} {x}\n" + " ".join(map(str, a)) + "\n"
        expected = brute(a, x)

        assert run(inp) == str(expected), (
            f"random test failed: n={n}, x={x}, a={a}"
        )
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 123456789 / 42` | `1` | Minimum size and singleton handling |
| `4 0 / 7 7 7 7` | `15` | The special case (x=0) and duplicate positions |
| `4 1 / 5 5 5 5` | `4` | Equal values cannot form pairs when (x>0) |
| `2 2 / 0 2` | `3` | The `>= x` boundary |
| `3 (2^60-1) / 0, 2^60-1, 2^60-2` | `4` | Highest supported bit |
| `300000 0 / 300000 zeros` | (2^{300000}-1\bmod998244353) | Maximum (n), large answer, and performance |
| Random cases with (n\le7) | Brute-force result | Cross-checks the complete DP and trie logic |

## Edge Cases

For (x=0), consider `4 0` with values `7 7 7 7`. Every pair has XOR at least zero, including equal-value pairs whose XOR is zero. The DP query accepts every previous value, so the DP values are (1,2,4,8), giving (15). The compressed trie does not need a special code path for (x=0), because at every bit an XOR bit of one is already greater than the corresponding zero bit, while the equality branch eventually reaches the leaf and accepts XOR zero.

For all equal values with positive (x), consider `4 1` with values `5 5 5 5`. Every pair of equal values has XOR zero, so only the four singleton subsequences are valid. The trie contains one leaf for value `5`, but its stored weight is updated after each occurrence. Every later query reaches that leaf and rejects it because `5 xor 5 = 0 < 1`. Thus each DP value remains one.

For the equality boundary, consider `2 2` with values `0 2`. After processing `0`, its DP value is one. When processing `2`, the trie query sees (0\oplus2=2), which is exactly (x), so it includes that previous DP value. The second DP value is consequently two, representing `[2]` and `[0,2]`, and the final answer is three.

For the 60-bit boundary, consider

```
3 1152921504606846975
0 1152921504606846975 1152921504606846974
```

The threshold is (2^{60}-1). The pair `0` with (2^{60}-1) has XOR exactly equal to the threshold and is valid. The other two pairs have XOR below the threshold, so the valid subsequences are the three singletons plus that one pair, giving `4`. The implementation checks bits 59 through 0, so the highest allowed bit is handled without an off-by-one error.

For the maximum-size case with (x=0), take (300000) zeros. Every non-empty subset of the 300000 positions is valid, so the answer is (2^{300000}-1) modulo (998244353). The DP counts these subsets without ever enumerating them. Each new zero can extend every previously counted subsequence, giving the familiar doubling sequence (1,2,4,\ldots), while the compressed trie stores only one leaf because all values are identical.
