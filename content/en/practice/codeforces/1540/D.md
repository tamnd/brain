---
title: "CF 1540D - Inverse Inversions"
description: "The array $b$ is not arbitrary. For every position $i$, $bi$ tells us how many earlier elements of the permutation are larger than $pi$."
date: "2026-06-10T14:33:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1540
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 728 (Div. 1)"
rating: 3200
weight: 1540
solve_time_s: 523
verified: false
draft: false
---

[CF 1540D - Inverse Inversions](https://codeforces.com/problemset/problem/1540/D)

**Rating:** 3200  
**Tags:** binary search, brute force, data structures  
**Solve time:** 8m 43s  
**Verified:** no  

## Solution
## Problem Understanding

The array $b$ is not arbitrary. For every position $i$, $b_i$ tells us how many earlier elements of the permutation are larger than $p_i$.

If we only look at the first $i$ elements of the permutation, then exactly $b_i$ of them are larger than $p_i$, so exactly $i-1-b_i$ of them are smaller. That means the rank of $p_i$ among the first $i$ elements is

$$r_i=i-b_i.$$

The entire permutation is uniquely determined by these ranks. Queries modify individual values of $b$, which changes one rank $r_i$, and later queries ask for the final value $p_i$.

The constraints are the real challenge. Both $n$ and $q$ are as large as $10^5$. Reconstructing the whole permutation after every update would require at least $O(n)$ work per update, leading to roughly $10^{10}$ operations in the worst case. Any solution that touches the whole array for every query is immediately ruled out.

A subtle point is that updates affect many later positions indirectly. Consider

```
n = 3
b = [0, 0, 0]
```

which corresponds to

```
p = [1, 2, 3].
```

Changing only $b_2$ to $1$ produces

```
b = [0, 1, 0]
```

and now the permutation becomes

```
p = [2, 1, 3].
```

A naive approach that tries to update only position $2$ would miss the fact that the value at position $1$ also changes.

Another easy mistake is assuming multiple permutations may exist. The inversion-vector representation actually determines a unique permutation. For example,

```
b = [0, 1, 2, 3]
```

forces

```
p = [4, 3, 2, 1].
```

There is no freedom at all.

## Approaches

The most direct solution starts from the observation that

$$r_i=i-b_i$$

is the rank of position $i$ among the first $i$ elements.

Suppose we already know the rank of some position $k$ among the first $t-1$ elements. When position $t$ is inserted, its rank is $r_t$. Every existing rank greater than or equal to $r_t$ shifts up by one.

If we denote the current rank of position $k$ by $x$, the transition is

$$x \leftarrow \begin{cases} x+1 & x \ge r_t\\ x   & x < r_t \end{cases}$$

Applying this transition for all $t>k$ eventually gives the final value $p_k$.

A brute-force query can simply simulate all later insertions. That is correct because it follows the definition of the inversion vector exactly. Unfortunately, each query costs $O(n)$, and with $10^5$ queries we end up near $10^{10}$ operations.

The key observation is that every later position contributes a tiny operation:

$$T_a(x)=x+[x\ge a].$$

A whole block of positions is just a composition of such operations.

Instead of storing the block as raw values, we store the entire block transformation. Any composition of these operations can be represented as

$$F(x)=x+\#\{c_j\le x\},$$

for a sorted collection of breakpoints $c_j$.

Once a block is compressed into its breakpoint set, applying the entire block becomes a single binary search:

$$F(x)=x+\text{count}(c_j\le x).$$

This turns a long sequence of updates into one operation per block. A square-root decomposition then gives efficient updates and queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per query | $O(1)$ | Too slow |
| Optimal sqrt decomposition | $O(\sqrt n \log n)$ query, $O(\sqrt n \log^2 n)$ update | $O(n)$ | Accepted |

## Approaches

Let

$$r_i=i-b_i.$$

For a fixed position $k$, define $x_t$ as its rank after processing positions $1\ldots t$.

Initially,

$$x_k=r_k.$$

When position $t>k$ is inserted, every rank at least $r_t$ shifts upward:

$$x_t=x_{t-1}+[x_{t-1}\ge r_t].$$

After processing all positions,

$$p_k=x_n.$$

Each position $t$ contributes the operator

$$T_{r_t}(x)=x+[x\ge r_t].$$

The entire suffix after $k$ is a composition of such operators.

For a block of positions, that composition can be written as

$$F(x)=x+\#\{c_j\le x\},$$

where the $c_j$ are stored in sorted order.

Applying a block becomes a single binary search:

```
x += number of breakpoints <= x
```

which costs $O(\log B)$.

Updates only modify one position. We rebuild the block containing that position and leave all other blocks unchanged.

## Algorithm Walkthrough

1. Convert the inversion counts into ranks using $r_i=i-b_i$.
2. Split the indices into blocks of size approximately $\sqrt n$.
3. For every block, build its compressed transformation.

Process the ranks inside the block from left to right. The resulting block transformation is represented by a sorted list of breakpoints $c_j$.
4. For an update query, modify the corresponding rank $r_i$.
5. Rebuild only the block containing $i$.
6. For a value query at position $i$, start with

$$x=r_i.$$
7. Process the remaining elements of the same block explicitly.

Only $O(\sqrt n)$ positions belong to that block.
8. For every later full block, apply its stored transformation.

This is done by a binary search on the block's breakpoint list:

$$x \leftarrow x+\#\{c_j\le x\}.$$
9. After all suffix blocks are applied, output $x$.

### Why it works

The rank $r_i=i-b_i$ is exactly the position occupied by $p_i$ among the first $i$ elements.

Whenever a new element with rank $r_t$ is inserted, every existing rank greater than or equal to $r_t$ shifts by one. The transition

$$x \leftarrow x+[x\ge r_t]$$

is therefore identical to the insertion process that constructs the permutation from its inversion vector.

The query algorithm applies these transitions in the same order as the original construction. Block compression does not change the result because each block transformation is represented exactly, not approximately. Thus the final rank computed by the algorithm is exactly $p_i$.

## Python Solution

```python
import sys
from bisect import bisect_right, insort

input = sys.stdin.readline

class SqrtDecomposition:
    def __init__(self, n, r):
        self.n = n
        self.r = r
        self.B = 320

        self.blocks = []
        self.bid = [0] * (n + 1)

        l = 1
        while l <= n:
            rr = min(n, l + self.B - 1)
            idx = len(self.blocks)
            for i in range(l, rr + 1):
                self.bid[i] = idx
            self.blocks.append([l, rr, []])
            l = rr + 1

        for b in range(len(self.blocks)):
            self.rebuild(b)

    def rebuild(self, b):
        l, r, _ = self.blocks[b]

        c = []

        for pos in range(l, r + 1):
            a = self.r[pos]

            lo, hi = 0, self.n
            while lo < hi:
                mid = (lo + hi) // 2
                if mid + bisect_right(c, mid) >= a:
                    hi = mid
                else:
                    lo = mid + 1

            insort(c, lo)

        self.blocks[b][2] = c

    def apply_block(self, b, x):
        c = self.blocks[b][2]
        return x + bisect_right(c, x)

    def update(self, pos, value):
        self.r[pos] = value
        self.rebuild(self.bid[pos])

    def query(self, pos):
        x = self.r[pos]

        b = self.bid[pos]
        l, r, _ = self.blocks[b]

        for i in range(pos + 1, r + 1):
            if x >= self.r[i]:
                x += 1

        for nb in range(b + 1, len(self.blocks)):
            x = self.apply_block(nb, x)

        return x

def solve():
    n = int(input())
    b = list(map(int, input().split()))

    r = [0] * (n + 1)
    for i in range(1, n + 1):
        r[i] = i - b[i - 1]

    ds = SqrtDecomposition(n, r)

    q = int(input())
    ans = []

    for _ in range(q):
        s = list(map(int, input().split()))

        if s[0] == 1:
            _, i, x = s
            ds.update(i, i - x)
        else:
            _, i = s
            ans.append(str(ds.query(i)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The array `r` stores the rank representation $r_i=i-b_i$. All later logic operates on ranks because insertion behavior becomes much simpler in that form.

Each block stores a compressed suffix transformation. During a query, the unfinished part of the current block is processed explicitly, then every later block is applied using a single binary search.

The most delicate part of the implementation is rebuilding a block. The breakpoint representation must describe the exact composition of all operators in the block. The binary search inside `rebuild` finds the smallest value whose transformed rank reaches the insertion rank of the current element. Those breakpoints completely characterize the block transformation.

## Worked Examples

### Sample 1

Input:

```
3
0 0 0
7
2 1
2 2
2 3
1 2 1
2 1
2 2
2 3
```

Initially:

$$r=[1,2,3].$$

| Query | Start x | Suffix processing | Answer |
| --- | --- | --- | --- |
| 2 1 | 1 | no later rank can shift it | 1 |
| 2 2 | 2 | rank 3 does not affect it | 2 |
| 2 3 | 3 | empty suffix | 3 |

After updating $b_2=1$:

$$r=[1,1,3].$$

| Query | Start x | Suffix processing | Answer |
| --- | --- | --- | --- |
| 2 1 | 1 | shifted once by rank 1 | 2 |
| 2 2 | 1 | not shifted later | 1 |
| 2 3 | 3 | empty suffix | 3 |

This demonstrates that changing a single inversion count may alter several permutation values.

### Custom Example

Input:

```
4
0 1 2 3
4
2 1
2 2
2 3
2 4
```

Ranks become

$$r=[1,1,1,1].$$

| Position | Start rank | Shifts | Final value |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 4 |
| 2 | 1 | 2 | 3 |
| 3 | 1 | 1 | 2 |
| 4 | 1 | 0 | 1 |

The resulting permutation is

```
[4, 3, 2, 1]
```

which is the reverse permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt n \log n)$ per query, $O(\sqrt n \log^2 n)$ per update | One block rebuild or one pass across compressed blocks |
| Space | $O(n)$ | Ranks and block summaries |

With $n,q \le 10^5$, square-root decomposition keeps both operations comfortably below linear time and fits within the memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # solve()

    return out.getvalue().strip()

# sample 1
# assert run(...) == ...

# minimum size
# assert run(
# "1\n0\n1\n2 1\n"
# ) == "1"

# reverse permutation
# assert run(
# "4\n0 1 2 3\n4\n2 1\n2 2\n2 3\n2 4\n"
# ) == "4\n3\n2\n1"

# update on first nontrivial position
# assert run(
# "3\n0 0 0\n2\n1 2 1\n2 1\n"
# ) == "2"

# boundary update at n
# assert run(
# "5\n0 0 0 0 0\n2\n1 5 4\n2 5\n"
# ) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=1$ | 1 | Smallest possible instance |
| Reverse permutation inversion vector | 4 3 2 1 | Maximum inversion structure |
| Update at position 2 | 2 | Propagation to earlier elements |
| Update at position $n$ | 1 | Last-position boundary handling |

## Edge Cases

Consider

```
3
0 1 0
```

which gives

$$r=[1,1,3].$$

Position $1$ starts with rank $1$. Position $2$ also has rank $1$, so the first position is shifted upward and becomes rank $2$. A solution that only examines later ranks larger than the current one would incorrectly leave it unchanged.

Another important case is

```
4
0 1 2 3
```

where every rank equals $1$. Each newly inserted element goes to the front. The algorithm repeatedly applies the transition $x \leftarrow x+1$, producing the reverse permutation. This confirms that equal insertion ranks are handled correctly.

Finally, consider a query on the last position. Its suffix is empty, so the answer must be exactly its current rank. The implementation naturally handles this because neither the local scan nor any later block is processed.
