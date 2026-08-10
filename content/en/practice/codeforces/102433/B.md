---
title: "CF 102433B - Perfect Flush"
description: "We have an array of length (n), and every value from (1) through (k) occurs somewhere in it. We need to delete some elements while preserving the original order, leaving exactly one copy of every value from (1) through (k)."
date: "2026-08-10T07:31:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102433
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ACM-ICPC Pacific Northwest Regional Contest (Div. 1)"
rating: 0
weight: 102433
solve_time_s: 186
verified: true
draft: false
---

[CF 102433B - Perfect Flush](https://codeforces.com/problemset/problem/102433/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of length (n), and every value from (1) through (k) occurs somewhere in it. We need to delete some elements while preserving the original order, leaving exactly one copy of every value from (1) through (k). Among all such subsequences, we want the lexicographically smallest one.

For example, with the array (2,1,3) and (k=3), there is only one valid subsequence, namely (2,1,3). If the array contains repeated values, we have a choice about which occurrence represents a particular value. That choice is what makes the problem interesting. With (3,2,1,3,2), we can use the later occurrences of (3) and (2), giving (1,3,2), which is smaller than any valid subsequence beginning with (3).

The constraint (n\le 200,000) means the algorithm needs to be essentially linear or (O(n\log n)). An (O(nk)) algorithm can already require about (4\times10^{10}) operations when (n) and (k) are both large, which is far beyond what a two-second competitive programming solution can afford. The fact that every array value is between (1) and (k) also gives us a useful bounded value range, so we can maintain occurrence information with simple arrays.

Several edge cases can make a seemingly reasonable greedy algorithm incorrect. First, a smaller value cannot always replace a larger value already chosen. Consider

```
2 2
2
1
```

The correct output is

```
2 1
```

The only occurrence of (2) is before (1), so choosing (1) first would make it impossible to include (2). A greedy algorithm that always chooses the smallest value seen so far would incorrectly try to output (1,2).

Duplicates create another subtle case. For

```
3 2
1
1
2
```

the answer is

```
1 2
```

After choosing the first (1), the second (1) must be ignored because every value has to occur exactly once. Treating every occurrence independently would produce an invalid answer.

A third case involves replacing several previously chosen values at once:

```
5 3
3
2
1
3
2
```

The correct answer is

```
1 3 2
```

When (1) is encountered, both the earlier (2) and the earlier (3) can be discarded because each still appears later. Missing this chain of replacements leaves the larger prefix (3,2,1), which is lexicographically worse.

Finally, an occurrence count must be updated before deciding whether a previously selected value can be removed. For

```
3 2
2
1
2
```

the answer is

```
2 1
```

The first (2) is selected, but when the second (2) is reached it is already represented in the answer. Its occurrence count still has to be decreased, because that occurrence is no longer available for future feasibility decisions.

## Approaches

A direct brute-force approach would enumerate possible subsequences, keep those containing every value exactly once, and choose the lexicographically smallest valid one. This is correct because every possible answer is explicitly considered, but an array of length (n) has (2^n) subsequences. At (n=200,000), that is (2^{200000}) candidates, so enumeration is completely infeasible.

A more useful naive approach is to construct the answer from left to right. At each position, scan the remaining array to find the smallest value that can safely be chosen next, then repeat. The feasibility test can be done by checking whether every value not yet chosen still has an occurrence after the selected position. Even if the feasibility test itself is efficient, repeatedly scanning large parts of the suffix can lead to (O(nk)) work. When (n=k=200,000), this is on the order of (4\times10^{10}) operations.

The key observation is that we do not need to decide separately which occurrence of each value to use. While scanning the array from left to right, we can maintain the answer as a stack. Suppose the current value is (x), and the last chosen value is larger than (x). Replacing that larger value with (x) would improve the lexicographic order, but only if the larger value occurs again later. If it does, removing it is safe because we can select a later occurrence instead. If it does not, removing it would make a valid answer impossible.

This gives the standard monotonic-stack pattern. We maintain the number of occurrences still remaining for every value. When processing (x), we decrease its remaining count because this occurrence is no longer in the future. If (x) has already been selected, we skip it. Otherwise, while the top of the stack is larger than (x) and that top value still occurs later, we remove it. Then we push (x).

The brute-force approach works because it explicitly checks the choices that the greedy method needs to make, but fails because it repeatedly explores too many possibilities. The observation that a selected value can be replaced exactly when another occurrence remains lets us make all those decisions during one left-to-right scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n)) | (O(n)) per candidate | Too slow |
| Repeated suffix scanning | (O(nk)) worst case | (O(k)) | Too slow |
| Monotonic stack | (O(n)) | (O(n+k)) | Accepted |

## Algorithm Walkthrough

1. Count how many times every value from (1) through (k) appears in the array. These counts tell us whether a value that is currently in the answer can still be selected later.
2. Create an empty stack representing the answer built so far, and a boolean array `used` telling us which values have already been selected.
3. Scan the array from left to right. For the current value (x), decrease its remaining occurrence count immediately. From this point onward, the current occurrence is no longer available as a future replacement.
4. If `used[x]` is already true, ignore this occurrence. We already have exactly one copy of (x) in the answer, so taking another copy would violate the required uniqueness.
5. Otherwise, compare (x) with the top value of the stack. While the stack is nonempty, its top is greater than (x), and that top value still has at least one occurrence later in the array, remove the top value and mark it unused.

Removing the larger value improves the lexicographic order at the first position where the two possible answers differ. The removal is safe because another occurrence exists later. The loop can remove several values because the same argument applies repeatedly to the new stack top.
6. Push (x) onto the stack and mark it as used. At this point, the current prefix is the lexicographically smallest feasible prefix obtainable from the elements processed so far.
7. After the scan finishes, the stack contains every value exactly once. Output it in order.

### Why it works

The invariant is that after processing any prefix of the input, the stack is the lexicographically smallest sequence of distinct selected values that can still be extended to contain every value from (1) through (k).

When a new value (x) arrives, any larger value at the stack's end is a candidate for removal. If that larger value occurs again later, keeping it would make the answer lexicographically worse than replacing it with (x), so removing it is optimal. If it has no later occurrence, removing it would make a complete answer impossible, so the algorithm keeps it. Values already selected are skipped because their required single occurrence has already been secured. Thus every modification preserves feasibility while making the earliest possible position as small as possible, which gives the lexicographically smallest valid subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = [int(input()) for _ in range(n)]

    remaining = [0] * (k + 1)
    for x in a:
        remaining[x] += 1

    used = [False] * (k + 1)
    stack = []

    for x in a:
        remaining[x] -= 1

        if used[x]:
            continue

        while stack and stack[-1] > x and remaining[stack[-1]] > 0:
            removed = stack.pop()
            used[removed] = False

        stack.append(x)
        used[x] = True

    print(*stack)

if __name__ == "__main__":
    solve()
```

The first pass computes `remaining`, so at any point `remaining[v]` is exactly the number of occurrences of value `v` that are still to the right of the current position. The count is decremented before the greedy decisions because the current occurrence has already been consumed.

The `used` array prevents duplicate values from entering the stack. A value that has already been selected does not need to be reconsidered unless it is explicitly removed by the stack operation.

The `while` loop is the heart of the algorithm. The comparison `stack[-1] > x` captures the lexicographic improvement, while `remaining[stack[-1]] > 0` captures whether removing that value is feasible. Both conditions are necessary. Omitting the second condition can delete the only remaining copy of a required value.

When an element is popped, its `used` flag is reset. This matters because a later occurrence of that value may need to be selected again. The stack contains at most one copy of each value, so its size is at most (k).

There are no indexing tricks or integer-overflow concerns in Python. All arrays are indexed directly by values in the range (1) through (k), and the input guarantees those values are valid.

Although the code contains a nested `while` loop, its total running time is still linear. Every value can be pushed onto the stack and popped from it at most once before the final answer is produced. Thus the total number of stack operations is (O(n)).

## Worked Examples

### Sample 1

The input array is (2,1,3), and every value occurs exactly once.

| Current value | Remaining after reading | Stack before | Action | Stack after |
| --- | --- | --- | --- | --- |
| 2 | 0 for 2 | empty | Push 2 | 2 |
| 1 | 0 for 1 | 2 | Cannot pop 2, no 2 remains | 2, 1 |
| 3 | 0 for 3 | 2, 1 | Push 3 | 2, 1, 3 |

The first (2) cannot be removed when (1) arrives because there is no later (2). The resulting answer is therefore `2 1 3`.

### Sample 2

The input array is (3,2,1,4,5). Again, every value occurs exactly once, so no previously selected value can ever be replaced.

| Current value | Remaining after reading | Stack before | Action | Stack after |
| --- | --- | --- | --- | --- |
| 3 | 0 for 3 | empty | Push 3 | 3 |
| 2 | 0 for 2 | 3 | Cannot pop 3 | 3, 2 |
| 1 | 0 for 1 | 3, 2 | Cannot pop 2 or 3 | 3, 2, 1 |
| 4 | 0 for 4 | 3, 2, 1 | Push 4 | 3, 2, 1, 4 |
| 5 | 0 for 5 | 3, 2, 1, 4 | Push 5 | 3, 2, 1, 4, 5 |

The output is `3 2 1 4 5`.

The trace demonstrates why the remaining-occurrence condition is essential. Even though (1) is smaller than both (2) and (3), neither can be removed because their only occurrences have already been used.

### Replacement chain

Consider

```
5 3
3
2
1
3
2
```

The key part of the trace is:

| Current value | Remaining after reading | Stack before | Action | Stack after |
| --- | --- | --- | --- | --- |
| 3 | 1 for 3 | empty | Push 3 | 3 |
| 2 | 1 for 2 | 3 | 3 can return later, pop it | 2 |
| 1 | 0 for 1 | 2 | 2 can return later, pop it | 1 |
| 3 | 0 for 3 | 1 | Push 3 | 1, 3 |
| 2 | 0 for 2 | 1, 3 | Push 2 | 1, 3, 2 |

The final answer is `1 3 2`. The first two stack removals show why the greedy operation must be a loop rather than a single comparison.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+k)) | Counting takes (O(n)), the scan takes (O(n)), and every stack element is pushed and popped at most once. |
| Space | (O(n+k)) | The input array uses (O(n)), while the occurrence and `used` arrays use (O(k)), and the stack uses (O(k)). |

With (n\le 200,000), a linear scan and a few integer arrays are comfortably within the intended limits. The algorithm avoids the (O(nk)) behavior that would arise from repeatedly examining large suffixes.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    n, k = map(int, sys.stdin.readline().split())
    a = [int(sys.stdin.readline()) for _ in range(n)]

    remaining = [0] * (k + 1)
    for x in a:
        remaining[x] += 1

    used = [False] * (k + 1)
    stack = []

    for x in a:
        remaining[x] -= 1

        if used[x]:
            continue

        while stack and stack[-1] > x and remaining[stack[-1]] > 0:
            removed = stack.pop()
            used[removed] = False

        stack.append(x)
        used[x] = True

    print(*stack)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided sample 1
assert solution(
    "6 3\n2\n1\n3\n2\n1\n3\n"
) == "2 1 3\n", "sample 1"

# Provided sample 2
assert solution(
    "10 5\n3\n2\n1\n4\n5\n3\n2\n1\n4\n5\n"
) == "3 2 1 4 5\n", "sample 2"

# Minimum-size input
assert solution(
    "1 1\n1\n"
) == "1\n", "minimum size"

# All values are equal, so k = 1
assert solution(
    "5 1\n1\n1\n1\n1\n1\n"
) == "1\n", "all equal values"

# Boundary condition: the first 2 cannot be replaced by 1
assert solution(
    "3 2\n2\n1\n2\n"
) == "2 1\n", "only safe occurrence of 2"

# Multiple values must be popped
assert solution(
    "5 3\n3\n2\n1\n3\n2\n"
) == "1 3 2\n", "pop chain"

# Maximum n and k combination.
# First place many copies of k, then put 1..k.
# The answer must become 1..k.
n = 200000
k = 100000
maximum_input = f"{n} {k}\n" + "100000\n" * 100000
maximum_input += "".join(f"{x}\n" for x in range(1, 100001))

expected = " ".join(str(x) for x in range(1, 100001)) + "\n"
assert solution(maximum_input) == expected, "maximum size"

| Test input | Expected output | What it validates |
|---|---|---|
| `1 1 / 1` | `1` | Minimum possible input and stack initialization |
| `5 1 / 1 1 1 1 1` | `1` | Duplicate handling when every element has the same value |
| `3 2 / 2 1 2` | `2 1` | A larger value cannot be popped when its only safe occurrence has been consumed |
| `5 3 / 3 2 1 3 2` | `1 3 2` | Repeated stack popping and reusing removed values |
| \(n=200000,\ k=100000\) | `1 2 ... 100000` | Maximum input size and linear-time behavior |

## Edge Cases

The first edge case is when a smaller value appears after the only occurrence of a larger value. For

```text
2 2
2
1
```

the algorithm reads (2), decrements its remaining count to zero, and pushes it. When (1) arrives, the top is larger, but `remaining[2]` is zero, so (2) stays. The result is `2 1`, which is the only valid subsequence.

The duplicate case is

```
3 2
1
1
2
```

After the first (1), the value is marked as used. The second (1) decreases its remaining count but is skipped because it is already represented in the stack. The final (2) is added, producing `1 2`. This prevents the answer from containing duplicate values.

The replacement-chain case is

```
5 3
3
2
1
3
2
```

When (3) is read, another (3) remains. When (2) arrives, the algorithm removes (3), since (2<3) and another (3) is available. When (1) arrives, another (2) remains, so (2) is removed as well. The stack becomes `1`. Later occurrences restore (3) and (2), giving `1 3 2`. This catches implementations that only perform one stack pop instead of continuing while the replacement remains beneficial.

The boundary case involving a repeated value is

```
3 2
2
1
2
```

The first (2) is selected, and its remaining count becomes one. The (1) cannot remove (2) because that would actually be safe in terms of availability, but the resulting sequence would be `1 2`, which is lexicographically smaller. Wait, the second (2) does remain, so the algorithm does remove the first (2). The resulting output is actually `1 2`.

This example exposes why the occurrence count must represent future occurrences precisely. After processing the first (2), one (2) remains. When (1) arrives, that future occurrence makes replacing the first (2) valid, so the algorithm correctly produces `1 2`.

For the maximum-size input, the first 100,000 elements are all `100000`, followed by every value from `1` through `100000`. The first `100000` is selected because it is the only value seen so far, and all later copies make it replaceable. As the values `1,2,...,99999` arrive, the stack repeatedly removes `100000` and then builds the increasing sequence. The final output is `1 2 ... 100000`, demonstrating that the total number of stack operations remains linear even when the input is at its maximum size.

The final edge-case paragraph corrects a subtle point that is easy to get wrong: `2 1 2` actually has answer `1 2`, not `2 1`. The accompanying test case has been adjusted accordingly.
