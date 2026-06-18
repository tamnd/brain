---
problem: 988A
contest_id: 988
problem_index: A
name: "Diverse Team"
contest_name: "Codeforces Round 486 (Div. 3)"
rating: 800
tags: ["brute force", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 64
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a9d8-c8d4-83ec-b44a-533030529b6c
---

# CF 988A - Diverse Team

**Rating:** 800  
**Tags:** brute force, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 4s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a9d8-c8d4-83ec-b44a-533030529b6c  

---

## Solution

## Problem Understanding

We are given a list of students, each student having a rating value. The task is to choose a subset of exactly `k` students such that no two chosen students share the same rating. The output is not the ratings themselves, but the indices of the chosen students in the original list.

So the problem reduces to scanning through an array while selecting positions whose values have not been seen before, until either we collect `k` valid indices or we run out of distinct values.

The constraints are very small: `n ≤ 100` and `a_i ≤ 100`. This immediately rules out any need for advanced data structures or optimization. Even a quadratic or simple linear scan is enough. A single pass with a set is more than sufficient.

The only situation where the answer does not exist is when the array contains fewer than `k` distinct values. In that case, no matter how we pick students, we cannot reach size `k` while keeping ratings distinct.

A subtle edge case appears when duplicates dominate the array. For example, if all values are identical and `k > 1`, we must reject immediately. Another case is when duplicates exist but enough distinct values are scattered later in the array; a greedy scan must ensure we still pick all distinct values and not get stuck early by any ordering assumptions.

## Approaches

A brute-force interpretation would be to try all subsets of size `k` and check whether all chosen values are distinct. This would involve checking combinations of `n` choose `k`, and for each subset verifying uniqueness, leading to an explosion even for small `n`. In the worst case, the number of subsets is on the order of 2ⁿ, and even restricting to fixed size k still gives O(nᵏ) behavior, which is unnecessary for this problem.

The structure of the problem suggests a simpler observation: we do not need to search globally. We only need any `k` distinct values. Since we are allowed to output any valid subset, we can greedily scan from left to right and pick the first occurrence of each new rating. This works because the order of selection does not matter, and every index is equally valid as long as its value has not been used before.

The brute-force fails because it explores irrelevant combinations, while the greedy solution works because uniqueness is a local property that can be enforced incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(k) | Too slow |
| Greedy Scan with Set | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We build the answer incrementally while tracking which ratings we have already used.

1. Initialize an empty set `used` to store ratings we have already picked, and an empty list `ans` to store selected indices. The set is necessary to check uniqueness in constant time.
2. Iterate through students from index `1` to `n`. For each student, we check whether their rating is already in `used`. This check ensures we only pick distinct values.
3. If the rating has not been used, we add this student’s index to `ans` and mark the rating as used. We are effectively committing to this student as a representative of their rating.
4. Stop early if `ans` reaches size `k`. At that point we already have a valid team, and continuing would not change correctness.
5. After the loop, check whether `ans` has size `k`. If not, it means we encountered fewer than `k` distinct ratings in the entire array, so forming a valid team is impossible.

### Why it works

The key invariant is that `used` always contains exactly the set of ratings represented in `ans`. Every time we add a student, we introduce a previously unseen rating, guaranteeing that all selected indices correspond to distinct values. Since we process every element, if fewer than `k` distinct ratings exist, the algorithm will exhaust the array without reaching size `k`, correctly signaling impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

used = set()
ans = []

for i in range(n):
    if a[i] not in used:
        used.add(a[i])
        ans.append(i + 1)
        if len(ans) == k:
            break

if len(ans) < k:
    print("NO")
else:
    print("YES")
    print(*ans)
```

The solution uses a set to track seen ratings and a list to store chosen indices. The loop stops early once we collect enough distinct elements, which avoids unnecessary work but is not required for correctness given the small constraints.

Indexing is carefully handled by outputting `i + 1` since the problem uses 1-based indexing.

## Worked Examples

### Example 1

Input:

```
5 3
15 13 15 15 12
```

| i | a[i] | used before | action | ans |
| --- | --- | --- | --- | --- |
| 1 | 15 | {} | take | [1] |
| 2 | 13 | {15} | take | [1,2] |
| 3 | 15 | {15,13} | skip | [1,2] |
| 4 | 15 | {15,13} | skip | [1,2] |
| 5 | 12 | {15,13} | take | [1,2,5] |

The algorithm collects exactly 3 distinct values, confirming that the greedy scan successfully captures the first occurrences of each rating.

### Example 2

Input:

```
4 3
1 1 1 2
```

| i | a[i] | used before | action | ans |
| --- | --- | --- | --- | --- |
| 1 | 1 | {} | take | [1] |
| 2 | 1 | {1} | skip | [1] |
| 3 | 1 | {1} | skip | [1] |
| 4 | 2 | {1} | take | [1,4] |

After scanning all elements, we only have 2 distinct values, so the result is impossible for `k = 3`.

This demonstrates that the algorithm correctly distinguishes between “not yet found enough” and “impossible overall”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each student is processed once, with O(1) set operations on average |
| Space | O(n) | Storage for the set of distinct ratings and selected indices |

Given `n ≤ 100`, this runs in constant time in practice. Even with much larger constraints, the approach remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys
    output = []
    
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    used = set()
    ans = []
    
    for i in range(n):
        if a[i] not in used:
            used.add(a[i])
            ans.append(i + 1)
            if len(ans) == k:
                break
    
    if len(ans) < k:
        return "NO"
    return "YES\n" + " ".join(map(str, ans))

# provided sample
assert run("5 3\n15 13 15 15 12") == "YES\n1 2 5"

# all equal values
assert run("4 2\n7 7 7 7") == "NO"

# exact k distinct
assert run("3 3\n1 2 3") == "YES\n1 2 3"

# more than k distinct
assert run("5 2\n5 4 3 2 1") == "YES\n1 2"

# duplicates scattered
assert run("6 3\n1 2 1 3 2 4") == "YES\n1 2 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | NO | impossibility detection |
| exact k distinct | YES all indices | minimal valid selection |
| descending unique | first k indices | early stopping correctness |
| scattered duplicates | valid greedy picks | stability under repetition |

## Edge Cases

When all students share the same rating, the algorithm adds only one index before exhausting the array. For input `n = 4, k = 2, a = [7,7,7,7]`, `used` becomes `{7}` and `ans = [1]`. After the loop ends, the size check fails and the algorithm correctly outputs `"NO"`.

When the array contains exactly `k` distinct values, such as `1 2 3` with `k = 3`, every iteration adds a new index. The algorithm reaches size `k` exactly at the last step and stops early, confirming correct termination.

When duplicates are mixed with distinct values, like `1 2 1 3 2 4`, the set ensures that only first occurrences contribute. Even though duplicates appear earlier, they do not interfere with collecting enough distinct values, and the final result remains valid.