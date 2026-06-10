---
title: "CF 1553H - XOR and Distance"
description: "We have a set of distinct integers $a1,dots,an$, each lying in the range $[0,2^k)$. For every mask $x$, we XOR every array element with $x$, producing the set $${a1oplus x,dots,anoplus x}.$$ Among all pairs in that transformed set, we want the smallest absolute difference."
date: "2026-06-10T13:07:43+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "divide-and-conquer", "trees"]
categories: ["algorithms"]
codeforces_contest: 1553
codeforces_index: "H"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2021-2022 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 2900
weight: 1553
solve_time_s: 169
verified: true
draft: false
---

[CF 1553H - XOR and Distance](https://codeforces.com/problemset/problem/1553/H)

**Rating:** 2900  
**Tags:** bitmasks, divide and conquer, trees  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of distinct integers $a_1,\dots,a_n$, each lying in the range $[0,2^k)$.

For every mask $x$, we XOR every array element with $x$, producing the set

$$\{a_1\oplus x,\dots,a_n\oplus x\}.$$

Among all pairs in that transformed set, we want the smallest absolute difference. Let that value be $f(x)$.

The task is to compute $f(x)$ for every mask $x\in[0,2^k)$.

The first thing that makes this problem difficult is that there are up to $2^{19}=524288$ different masks, and we need an answer for every one of them. Any solution that processes each query mask independently is already in trouble.

A second obstacle is that $n$ can also be as large as $2^k$. Even checking all pairs for a single mask would take $O(n^2)$, which is completely impossible.

The interesting part is that $k\le 19$. Whenever the bit width is this small, a solution working directly on the whole $2^k$ mask space becomes realistic. A complexity around $O(k2^k)$ is roughly ten million operations, which fits comfortably.

A common mistake is to think that XOR preserves differences. It does not. For example, with numbers $0$ and $3$, the difference is $3$, but after XOR with $1$ they become $1$ and $2$, whose difference is only $1$.

Another easy trap is assuming the closest pair before XOR remains the closest pair afterward. Consider:

```
a = [0, 3, 6]
```

For $x=0$, the answer is $3$. For $x=1$, the transformed numbers are $[1,2,7]$, and the answer becomes $1$. The identity of the optimal pair changed.

## Approaches

The brute force approach is straightforward.

For every mask $x$, compute all values $a_i\oplus x$, sort them, and scan adjacent elements to find the minimum difference. The closest pair in a sorted array must be adjacent.

This is correct, but the complexity is

$$2^k \cdot O(n\log n).$$

In the worst case $n=2^k=524288$, which is astronomically large.

The key observation is that we do not actually care about the transformed numbers themselves. We only care about three quantities for every mask:

$$\text{minimum value},
\qquad
\text{maximum value},
\qquad
\text{minimum pair distance}.$$

These quantities can be merged recursively along the bit structure of the numbers.

Think of all $k$-bit numbers as leaves of a binary trie. A node at bit $d$ splits into numbers whose $d$-th bit is $0$ and numbers whose $d$-th bit is $1$.

When we decide the $d$-th bit of the query mask $x$, XOR either keeps those two halves in their natural order or swaps them. The relative offset between the halves is exactly $2^d$.

That means if we already know, for both children, the minimum transformed value, maximum transformed value, and best answer, then we can merge them in constant time.

Running this merge for every bit and every mask yields an $O(k2^k)$ solution. The recurrence is essentially a divide-and-conquer DP over the hypercube.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^k n\log n)$ | $O(n)$ | Too slow |
| Optimal | $O(k2^k)$ | $O(2^k)$ | Accepted |

## Algorithm Walkthrough

### State Definition

For every mask $m$, maintain three values.

`mn[m]` is the minimum transformed value currently reachable.

`mx[m]` is the maximum transformed value currently reachable.

`F[m]` is the minimum distance between any two transformed values.

Initially only the original array elements exist.

For every value present in the array:

```
mn[value] = mx[value] = 0
```

For every absent value:

```
mn = +INF
mx = -INF
F  = +INF
```

### Merge Interpretation

Suppose we are processing bit $d$.

Let

```
l = mask with bit d = 0
r = l xor (1<<d)
```

represent the two children of a trie node.

If query bit $x_d=0$, the right child contributes an extra $2^d$.

If query bit $x_d=1$, the left child contributes an extra $2^d$.

This gives the transitions for minima and maxima:

$$mn[l]=\min(mn_l,mn_r+2^d)$$

$$mn[r]=\min(mn_r,mn_l+2^d)$$

and similarly for maxima.

### Computing the Best Distance

The optimal pair can lie entirely inside one child, or it can use one element from each child.

The first case is already stored in the children.

For a cross pair, after ordering, the smallest possible gap is

$$(\text{minimum right})-(\text{maximum left}).$$

Under $x_d=0$, that becomes

$$mn[r]-mx[l]+2^d.$$

Under $x_d=1$, it becomes

$$mn[l]-mx[r]+2^d.$$

We minimize the answer with those values.

### Full Procedure

1. Create arrays `mn`, `mx`, and `F` of size $2^k$.
2. Initialize present numbers with `mn=mx=0`.
3. Process bits from low to high.
4. For every pair of masks differing only in the current bit, merge their information.
5. Update `F` using both child answers and the cross-child candidate.
6. After all bits are processed, `F[x]` equals the required answer for mask `x`.

### Why it works

At any stage, a state represents all numbers inside a trie subtree after applying the already processed query bits.

`mn` and `mx` describe the extreme transformed values inside that subtree.

`F` stores the best pair distance completely contained in that subtree.

When two subtrees are merged, every valid pair belongs to exactly one of three categories: entirely in the left child, entirely in the right child, or crossing between them. The recurrence explicitly takes the minimum over all three possibilities.

Since every pair is considered exactly at the lowest node containing both elements, no candidate is missed and no invalid candidate is introduced. By induction on the processed bits, the final `F[x]` is precisely the minimum pair distance for query mask `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    M = 1 << k
    INF = 10 ** 9

    mn = [INF] * M
    mx = [-INF] * M
    F = [INF] * M

    for x in a:
        mn[x] = 0
        mx[x] = 0

    for d in range(k):
        bit = 1 << d

        for r in range(M):
            if (r >> d) & 1:
                l = r ^ bit

                if F[r] < F[l]:
                    F[l] = F[r]
                elif F[l] < F[r]:
                    F[r] = F[l]

                v = mn[r] - mx[l] + bit
                if v < F[l]:
                    F[l] = v

                v = mn[l] - mx[r] + bit
                if v < F[r]:
                    F[r] = v

                mnl, mnr = mn[l], mn[r]
                mxl, mxr = mx[l], mx[r]

                mn[l] = min(mnl, mnr + bit)
                mn[r] = min(mnr, mnl + bit)

                mx[l] = max(mxl, mxr + bit)
                mx[r] = max(mxr, mxl + bit)

    print(*F)

solve()
```

The initialization places a zero-length interval at every value present in the input set. Absent values act as empty leaves through the `INF` and `-INF` sentinels.

The outer loop processes bits exactly like merging levels of a binary trie. Each pair `(l,r)` corresponds to two sibling subtrees.

The subtle part is updating `F` before overwriting `mn` and `mx`. The cross-subtree distance must use the old child information. Updating the extrema first would corrupt the recurrence.

Another detail is that the answer array is exactly `F`. After the final merge level, each index corresponds to one complete query mask.

## Worked Examples

### Example 1

Input:

```
3 3
6 0 3
```

Initial active masks:

| Mask | Present |
| --- | --- |
| 0 | Yes |
| 3 | Yes |
| 6 | Yes |

Final result:

| x | f(x) |
| --- | --- |
| 0 | 3 |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 2 |
| 5 | 1 |
| 6 | 1 |
| 7 | 3 |

Output:

```
3 1 1 2 2 1 1 3
```

This example shows that changing the query mask can completely change which pair becomes optimal.

### Example 2

Input:

```
3 4
13 4 2
```

Final answers:

| x | f(x) |
| --- | --- |
| 0 | 2 |
| 1 | 2 |
| 2 | 6 |
| 3 | 6 |
| ... | ... |

Output:

```
2 2 6 6 3 1 2 2 2 2 1 3 6 6 2 2
```

This example demonstrates that the answer is highly non-monotonic with respect to the query mask.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k2^k)$ | Every bit processes all masks once |
| Space | $O(2^k)$ | Three arrays of size $2^k$ |

With $k\le 19$, we have at most $524288$ masks. The total work is roughly $19 \cdot 524288$, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        M = 1 << k
        INF = 10 ** 9

        mn = [INF] * M
        mx = [-INF] * M
        F = [INF] * M

        for x in a:
            mn[x] = 0
            mx[x] = 0

        for d in range(k):
            bit = 1 << d
            for r in range(M):
                if (r >> d) & 1:
                    l = r ^ bit

                    F[l] = min(F[l], F[r])
                    F[r] = min(F[r], F[l])

                    F[l] = min(F[l], mn[r] - mx[l] + bit)
                    F[r] = min(F[r], mn[l] - mx[r] + bit)

                    mnl, mnr = mn[l], mn[r]
                    mxl, mxr = mx[l], mx[r]

                    mn[l] = min(mnl, mnr + bit)
                    mn[r] = min(mnr, mnl + bit)

                    mx[l] = max(mxl, mxr + bit)
                    mx[r] = max(mxr, mxl + bit)

        print(*F)

    solve()
    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided samples
assert run("3 3\n6 0 3\n") == "3 1 1 2 2 1 1 3\n"

assert run("3 4\n13 4 2\n") == \
       "2 2 6 6 3 1 2 2 2 2 1 3 6 6 2 2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `3 1 1 2 2 1 1 3` | Basic correctness |
| Sample 2 | Given output | Larger bit width |
| Two adjacent numbers | All answers equal to 1 | Minimum possible distance |
| Full set of masks | All answers equal to 1 | Dense input behavior |
| Numbers in opposite halves | Large answers possible | Cross-subtree transitions |

## Edge Cases

Consider:

```
2 1
0 1
```

For both query masks, the transformed set remains `{0,1}` in some order. The answer is always `1`.

The DP handles this naturally because the only valid pair is a cross-child pair at the lowest merge, producing distance $2^0=1$.

Now consider:

```
2 3
0 7
```

For every query mask, the transformed values remain complementary endpoints of the range. Their difference is always `7`.

The recurrence computes this through repeated cross-subtree merges. No smaller candidate exists inside any subtree because each subtree contains only one element.

Finally, consider a case where the closest pair changes after XOR:

```
3 3
0 3 6
```

At `x=0`, the answer is `3`.

At `x=1`, the transformed values are `1,2,7`, and the answer becomes `1`.

Because the DP does not track a specific pair and instead tracks the minimum over all possible pairs inside every subtree, it automatically adapts when the optimal pair changes.
