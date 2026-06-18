---
problem: 946B
contest_id: 946
problem_index: B
name: "Weird Subtraction Process"
contest_name: "Educational Codeforces Round 39 (Rated for Div. 2)"
rating: 1100
tags: ["math", "number theory"]
answer: passed_samples
verified: true
solve_time_s: 63
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a327b46-911c-83ec-af62-8431b2a8c956
---

# CF 946B - Weird Subtraction Process

**Rating:** 1100  
**Tags:** math, number theory  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 3s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a327b46-911c-83ec-af62-8431b2a8c956  

---

## Solution

## Problem Understanding

We are given two positive integers representing the sizes of two piles. A deterministic process repeatedly modifies these two values using a very specific rule: if one value is at least twice the other, we subtract twice the smaller value from the larger one. The process stops only when neither value is at least twice the other, or when one of them becomes zero.

The task is not to simulate a fixed number of steps, but to determine the final stable pair after all possible reductions have been applied.

The constraints allow values up to $10^{18}$, which immediately rules out step-by-step simulation. A single subtraction step might be cheap, but in worst cases the number of iterations is proportional to the magnitude of the numbers. For example, starting from $(10^{18}, 1)$, a naive simulation would require about $5 \cdot 10^{17}$ operations, which is far beyond any feasible time limit.

The key difficulty is that the process is not symmetric subtraction; it only triggers when one value is at least double the other. This condition creates long runs where one side shrinks rapidly in chunks, but also cases where roles alternate. A careless simulation often fails because it assumes only one side dominates or forgets that after reducing one variable, the condition may immediately flip and enable the opposite operation.

A typical edge case is when values alternate between triggering reductions:

Input:

```
12 5
```

Correct output:

```
0 1
```

A naive approach might subtract only once per check and miss repeated chained reductions that happen immediately after state changes.

## Approaches

A brute-force simulation directly follows the rules: repeatedly check whether $a \ge 2b$ or $b \ge 2a$, and perform subtraction accordingly. This is correct because each operation exactly mirrors the problem statement. However, each step strictly reduces at least one variable, and in worst cases only by a small amount relative to its size. If one number is much larger than the other, say $a = 10^{18}$ and $b = 1$, then each valid step reduces $a$ by 2, leading to roughly $5 \cdot 10^{17}$ iterations.

The key observation is that repeated subtraction of the same form behaves like Euclid’s algorithm with a twist: instead of subtracting one copy of the smaller value, we subtract it in chunks of size $2b$. This means we can replace many repeated steps with a single integer division step. If $a \ge 2b$, we want to apply the operation as many times as possible in one shot:

$$a \leftarrow a \bmod (2b)$$

because each operation reduces $a$ by exactly $2b$, and we continue until the condition no longer holds.

The same idea applies symmetrically for $b$. This turns the process into a logarithmic reduction similar to the Euclidean algorithm, since at each phase at least one variable shrinks dramatically.

The subtlety is that after each bulk reduction, we must re-evaluate both conditions because control can switch between $a$ and $b$ multiple times before termination.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(a,b)) | O(1) | Too slow |
| Optimal | O(log max(a,b)) | O(1) | Accepted |

## Algorithm Walkthrough

We repeatedly apply the largest possible valid reduction until neither side can trigger an operation.

1. Check whether both values are positive. If either becomes zero, the process ends immediately because no rule can apply.
2. If $a \ge 2b$, replace $a$ with $a \bmod (2b)$. This compresses all repeated subtractions into a single step because each operation removes exactly $2b$.
3. After updating $a$, immediately re-check conditions, since reducing $a$ may allow $b \ge 2a$ to become true.
4. If $b \ge 2a$, replace $b$ with $b \bmod (2a)$, for the same reason as above.
5. Repeat until neither condition holds.

The reason this ordering works is that each modulo operation preserves the effect of repeated valid subtractions without skipping any intermediate state that could change which side dominates.

### Why it works

The process always maintains the invariant that the larger value decreases strictly while the smaller value remains unchanged during that phase. Each bulk reduction simulates a maximal sequence of identical legal moves. Since each modulo step reduces at least one number to strictly less than twice the other, the system eventually reaches a state where neither condition can hold, matching the termination condition of the original process.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    
    while True:
        if a == 0 or b == 0:
            break
        
        if a >= 2 * b:
            a %= 2 * b
            continue
        
        if b >= 2 * a:
            b %= 2 * a
            continue
        
        break
    
    print(a, b)

if __name__ == "__main__":
    solve()
```

The solution directly encodes the process as a loop with two symmetric bulk-reduction rules. The key implementation choice is using modulo instead of repeated subtraction, which ensures each phase runs in constant time. The `continue` statements ensure that after each reduction, the algorithm immediately re-evaluates both directions, since the dominance relationship may change after a single update.

Care must be taken with ordering: checking the `a` condition first and then the `b` condition matches the process structure and avoids skipping a newly enabled transition.

## Worked Examples

### Example 1

Input:

```
12 5
```

| Step | a | b | Action |
| --- | --- | --- | --- |
| 1 | 12 | 5 | a >= 2b → a = 12 % 10 = 2 |
| 2 | 2 | 5 | b >= 2a → b = 5 % 4 = 1 |
| 3 | 2 | 1 | a >= 2b → a = 2 % 2 = 0 |
| 4 | 0 | 1 | stop |

Output:

```
0 1
```

This trace shows how the process alternates between reducing $a$ and $b$, and how modulo operations capture multiple chained subtractions in a single step.

### Example 2

Input:

```
31 12
```

| Step | a | b | Action |
| --- | --- | --- | --- |
| 1 | 31 | 12 | a >= 2b → a = 31 % 24 = 7 |
| 2 | 7 | 12 | b >= 2a → b = 12 % 14 = 12 |
| 3 | 7 | 12 | no condition holds → stop |

Output:

```
7 12
```

This demonstrates that the process may terminate without one value becoming zero, when neither side dominates by a factor of two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log max(a, b)) | Each modulo step reduces one value significantly, similar to Euclid’s algorithm |
| Space | O(1) | Only two integers are stored |

The logarithmic behavior ensures the solution easily fits within limits even for values up to $10^{18}$, since the number of reductions is proportional to the number of times the magnitude can be halved.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("12 5\n") == "0 1"

# minimum case
assert run("1 1\n") == "1 1"

# one side dominant
assert run("1000000000000000000 1\n") in ["0 1", "1 0"]

# equal powers of two pattern
assert run("8 2\n") == "0 2"

# alternating reduction
assert run("31 12\n") == "7 12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 1 | immediate termination |
| 10^18 1 | (0,1) or (1,0) | extreme dominance |
| 8 2 | 0 2 | repeated a-side reduction |
| 31 12 | 7 12 | alternating reductions |

## Edge Cases

One edge case is when the values are already in a stable configuration where neither is at least double the other. For example, input:

```
7 12
```

The algorithm first checks $a \ge 2b$, which is false. Then it checks $b \ge 2a$, which is also false. The loop terminates immediately and outputs $7 12$, matching the correct behavior because no rule can be applied.

Another edge case occurs when repeated reductions reduce a value exactly to zero. For instance:

```
2 1
```

Here, $a \ge 2b$ holds, so $a = 2 \bmod 2 = 0$. The process then stops immediately since one value is zero, producing output:

```
0 1
```

This confirms that modulo-based reduction correctly handles exact divisibility without requiring special casing.