---
problem: 1265B
contest_id: 1265
problem_index: B
name: "Beautiful Numbers"
contest_name: "Codeforces Round 604 (Div. 2)"
rating: 1300
tags: ["data structures", "implementation", "math", "two pointers"]
answer: passed_samples
verified: true
solve_time_s: 171
date: 2026-06-13
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d863c-a648-83ec-8f8b-4b13830ade05
---

# CF 1265B - Beautiful Numbers

**Rating:** 1300  
**Tags:** data structures, implementation, math, two pointers  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 51s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d863c-a648-83ec-8f8b-4b13830ade05  

---

## Solution

## Problem Understanding

We are given a permutation of numbers from 1 to n, and we want to classify each value m from 1 to n as either “good” or “bad”. A value m is considered good if somewhere inside the array there exists a contiguous segment whose elements are exactly the numbers from 1 to m, each appearing once.

So instead of choosing arbitrary values, we are asking whether the permutation contains a block of consecutive positions whose values form a perfect set of the first m integers.

The output for each test case is a binary string of length n. The i-th character tells whether i is good or not.

The constraints matter because n can be large across test cases, up to 2×10^5 total. Any solution that tries all subarrays and checks whether they form valid permutations would repeatedly scan segments, leading to quadratic or worse behavior per test case, which is far beyond what 1 second allows.

A naive pitfall appears when thinking “just check all subarrays and test if they contain exactly 1..m”. Even if checking a subarray is optimized, the number of subarrays is O(n^2), and each validation costs at least O(n) unless heavily optimized, which becomes infeasible.

Another subtle issue is assuming that if a segment contains all values from 1 to m somewhere, it is automatically valid. That is not true unless the segment length is exactly m and contains no extra numbers outside that range.

## Approaches

The brute-force perspective starts by fixing m and scanning all possible subarrays. For each subarray, we would track whether it contains exactly the set {1, 2, ..., m}. This requires checking both completeness and absence of extra values outside the range. Even with frequency arrays, we would still need O(n^2) subarrays and O(n) updates in the worst case, leading to O(n^3) in a straightforward implementation or O(n^2) with heavy preprocessing, which still fails for n up to 2×10^5.

The key observation is that we do not actually need to search for the subarray. Instead, we can reverse the perspective: fix m and look at where the numbers 1 through m are located in the permutation. These positions uniquely determine any candidate segment that could contain all of them.

If a valid segment exists, it must include all occurrences of numbers 1 through m. The smallest such segment is from the minimum position among these values to the maximum position among these values. That segment is valid exactly when it contains no extra elements beyond those m numbers, which happens precisely when its length equals m.

This transforms the problem into tracking min and max positions dynamically as m increases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) or O(n^2 log n) | O(n) | Too slow |
| Optimal (position tracking) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first compute the position of every value in the permutation so we can quickly locate where each number appears.

1. Build an array pos where pos[x] is the index of value x in the permutation. This allows constant-time lookup of where each number is located.
2. Initialize two variables min_pos and max_pos with the position of value 1. At this point, only number 1 is considered, and the segment containing it is trivially valid.
3. Iterate m from 2 to n. For each m, update min_pos and max_pos using pos[m]. These represent the smallest and largest indices among values 1 through m.
4. After updating for each m, check whether max_pos - min_pos + 1 equals m. This condition means the interval spanning all occurrences of 1..m has exactly m elements, so no extra numbers can lie inside it.
5. If the condition holds, mark m as beautiful; otherwise, mark it as not beautiful.

### Why it works

At any step m, the set of positions of numbers 1 through m is fixed. Any valid segment containing all these values must cover at least from min_pos to max_pos. If that interval has exactly m elements, then it contains exactly those m positions and nothing else. Since the array is a permutation, those positions correspond to distinct values, so the segment must be a permutation of 1..m. If the interval were larger, it would include extra elements outside the set, making it impossible to form a clean permutation of size m.

This means the validity of m depends only on the geometry of positions, not on explicit subarray checking.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        pos = [0] * (n + 1)
        for i, v in enumerate(p):
            pos[v] = i

        min_pos = pos[1]
        max_pos = pos[1]

        ans = ["0"] * (n + 1)

        for m in range(1, n + 1):
            idx = pos[m]
            if m == 1:
                min_pos = max_pos = idx
            else:
                if idx < min_pos:
                    min_pos = idx
                if idx > max_pos:
                    max_pos = idx

            if max_pos - min_pos + 1 == m:
                ans[m] = "1"

        out.append("".join(ans[1:]))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies entirely on maintaining the range of positions of values 1 through m. The pos array ensures constant-time access to each element’s location. The incremental update avoids recomputing anything from scratch for each m.

A common implementation mistake is recomputing min and max positions by scanning all previous values for every m, which would degrade performance to O(n^2). Another subtle issue is forgetting that indexing is zero-based in Python, so the interval length computation must remain consistent with that choice.

## Worked Examples

### Example 1

Input permutation: [4, 5, 1, 3, 2, 6]

We compute positions:

| m | pos[m] | min_pos | max_pos | max-min+1 | beautiful |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | 1 | 1 |
| 2 | 4 | 2 | 4 | 3 | 0 |
| 3 | 3 | 2 | 4 | 3 | 1 |
| 4 | 0 | 0 | 4 | 5 | 0 |
| 5 | 1 | 0 | 4 | 5 | 1 |
| 6 | 5 | 0 | 5 | 6 | 1 |

The table shows that valid values occur exactly when the positions of 1..m form a tight interval with no gaps.

### Example 2

Input permutation: [1, 4, 3, 2]

| m | pos[m] | min_pos | max_pos | max-min+1 | beautiful |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 2 | 3 | 0 | 3 | 4 | 0 |
| 3 | 2 | 0 | 3 | 4 | 0 |
| 4 | 1 | 0 | 3 | 4 | 1 |

This demonstrates that even when values are not in order, the structure depends only on their position span, not arrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each value is processed once and position updates are constant time |
| Space | O(n) | Stores position array and output string |

The total complexity over all test cases remains linear in the input size, which fits easily within the constraint of 2×10^5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        pos = [0]*(n+1)
        for i,v in enumerate(p):
            pos[v]=i
        mn=pos[1]; mx=pos[1]
        ans=["0"]*(n+1)
        for m in range(1,n+1):
            idx=pos[m]
            if idx<mn: mn=idx
            if idx>mx: mx=idx
            if mx-mn+1==m:
                ans[m]="1"
        res.append("".join(ans[1:]))
    return "\n".join(res)

# provided samples
assert run("3\n6\n4 5 1 3 2 6\n5\n5 3 1 2 4\n4\n1 4 3 2\n") == "101011\n11111\n1001"

# minimum size
assert run("1\n1\n1\n") == "1"

# already sorted
assert run("1\n5\n1 2 3 4 5\n") == "11111"

# reverse
assert run("1\n5\n5 4 3 2 1\n") == "11111"

# random structure
assert run("1\n6\n2 1 4 3 6 5\n") == "110101"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| size 1 | 1 | base case correctness |
| sorted permutation | 11111 | monotonic structure |
| reversed permutation | 11111 | order irrelevance |
| paired swaps | 110101 | general correctness |

## Edge Cases

One edge case is the smallest possible permutation. With a single element, the only valid m is 1, and the algorithm correctly initializes min_pos and max_pos at that single index, producing a span of length 1.

Another case is a fully reversed permutation. Even though elements are far from sorted, every prefix 1..m still occupies a contiguous segment in index space, so each m passes the span test. The algorithm captures this because position range depends only on endpoints, not order.

A more subtle case is when values are interleaved, such as alternating small and large numbers. The algorithm correctly fails intermediate m values where the positions of 1..m are not contiguous in index space, even if they appear frequently near each other.