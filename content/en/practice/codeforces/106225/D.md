---
title: "CF 106225D - Dungeon Equilibrium"
description: "We are given an array where each value represents a monster type. A level is considered balanced when every type that remains appears exactly as many times as its own value. For example, if type 4 is present, then it must occur exactly four times."
date: "2026-06-19T14:02:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106225
codeforces_index: "D"
codeforces_contest_name: "2025-2026 ICPC Southwestern European Regional Contest (SWERC 2025)"
rating: 0
weight: 106225
solve_time_s: 59
verified: true
draft: false
---

[CF 106225D - Dungeon Equilibrium](https://codeforces.com/problemset/problem/106225/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where each value represents a monster type. A level is considered balanced when every type that remains appears exactly as many times as its own value. For example, if type `4` is present, then it must occur exactly four times. Types that are completely removed impose no requirements. The task is to delete as few elements as possible so that the remaining multiset satisfies this rule.

The input consists of `n` monster types, each between `0` and `n`. Since only deletions are allowed, we never increase the frequency of any value. For each type we either keep it with frequency exactly equal to its value, or remove all copies of that type.

The bound `n ≤ 1000` is small, so even quadratic solutions would fit comfortably. Still, the structure of the problem allows a linear solution after counting frequencies. The only information that matters is how many times each value appears, not the order of the array.

Several situations are easy to mishandle.

Suppose a value appears fewer times than its own value.

```
3
2 2 1
```

Type `2` appears twice, so it can stay. Type `1` appears once, so it can also stay. No deletions are needed and the answer is `0`. A careless approach that removes any value whose count is not larger than the value would incorrectly delete type `1`.

Another case is when a value appears too few times.

```
2
3 3
```

Type `3` appears only twice, but it would need three copies to remain. Since adding elements is impossible, both copies must be deleted. The answer is `2`.

A special value is `0`.

```
4
0 0 1 1
```

If type `0` remains, it would need to appear exactly zero times, which means it cannot exist at all. Both zeroes must be removed. Type `1` appears twice, so one copy is removed and one is kept. The answer is `3`. Forgetting that zero requires zero occurrences leads to wrong answers.

## Approaches

The most direct brute-force idea is to process each distinct value independently. For a value `x` with frequency `f`, we can try all possibilities and determine whether keeping some copies is legal. Since the only valid remaining frequency is exactly `x`, there are only two meaningful choices. If `f ≥ x`, we may keep `x` copies and delete `f - x`, otherwise we must delete all `f` copies.

A less organized brute-force implementation might repeatedly scan the array for each value, leading to about `n²` operations in the worst case. With `n = 1000`, this still works, but it does unnecessary work.

The key observation is that different values do not interact. The decision for type `5` has no effect on the decision for type `7`. Once we know the frequency of every value, the minimum number of deletions for each type is determined independently.

If a value `x` appears `f` times, two cases arise. When `f < x`, keeping the type is impossible because we cannot create additional copies, so all `f` occurrences are deleted. When `f ≥ x`, we keep exactly `x` copies and delete the extra `f - x`.

A frequency map gives all information needed, and each distinct value is processed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and count how many times each value appears.
2. Initialize the answer to zero.
3. For every distinct value `x` with frequency `f`, determine whether enough copies exist to keep the type.
4. If `f < x`, add `f` to the answer because all copies of this value must be removed.

A value cannot survive with fewer than `x` occurrences, and adding elements is not allowed.
5. Otherwise, add `f - x` to the answer because exactly `x` copies should remain.

Any copies beyond the required amount are unnecessary and must be deleted.
6. Output the accumulated answer.

### Why it works

Each value is completely independent of the others. For a type `x`, the only legal remaining frequency is `x`. If the current frequency `f` is smaller than `x`, no valid configuration containing that type exists, so deleting all copies is unavoidable. If `f` is at least `x`, keeping exactly `x` copies minimizes deletions because any smaller positive frequency is invalid and any larger frequency violates the condition. Summing the optimal cost for every value gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution
from collections import Counter

n = int(input())
a = list(map(int, input().split()))

cnt = Counter(a)

ans = 0

for x, f in cnt.items():
    if f < x:
        ans += f
    else:
        ans += f - x

print(ans)
```

The first part counts the frequency of every monster type using `Counter`. Since the order of the array is irrelevant, frequencies contain all necessary information.

The variable `ans` stores the total number of deletions. For each value `x`, the code distinguishes the two cases described in the algorithm.

When `f < x`, every occurrence is removed because reaching frequency `x` is impossible. Otherwise, exactly `x` copies are kept and the excess `f - x` copies are deleted.

The value `0` is handled automatically. Since `f < 0` is never true, the second branch contributes `f - 0 = f`, meaning all zeroes are deleted, which matches the definition.

## Worked Examples

### Sample 1

Input

```
5
1 1 2 2 3
```

| Value x | Frequency f | Action | Added to Answer | Running Answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | Keep 1 copy | 1 | 1 |
| 2 | 2 | Keep 2 copies | 0 | 1 |
| 3 | 1 | Remove all copies | 1 | 2 |

The final answer is `2`. One copy of type `1` and the only copy of type `3` are deleted. The remaining array can be `[1, 2, 2]`.

### Sample 2

Input

```
10
1 2 3 2 4 4 4 4 5 2
```

| Value x | Frequency f | Action | Added to Answer | Running Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | Keep 1 copy | 0 | 0 |
| 2 | 3 | Keep 2 copies | 1 | 1 |
| 3 | 1 | Remove all copies | 1 | 2 |
| 4 | 4 | Keep 4 copies | 0 | 2 |
| 5 | 1 | Remove all copies | 1 | 3 |

The answer is `3`. Type `2` contributes one deletion because it appears once too many. Types `3` and `5` cannot reach their required frequencies, so all copies of those types are removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting frequencies and processing each distinct value together require linear time |
| Space | O(n) | The frequency table may contain up to n distinct values |

Since the array length is at most 1000, this solution is easily fast enough. Even for much larger limits, a linear pass over the frequencies would remain efficient.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    cnt = Counter(a)

    ans = 0
    for x, f in cnt.items():
        if f < x:
            ans += f
        else:
            ans += f - x

    return str(ans)

# provided samples
assert run("5\n1 1 2 2 3\n") == "2", "sample 1"
assert run("10\n1 2 3 2 4 4 4 4 5 2\n") == "3", "sample 2"

# custom cases
assert run("1\n1\n") == "0", "minimum size"
assert run("4\n0 0 0 0\n") == "4", "all zeroes"
assert run("5\n5 5 5 5 5\n") == "0", "all equal and already balanced"
assert run("2\n3 3\n") == "2", "frequency smaller than value"
assert run("6\n2 2 2 2 1 1\n") == "3", "excess copies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum input size |
| `0 0 0 0` | `4` | Zero values must disappear |
| `5 5 5 5 5` | `0` | Already balanced array |
| `3 3` | `2` | Impossible to keep a value with insufficient frequency |
| `2 2 2 2 1 1` | `3` | Removing excess copies correctly |

## Edge Cases

Consider the input

```
2
3 3
```

The frequency table contains only value `3` with frequency `2`. Since `2 < 3`, keeping type `3` is impossible. The algorithm adds `2` to the answer and outputs `2`. Any attempt to keep these monsters would leave frequency `2`, which violates the requirement.

Now consider

```
4
0 0 1 1
```

The frequencies are `0 → 2` and `1 → 2`. For value `0`, the algorithm contributes `2 - 0 = 2`, removing all zeroes. For value `1`, it contributes `2 - 1 = 1`, keeping exactly one copy. The final answer is `3`.

Finally, consider

```
3
2 2 1
```

Type `2` appears twice and type `1` appears once. Both frequencies already match their values, so each contributes zero deletions. The answer is `0`, confirming that the algorithm leaves already balanced configurations unchanged.
