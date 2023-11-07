# Accelerating Program Analyzers by Unleashing of Power of Compiler Optimizations

`rainoftime@gmail.com`

## Problem statement

Given an input LLVM bitcode (the program) I and a static analyzer P,
we aim to generate a compiler optimization strategy F that can transform I to a new bitcode $I'$,
such that P runs faster on I'.



## Black-box optimization

Currently, we only use runtime as feedback and have implemented two modes:

- (parallel) random search
- genetic algorithm-based search

NOTE: The example code uses LLVM 3.6 (and only a subset of the options)

## Other approaches (TODO)

There are may problems to address

- Features + ML?
- Deep learning