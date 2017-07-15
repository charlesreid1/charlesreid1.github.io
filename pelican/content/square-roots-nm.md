Title: Computing Square Roots: Part 1: Using Newton's Method
Date: 2017-07-14 20:00
Category: Numerics
Tags: computer science, java, mathematics, square roots, numerical methods, newtons method

Table of Contents:
* Newton's method basics
* Newton's method for square roots
* Iterative technique to find square roots
* Speed and timing



## Newton's Method for Finding Roots of Equations

Suppose we have a function $f(x)$ and we want to 
compute values of $x$ for which $f(x)=0$. These values 
of $x$ are called the **roots** of $f(x)$.

We can compute the roots using Newton's Method,
which utilizes the derivative of the function
to iteratively compute the roots of the function.

Newton's method begins with an initial guess.
It evaluates the derivative of the fnction at the 
initial guess, which gives the slope of the tangent line,
and computes the root of the tangent line as the next
approximation of the root of the function.

This is based on the point-slope formula,

$$
y - y_0 = m(x - x_0) 
$$ 

Now the left side becomes 

$$
f(x) - f(x_0) = f'(x_0)(x - x_0)
$$

and at the root, we know $f(x)=0$, so rearranging this equation
into an expression for the root $x$ gives: 

$$
x = x_0 - \dfrac{f(x_0)}{f'(x_0)}
$$

Now, this is the equation for the next approximation for the root.
To turn this into an iterative procedure, we write this as

$$
x_{i+1} = x_{i} - \dfrac{f(x_i)}{f'(x_i)}
$$

Newton's Method then allows us to evaluate the 
above expression as many times as we would like
to achive the desired accuracy. 

Two caveats with Newton's Method: 

* The function must be relatively well-behaved; 
	Newton's Method does not converge for functions with
	large, high-order derivatives.
* The convergence of the method depends on the accuracy 
	of the initial guess. If you can make a good guess, do it!

## Newton's Method for Finding Square Roots

Note that we can use the procedure and equation from above
to compute the numerical value of a given function to an arbitrary
degree of accuracy, so long as we have the derivative (and a program 
that can keep track of arbitrary digits).

Suppose we want to use Newton's Method to compute $\sqrt{2}$.
Then we can solve for the roots of the following function:

$$
f(x) = x^2 - a
$$

for $a = 2$.

Note that the derivative of this function is computed using the power rule,
which is trivial to implement, so we can also use this method to compute
general $n^{th}$ roots of $a$, by solving for roots of:

$$
f(x) = x^n - a
$$

For a monomial with nonzero power, the derivative is always l$f'(x) = n x^{n-1}$, 
so in the square root case we have $f'(x) = 2x$. Now we plug these two functions
into the iterative formula for Newton's Method to get:

$$
\begin{array}
a x_{i+1} &=& x_{i} - \dfrac{f(x_n)}{f'(x_n)} \\
x_{i+1} &=& x_{i} - \dfrac{x_i^2 - a}{2 x_i }
\end{array}
$$

This can be implemented in a programming language to yield an iterative
method for computing square roots.













