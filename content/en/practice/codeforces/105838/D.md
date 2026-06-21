---
title: "CF 105838D - Cowardly Lizard V"
description: "We are given several independent test cases. In each test case, there are $n$ caves labeled from 1 to $n$, and a sequence of $n$ planned inspections, where each inspection targets one cave. The sequence is fixed and known in advance."
date: "2026-06-22T01:20:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105838
codeforces_index: "D"
codeforces_contest_name: "The 14th Huazhong Agricultural University Programming Contest"
rating: 0
weight: 105838
solve_time_s: 65
verified: true
draft: false
---

[CF 105838D - Cowardly Lizard V](https://codeforces.com/problemset/problem/105838/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there are $n$ caves labeled from 1 to $n$, and a sequence of $n$ planned inspections, where each inspection targets one cave. The sequence is fixed and known in advance.

The player must choose exactly one cave $x$ to hide in, and cannot change it afterward. The goal is to pick a cave that is never inspected in the entire sequence. In other words, we want a value $x$ between 1 and $n$ such that it does not appear anywhere in the array.

The output for each test case is any such valid cave number if it exists, otherwise we output -1 when every cave from 1 to $n$ appears at least once.

The constraints allow up to 1000 test cases with total $n$ across all tests up to $2 \cdot 10^5$. This means any solution that is roughly linear per test case is fine, but anything quadratic per test case would be too slow because it could degrade to about $10^{10}$ operations in the worst distribution.

A subtle case appears when the array is a permutation of $1..n$. In that case every number is present exactly once, so there is no valid choice and the answer must be -1. Another edge case is $n = 1$. If the only value is 1, the answer is -1; if somehow it is not 1 (which cannot happen due to constraints), it would be 1.

A naive mistake is to assume the answer is always the smallest missing number without properly tracking presence, or to forget that we must consider the full range $1..n$, not just the values that appear in the sequence.

## Approaches

The most direct idea is to try every candidate cave $x$ from 1 to $n$, and for each one scan the entire sequence to check whether it appears. If we find any $x$ that never appears, we output it immediately.

This works because it explicitly verifies the condition in the problem. However, the cost is high. For each of $n$ candidates, we may scan up to $n$ elements, leading to $O(n^2)$ per test case. With total $2 \cdot 10^5$, this becomes far too slow.

The key observation is that we do not need to test each candidate independently. We only care about which values appear at least once. Once we know the set of present values, any number from 1 to $n$ not in that set is valid. This reduces the problem to a single pass marking structure.

We can maintain a boolean array of size $n$, mark each seen value, and then scan once to find any unmarked index. This brings the solution down to linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Marking / Boolean array | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the array $a$. We want to record which values from 1 to $n$ appear.
2. Create a boolean array `seen` of size $n+1$, initialized to false. This will track whether each cave number appears in the inspection sequence.
3. Traverse the array $a$. For each value $a_i$, mark `seen[a_i] = true`. This step compresses all information about the sequence into presence data.
4. After processing all elements, iterate from 1 to $n$. The first index $x$ such that `seen[x]` is false is a valid answer, since it never appears in the sequence.
5. If no such $x$ exists, output -1. This happens exactly when every number from 1 to $n$ was marked, meaning the sequence contains all possible caves.

Why it works: the algorithm reduces the problem to checking membership in a set. Since the only requirement is absence from the sequence, any value not marked as present is automatically valid. If all values are marked, the sequence covers the entire domain, leaving no valid choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        
        seen = [False] * (n + 1)
        for x in a:
            seen[x] = True
        
        ans = -1
        for i in range(1, n + 1):
            if not seen[i]:
                ans = i
                break
        
        out.append(str(ans))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the marking strategy. The `seen` array is reset per test case, ensuring no leakage between cases. The first loop compresses the input into presence information. The second loop performs a linear scan to locate any missing value.

A subtle detail is that we stop at the first missing value rather than collecting all missing values, since any valid answer is acceptable. This keeps the logic minimal and avoids unnecessary work.

## Worked Examples

### Example 1

Input:

```
1
3
1 2 3
```

| Step | Seen array updates | Missing scan | Current answer |
| --- | --- | --- | --- |
| After processing | [_, T, T, T] | checking 1..3 | - |
| Scan | 1→T, 2→T, 3→T | none found | -1 |

Here every value appears, so no valid cave exists.

### Example 2

Input:

```
1
5
2 2 3 5 5
```

| Step | Seen updates | Missing scan | Current answer |
| --- | --- | --- | --- |
| After processing | [_, F, T, T, F, T] | start from 1 | 1 |

Value 1 is never seen, so it is immediately valid and returned.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | one pass to mark + one scan to find answer |
| Space | $O(n)$ | boolean array for presence tracking |

The total $n$ over all test cases is bounded by $2 \cdot 10^5$, so the algorithm runs comfortably within limits since it performs only a few linear passes over the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            n = int(input())
            a = list(map(int, input().split()))
            seen = [False] * (n + 1)
            for x in a:
                seen[x] = True
            ans = -1
            for i in range(1, n + 1):
                if not seen[i]:
                    ans = i
                    break
            out.append(str(ans))
        print("\n".join(out))

    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

# provided sample
assert run("1\n1\n1\n") == "-1"

# all equal but missing others
assert run("1\n5\n2 2 2 2 2\n") in {"1", "3", "4", "5"}

# permutation case
assert run("1\n4\n1 2 3 4\n") == "-1"

# single missing at end
assert run("1\n3\n1 2 1\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | any missing index | duplicates do not matter |
| full permutation | -1 | no valid answer exists |
| small n with repetition | correct missing detection | correctness of marking |

## Edge Cases

A key edge case is when the array is a perfect permutation of $1..n$. For example:

```
1
4
1 2 3 4
```

The marking array becomes fully true for all indices 1 through 4. The scan finds no false entry, and the algorithm correctly outputs -1.

Another case is when the sequence contains only one repeated value:

```
1
5
2 2 2 2 2
```

Here only index 2 is marked true. The scan immediately finds 1 as the first missing value and returns it. This shows that duplicates do not affect correctness, since we only care about presence, not frequency.
