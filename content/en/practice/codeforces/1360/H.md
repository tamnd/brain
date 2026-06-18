---
problem: 1360H
contest_id: 1360
problem_index: H
name: "Binary Median"
contest_name: "Codeforces Round 644 (Div. 3)"
rating: 2100
tags: ["binary search", "bitmasks", "brute force", "constructive algorithms"]
answer: passed_samples
verified: true
solve_time_s: 277
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e3ffc-019c-83ec-9f2e-0b9dbb143a88
---

# CF 1360H - Binary Median

**Rating:** 2100  
**Tags:** binary search, bitmasks, brute force, constructive algorithms  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 37s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e3ffc-019c-83ec-9f2e-0b9dbb143a88  

---

## Solution

## Problem Understanding

We start with the full space of all binary strings of length `m`, ordered in standard lexicographic order, which is equivalent to sorting them as fixed-length binary numbers from `0...0` up to `1...1`. From this complete ordered set, a small collection of up to 100 strings is removed. After these removals, we conceptually look at the remaining strings, sort them again in lexicographic order, and pick the middle element, where “middle” is defined as the element at index ⌊(k−1)/2⌋ among the remaining k strings.

A useful way to think about the structure is that the full set is the interval `[0, 2^m − 1]`, interpreted as binary numbers with leading zeros. Removing strings deletes up to 100 points from this very large ordered universe. The task is to determine the median of what remains without ever constructing or sorting the full set.

The constraints are the key signal. The length `m` can be as large as 60, which makes `2^m` astronomically large, so any method that iterates over all strings is impossible. However, the number of removed elements is tiny, at most 100 per test case, and the total input size across tests is bounded. This asymmetry strongly suggests that the answer depends on how removals shift positions in a global order rather than on enumerating states.

A naive approach would be to explicitly generate all `2^m` strings, delete the forbidden ones, sort, and pick the median. This immediately fails because even for `m = 60`, the universe size is far beyond any computational limit.

Another subtle pitfall is trying to binary search the answer by checking rank via counting how many valid strings are less than a candidate. If implemented naively, this still requires iterating over all `2^m` possibilities or simulating large counts inefficiently. The correct approach must avoid touching the full space entirely.

## Approaches

The brute-force viewpoint is straightforward: enumerate all binary strings of length `m`, remove the forbidden ones, sort the remaining list, and pick the middle. This works conceptually because lexicographic order matches numeric order on binary representations. The cost, however, is exponential: generating `2^60` candidates is impossible, and even storing them is infeasible.

The key observation is that we never need the full set. We only need to know how many valid strings lie before a candidate position. Since only up to 100 strings are removed, the structure of the complement is almost complete. Each removed string only creates a small “gap” in the otherwise continuous order.

This suggests thinking in terms of order statistics over a nearly full interval. Instead of iterating over all candidates, we can binary search the answer in the range `[0, 2^m - 1]`. For a candidate number `x`, we compute how many valid strings are ≤ x. This is simply `(x + 1) - count_removed_leq(x)`. Since `n ≤ 100`, counting removed elements ≤ x is O(n), making each check fast.

Binary search over a 60-bit space requires at most 60 iterations, and each iteration costs O(n), so the total is very small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m log 2^m) | O(2^m) | Impossible |
| Optimal | O(n log 2^m) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each binary string as a 60-bit integer.

1. Convert all removed strings into integers. This allows direct comparison using numeric order, which matches lexicographic order due to fixed length. This step is essential because it turns string comparison into arithmetic comparison.
2. Sort the removed values. Sorting enables fast prefix counting using binary search.
3. Define a function `removed_leq(x)` that returns how many removed numbers are ≤ x using binary search over the sorted removed array. This gives us fast access to “how many forbidden values are in the prefix up to x”.
4. Define `valid_leq(x) = (x + 1) - removed_leq(x)`. This represents how many valid strings lie in `[0, x]`.
5. Compute the target rank `target = (2^m - n - 1) // 2`. This is the index of the median in zero-based indexing.
6. Binary search the smallest `x` such that `valid_leq(x) > target`. That `x` is exactly the median string.

The binary search works over the full numeric range `[0, 2^m - 1]`, which is safe because all valid strings lie inside it.

### Why it works

The function `valid_leq(x)` is monotonic in `x`, because increasing `x` can only increase the number of valid strings in the prefix. This guarantees that binary search is valid. Each removed string subtracts exactly one point from the prefix count, so the deviation from the full prefix `[0, x]` is always precisely the number of forbidden elements inside it. As a result, we recover exact rank information without enumerating the set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_int(s):
    return int(s, 2)

def count_leq(arr, x):
    # number of elements <= x in sorted arr
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        rem = [to_int(input().strip()) for _ in range(n)]
        rem.sort()

        total = (1 << m)
        k = total - n
        target = (k - 1) // 2

        def valid_leq(x):
            return (x + 1) - count_leq(rem, x)

        lo, hi = 0, (1 << m) - 1
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if valid_leq(mid) > target:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        s = bin(ans)[2:].zfill(m)
        print(s)

if __name__ == "__main__":
    solve()
```

The solution relies on treating binary strings as integers, which removes all lexicographic complexity. The sorted removal list is used only for counting exclusions efficiently. The binary search finds the exact rank position without ever constructing the full set.

A subtle implementation detail is padding with `zfill(m)`, since numeric conversion drops leading zeros but the output must preserve fixed length. Another important point is using `x + 1` in `valid_leq(x)`, which ensures correct counting in inclusive ranges.

## Worked Examples

### Example 1

Input:

```
n = 3, m = 3
removed = [010, 001, 111]
```

Sorted removed integers: `[1, 2, 7]`

Full range is `[0..7]`, valid count is `5`, target index is `2`.

| mid (x) | valid_leq(x) | decision |
| --- | --- | --- |
| 3 | 2 | go right |
| 5 | 4 | go left |
| 4 | 3 | go left |

Final answer is `4` → `100`.

This trace shows how prefix counting avoids enumerating the valid set explicitly.

### Example 2

Input:

```
n = 1, m = 1
removed = [1]
```

Remaining set is `[0]`, so answer is `0`.

Binary search operates on `[0,1]`:

| mid | valid_leq(mid) | decision |
| --- | --- | --- |
| 0 | 1 | found |

This demonstrates correctness when the universe collapses to a single valid element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log 2^m) | binary search over 60-bit range, each step counts removed elements |
| Space | O(n) | storing removed values |

The binary search runs at most 60 iterations, and each iteration does a binary search over at most 100 elements. This fits easily within the limits even for 1000 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample 1
assert run("""5
3 3
010
001
111
4 3
000
111
100
011
1 1
1
1 1
0
3 2
00
01
10
""") == """100
010
0
1
11"""

# single element left
assert run("""1
1 1
1
""") == "0"

# no removals except one
assert run("""1
1 2
11
""") == "10"

# maximum m small n
assert run("""1
2 3
000
111
""") == "011"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | mixed | correctness on general case |
| 1 1 removed | 0 | smallest edge |
| m=2 single removal | 10 | prefix shift |
| sparse removals | 011 | ranking stability |

## Edge Cases

A key edge case is when the median lies immediately next to a removed number. For example, if `m = 3` and we remove `011`, the range is split around a single missing point. The algorithm still works because prefix counting naturally skips the missing value without needing explicit gap handling.

Another case is when the removed values cluster at the beginning of the range. Suppose we remove `000`, `001`, `010`. The prefix function `valid_leq(x)` correctly compresses the early segment so that the binary search starts effectively from the first valid block `011`. Even though the numeric gap is large, the count adjustment remains linear in the number of removals, so correctness is preserved.

Finally, when `n = 0`, the answer is simply the middle of the full range, which binary search also finds because `removed_leq(x)` is always zero and the structure reduces to pure counting over `[0, 2^m - 1]`.