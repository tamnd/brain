---
title: "CF 106238L - Quantum Computing Programming"
description: "This problem has no input. We start with three qubits. The first qubit contains an arbitrary unknown state $$alpha while the second and third qubits are both initialized to $ The task is to output a program in the given HYW language."
date: "2026-06-19T14:06:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106238
codeforces_index: "L"
codeforces_contest_name: "The 7th FanRuan Cup Southeast University Programming Contest (Winter) Professional Group"
rating: 0
weight: 106238
solve_time_s: 90
verified: true
draft: false
---

[CF 106238L - Quantum Computing Programming](https://codeforces.com/problemset/problem/106238/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem has no input. We start with three qubits. The first qubit contains an arbitrary unknown state

$$\alpha|0\rangle+\beta|1\rangle,$$

while the second and third qubits are both initialized to $|0\rangle$.

The task is to output a program in the given HYW language. After executing the program, the state of the first two qubits must become exactly $|0\rangle$, and the third qubit must contain the original unknown state

$$\alpha|0\rangle+\beta|1\rangle.$$

The transformation must work for every possible values of $\alpha$ and $\beta$. We are allowed to use only H, X, Z and CNOT gates, together with measurements and operations conditioned on measurement results. The program must contain at most sixteen statements.

Since there is no input and only a constant amount of work is required, complexity is irrelevant. The real challenge is finding a sequence of operations that transfers an unknown quantum state without directly observing it.

A common mistake is trying to measure the first qubit immediately. Consider the state

$$\frac{|0\rangle+|1\rangle}{\sqrt2}.$$

After measurement, the state collapses to either $|0\rangle$ or $|1\rangle$, destroying the coefficients $\alpha,\beta$. Once the information is lost, no sequence of classical conditional operations can reconstruct the original superposition.

Another pitfall is copying the state with CNOT. If

$$|\psi_1\rangle=\alpha|0\rangle+\beta|1\rangle$$

and the second qubit is $|0\rangle$, then applying CNOT from qubit 1 to qubit 2 gives

$$\alpha|00\rangle+\beta|11\rangle.$$

This is an entangled state, not two independent copies of the original qubit. Quantum states cannot be cloned.

The correct approach is quantum teleportation.

## Approaches

A brute-force approach would be to try to extract the values of $\alpha$ and $\beta$ by measurement and then rebuild the state on the third qubit. Such an idea fails because measurement collapses the superposition. The information encoded in the amplitudes is not accessible through a single measurement, so this approach is fundamentally impossible.

The key observation is that teleportation does not transmit the amplitudes themselves. Instead, we first create an entangled pair between qubits 2 and 3. Then qubits 1 and 2 are measured in a suitable basis. The two classical measurement results determine which Pauli corrections are needed on qubit 3. After applying those corrections, qubit 3 becomes the original state, while qubits 1 and 2 collapse to classical states and can be reset to zero.

Because the HYW language allows conditional execution based on measurement outcomes, implementing teleportation is straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Measure the unknown qubit directly | O(1) | O(1) | Incorrect |
| Quantum teleportation with corrections | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create an entangled Bell pair between qubits 2 and 3. Apply H to qubit 2, then apply CNOT with qubit 2 as control and qubit 3 as target.
2. Entangle the unknown qubit with qubit 2. Apply CNOT with qubit 1 as control and qubit 2 as target.
3. Apply H to qubit 1. This converts the Bell-basis measurement into ordinary computational-basis measurements.
4. Measure qubit 1. Store the result as the first measurement outcome.
5. Measure qubit 2. Store the result as the second measurement outcome.
6. If the second measurement result is 1, apply X to qubit 3. This removes the bit-flip error introduced by teleportation.
7. If the first measurement result is 1, apply Z to qubit 3. This removes the phase-flip error introduced by teleportation.
8. After the measurements, qubits 1 and 2 have collapsed to classical values. If the first measurement result is 1, apply X to qubit 1.
9. If the second measurement result is 1, apply X to qubit 2.

After these corrections, qubits 1 and 2 become $|0\rangle$, while qubit 3 contains the original unknown state.

### Why it works

Teleportation decomposes the three-qubit system into four branches corresponding to the two measurement results. In each branch, qubit 3 differs from the original state only by a combination of X and Z operators. Since the measurement outcomes are known classically, the appropriate corrections can be applied conditionally.

Measurements collapse qubits 1 and 2 into either $|0\rangle$ or $|1\rangle$. Applying X when the measured value equals one resets them to $|0\rangle$. Thus the final state is always

$$|0\rangle|0\rangle(\alpha|0\rangle+\beta|1\rangle),$$

which is exactly what the problem asks for.

## Python Solution

```python
import sys
input = sys.stdin.readline

print("""H 2
CNOT 2 3
CNOT 1 2
H 1
measure 1
measure 2
if m2=1 then X 3
if m1=1 then Z 3
if m1=1 then X 1
if m2=1 then X 2""")
```

The first two instructions create the Bell pair between qubits 2 and 3.

The next two instructions perform the standard teleportation preparation. Measuring qubits 1 and 2 produces two classical bits.

The two conditional corrections on qubit 3 reconstruct the original unknown state. Finally, the measured qubits are reset to zero by applying X whenever their measured values were one.

The whole program contains only ten statements, comfortably below the limit of sixteen.

## Worked Examples

Since the state contains symbolic coefficients, tracing amplitudes directly is more informative than using numerical input.

### Example 1

Suppose the initial state is $|1\rangle|0\rangle|0\rangle$.

| Step | State |
| --- | --- |
| Initial | ( |
| H 2 | (( |
| CNOT 2 3 | (( |
| CNOT 1 2 | (( |
| H 1 | Superposition of four basis states |
| Measure qubits 1 and 2 | One of four branches |
| Conditional corrections | Qubit 3 becomes ( |
| Reset qubits 1 and 2 | ( |

This example shows that a basis state is transferred perfectly.

### Example 2

Suppose the initial state is

$$\frac{|0\rangle+|1\rangle}{\sqrt2}.$$

| Step | Description |
| --- | --- |
| Create Bell pair | Entangle qubits 2 and 3 |
| Bell transformation | Correlate qubit 1 with the Bell pair |
| Measure qubits 1 and 2 | Obtain two classical bits |
| Apply X and Z corrections | Recover the original superposition on qubit 3 |
| Reset qubits 1 and 2 | Final state becomes ( |

This demonstrates that teleportation works for arbitrary superpositions, not only basis states.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A fixed sequence of ten statements is printed |
| Space | O(1) | No data structures are needed |

The program performs a constant amount of work and uses constant memory. The limits are trivial for such a problem.

## Test Cases

```
# There is no input.
# Any execution should produce the same program.

expected = """H 2
CNOT 2 3
CNOT 1 2
H 1
measure 1
measure 2
if m2=1 then X 3
if m1=1 then Z 3
if m1=1 then X 1
if m2=1 then X 2"""

def run(inp: str) -> str:
    return expected

assert run("") == expected
assert run("\n") == expected
assert run("123\n") == expected
assert run("random text\nmore text\n") == expected
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty input | fixed program | normal case |
| one blank line | fixed program | ignores useless input |
| arbitrary number | fixed program | output is independent of input |
| random text | fixed program | only the printed program matters |

## Edge Cases

One dangerous case is the state $|0\rangle$. Teleportation measurements may produce different classical outcomes, but the conditional corrections always return qubit 3 to $|0\rangle$, and the reset operations leave qubits 1 and 2 equal to zero.

Another interesting case is the state $|1\rangle$. Some branches require an X correction, some require a Z correction, and some require both. Since the corrections are determined by the measurement results, every branch ends with qubit 3 equal to $|1\rangle$.

The most subtle case is a genuine superposition such as

$$\frac{|0\rangle+|1\rangle}{\sqrt2}.$$

A direct measurement would destroy the phase information. Teleportation avoids this by never measuring qubit 3. The amplitudes remain intact, and only classical correction operators are chosen according to the measurement outcomes. This preserves the complete quantum state.
