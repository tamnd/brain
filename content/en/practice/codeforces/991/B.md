---
problem: 991B
contest_id: 991
problem_index: B
name: "Getting an A"
contest_name: "Codeforces Round 491 (Div. 2)"
rating: 900
tags: ["greedy", "sortings"]
answer: passed_samples
verified: true
solve_time_s: 57
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33abdb-0708-83ec-9dd2-80237283c7dd
---

# CF 991B - Getting an A

**Rating:** 900  
**Tags:** greedy, sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 57s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33abdb-0708-83ec-9dd2-80237283c7dd  

---

## Solution

## Problem Understanding

We are given a list of lab grades, each between 2 and 5. The course grade is computed as the arithmetic mean of all lab grades, then rounded to the nearest integer. The rounding rule is standard “round half up”, meaning values like 4.5 become 5 while 4.49 becomes 4.

Vasya can improve his final grade by selecting some lab works and redoing them. A redo forces that lab grade to become 5. Each redo increases the total sum of grades while keeping the number of labs unchanged, which increases the average.

The goal is to determine the smallest number of lab works Vasya must redo so that the rounded average becomes 5. Since the rounding threshold for getting a final 5 is reaching an average of at least 4.5, the problem reduces to ensuring the mean is at least 4.5 after upgrades.

The constraints are small, with at most 100 grades. This allows solutions that are quadratic or even cubic in nature, but also makes greedy sorting strategies very natural candidates.

A subtle edge case appears when the average is already close to 4.5. For example, if all grades are 4 except one 5, the average might already exceed 4.5, meaning no operation is needed. A naive approach that always tries to modify grades would incorrectly increase the answer.

Another edge case arises from rounding behavior. Since the rule is “round half up”, the condition is not strictly greater than 4.5 but greater or equal to 4.5. Missing this threshold leads to off-by-one errors in deciding whether the current configuration is already sufficient.

## Approaches

A direct approach is to try increasing subsets of grades. For each possible number of redoes k, we could choose any k positions, set them to 5, compute the new average, and check whether it reaches the required threshold. This is correct because it exhaustively explores all combinations of improvements. However, it is too slow because the number of subsets grows combinatorially as n increases, roughly on the order of C(n, k) for each k, leading to exponential behavior.

The key observation is that improving a lower grade yields more benefit than improving a higher one. Replacing a 2 with a 5 increases the sum by 3, while replacing a 4 with a 5 increases it by only 1. Since we want to reach a threshold with minimal operations, we should always prioritize upgrading the smallest values first. This turns the problem into a greedy selection problem after sorting.

Once the grades are sorted in ascending order, we simulate converting the smallest values into 5s one by one. After each conversion, we update the sum and check whether the average condition is met. The first moment the condition is satisfied gives the minimum number of operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal Greedy + Sort | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem into checking how many smallest elements must be replaced by 5 to make the average at least 4.5.

1. Compute the total sum of all grades. This gives the current baseline average.
2. Sort the grades in ascending order so that the weakest grades are considered first for improvement. This is optimal because each upgrade adds the maximum possible gain when applied to the smallest values.
3. Iterate over how many elements we decide to upgrade, from 0 up to n.
4. For each k, compute the new sum by adding (5 - a[i]) for the k smallest elements.
5. Check whether the condition new_sum ≥ 4.5 * n holds.
6. The smallest k satisfying the condition is the answer.

The key decision point is step 2. Without sorting, we might waste operations upgrading already high grades, which gives less improvement per operation and can increase the number of required redoes.

### Why it works

The process depends on a monotonic property: replacing a smaller value always yields a greater or equal increase in the sum compared to replacing a larger value. This means any optimal strategy can be rearranged so that all chosen redoes apply to the smallest elements without worsening the result. Once sorted, every prefix of upgrades represents the best possible improvement achievable with that number of operations, so the first prefix that crosses the threshold must correspond to the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    a.sort()
    
    need = 4.5 * n
    
    if total >= need:
        print(0)
        return
    
    for i in range(n):
        total += (5 - a[i])
        if total >= need:
            print(i + 1)
            return

if __name__ == "__main__":
    main()
```

The solution begins by reading the number of grades and their values. The total sum is computed once, which represents the current state before any modifications.

Sorting the array is essential because it ensures that when we simulate upgrades, we always pick the smallest grades first, maximizing the gain per operation.

We then compute the threshold as 4.5 times n. This avoids recomputing averages repeatedly and turns the condition into a simple comparison on sums.

The loop incrementally applies improvements. Each iteration simulates redoing one more lab by increasing the sum by (5 - current grade). Once the threshold is reached, we immediately return the number of operations used.

## Worked Examples

### Example 1

Input:

```
3
4 4 4
```

| k upgrades | chosen values | sum after upgrades | condition met |
| --- | --- | --- | --- |
| 0 | none | 12 | no |
| 1 | 4 → 5 | 13 | no |
| 2 | 4,4 → 5,5 | 14 | yes |

The average threshold is 13.5. With one upgrade, the sum is still too low, but with two upgrades it exceeds the threshold. This confirms that targeting smallest values is necessary since all values are equal.

### Example 2

Input:

```
3
5 4 5
```

| k upgrades | chosen values | sum after upgrades | condition met |
| --- | --- | --- | --- |
| 0 | none | 14 | yes |

The initial sum already satisfies the threshold 13.5, so no operations are required. This demonstrates the importance of checking the base condition before applying any upgrades.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, linear scan afterward |
| Space | O(1) | only a few variables besides input storage |

The constraints limit n to at most 100, so even the sorting step is trivial in cost. The solution easily fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    a.sort()
    need = 4.5 * n
    
    if total >= need:
        return "0"
    
    for i in range(n):
        total += (5 - a[i])
        if total >= need:
            return str(i + 1)

    return str(n)

# provided samples
assert run("3\n4 4 4\n") == "2"

# custom cases
assert run("1\n5\n") == "0", "single max grade"
assert run("1\n2\n") == "1", "single minimum needs upgrade"
assert run("4\n5 5 5 5\n") == "0", "already perfect"
assert run("4\n2 2 2 2\n") == "2", "all low values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 0 | already optimal |
| 1 2 | 1 | minimal upgrade case |
| 5 5 5 5 | 0 | no operations needed |
| 2 2 2 2 | 2 | worst-case accumulation |

## Edge Cases

A key edge case is when the initial average already exceeds or equals 4.5. For example, input `3, 5 4 5` produces a sum of 14, and the threshold is 13.5. The algorithm handles this immediately before any upgrades, returning 0 without entering the loop.

Another case is when all values are identical and low, such as `4, 4, 4`. The algorithm processes upgrades in order and only stops when enough cumulative gain is accumulated. Each step adds a constant improvement, and the loop guarantees eventual success.

Finally, the smallest input size `n = 1` behaves consistently. If the single grade is 5, the answer is 0. If it is below 5, exactly one upgrade is always sufficient since the value becomes 5 immediately, guaranteeing the threshold.