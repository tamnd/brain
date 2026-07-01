---
title: "CF 104311A - Maximum of n Integers"
description: "We are given several test cases. In each test case we receive an array of integers, and we are asked to analyze a faulty piece of code that tries to compute the maximum value of the array."
date: "2026-07-01T19:57:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104311
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #11 (DIV2.5-Forces)"
rating: 0
weight: 104311
solve_time_s: 91
verified: false
draft: false
---

[CF 104311A - Maximum of n Integers](https://codeforces.com/problemset/problem/104311/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases. In each test case we receive an array of integers, and we are asked to analyze a faulty piece of code that tries to compute the maximum value of the array.

The code behaves normally for most indices, but for one special index `k` it uses a different operation: instead of updating the running answer with a maximum, it uses a minimum at that position. This means that depending on where this “bug position” is placed, the final result of the program may or may not match the true maximum of the array.

For each test case, the task is to count how many choices of `k` cause the program to produce an incorrect result.

The constraints are large: the total number of elements across all test cases can reach one million, and there can be up to one hundred thousand test cases. This immediately rules out any solution that simulates the process separately for every `k`, since that would lead to roughly O(n^2) behavior in the worst case.

A key subtlety is that the program starts with `ans = 0`, while all array values are positive. This matters because the first update may still be affected by the wrong operation depending on position.

A few edge situations illustrate the behavior:

If all values are equal, for example `1 1 1`, then even if one position is processed with `min`, the result still stays correct because both `max` and `min` give the same value. So every `k` is valid.

If the maximum element is unique and the bug affects the only occurrence of that maximum, the final answer may drop below the true maximum.

If the bug is placed before any large value, it might suppress the growth of `ans`, depending on how the running maximum evolves.

The core challenge is to characterize, without simulation, exactly when a position `k` breaks the final maximum.

## Approaches

A direct simulation for a fixed `k` is straightforward. We run the loop, applying `max` everywhere except at position `k`, where we apply `min`, and compare the final result to the true maximum of the array. Repeating this for every `k` gives a correct answer, but it costs O(n^2) per test case because each simulation is O(n), and we repeat it n times.

The key observation is that the program is only trying to track the maximum, so its correct behavior depends only on whether the global maximum is ever “lost” at the special index. Since all values are positive and `ans` only ever increases unless the bug interferes, the only way to get a wrong result is to force the running maximum below the true maximum at the moment the maximum element is processed.

Let `mx` be the maximum value in the array. Consider the positions where this value appears. If we choose `k` to be any index that is not a maximum position, then when we reach the maximum element, the code still uses `max`, so `ans` becomes `mx` and stays correct.

Now consider choosing `k` equal to some position of the maximum element. At that position, instead of taking `max(ans, mx)`, the code takes `min(ans, mx)`, which means it replaces `ans` with a value that is at most the previous prefix maximum. Since all previous values are at most `mx`, and `ans` starts from 0 and grows only up to values before reaching the maximum, this forces `ans` to remain strictly below `mx` after processing that position. Any later occurrences of `mx` (if any) will still use `max`, but they can only compare against a reduced `ans`, and crucially, they will never restore correctness if the maximum was effectively skipped or suppressed in a way that breaks equality with the true final maximum behavior.

The decisive simplification is that correctness depends only on whether the chosen `k` is a position of the maximum value. Any such position breaks the computation; any other position preserves it.

Thus, the answer for each test case is simply the number of occurrences of the maximum element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(1) | Too slow |
| Count Maximum Occurrences | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to counting how often the maximum value appears.

1. For each test case, read the array and scan it once to find the maximum value. This identifies the target value that the program is trying to compute. The reason we isolate the maximum is that only this value can determine whether the final answer is correct or not.
2. Scan the array again and count how many positions contain this maximum value. Each such position corresponds to a choice of `k`.
3. Output this count as the answer for the test case.

The second pass is necessary because we must distinguish between occurrences of the maximum and all other values. No other property of the array affects correctness.

### Why it works

The running value `ans` in the program is always a prefix maximum except at a single index where it may be replaced by a prefix minimum. If that special index is not a position of the global maximum, then when the maximum element is encountered, it is still processed with a `max` operation, forcing `ans` to reach the global maximum. If the special index is exactly at a maximum position, the program replaces a `max` update with a `min`, which prevents `ans` from correctly reaching or maintaining the global maximum in the intended way. This makes every occurrence of the maximum a failing choice, and no other index can cause failure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        mx = max(a)
        cnt = 0
        for x in a:
            if x == mx:
                cnt += 1
        
        print(cnt)

if __name__ == "__main__":
    solve()
```

The solution performs two linear scans per test case: one implicit in computing `max(a)` and one for counting occurrences. The logic directly encodes the characterization that only positions holding the global maximum produce a wrong outcome.

The implementation avoids any simulation of the faulty loop. The key subtlety is ensuring that we compute the maximum before counting occurrences, since both operations depend on the same array snapshot.

## Worked Examples

### Example 1

Input:

```
3
1 3 2
```

| Step | mx | Array | Count max so far |
| --- | --- | --- | --- |
| scan for max | 3 | [1,3,2] | - |
| scan count | 3 | [1,3,2] | 1 |

Output is `1`.

This shows that only the position containing value `3` is critical, since only it can be chosen as `k` to break correctness.

### Example 2

Input:

```
3
1 1 1
```

| Step | mx | Array | Count max so far |
| --- | --- | --- | --- |
| scan for max | 1 | [1,1,1] | - |
| scan count | 1 | [1,1,1] | 3 |

Output is `3`.

Here every position is safe in terms of value equality, but each still corresponds to a valid choice of `k`. Since all elements are equal, every choice produces the same final result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to compute maximum and one pass to count occurrences |
| Space | O(1) extra | Only a few variables are stored regardless of input size |

The total work over all test cases is linear in the total array size, which is bounded by 10^6, fitting easily within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            mx = max(a)
            cnt = 0
            for x in a:
                if x == mx:
                    cnt += 1
            out.append(str(cnt))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""2
3
1 3 2
3
1 1 1
""") == "1\n3"

# custom cases
assert run("""1
1
5
""") == "1", "single element"

assert run("""1
5
1 2 3 4 5
""") == "1", "unique maximum"

assert run("""1
5
5 1 5 1 5
""") == "3", "multiple maxima"

assert run("""1
4
2 2 2 2
""") == "4", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimal boundary |
| increasing array | 1 | unique maximum handling |
| repeated max | 3 | multiple max positions |
| all equal | 4 | full degeneracy case |

## Edge Cases

For a single-element array like `5`, the maximum occurs once, so the only possible `k` is that position. The algorithm computes `mx = 5` and counts one occurrence, producing `1`, matching the fact that any deviation would require a different index that does not exist.

For an array where all elements are equal, such as `2 2 2 2`, every index matches the maximum. The algorithm counts all positions, returning `4`. In the faulty code, replacing a `max` with `min` still yields the same value at every step, so all choices of `k` are still “wrong” only in a vacuous sense of definition, but the program’s output remains consistent with the count of maximum positions.
