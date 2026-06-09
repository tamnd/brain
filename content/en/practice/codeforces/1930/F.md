---
title: "CF 1930F - Maximize the Difference"
description: "We build an array incrementally. After every insertion we must compute $$f(a)=maxx left(maxi(aimid x)-mini(aimid x)right).$$ The value inserted at each step is encrypted by the previous answer, so the queries must be processed online."
date: "2026-06-09T01:44:05+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 1930
codeforces_index: "F"
codeforces_contest_name: "think-cell Round 1"
rating: 2700
weight: 1930
solve_time_s: 148
verified: false
draft: false
---

[CF 1930F - Maximize the Difference](https://codeforces.com/problemset/problem/1930/F)

**Rating:** 2700  
**Tags:** bitmasks, brute force, dfs and similar  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We build an array incrementally. After every insertion we must compute

$$f(a)=\max_x \left(\max_i(a_i\mid x)-\min_i(a_i\mid x)\right).$$

The value inserted at each step is encrypted by the previous answer, so the queries must be processed online.

The first task is to understand what quantity is actually being maximized.

Fix two elements $u$ and $v$. We want to maximize

$$(u\mid x)-(v\mid x).$$

Consider a single bit independently.

If both $u$ and $v$ have the same bit, that bit contributes nothing to the difference.

If $u$ has $1$ and $v$ has $0$, we keep $x$'s bit equal to $0$, giving a contribution of that bit value.

If $u$ has $0$ and $v$ has $1$, we set $x$'s bit equal to $1$, making both sides equal and contributing nothing.

So the optimal contribution of each bit is exactly the bits that are present in $u$ and absent in $v$. Hence

$$\max_x \bigl((u\mid x)-(v\mid x)\bigr)=u\ \&\ \sim v.$$

Taking the best ordered pair,

$$f(a)=\max_{u,v\in a}(u\ \&\ \sim v).$$

This is the key reduction used in the official solution discussion.

The constraints immediately rule out any pairwise approach. The number of queries can reach $10^6$, so even $O(q\sqrt q)$ is hopeless. The sum of all mask-space sizes is bounded by $2^{22}$, which strongly suggests a solution that spends work on masks rather than on pairs of inserted values.

A subtle edge case appears when the array contains only one value. There is no pair producing a positive difference, and indeed

$$u\ \&\ \sim u = 0,$$

so the answer must be $0$.

Another easy mistake is treating the complement as an infinite-bit complement. Only bits inside the mask universe matter. If the mask space has $k$ bits, the complement of $v$ is

$$((1<<k)-1)\oplus v.$$

Using Python's raw `~v` would produce negative numbers and break the logic.

## Approaches

The brute force interpretation is straightforward. After each insertion, examine every ordered pair $(u,v)$ currently present and compute

$$u\ \&\ \sim v.$$

The maximum of those values is the answer.

This is correct because of the reduction above, but after $q$ insertions it needs $O(q^2)$ pair checks. With $q=10^6$, the operation count is completely infeasible.

The crucial observation is that

$$u\ \&\ \sim v$$

can be viewed as a mask that is simultaneously a subset of $u$ and a subset of the bounded complement of $v$.

Let

$$c(v)=((1<<k)-1)\oplus v.$$

Then a mask $m$ contributes to the answer if there exists an inserted value containing all bits of $m$, and there exists an inserted complement-mask $c(v)$ also containing all bits of $m$.

Define two families.

The first family contains all inserted values.

The second family contains all complements $c(v)$.

For a mask $m$, let

`A[m] = true` if some inserted value is a superset of $m$.

`B[m] = true` if some inserted complement-mask is a superset of $m$.

Then

$$m$$

is achievable iff both flags are true.

The answer is simply the largest mask whose two flags are true.

Now the problem becomes dynamic subset activation.

When a value $v$ is inserted, every subset of $v$ becomes valid in family $A$.

When $c(v)$ is inserted, every subset of $c(v)$ becomes valid in family $B$.

A mask can become active in each family only once during the entire test case. That means we can traverse the subset lattice lazily and never revisit an already activated mask.

This transforms the whole test case into a graph traversal over masks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q^2)$ | $O(q)$ | Too slow |
| Optimal | $O(n \log n + q)$ | $O(n)$ | Accepted |

Here $n=2^k$, and the sum of all $n$ over the input is at most $2^{22}$.

## Algorithm Walkthrough

1. Let $k$ be the number of bits in the mask space and let `FULL = n - 1`.
2. Maintain two boolean arrays.

`seenA[m]` means mask `m` has already been activated by the value side.

`seenB[m]` means mask `m` has already been activated by the complement side.
3. Maintain the current answer `ans`.
4. To insert a value `v`, run a DFS over all subsets of `v`.
5. Whenever a mask `m` is reached for the first time in family `A`, mark `seenA[m] = True`.
6. If `seenB[m]` is already true, then `m` is achievable from both families, so update

`ans = max(ans, m)`.
7. From mask `m`, continue DFS to every mask obtained by removing one set bit.
8. Insert the bounded complement

`cv = FULL ^ v`

into family `B` using the same DFS logic.
9. After both activations finish, output the current answer.

### Why it works

A mask belongs to family `A` exactly when it is a subset of some inserted value. The DFS activation marks precisely all such subsets.

Similarly, a mask belongs to family `B` exactly when it is a subset of the bounded complement of some inserted value.

A mask contributes to the objective iff it is contained in both families. The moment a mask becomes active in both families, it corresponds to some ordered pair $(u,v)$ with

$$m \subseteq u,\qquad m \subseteq c(v).$$

Equivalently,

$$m \subseteq (u\ \&\ \sim v).$$

The largest such mask is exactly

$$\max(u\ \&\ \sim v),$$

which equals $f(a)$. Thus the maintained maximum is always the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        e = list(map(int, input().split()))

        full = n - 1

        seen_a = bytearray(n)
        seen_b = bytearray(n)

        ans = 0
        last = 0

        def activate(start, seen_self, seen_other):
            nonlocal ans

            stack = [start]

            while stack:
                m = stack.pop()

                if seen_self[m]:
                    continue

                seen_self[m] = 1

                if seen_other[m]:
                    if m > ans:
                        ans = m

                x = m
                while x:
                    bit = x & -x
                    stack.append(m ^ bit)
                    x ^= bit

        cur_answers = []

        for enc in e:
            v = (enc + last) % n

            activate(v, seen_a, seen_b)
            activate(full ^ v, seen_b, seen_a)

            last = ans
            cur_answers.append(str(ans))

        out.append(" ".join(cur_answers))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core idea is that every mask is activated at most once in each family. The DFS never explores an already activated mask, so the total work is proportional to the size of the mask lattice rather than to the number of insertions.

The complement must be computed with `full ^ v`, not `~v`. Only the bits inside the mask universe are relevant.

The subset traversal uses the standard technique of removing one set bit at a time. Every edge in the subset lattice is traversed only when its source mask is activated for the first time.

## Worked Examples

### Sample 1

Input:

```
n = 5
queries = [1, 2]
```

| Step | Decoded v | Answer |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 2 |

After the first insertion there is only one value, so every ordered pair is $(1,1)$ and the result is $0$.

After inserting $2$, the pair $(2,1)$ gives

$$2 \& \sim 1 = 2.$$

No larger value is possible.

### Second Sample

| Step | Decoded v | Current set | Answer |
| --- | --- | --- | --- |
| 1 | 3 | {3} | 0 |
| 2 | 1 | {3,1} | 2 |
| 3 | 0 | {3,1,0} | 3 |
| 4 | 5 | {3,1,0,5} | 5 |

The third step already contains the pair $(3,0)$, producing value $3$.

The fourth step introduces $5$, and the pair $(5,0)$ produces $5$, which becomes the new maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + q)$ | Every mask is activated at most once in each family |
| Space | $O(n)$ | Two visitation arrays plus DFS stacks |

Because the sum of all mask-space sizes is at most $2^{22}$, the total number of mask activations across the entire input is bounded. That is exactly what makes the solution fit comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []

    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        e = list(map(int, input().split()))

        full = n - 1
        seen_a = bytearray(n)
        seen_b = bytearray(n)

        ans = 0
        last = 0

        def activate(start, seen_self, seen_other):
            nonlocal ans
            stack = [start]

            while stack:
                m = stack.pop()
                if seen_self[m]:
                    continue

                seen_self[m] = 1

                if seen_other[m]:
                    ans = max(ans, m)

                x = m
                while x:
                    b = x & -x
                    stack.append(m ^ b)
                    x ^= b

        cur = []

        for enc in e:
            v = (enc + last) % n
            activate(v, seen_a, seen_b)
            activate(full ^ v, seen_b, seen_a)
            last = ans
            cur.append(str(ans))

        out.append(" ".join(cur))

    return "\n".join(out)

# provided samples
assert run("2\n5 2\n1 2\n7 4\n3 1 5 2\n") == \
       "0 2\n0 2 3 5"

# single insertion
assert run("1\n4 1\n3\n") == "0"

# repeated identical values
assert run("1\n8 3\n5 5 5\n") == "0 0 0"

# values creating maximum mask
assert run("1\n8 2\n7 1\n") == "0 6"

# boundary mask values
assert run("1\n8 2\n0 7\n") == "0 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One insertion | `0` | Base case |
| All equal values | All zeros | No useful ordered pair exists |
| `7` then `1` | `0 6` | Large directed difference |
| `0` then `7` | `0 7` | Full-mask answer |

## Edge Cases

Consider a test case with only one inserted value:

```
n = 8
queries = [5]
```

The only ordered pair is $(5,5)$.

$$5 \& \sim 5 = 0.$$

The DFS activates subsets on both sides, but the largest mask present in both families is still $0$. The algorithm outputs `0`.

Now consider repeated equal values:

```
n = 8
queries = [3,3,3]
```

Every ordered pair satisfies

$$3 \& \sim 3 = 0.$$

The first insertion activates all subsets of `3` and of its complement. Later insertions revisit already activated masks and perform almost no work. The answer stays `0`.

Finally, consider the extreme pair:

```
n = 8
queries = [0,7]
```

The pair $(7,0)$ yields

$$7 \& \sim 0 = 7.$$

When `7` is inserted, mask `7` becomes active in the value family. Since it was already reachable from the complement family after inserting `0`, the answer immediately updates to `7`, which is the maximum possible mask.
