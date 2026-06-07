---
title: "CF 486E - LIS of Sequence"
description: "We are given an array and we care about its longest increasing subsequences. An index belongs to a longest increasing subsequence if the value at that position is selected as one of the elements of that subsequence. The task is not to count LISs."
date: "2026-06-07T17:29:17+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "hashing", "math"]
categories: ["algorithms"]
codeforces_contest: 486
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 277 (Div. 2)"
rating: 2200
weight: 486
solve_time_s: 143
verified: true
draft: false
---

[CF 486E - LIS of Sequence](https://codeforces.com/problemset/problem/486/E)

**Rating:** 2200  
**Tags:** data structures, dp, greedy, hashing, math  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we care about its longest increasing subsequences. An index belongs to a longest increasing subsequence if the value at that position is selected as one of the elements of that subsequence.

The task is not to count LISs. Instead, for every position we must determine which of three categories it belongs to.

A position is in group 1 if it never appears in any LIS.

A position is in group 2 if it appears in at least one LIS, but there exists another LIS that does not use it.

A position is in group 3 if every possible LIS must contain that position.

The array length can reach $10^5$. Any algorithm that explicitly enumerates increasing subsequences is hopeless because the number of LISs can be exponential. Even an $O(n^2)$ dynamic programming solution performs about $10^{10}$ comparisons in the worst case, which is far beyond the limit. The target complexity is roughly $O(n \log n)$.

The tricky part is distinguishing group 2 from group 3. Knowing that an index belongs to some LIS is not enough. We must know whether there is any alternative way to build an LIS without using that position.

Consider the array:

```
1 3 2 5
```

The LIS length is 3. There are two LISs:

```
1 3 5
1 2 5
```

Positions containing 3 and 2 belong to some LIS, but not all LISs. Their answer must be `2`.

Another subtle case is:

```
1 2 3
```

There is only one LIS. Every position belongs to it, so the answer is:

```
333
```

A careless solution that only checks whether a position can appear in an LIS would incorrectly print `222`.

One more important example is:

```
2 2 2
```

The LIS length is 1. Each position individually forms an LIS. No position is mandatory because we can choose any of the three. The correct answer is:

```
222
```

Treating all LIS-length-1 positions as mandatory would be wrong.

## Approaches

The brute force idea is conceptually simple. Generate every longest increasing subsequence, record which indices appear, then classify each index according to how many LISs contain it. This is correct because it directly follows the definition.

The problem is scale. Even for moderate inputs the number of LISs can be enormous. An array like

```
1 2 1 2 1 2 ...
```

already creates many choices. Enumerating all LISs becomes exponential.

The key observation is that we do not need the LISs themselves. We only need structural information about where each position can sit inside an LIS.

Let $L_i$ be the length of the longest increasing subsequence ending at position $i$.

Let $R_i$ be the length of the longest increasing subsequence starting at position $i$.

If the overall LIS length is $K$, then position $i$ can belong to some LIS exactly when

$$L_i + R_i - 1 = K.$$

The reason is that $L_i$ describes the best increasing chain reaching $i$, $R_i$ describes the best increasing chain leaving $i$, and position $i$ is counted in both parts.

This already separates group 1 from the others.

The remaining question is deciding whether a position is mandatory.

Every position that lies on an LIS occupies a specific layer, namely layer $L_i$. Along any LIS we must choose exactly one position from each layer $1,2,\ldots,K$.

Suppose among all positions satisfying

$$L_i + R_i - 1 = K$$

there is only one position in layer $t$.

Every LIS must take one position from layer $t$, and there is only one candidate. That position is unavoidable and belongs to group 3.

If a layer contains two or more candidates, then none of them is individually mandatory. We can choose another candidate from the same layer when constructing an LIS. Those positions belong to group 2.

This leads to an $O(n \log n)$ solution using the standard patience-sorting LIS algorithm twice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute $L_i$, the LIS length ending at each position.

Process the array from left to right using the patience-sorting technique. For each value, find its insertion position in the tails array with binary search. The insertion index plus one is $L_i$.
2. Compute $R_i$, the LIS length starting at each position.

Process the array from right to left. Apply the same LIS procedure to the values $-a_i$. This is equivalent to computing increasing subsequences when moving rightward from position $i$.
3. Let

$$K = \max(L_i).$$

This is the overall LIS length.
4. For every position, check whether

$$L_i + R_i - 1 = K.$$

If not, the position cannot belong to any LIS. Mark it as group `1`.
5. For every position satisfying the equality above, count how many such positions exist in each layer $L_i$.
6. For each position on some LIS:

If its layer contains exactly one valid position, mark it as group `3`.

Otherwise mark it as group `2`.
7. Output the resulting string.

### Why it works

The values $L_i$ and $R_i$ describe the longest increasing chains entering and leaving position $i$. A position can participate in an LIS only when these two chains combine to the global LIS length, which is exactly the condition

$$L_i + R_i - 1 = K.$$

Every LIS contains one position from each layer. The layer of a position is $L_i$. Among positions that can appear in an LIS, if a layer contains only one candidate, every LIS must use that candidate because the layer cannot be skipped. Conversely, if a layer contains multiple candidates, no single candidate is forced. Replacing one candidate by another preserves the existence of an LIS through that layer. Thus unique-layer candidates are precisely the positions belonging to every LIS.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    L = [0] * n
    tails = []

    for i, x in enumerate(a):
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
        L[i] = pos + 1

    K = len(tails)

    R = [0] * n
    tails = []

    for i in range(n - 1, -1, -1):
        x = -a[i]
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
        R[i] = pos + 1

    layer_count = [0] * (K + 1)

    for i in range(n):
        if L[i] + R[i] - 1 == K:
            layer_count[L[i]] += 1

    ans = ['1'] * n

    for i in range(n):
        if L[i] + R[i] - 1 != K:
            ans[i] = '1'
        elif layer_count[L[i]] == 1:
            ans[i] = '3'
        else:
            ans[i] = '2'

    print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The first LIS pass computes the longest increasing subsequence ending at every position. The tails array maintains the smallest possible ending value for each LIS length. This is the standard $O(n \log n)$ LIS technique.

The second pass is slightly less obvious. Processing from right to left while applying the same logic to negated values computes the longest increasing subsequence starting at each position. Using negation converts the needed ordering into the same binary-search structure used in the forward pass.

After obtaining $L$ and $R$, the condition

$$L_i + R_i - 1 = K$$

identifies exactly the positions that lie on at least one LIS. Only those positions participate in layer counting.

The layer count array is indexed by $L_i$. A common mistake is counting all positions in a layer. We must count only positions that satisfy the LIS condition. Positions that never belong to an LIS must not influence the mandatory-position test.

## Worked Examples

### Example 1

Input:

```
1
4
```

| i | a[i] | L[i] | R[i] | L+R-1 |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 1 | 1 |

Here $K=1$.

Layer 1 contains exactly one valid position.

Output:

```
3
```

This demonstrates the simplest case. The only position belongs to every LIS because every LIS consists of that single element.

### Example 2

Input:

```
4
1 3 2 5
```

| i | a[i] | L[i] | R[i] | L+R-1 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 3 | 3 |
| 2 | 3 | 2 | 2 | 3 |
| 3 | 2 | 2 | 2 | 3 |
| 4 | 5 | 3 | 1 | 3 |

The LIS length is $K=3$.

Valid positions by layer:

| Layer | Positions |
| --- | --- |
| 1 | {1} |
| 2 | {2, 3} |
| 3 | {4} |

Layers 1 and 3 contain a unique candidate, so positions 1 and 4 are mandatory.

Layer 2 contains two candidates, so neither is mandatory.

Output:

```
3223
```

This example shows why merely belonging to an LIS is insufficient. Positions 2 and 3 both appear in some LIS, but neither appears in all LISs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Two LIS passes with binary search |
| Space | O(n) | Arrays L, R, answer, and layer counts |

With $n \le 10^5$, an $O(n \log n)$ solution performs roughly a few million operations, which comfortably fits within the limits. The memory usage is linear in the array size and is well below 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    L = [0] * n
    tails = []

    for i, x in enumerate(a):
        p = bisect_left(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
        L[i] = p + 1

    K = len(tails)

    R = [0] * n
    tails = []

    for i in range(n - 1, -1, -1):
        x = -a[i]
        p = bisect_left(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
        R[i] = p + 1

    cnt = [0] * (K + 1)

    for i in range(n):
        if L[i] + R[i] - 1 == K:
            cnt[L[i]] += 1

    ans = []

    for i in range(n):
        if L[i] + R[i] - 1 != K:
            ans.append('1')
        elif cnt[L[i]] == 1:
            ans.append('3')
        else:
            ans.append('2')

    return ''.join(ans)

# provided sample
assert run("1\n4\n") == "3", "sample 1"

# custom cases
assert run("3\n1 2 3\n") == "333", "unique LIS"
assert run("3\n2 2 2\n") == "222", "many LIS of length 1"
assert run("4\n1 3 2 5\n") == "3223", "two middle alternatives"
assert run("5\n5 4 3 2 1\n") == "22222", "all positions form LIS length 1"
assert run("4\n1 2 1 2\n") == "2222", "multiple choices in every layer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 4` | `3` | Minimum size |
| `1 2 3` | `333` | Unique LIS |
| `2 2 2` | `222` | Multiple LISs of length 1 |
| `1 3 2 5` | `3223` | Mandatory and optional positions together |
| `5 4 3 2 1` | `22222` | Strictly decreasing sequence |
| `1 2 1 2` | `2222` | Multiple candidates in each layer |

## Edge Cases

Consider:

```
3
2 2 2
```

We get:

```
L = [1, 1, 1]
R = [1, 1, 1]
K = 1
```

Every position satisfies $L_i + R_i - 1 = 1$, so all positions belong to some LIS. Layer 1 contains three candidates, not one. The algorithm outputs:

```
222
```

which is correct because any single element is an LIS.

Consider:

```
3
1 2 3
```

The values are:

```
L = [1, 2, 3]
R = [3, 2, 1]
K = 3
```

Each layer contains exactly one valid position. The algorithm outputs:

```
333
```

Every LIS must use all three positions.

Consider:

```
4
1 3 2 5
```

The middle positions both lie on an LIS:

```
L = [1, 2, 2, 3]
R = [3, 2, 2, 1]
```

Layer 2 contains two valid candidates. The algorithm outputs:

```
3223
```

which correctly captures that positions 2 and 3 are interchangeable, while positions 1 and 4 are unavoidable.
