---
title: "CF 1896A - Jagged Swaps"
description: "We are given a permutation and a very specific swap operation. A swap is allowed only at a position i where the element is a local maximum. In other words, a[i] must be larger than both of its neighbors."
date: "2026-06-08T21:37:07+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1896
codeforces_index: "A"
codeforces_contest_name: "CodeTON Round 7 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 800
weight: 1896
solve_time_s: 109
verified: true
draft: false
---

[CF 1896A - Jagged Swaps](https://codeforces.com/problemset/problem/1896/A)

**Rating:** 800  
**Tags:** sortings  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation and a very specific swap operation.

A swap is allowed only at a position `i` where the element is a local maximum. In other words, `a[i]` must be larger than both of its neighbors. When such a position exists, we may swap `a[i]` with the element immediately to its right.

The task is not to actually sort the permutation. We only need to determine whether some sequence of valid operations can eventually transform the permutation into increasing order.

The constraints are surprisingly small. The permutation length is at most 10, and there are at most 5000 test cases. A brute-force search over all reachable states would actually be possible because the state space is bounded by `10!`, but that is still far larger than necessary. The problem is designed around a simple observation about what the operation can and cannot change.

The main trap is assuming that elements can move freely through repeated swaps. The operation is extremely restrictive.

Consider:

```
3
3 1 2
```

The first element is `3`. There is no valid operation involving position 1 because the operation only allows indices from 2 to `n-1`. The permutation can never become sorted, so the answer is `NO`.

Another easy-to-miss case is:

```
5
1 3 2 5 4
```

This looks only partially sorted, but both `3` and `5` are local maxima. Performing the allowed swaps gives:

```
1 3 2 5 4
→ 1 2 3 5 4
→ 1 2 3 4 5
```

The answer is `YES`.

The most important edge case is when the smallest element is not already at the front.

Example:

```
5
2 1 3 4 5
```

The permutation is almost sorted, but the element `1` can never move to position 1. The answer is `NO`.

Understanding why this happens leads directly to the solution.

## Approaches

A brute-force approach would treat every permutation as a state and repeatedly apply every valid operation. We could perform a graph search and check whether the sorted permutation is reachable.

This works because `n ≤ 10`, but it is still unnecessary. In the worst case there are up to `10! = 3,628,800` states. Even though many are unreachable, exploring states for thousands of test cases would be excessive.

The key observation comes from examining what happens to the first element.

Every allowed operation uses an index between `2` and `n-1` and swaps positions `i` and `i+1`.

Position `1` is never touched.

That means the first element of the permutation never changes.

What must the first element be in a sorted permutation? Since the array is a permutation of `1..n`, the sorted permutation always begins with `1`.

So if the first element is not `1`, sorting is impossible.

The surprising part is that if the first element already equals `1`, sorting is always possible.

Why? Every element larger than `1` can eventually be moved rightward through a sequence of valid local-maximum swaps. The official solution observation is that having `1` fixed at the front is both necessary and sufficient.

The entire problem reduces to checking a single value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of reachable states) | O(number of reachable states) | Unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the permutation.
2. Check the first element.
3. If the first element equals `1`, print `"YES"`.

A sorted permutation must begin with `1`, and when `1` is already fixed at the front, the allowed operations are sufficient to sort the remaining elements.
4. Otherwise print `"NO"`.

The first position can never participate in any operation, so a value different from `1` can never be replaced by `1`.

### Why it works

The invariant is that position 1 never changes.

Every operation swaps positions `i` and `i+1` where `2 ≤ i ≤ n-1`. Since position 1 is never involved, the first element remains constant throughout the entire process.

A sorted permutation of `1..n` must start with `1`. If the first element is not `1`, reaching the sorted permutation is impossible.

Conversely, if the first element is `1`, the remaining elements can always be rearranged into sorted order using the allowed local-maximum swaps. This fact was the core observation behind the problem and makes the condition both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    if a[0] == 1:
        print("YES")
    else:
        print("NO")
```

The implementation follows the proof directly.

For each test case we read the permutation and inspect only its first element. No simulation is required.

A common mistake is trying to model the swaps explicitly. The operation looks like a sorting process, but the invariant on the first position completely determines the answer.

Another possible mistake is checking whether the permutation is already sorted. A permutation such as:

```
1 3 2
```

is not initially sorted, yet the answer is still `"YES"` because the allowed operation can finish the sorting.

## Worked Examples

### Example 1

Input permutation:

```
1 3 2 5 4
```

| Step | First Element | Decision |
| --- | --- | --- |
| Read array | 1 | Check condition |
| Condition | 1 == 1 | YES |

Output:

```
YES
```

This example demonstrates the sufficiency of the condition. The array is not sorted initially, but having `1` fixed at the front guarantees that sorting is achievable.

### Example 2

Input permutation:

```
5 1 2 3 4
```

| Step | First Element | Decision |
| --- | --- | --- |
| Read array | 5 | Check condition |
| Condition | 5 != 1 | NO |

Output:

```
NO
```

This example demonstrates the invariant. Since position 1 never changes, the value `5` can never leave the first position, making a fully sorted permutation impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only the first element is inspected |
| Space | O(1) | No extra data structures are used |

Even with 5000 test cases, the total work is negligible. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append("YES" if a[0] == 1 else "NO")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""6
3
1 2 3
5
1 3 2 5 4
5
5 4 3 2 1
3
3 1 2
4
2 3 1 4
5
5 1 2 3 4
"""
) == "YES\nYES\nNO\nNO\nNO\nNO"

# minimum size, already sorted
assert run(
"""1
3
1 2 3
"""
) == "YES"

# minimum size, impossible
assert run(
"""1
3
2 1 3
"""
) == "NO"

# n = 10, first element is 1
assert run(
"""1
10
1 10 9 8 7 6 5 4 3 2
"""
) == "YES"

# n = 10, first element not 1
assert run(
"""1
10
10 1 2 3 4 5 6 7 8 9
"""
) == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3` | YES | Minimum valid sorted permutation |
| `2 1 3` | NO | Smallest impossible case |
| `1 10 9 8 7 6 5 4 3 2` | YES | Large size, condition still sufficient |
| `10 1 2 3 4 5 6 7 8 9` | NO | Large size, first-position invariant |

## Edge Cases

Consider:

```
1
3
2 1 3
```

The algorithm checks the first element and finds `2`. Since position 1 can never participate in a swap, `2` will remain there forever. The output is:

```
NO
```

Now consider:

```
1
5
1 5 4 3 2
```

The algorithm sees that the first element is already `1` and prints:

```
YES
```

Even though the rest of the permutation is heavily unsorted, the theorem behind the solution guarantees that the allowed operations can sort it.

Finally, consider the already sorted case:

```
1
4
1 2 3 4
```

The first element is `1`, so the algorithm outputs:

```
YES
```

No operations are needed, and the condition still correctly identifies the answer.
