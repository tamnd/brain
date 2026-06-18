---
problem: 1352C
contest_id: 1352
problem_index: C
name: "K-th Not Divisible by n"
contest_name: "Codeforces Round 640 (Div. 4)"
rating: 1200
tags: ["binary search", "math"]
answer: passed_samples
verified: true
solve_time_s: 157
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e2bb2-e3e0-83ec-8dea-7fd34d7f3a5f
---

# CF 1352C - K-th Not Divisible by n

**Rating:** 1200  
**Tags:** binary search, math  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 37s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e2bb2-e3e0-83ec-8dea-7fd34d7f3a5f  

---

## Solution

## Problem Understanding

We are looking at a filtered sequence of positive integers where every multiple of a fixed number is removed. Instead of working with the full list of natural numbers, imagine marking all numbers that are divisible by `n` as forbidden, then compressing what remains into a clean sequence. The task is to determine which number appears in position `k` of this compressed sequence.

The key difficulty is that the filtered sequence is not given explicitly. For large values, the sequence is extremely long, so we need a way to jump directly to the answer without enumerating elements one by one.

The constraints make a naive simulation infeasible. Since both `n` and `k` can be up to one billion and there can be up to 1000 test cases, any method that iterates through integers and checks divisibility would require up to 10^9 operations per test case in the worst case. That is far beyond what can run in one second.

A subtle edge case appears when `n` is small. For example, if `n = 2` and `k = 1`, the answer is `1`, but if one mistakenly counts indices incorrectly and starts from zero or includes multiples of `n`, off-by-one shifts quickly propagate. Another edge case is when `n` is very large, such as `n = 10^9`. In this case, almost every number is valid except one every billion steps, so the answer is extremely close to `k`, and naive filtering would waste almost all work on numbers that should not be removed.

## Approaches

A brute-force approach would iterate through positive integers, maintain a counter of how many numbers are not divisible by `n`, and stop when reaching the `k`-th valid number. This is straightforward and correct because it directly simulates the definition of the sequence. However, its cost depends on how many numbers we scan. In the worst case, if `n = 2`, only half the numbers are valid, so we may need to check roughly `2k` numbers per test case. With `k` up to 10^9, this becomes completely impossible.

The key observation is to stop thinking about the sequence incrementally and instead reason in blocks. In every block of `n` consecutive integers, exactly `n - 1` of them are valid because only one number in each block is divisible by `n`. This transforms the problem into counting full blocks and then handling a remainder inside a partial block.

Once this structure is recognized, we can compute how many full blocks of size `n` are needed to reach the `k`-th valid number, and then adjust for the missing multiples that were skipped.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per test | O(1) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many complete groups of `n` numbers are needed to cover `k` valid numbers. Each group contributes `n - 1` valid numbers, so we divide `k` by `n - 1`. This tells us how many full blocks we can fit before reaching the target position.
2. Compute the remainder of valid numbers needed after these full blocks. This remainder determines how far into the next block the answer lies.
3. Convert the block count into an actual number position by multiplying the number of full blocks by `n`. This gives a baseline position in the original integer line that accounts for skipped multiples.
4. If the remainder is non-zero, we move forward by that remainder to land on the correct valid number. If the remainder is zero, we are exactly at the boundary and must step back by one to avoid landing on a multiple of `n`.

### Why it works

The core invariant is that every consecutive segment of `n` integers contains exactly `n - 1` valid numbers, and exactly one excluded number at a fixed offset (multiples of `n`). By grouping the number line into equal-sized blocks, we transform a scattered removal process into a periodic pattern. This periodicity guarantees that counting valid numbers globally is equivalent to counting full blocks plus a local adjustment inside a single block, so no information is lost when compressing the sequence into block arithmetic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())

        # number of full blocks of size (n-1) valid numbers
        blocks = (k - 1) // (n - 1)

        # position after accounting for removed multiples
        ans = blocks * n + (k - blocks * (n - 1))

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the block reasoning. The expression `(k - 1) // (n - 1)` computes how many complete `(n - 1)`-sized groups of valid numbers fit before reaching `k`. Multiplying by `n` shifts those groups back into the original number line, reinserting the skipped multiples.

The final adjustment adds the remaining offset within the current block. The subtraction of 1 in the block computation is crucial to avoid off-by-one errors when `k` is exactly divisible by `n - 1`, where the answer should land just before a multiple of `n`, not on it.

## Worked Examples

We trace two cases to see how block structure replaces explicit enumeration.

First example: `n = 3, k = 7`.

| Step | blocks | remainder logic | result |
| --- | --- | --- | --- |
| compute blocks | 3 | (7-1)//2 = 3 | 3 full blocks |
| base position | 3 | 3 * 3 = 9 | starting point |
| remainder | 1 | 7 - 6 = 1 | move 1 step |
| final answer | - | - | 10 |

This shows that after accounting for three full blocks of size 3 (each contributing 2 valid numbers), we land near 9 and then adjust inside the next block.

Second example: `n = 4, k = 12`.

| Step | blocks | remainder logic | result |
| --- | --- | --- | --- |
| compute blocks | 4 | (12-1)//3 = 3 | 3 full blocks |
| base position | 3 | 3 * 4 = 12 | starting point |
| remainder | 3 | 12 - 9 = 3 | move 3 steps |
| final answer | - | - | 15 |

This confirms that full blocks contribute structure, while the remainder handles local positioning inside a block.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each query uses a constant number of arithmetic operations |
| Space | O(1) | No additional data structures are used |

The solution easily fits within limits because even 1000 test cases require only simple integer arithmetic, with no iteration over large ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        blocks = (k - 1) // (n - 1)
        ans = blocks * n + (k - blocks * (n - 1))
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("6\n3 7\n4 12\n2 1000000000\n7 97\n1000000000 1000000000\n2 1\n") == \
"10\n15\n1999999999\n113\n1000000001\n1"

# custom cases
assert run("1\n3 1\n") == "1", "first valid number"
assert run("1\n3 2\n") == "2", "simple progression"
assert run("1\n3 3\n") == "4", "skip multiple"
assert run("1\n10 9\n") == "10", "boundary before multiple"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 | 1 | smallest non-multiple case |
| 3 3 | 4 | crossing a multiple boundary |
| 10 9 | 10 | edge just before excluded number |

## Edge Cases

When `k` is very small, such as `k = 1`, the formula still works because `(k - 1) // (n - 1)` becomes zero, placing the answer correctly at the first valid number, which is always `1`.

When `k` is exactly a multiple of `n - 1`, the computation lands precisely at the boundary of a block. In that situation, the multiplication by `n` ensures we skip the excluded multiples correctly, and the remainder adjustment avoids stepping onto a forbidden multiple.

When `n` is extremely large, the block size becomes so sparse that almost every number is valid. The formula degenerates cleanly into returning `k` or `k + 1` depending on alignment, matching the intuitive sequence structure without requiring special handling.