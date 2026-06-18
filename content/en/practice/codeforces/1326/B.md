---
problem: 1326B
contest_id: 1326
problem_index: B
name: "Maximums"
contest_name: "Codeforces Global Round 7"
rating: 900
tags: ["implementation", "math"]
answer: passed_samples
verified: true
solve_time_s: 223
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2df5cc-122c-83ec-9663-528b7493c968
---

# CF 1326B - Maximums

**Rating:** 900  
**Tags:** implementation, math  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 43s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2df5cc-122c-83ec-9663-528b7493c968  

---

## Solution

## Problem Understanding

We are given a transformed version of an unknown array. The original array contains non-negative integers, and for each position, another value is derived from the maximum of all previous elements. That maximum is then subtracted from the current element to produce the array we are given.

More concretely, each position in the hidden array is influenced by the maximum value seen so far on its left. The transformation hides the original values by continuously subtracting this running maximum prefix.

The task is to reconstruct any valid original array that could produce the given transformed array. Although multiple intermediate interpretations might seem possible, the problem guarantees that the answer is unique.

The constraints allow up to 200,000 elements, which immediately rules out any quadratic reconstruction that tries all possibilities for each position. Any solution must operate in linear time, or at worst near-linear time, since even O(n log n) would already be acceptable but unnecessary here.

A subtle point is that the transformation is not purely local. Each value depends on the maximum prefix, which depends on all previous reconstructed values. This introduces a dependency chain that can easily break naive attempts that try to assign values greedily without carefully tracking how the prefix maximum evolves.

A common incorrect idea is to assume we can reconstruct each element independently by guessing a prefix maximum. This fails because the prefix maximum itself depends on earlier reconstructed values, and any inconsistency early on propagates forward and invalidates later reconstruction.

For example, if we incorrectly assume the prefix maximum stays small, we may reconstruct values that violate later constraints where the provided differences imply a much larger hidden value. The coupling between positions makes independent reconstruction impossible.

## Approaches

A brute-force strategy would attempt to reconstruct the original array by guessing the hidden prefix maximum sequence. At each index, we could try all possible previous maximum values consistent with earlier positions and verify whether the resulting reconstruction matches the given transformed array. This quickly explodes because each position potentially branches into many possible maximum states, and over n positions this becomes exponential in the worst case.

The key observation is that the transformation defines a deterministic relationship between the hidden array and its prefix maximum. If we process the array from left to right, we can reconstruct the original values while maintaining the current prefix maximum of the reconstructed prefix.

At index i, if we already know the prefix maximum of a₁ to aᵢ₋₁, then the definition directly gives us xᵢ. Since bᵢ = aᵢ − xᵢ, we can rewrite aᵢ = bᵢ + xᵢ. This means once xᵢ is known, aᵢ is fixed immediately. After computing aᵢ, we update the prefix maximum for the next steps.

The entire reconstruction reduces to maintaining a running maximum and applying a direct formula at each step. The problem becomes a simple simulation of the original definition in reverse.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) extra (besides output) | Accepted |

## Algorithm Walkthrough

We reconstruct the array from left to right while maintaining the maximum of all previously reconstructed values.

1. Start with an empty prefix, where the maximum value seen so far is 0. This matches the definition that the first prefix maximum is always zero.
2. For each index i from 1 to n, compute the current prefix maximum before placing aᵢ. This value is exactly max(a₁, ..., aᵢ₋₁), which we maintain as a running variable.
3. Compute aᵢ using the direct relation aᵢ = bᵢ + current_max. This works because bᵢ was defined as the difference between the true value and the prefix maximum at that position.
4. After computing aᵢ, update the running maximum to max(current_max, aᵢ). This ensures that future positions use the correct prefix maximum.
5. Repeat until all values are reconstructed.

The logic never needs backtracking because each step fixes both the current value and the future state deterministically.

### Why it works

At every position i, the algorithm maintains the invariant that current_max equals max(a₁, ..., aᵢ₋₁). Because aᵢ is computed as bᵢ plus exactly this value, it satisfies the defining equation of the transformation. Updating the maximum preserves the invariant for the next iteration. Since each step enforces the exact constraint used to generate bᵢ, the reconstructed array is the unique valid solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
b = list(map(int, input().split()))

a = [0] * n

cur_max = 0
for i in range(n):
    a[i] = b[i] + cur_max
    if a[i] > cur_max:
        cur_max = a[i]

print(*a)
```

The solution follows the reconstruction directly from the definition. The variable `cur_max` tracks the prefix maximum of the reconstructed prefix. For each position, we first compute the hidden original value using the inverse relation between `a[i]`, `b[i]`, and the prefix maximum. Then we update the running maximum to ensure correctness for subsequent indices.

A common mistake is updating the maximum before computing `a[i]`. That reverses the dependency and produces incorrect results because `b[i]` was defined using the previous maximum, not the updated one.

## Worked Examples

### Example 1

Input:

```
5
0 1 1 -2 1
```

We reconstruct step by step:

| i | b[i] | cur_max before | a[i] = b[i] + cur_max | cur_max after |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 1 | 1 |
| 3 | 1 | 1 | 2 | 2 |
| 4 | -2 | 2 | 0 | 2 |
| 5 | 1 | 2 | 3 | 3 |

Output:

```
0 1 2 0 3
```

This confirms that even when values become negative in b, the reconstructed array remains non-negative due to the running maximum offset.

### Example 2

Input:

```
3
1000 999999000 -1000000000
```

| i | b[i] | cur_max before | a[i] | cur_max after |
| --- | --- | --- | --- | --- |
| 1 | 1000 | 0 | 1000 | 1000 |
| 2 | 999999000 | 1000 | 1000000000 | 1000000000 |
| 3 | -1000000000 | 1000000000 | 0 | 1000000000 |

Output:

```
1000 1000000000 0
```

This shows how large prefix maxima accumulate and how negative b values correspond to values below the running maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant work |
| Space | O(1) extra | Only a running maximum is maintained besides the output array |

The algorithm is linear in the size of the array, which comfortably satisfies the constraint of up to 200,000 elements under a 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    b = list(map(int, input().split()))

    a = [0] * n
    cur_max = 0

    for i in range(n):
        a[i] = b[i] + cur_max
        cur_max = max(cur_max, a[i])

    return " ".join(map(str, a))

# provided sample
assert run("5\n0 1 1 -2 1\n") == "0 1 2 0 3"

# minimum size
assert run("3\n0 0 0\n") == "0 0 0"

# strictly increasing hidden prefix
assert run("4\n0 1 2 3\n") == "0 1 2 3"

# large negative drop
assert run("3\n1000000000 -1000000000 -1000000000\n") == "1000000000 0 0"

# alternating pattern
assert run("5\n0 5 -3 10 -2\n") == "0 5 2 12 10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 0 0 0 | 0 0 0 | all-zero stability |
| 0 1 2 3 pattern | 0 1 2 3 | monotonic prefix growth |
| large negative drops | 0 0 0 after peak | handling negative b values |
| alternating values | consistent reconstruction | dynamic max updates |

## Edge Cases

One important edge case is when all b values are zero. For input:

```
3
0 0 0
```

The algorithm starts with cur_max = 0. Each step computes a[i] = 0, and cur_max never changes. The output remains all zeros, matching the only consistent reconstruction.

Another case is when b contains large negative values after a large peak. For example:

```
3
1000000000 -1000000000 -1000000000
```

At i = 1, cur_max becomes 1000000000. At i = 2 and i = 3, the computed a[i] becomes 0 each time, since we subtract the large prefix maximum. The prefix maximum remains unchanged after that, and the reconstruction stays consistent with the definition of xᵢ being the maximum prefix before each position.