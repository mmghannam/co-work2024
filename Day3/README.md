# Day3: Branch-and-Price Tutorial

## Prerequisites and nice-to-have's
- PySCIPOpt. In order to install PySCIPOpt, simply use `pip install pyscipopt` in your terminal. See the [documentation](https://pyscipopt.readthedocs.io/en/latest/install.html) if in need of more information.
- Some familiarity with Branch-and-Price/column generation. While not strictly necessary, it will allow you to focus on the implementation itself. [Marco Lubbecke's online tutorial](https://www.youtube.com/watch?v=vx2LNKx48vY) can be helpful.

## Useful links
- [Documentation](https://pyscipopt.readthedocs.io/en/latest/install.html)
- [Old Documentation](https://scipopt.github.io/PySCIPOpt/docs/html/classpyscipopt_1_1scip_1_1Model.html) (we are in the process of migrating the documentation)
- [PySCIPOpt repository](https://github.com/scipopt/PySCIPOpt)


## Introduction
In this tutorial, we will present how to implement a branch-and-price algorithm in PySCIPOpt. We will use the well-known [bin packing problem](https://www.wikiwand.com/en/articles/Bin_packing_problem) as an example. Bin packing is a combinatorial optimization problem where a finite number of items of different sizes must be packed into bins or containers each with a fixed capacity. The goal is to minimize the number of bins used. The problem is NP-hard and has many applications in logistics and resource allocation.

The first two chapters will give a light overview of bin packing, both its compact and extended formulations. Implementation exercises start in Chapter 3.

If you try to run the branch-and-price code, you will encounter errors. That is because some code is missing and must be implemented by you. The error messages tell you what you should do. Eg: "The knapsack solver is not implemented yet" implies that you should implement the knapsack solver.


## 1. Compact Formulation
We first present the so-called "compact" formulation of the bin packing problem.
> The compactness comes from the fact the number of variables and constraints is polynomial in the number of items.

In this formulation, we have $x_{ij}$ variables that are equal to 1 if item i is packed into bin j and 0 otherwise. We also have a set of constraints that ensure that each item is packed into exactly one bin and that the total size of the items in each bin does not exceed the bin capacity. Additionally, we have a set of variables used to compute the objective value, $y_j$ that are equal to 1 if bin j is used and 0 otherwise. The objective is to minimize the number of bins used. For simplicity, we will assume that the bins have identical capacities.

The compact formulation is as follows:

$$
\begin{align*}
\text{minimize} & \quad \sum_{j=1}^{n} y_j \\
\text{subject to} & \quad \sum_{j=1}^{n} x_{ij} = 1, \quad \forall i \in \lbrace1, \ldots, m\rbrace \\
& \quad \sum_{i=1}^{m} s_i x_{ij} \leq C, \quad \forall j \in \lbrace1, \ldots, n\rbrace \\
& \quad x_{ij} \in \lbrace0, 1\rbrace, \quad \forall i \in \lbrace1, \ldots, m\rbrace, j \in \lbrace1, \ldots, n\rbrace \\
& \quad y_j \in \lbrace0, 1\rbrace, \quad \forall j \in \lbrace1, \ldots, n\rbrace
\end{align*}
$$

An implementation of this is provided in [scipack/compact.py](scipack/compact.py).

## 2. Extended Formulation: Modeling with Packings
Next, we switch our perspective to the so-called "extended" formulation of the bin packing problem. Instead of modeling with assignments of items to bins we "extend" all possible packings of items into bins. A packing is simply a subset of items that be packed into a bin (respecting its capacity). Using this concept of packings we arrive at an equivalent formulation:

Given a set of items $I$ and a set of packings $\mathcal{P}$, we have a variable $z_P$ that is equal to 1 if packing $P$ is used and 0 otherwise. We have a set of constraints that ensure that each item is packed into exactly one bin and that the total size of the items in each bin does not exceed the bin capacity. The objective is to minimize the number of bins used.

$$
\begin{align*}
\text{minimize} & \quad \sum_{p \in \mathcal{P}} z_p \\
\text{subject to} & \quad \sum_{p \in \mathcal{P}} a_i^{p} z_p = 1, \quad \forall i \in I \\
& \quad z_p \in \lbrace0, 1\rbrace, \quad \forall p \in \mathcal{P}
\end{align*}
$$

where $\mathcal{P}$ is the set of all possible packings of items into bins.

This formulation has one problem. The size of the problem grows exponentially with the number of items. Only instances with a small number of items can be even loaded in memory. Therefore, we attempt to solve it using a branch-and-price algorithm. This formulation and the general structure required for solving this problem can be found in [scipack/bnp.py](scipack/bnp.py) (but again, it's missing some code snippets you must add).

## 3. Branch-and-Price Algorithm
In this section, we will first discuss how to solve the linear relaxation of the problem using column generation. Then, we will discuss how to handle branching decisions and infeasibility.

### 3.1 Column Generation

Thinking of the exponential number of possible packings, one realizes that most of them are actually not that useful. For example, if packing 1 corresponds to using item A, and packing 2 to using items A and B, why would we ever choose packing 1? Most of the packings are inefficient like this, hinting that only a handful of columns are actually useful. Column generation (which is heavily linked to the simplex algorithm) will find these columns.

Column generation iteratively solves two problems. A Restricted Master Problem (RMP), which is the extended formulation restricted to a very small set of columns, and a pricing problem that generates new columns to add to the RMP. How can it tell which columns to generate? By using the RMP's dual information.

The generic algorithm goes like this:

1. Use a small fixed set of columns to solve the problem
2. Get dual information to find out which type of columns would be beneficial
3. Solve a pricing problem to produce the best column with these characteristics
4. If the reduced cost of this column is negative, add to the columns in 1. and repeat. Otherwise, optimality is achieved.

> Column generation is a method for solving linear programs. Branch and Price is using a Branch and Bound where the linear relaxation of each node is solved with column generation.

The column that should be added to the RMP is the one with the most negative reduced cost, as it is the one that locally improves the solution the most (recall that we are solving an LP). We also need to ensure that the resulting column satisfies the constraints of the compact formulation - it should not exceed the bin capacity. So the column-generating problem should be something like:

$$
\begin{align*}
\text{minimize} & \quad 1 - \sum_{i \in I} a_i\pi_i \\
\text{subject to} & \quad \sum_{i \in I} a_i \leq C \\
& \quad a_i \in \lbrace0, 1\rbrace, \quad \forall i \in I,
\end{align*}
$$

where $a_i$ is a variable indicating if item $i$ belongs to the packing we are constructing. If we massage the objective function a little, we see that

$\text{minimize} \hspace{0.5em} 1 - \displaystyle\sum_{i \in I} a_i\pi_i = 1 + \text{minimize} - \displaystyle\sum_{i \in I} a_i\pi_i = 1 - \text{maximize} \displaystyle\sum_{i \in I} a_i\pi_i$

 This objective function, allied to the constraint, is precisely a knapsack problem. This is very helpful, as it is crucial in column generation to have the ability to quickly generate columns, and knapsack is one of the most well-studied problems in Operations Research, for which there are incredibly efficient algorithms.

 When the objective of the pricing problem is $\geq 0$, this means that the most beneficial packing is not good enough to justify using another bin. And it is at this point that we know we have reached the optimal solution (for the LP).

To reduce the complexity of the code each of the following exercises is accompanied by a test.
Running the test validates the correctness of the code of this particular exercise.

#### Exercise 1: Pricing

**Your task:** Implement the knapsack pricing problem solver (by implementing a MIP) `solve_knapsack` in `knapsack.py`.
To check if your implementation is correct you can run the `test_knapsack.py` file.

SCIP can handle pricing internally with the `pricer` plugin. You can see the basic infrastructure in `pricer.py`. The pricer gets the dual information from the RMP (with `getDualsolLinear`), feeds it into the pricing problem (`pricing_solver`), and decides whether to add the resulting column or not (when checking `if min_redcost < 0`). For the curious, you can see more details in [here](https://www.scipopt.org/doc/html/PRICER.php).


### Branching

When dealing with compact formulations, solvers tend to have very efficient branching rules. This is sometimes not the case when doing branch-and-price, as the usual variable branching techniques can exhibit strong deficiencies. Suppose we decide to branch on variable $x$. In one of the branches, we add the constraint $x=0$, and in the other $x=1$. This leads to the following:

- $x=1$. We are forcing the resulting RMP to use this specific column, out of a gigantic number of them;
- $x=0$. We are forbidding the resulting RMP to use this specific column, out of a gigantic number of them.

In the first case, the RMP is heavily restricted, and in the second is almost not restricted at all. This translates into a very unbalanced tree, which makes the Branch and Bound process incredibly inefficient.

The standard way of branching in branch and price for bin packing is the [Ryan-Foster branching](https://www.scipopt.org/doc/html/BINPACKING_BRANCHING.php). The idea is, rather than focusing on a single item, focus on pairs of items. Thus, given two items $i$ and $j$ the two branches look like:

1. Apart: Item $i$ and item $j$ must not appear in the same bin
2. Together: Item $i$ and item $j$ must appear in the same bin

This also splits the problem in two but in a much more evenly way.

So how do we implement this? We first need to find a fractional pair of items.
Let's compute the value of implicit pair variables $x_{ij}$ for all pairs of items $i$ and $j$.
The value of $x_{ij}$ is the sum of the values of all packing variables $y_p$ that contain both items $i$ and $j$.
From this, we can find a fractional pair of items, i.e., a pair of items $i$ and $j$ such that $x_{ij}$ is fractional.

We then use this fractional pair to create the branching constraints. We create two child nodes, one where the two items in the fractional pair must be together (in the same bin) and one where they are apart (in different bins).

#### Exercise 2: Finding Fractional Pairs
**Your task:** Go to `ryan_foster.py` and fill in the missing implementation of the `all_fractional_pairs` function.
This function should return a list of all fractional pairs of items (see above for a definition of a fractional pair).
You can test your implementation by running the `test_fractional_pairs.py` file.

#### Exercise 3: Branching
**Your task:** Fill in the missing pieces in `ryan_foster.py` (marked with `?`) that save the branching decisions at the child nodes.

#### Exercise 4: Handling Branching Decisions in Pricing
**Your task:** Enforce the branching decisions in the pricing problem by implementing the `solve_knapsack_with_constraints` function in `knapsack.py`. You can start
by copying the `solve_knapsack` function and modifying it by adding the necessary constraints.
You can test your implementation by running the `test_knapsack_with_constraints.py` file.

The pricing problem does not have information regarding the branching decisions unless explicitly told. Using Ryan-Foster as an example, it might happen that the parent node decided that items $i_1, i_2$ must be kept apart, but the pricing problem does not know this and might generate a packing containing both items. To ensure proper branching, we need to force the prior branching decisions into the pricing problem.


### 3.2 Final step
Now that we have implemented the pricing problem, and the branching rule, and handled infeasibility, you have now successfully implemented a full branch-and-price algorithm. Congrats!
You can test your implementation by running the `test_bnp.py` file.

### 3.3 Improving the vanilla Branch-and-Price
There are many more tricks to make your Branch-and-Price code faster and more robust. The following is a collection of bonus exercises that ask you to implement some of these tricks. You may complete them in any order you'd like.

#### Bonus Exercise 1: Handling numerics
If you managed to implement everything correctly, try to run your code to solve an instance with many items. Let's say 200. You will most likely get into an infinite loop. 

Investigate why this happens (the name of the exercise should give you a hint) and fix it.

#### Bonus Exercise 2: Using integrality
As the objective function of the RMP always takes integer values, you can inform SCIP about it with the [setObjIntegral](https://scipopt.github.io/PySCIPOpt/docs/html/classpyscipopt_1_1scip_1_1Model.html#ae9f1c77d31148661be3e4261df738b39) method. In some instances, it might give you a performance improvement.  

#### Bonus Exercise 3: Initializing column generation
Column generation requires an initial set of columns in order to get started. The current implementation starts with the single item per bin solution.
Experiment with different ways of providing these columns for the bin packing problem.

#### Bonus Exercises 4: Multiple columns per iteration
The current implementation only adds one column per iteration. Implement adding multiple columns per iteration and report how it affects the performance.

#### Bonus Exercise 5: Speeding up pricing
Think of simple ways to speed up the pricing rounds and also reduce their invocations. Are there better algorithms for knapsack?

#### Bonus Exercise 6: Different-sized bins
What is needed to allow for bins of different sizes?

#### Bonus Exercise 7: Lagrangian bound
Read about the Lagrangian bound in the context of column generation and implement it in your pricer.
Hint: You can return your computed lower-bound in the pricer and SCIP will use it to prune the tree.
