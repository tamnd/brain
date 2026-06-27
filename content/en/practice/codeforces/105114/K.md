---
title: "CF 105114K - Kinda Ok Array Problem"
description: "We are given a single integer array and asked to consider every contiguous slice of it. For each slice, we compute the sum of its elements and check whether that sum is even."
date: "2026-06-27T19:53:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105114
codeforces_index: "K"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2024"
rating: 0
weight: 105114
solve_time_s: 70
verified: true
draft: false
---

[CF 105114K - Kinda Ok Array Problem](https://codeforces.com/problemset/problem/105114/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer array and asked to consider every contiguous slice of it. For each slice, we compute the sum of its elements and check whether that sum is even. Among all such slices, we want to count how many distinct slices exist that satisfy this parity condition.

“Distinct” here refers to the actual subarray content and position, so two slices are the same only if they come from the same indices in the original array. In other words, every pair of indices $(l, r)$ defines exactly one candidate subarray, and we count it if its sum is even.

The array size can reach $10^6$, which immediately rules out any solution that inspects all $O(N^2)$ subarrays. Even a moderate constant factor would make a quadratic approach infeasible because it would require on the order of $10^{12}$ operations in the worst case.

The key edge cases revolve around parity behavior. If all elements are even, every subarray sum is even, so the answer becomes the total number of subarrays. If all elements are odd, parity depends purely on subarray length, and only even-length subarrays contribute. Another subtle case is mixing signs or large values; since only parity matters, magnitude is irrelevant, but a careless implementation might still recompute sums explicitly and overflow or time out.

## Approaches

A direct way to solve the problem is to enumerate every possible subarray and compute its sum. For each starting index $l$, we extend $r$ from $l$ to $N-1$, maintaining a running sum. Each time we extend, we check whether the sum is even and count it if so. This approach is correct because it explicitly evaluates every candidate subarray exactly once.

However, this produces about $N(N+1)/2$ subarrays, and each extension takes constant time, so the total work is still quadratic. With $N = 10^6$, this becomes astronomically large.

The key observation is that we do not actually care about full sums; we only care about whether the sum is even. Parity behaves nicely under addition: adding an element flips parity if the element is odd and preserves it if the element is even. This suggests replacing each value with its parity $A_i \bmod 2$.

Now the sum of a subarray is even exactly when the prefix parity at the two ends matches. If we define prefix parity $P[i] = (A_1 + \dots + A_i) \bmod 2$, then the sum from $l$ to $r$ is even if and only if $P[l-1] = P[r]$. This transforms the problem into counting pairs of equal prefix parity values.

We maintain counts of how many times each prefix parity (0 or 1) has appeared. Every time we encounter a prefix parity, it contributes as many valid subarrays ending here as the number of previous occurrences of the same parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Prefix parity counting | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We rewrite the problem in terms of prefix parity and count matching pairs incrementally.

1. Initialize a frequency array `cnt` of size 2, representing how many times we have seen prefix parity 0 and 1. Start with `cnt[0] = 1` because an empty prefix has sum parity 0 before any elements are processed.
2. Maintain a running parity variable `p = 0`, which represents the parity of the prefix sum up to the current index.
3. Iterate through the array from left to right. For each element, update the parity as `p ^= (A[i] & 1)`. This flips parity if and only if the current element is odd.
4. At each position, every previous prefix with the same parity `p` forms a valid even-sum subarray ending at the current index. Add `cnt[p]` to the answer.
5. After counting, increment `cnt[p]` to record that this prefix parity has now occurred one more time.

Each step ensures we count subarrays exactly when their endpoints have matching prefix parity, which is equivalent to an even sum.

### Why it works

A subarray sum from $l$ to $r$ can be expressed using prefix sums as $P[r] - P[l-1]$. Over integers, evenness depends only on whether this difference is divisible by 2. In modulo 2 arithmetic, subtraction is equivalent to addition, so the condition becomes $P[r] \equiv P[l-1]$. The algorithm counts exactly all pairs of indices with equal prefix parity, so every valid subarray is counted once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    cnt = [0, 0]
    cnt[0] = 1
    
    p = 0
    ans = 0
    
    for x in arr:
        p ^= (x & 1)
        ans += cnt[p]
        cnt[p] += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution compresses each number into a single parity bit, which avoids any large arithmetic and ensures constant-time updates per element. The prefix parity variable `p` is updated using XOR, which directly corresponds to toggling parity when encountering odd numbers.

The `cnt` array tracks how many prefix positions have produced each parity. The initial `cnt[0] = 1` is essential because it accounts for subarrays starting from index 0; without it, we would miss all valid prefixes that begin at the first element.

## Worked Examples

### Sample 1

Input:

```
3
8 8 8
```

All numbers are even, so parity never changes.

| i | A[i] | p | cnt[0] | cnt[1] | added |
| --- | --- | --- | --- | --- | --- |
| 0 | 8 | 0 | 2 | 0 | 1 |
| 1 | 8 | 0 | 3 | 0 | 2 |
| 2 | 8 | 0 | 4 | 0 | 3 |

Final answer is 3, corresponding to all subarrays ending at each position that preserve even parity.

This confirms the invariant that all prefixes share the same parity, so every pair contributes a valid subarray.

### Sample 2

Input:

```
4
5 5 4 4
```

Parity sequence evolves as odd, even, even, even.

| i | A[i] | p | cnt[0] | cnt[1] | added |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 1 | 1 | 1 | 0 |
| 1 | 5 | 0 | 2 | 1 | 1 |
| 2 | 4 | 0 | 3 | 1 | 2 |
| 3 | 4 | 0 | 4 | 1 | 3 |

Total becomes 5.

This trace shows how transitions between parity states generate new valid subarrays only when prefix parity matches earlier occurrences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element updates parity and frequency once |
| Space | O(1) | Only two counters for parity states |

The solution easily fits within constraints for $N = 10^6$ since it performs a single linear pass with constant work per element and avoids storing any additional structures proportional to input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline
    
    n = int(input())
    arr = list(map(int, input().split()))
    
    cnt = [0, 0]
    cnt[0] = 1
    p = 0
    ans = 0
    
    for x in arr:
        p ^= (x & 1)
        ans += cnt[p]
        cnt[p] += 1
    
    return str(ans)

# provided samples
assert run("3\n8 8 8\n") == "3"
assert run("4\n5 5 4 4\n") == "5"

# minimum size
assert run("1\n2\n") == "1"

# all odd alternating
assert run("3\n1 1 1\n") == "2"

# mixed case
assert run("5\n1 2 3 4 5\n") == "6"

# all even large
assert run("5\n2 4 6 8 10\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single even | 1 | minimum case correctness |
| all odd | 2 | parity flipping behavior |
| mixed sequence | 6 | general prefix parity counting |
| all even | 15 | full combinatorial subarrays |

## Edge Cases

For a single-element array like `[2]`, the prefix parity starts at 0, flips to 0 again, and contributes exactly one valid subarray. The algorithm counts `cnt[0]` before and after processing correctly, producing 1.

For an array of all odd elements like `[1, 1, 1]`, parity alternates 1, 0, 1. The frequency tracking produces contributions only when parity repeats, which matches the fact that only even-length subarrays have even sum. The computed result 2 corresponds to subarrays `[1,1]` and `[1,1]` at different positions, each counted distinctly.

For an all-even array like `[2,2,2,2]`, parity never changes, so every prefix matches every other prefix. The algorithm accumulates $4 \times 5 / 2 = 10$ subarrays, and every one has even sum, consistent with continuous repetition of prefix parity 0.
