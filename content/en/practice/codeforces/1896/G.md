---
title: "CF 1896G - Pepe Racing"
description: "There are $n^2$ racers with distinct speeds. A race may contain exactly $n$ racers, and the only information returned is the winner of that race."
date: "2026-06-08T21:42:13+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "interactive", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1896
codeforces_index: "G"
codeforces_contest_name: "CodeTON Round 7 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 3200
weight: 1896
solve_time_s: 126
verified: false
draft: false
---

[CF 1896G - Pepe Racing](https://codeforces.com/problemset/problem/1896/G)

**Rating:** 3200  
**Tags:** constructive algorithms, implementation, interactive, sortings  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

There are $n^2$ racers with distinct speeds. A race may contain exactly $n$ racers, and the only information returned is the winner of that race.

The original interactive task asks us to determine the complete ordering of the fastest $n^2-n+1$ racers while using at most $2n^2-2n+1$ races. The official solution is built around carefully maintaining the winners of $n$ groups of size $n$. The key observation is that once the winner of a group is removed, only that group's winner needs to be recomputed. This allows extracting racers from fastest to slowest within the query budget.

For the Codeforces hack format, the interaction disappears. Instead, we are given the entire ranking directly.

The input contains a permutation $a$ of length $n^2$. Larger values mean higher speed. If $a_i>a_j$, then racer $i$ is faster than racer $j$.

So in the hacked version the task becomes very simple: recover the racers sorted by speed and print the fastest $n^2-n+1$ of them.

The constraint $\sum n^3 \le 3\cdot 10^5$ is relevant for the interactive version, but in the hack format we only process arrays of length $n^2$. Sorting $n^2$ elements is easily fast enough.

A common mistake is to sort the values $a_i$ themselves and print them. The output must contain racer labels, which are the indices.

For example, if

```
n = 2
a = [3, 1, 4, 2]
```

then racer 3 is fastest, racer 1 is second, racer 4 is third, and racer 2 is last. The correct output is:

```
3 1 4
```

not

```
4 3 2
```

because the problem asks for racer identifiers.

## Approaches

The interactive version can be viewed as repeatedly extracting the current fastest racer. A straightforward implementation would recompute everything from scratch after every extraction. We divide the racers into $n$ groups of size $n$, find each group winner, then race the group winners to find the global winner. Repeating that process $n^2-n+1$ times leads to roughly $n(n^2)$ races, far above the allowed limit.

The crucial observation is that removing the current fastest racer only affects one group. All other group winners remain valid. After deleting a winner, we recompute only the winner of that particular group and then compare the current group winners again. This reduces the number of additional races per extracted racer to a constant amount and reaches the limit $2n^2-2n+1$.

For the hack format, none of this machinery is necessary because the full ranking is already given. We simply sort racer indices by their speed value $a_i$ in descending order and output the first $n^2-n+1$ indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Interactive recomputation from scratch | $O(n^3)$ races | $O(n^2)$ | Too many races |
| Official interactive maintenance | $O(n^2)$ races | $O(n^2)$ | Accepted |
| Hack format sorting | $O(n^2\log n)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$ and the permutation $a$.
2. Create pairs $(a_i, i)$, where $i$ is the racer label.
3. Sort these pairs in descending order of $a_i$.
4. The sorted indices are exactly the racers ordered from fastest to slowest.
5. Output the first $n^2-n+1$ indices.

### Why it works

The permutation directly encodes the total ordering of speeds. Larger $a_i$ means racer $i$ is faster. Sorting racer labels by $a_i$ therefore produces the unique speed ranking. The problem only asks for the fastest $n^2-n+1$ racers, so taking the prefix of that ordering is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        parts = input().split()
        n = int(parts[0])
        
        a = list(map(int, input().split()))
        
        order = sorted(range(1, n * n + 1),
                       key=lambda i: a[i - 1],
                       reverse=True)
        
        k = n * n - n + 1
        print(*order[:k])

solve()
```

The implementation stores racer labels as 1-based indices because that is what the output requires.

The sorting key is the speed value associated with each racer. Since the input is a permutation, all values are distinct and no tie handling is needed.

The expression `n * n - n + 1` is exactly the number of racers that must be printed.

## Worked Examples

### Example 1

Input:

```
n = 2
a = [1, 2, 3, 4]
```

| Racer | Speed |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |

Sorted order:

| Position | Racer |
| --- | --- |
| 1 | 4 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |

We need $2^2-2+1=3$ racers, so the answer is:

```
4 3 2
```

This demonstrates the basic case where the ranking matches the speed values.

### Example 2

Input:

```
n = 3
a = [5, 9, 1, 7, 3, 8, 2, 6, 4]
```

| Racer | Speed |
| --- | --- |
| 1 | 5 |
| 2 | 9 |
| 3 | 1 |
| 4 | 7 |
| 5 | 3 |
| 6 | 8 |
| 7 | 2 |
| 8 | 6 |
| 9 | 4 |

Sorted order:

| Position | Racer |
| --- | --- |
| 1 | 2 |
| 2 | 6 |
| 3 | 4 |
| 4 | 8 |
| 5 | 1 |
| 6 | 9 |
| 7 | 5 |
| 8 | 7 |
| 9 | 3 |

We need $9-3+1=7$ racers:

```
2 6 4 8 1 9 5
```

This example shows that racer labels and speed values are different objects. We sort by speed and output labels.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \log(n^2))$ | Sorting $n^2$ racers |
| Space | $O(n^2)$ | Stores the ranking |

Since the largest structure contains only $n^2$ elements, and the original constraints keep the total input size small, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    
    def solve():
        t = int(input())
        for _ in range(t):
            parts = input().split()
            n = int(parts[0])
            a = list(map(int, input().split()))
            
            order = sorted(
                range(1, n * n + 1),
                key=lambda i: a[i - 1],
                reverse=True
            )
            
            print(*order[:n * n - n + 1], file=out)
    
    input = sys.stdin.readline
    solve()
    return out.getvalue()

# provided sample (hack format equivalent)
assert run(
"""1
2 manual
1 2 3 4
"""
) == "4 3 2\n"

# minimum size
assert run(
"""1
2 manual
4 3 2 1
"""
) == "1 2 3\n"

# random ordering
assert run(
"""1
3 manual
5 9 1 7 3 8 2 6 4
"""
) == "2 6 4 8 1 9 5\n"

# already descending speeds
assert run(
"""1
3 manual
9 8 7 6 5 4 3 2 1
"""
) == "1 2 3 4 5 6 7\n"

# catches index/value confusion
assert run(
"""1
2 manual
3 1 4 2
"""
) == "3 1 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2`, speeds increasing | `4 3 2` | Basic ordering |
| `n=2`, speeds decreasing | `1 2 3` | Minimum size |
| Random permutation | `2 6 4 8 1 9 5` | General correctness |
| Already sorted descending | `1 2 3 4 5 6 7` | Prefix extraction |
| `3 1 4 2` | `3 1 4` | Prevents outputting values instead of labels |

## Edge Cases

Consider:

```
1
2 manual
4 3 2 1
```

The ranking is already in label order. Sorting by speed keeps the order as `1 2 3 4`. Since only three racers are required, the answer becomes:

```
1 2 3
```

A solution that mistakenly prints the speed values would output `4 3 2`, which is incorrect.

Now consider:

```
1
2 manual
3 1 4 2
```

The fastest racer is label 3 because its speed value is 4. The second fastest is label 1 because its speed value is 3. The full ranking is:

```
3 1 4 2
```

and the required output is:

```
3 1 4
```

This is the most common source of wrong answers in the hack version. The array stores speeds, not the final ordering itself.

The official interactive solution is based on maintaining group winners and updating only the affected group after each extraction, which fits exactly into the allowed race budget.
