---
title: "Chapter 2. Propositions and Proofs"
description: "This chapter introduces the proof layer of Lean."
---

This chapter introduces the proof layer of Lean. The central idea is that a proposition is a type, and a proof is a term of that type. This principle is often called propositions as types. It gives Lean a uniform foundation: definitions, programs, propositions, and proofs are all checked by the same kernel.

The chapter begins with implication, conjunction, disjunction, negation, truth, falsehood, equality, and quantifiers. These are the ordinary logical forms used in mathematics, but in Lean they also have exact introduction and elimination rules. To prove an implication, introduce its assumption. To prove a conjunction, prove both parts. To use a disjunction, split into cases. To prove an existential statement, provide a witness and a proof that the witness satisfies the property.

The practical goal is to make each logical connective feel mechanical. Once you know the shape of the goal, you know the first move. Once you know the shape of a hypothesis, you know how it can be used. This chapter develops that habit through small proof recipes.

A second theme is the relation between constructive and classical reasoning. Lean is constructive by default, so a proof of existence normally contains data. Classical principles such as excluded middle and proof by contradiction can be used explicitly when needed. The chapter shows where classical reasoning changes the proof shape and how to keep that dependency visible.

Equality receives special attention because it connects logic with computation. Some equalities are solved by reflexivity because both sides reduce to the same expression. Other equalities require rewriting, symmetry, transitivity, or intermediate lemmas. These simple equality patterns become the basis for later automation with `rw`, `simp`, and `calc`.

By the end of the chapter, you should be able to read a Lean goal as an instruction. A goal of the form `P -> Q` asks for `intro`. A goal of the form `P ∧ Q` asks for `constructor`. A hypothesis of the form `P ∨ Q` asks for `cases`. A hypothesis of the form `False` solves any goal. This correspondence between logical form and proof action is the main skill developed here.
