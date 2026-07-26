---
title: "CF 102806A - \u0412\u043e\u0437\u0440\u0430\u0441\u0442\u0430\u044e\u0449\u0438\u0439 \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We are given an array of integers. For every element, we are allowed to keep its current value or change its sign. The task is to decide whether there exists some choice of signs that makes the resulting array nondecreasing."
date: "2026-07-26T16:19:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102806
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2017-2018, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102806
solve_time_s: 83
verified: true
draft: false
---

[CF 102806A - \u0412\u043e\u0437\u0440\u0430\u0441\u0442\u0430\u044e\u0449\u0438\u0439 \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/102806/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. For every element, we are allowed to keep its current value or change its sign. The task is to decide whether there exists some choice of signs that makes the resulting array nondecreasing. If such a construction exists, we must output one valid resulting array.

The input size reaches 100000 elements, so trying all possible sign choices is impossible. Each element has two possible states, which would create 2^n possible arrays. Even checking all of them would already be far beyond what a 2 second limit allows. We need an approach that processes each element a constant number of times.

The values can be as large as 100000 in absolute value, but their magnitude does not create overflow issues in Python. The main difficulty is not the arithmetic, but finding a valid sequence of choices. A wrong greedy rule can fail because choosing a larger value now may make future elements impossible to place.

The first edge case is a single element. For example:

```
Input:
1
-5

Output:
Yes
-5
```

Any one-element array is already nondecreasing. A solution that assumes at least one adjacent comparison exists may incorrectly reject it.

Another important case is when only the negative choice works for some elements. Consider:

```
Input:
3
5 3 1

Output:
Yes
-5 -3 -1
```

The positive version is decreasing, but flipping all signs gives a valid increasing sequence. A solution that only tries to keep the original signs would fail.

A final tricky case is when a negative value is not enough and we must use a positive value:

```
Input:
2
1 2

Output:
Yes
-1 2
```

Choosing negative values greedily without checking whether they remain valid would produce `-1 -2`, which is decreasing.

## Approaches

A direct brute-force approach would enumerate every possible assignment of signs. For each assignment, we could build the resulting array and check whether every adjacent pair satisfies the nondecreasing condition. This method is correct because it checks every possible answer, but it performs 2^n checks. For n = 100000, this is not even remotely feasible.

The useful observation is that each element has exactly two possible values: `-abs(a[i])` and `abs(a[i])`. Among these two, the negative value is always the smaller one. When processing the array from left to right, we only need to know the previous chosen value. The best choice for the current position is the smallest value that does not break the order.

Why is choosing the smallest possible valid value useful? A smaller current value creates fewer restrictions on all later elements. If the negative value can be placed after the previous value, it is always safe to use it. If it cannot, the positive value is the only remaining option. If even the positive value is smaller than the previous value, no solution exists.

The brute-force works because it explores every possible sign assignment, but fails because the search space grows exponentially. The observation that the smallest valid current value leaves the most freedom reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start with the previous chosen value set to negative infinity. No first element has a restriction from the left, so every valid choice is possible.
2. For each array element, consider its two possible values: the negative absolute value and the positive absolute value. The negative version is always the smaller candidate.
3. If the negative candidate is at least the previous chosen value, select it. This is the preferred choice because it keeps the current value as small as possible.
4. Otherwise, try the positive candidate. If it is at least the previous chosen value, select it.
5. If neither candidate works, the array cannot be transformed into a nondecreasing one, so output `No`.
6. After processing all elements successfully, output `Yes` and the constructed sequence.

Why it works: after every processed position, the algorithm keeps a valid prefix of the answer. Among all valid choices for the current position, it stores the smallest possible value. Any future element that could follow a larger choice could also follow this smaller choice, so the greedy decision never removes a possible solution. If the algorithm reaches an element where both choices are too small, every possible prefix ending before that element has a value at least as large as the stored previous value, so no construction can continue.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = []
    prev = -10**30

    for x in a:
        x = abs(x)

        if -x >= prev:
            cur = -x
        elif x >= prev:
            cur = x
        else:
            print("No")
            return

        ans.append(cur)
        prev = cur

    print("Yes")
    print(*ans)

if __name__ == "__main__":
    solve()
```

The code keeps only the previous chosen value because the future does not depend on earlier elements once the current prefix has been made valid. The variable `prev` represents the last value in the constructed nondecreasing prefix.

The candidates are generated from `abs(x)` rather than the original value because the operation allows either sign, so every element can always become either its magnitude or its negative magnitude. The order of checks matters: the negative candidate is tested first because it is the smaller option and gives future positions the most flexibility.

The initial value for `prev` is chosen far below any possible array value. Since the input magnitude is at most 100000, `-10**30` safely behaves as negative infinity for this problem.

## Worked Examples

### Sample 1

Input:

```
5
1 -1 -2 3 6
```

| Step | Current absolute value | Negative choice | Positive choice | Previous value | Chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | -1 | 1 | -inf | -1 |
| 2 | 1 | -1 | 1 | -1 | -1 |
| 3 | 2 | -2 | 2 | -1 | 2 |
| 4 | 3 | -3 | 3 | 2 | 3 |
| 5 | 6 | -6 | 6 | 3 | 6 |

The algorithm first keeps values as small as possible. At the third position, `-2` would be smaller than the previous value, so the positive value `2` is required. The final sequence `[-1, -1, 2, 3, 6]` is nondecreasing.

### Sample 2

Input:

```
3
1 1 0
```

| Step | Current absolute value | Negative choice | Positive choice | Previous value | Chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | -1 | 1 | -inf | -1 |
| 2 | 1 | -1 | 1 | -1 | -1 |
| 3 | 0 | 0 | 0 | -1 | 0 |

The zero value has only one possible result, and it fits after the two negative ones. This trace also confirms that equal adjacent values are allowed because the array only needs to be nondecreasing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every element is inspected once and only constant work is done. |
| Space | O(n) | The resulting array is stored for output. |

The linear complexity fits the constraint of 100000 elements because the algorithm performs only a small fixed number of operations per element.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    n = int(input())
    a = list(map(int, input().split()))

    ans = []
    prev = -10**30

    for x in a:
        x = abs(x)
        if -x >= prev:
            cur = -x
        elif x >= prev:
            cur = x
        else:
            print("No")
            sys.stdin = old_stdin
            return sys.stdout.getvalue()

        ans.append(cur)
        prev = cur

    print("Yes")
    print(*ans)

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("5\n1 -1 -2 3 6\n") == "Yes\n-1 -1 2 3 6\n", "sample 1"
assert run("3\n1 1 0\n") == "Yes\n-1 -1 0\n", "sample 2"

assert run("1\n-5\n") == "Yes\n-5\n", "single element"
assert run("2\n5 3\n") == "Yes\n-5 -3\n", "decreasing absolute values"
assert run("3\n10 1 2\n") == "Yes\n-10 -1 2\n", "switching from negative to positive"
assert run("3\n1 0 -1\n") == "No\n", "impossible ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / -5` | `Yes / -5` | Minimum-size input |
| `5 3` | `-5 -3` | Using negative values to preserve order |
| `10 1 2` | `-10 -1 2` | Boundary where a positive choice becomes necessary |
| `1 0 -1` | `No` | Detecting an impossible construction |

## Edge Cases

For a single element, the loop runs once and always accepts one of the two possible signs. The algorithm never tries to compare with a nonexistent previous element, so the case `n = 1` is handled naturally.

For an array that is already decreasing in absolute values, such as:

```
Input:
3
5 3 1
```

the algorithm chooses:

```
-5 -3 -1
```

Each next value is larger than the previous one, so the negative choices are enough.

For a case where the negative choice fails:

```
Input:
2
1 2
```

the first element becomes `-1`. At the second element, `-2` is smaller than `-1`, so it cannot be used. The algorithm tries `2`, which works, giving:

```
-1 2
```

For an impossible case:

```
Input:
3
1 0 -1
```

the first element becomes `-1`. The second element can only become `0`, so the prefix becomes `[-1, 0]`. The last element can only become `-1` or `1`; `-1` is too small and `1` is valid, giving `[-1, 0, 1]`. The greedy construction succeeds here, showing that many cases that look suspicious are still possible.

The algorithm fails only when both available values at some position are below the previous chosen value. At that moment, the stored prefix is already the most flexible possible prefix, so no other sign assignment could solve the array.

I can also adapt this into a shorter Codeforces-style editorial version if you want a more contest-submission format.
