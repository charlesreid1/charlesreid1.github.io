Title: Computing Square Roots: Part 1: Using Newton's Method
Date: 2017-07-14 18:00
Category: Mathematics
Tags: computer science, java, mathematics, number theory, square roots, numerical methods, newtons method, irrational numbers

## Table of Contents

* [Newton's Method for Finding Roots of Equations](#newton-roots)

* [Newton's Method for Finding Square Roots](#newton-square-roots)

* [Newton's Method for Finding Square Roots: Program](#newton-program)

* [Accuracy](#newton-accuracy)

* [Speed](#newton-speed)

* [Next Steps](#newton-next)

* [References](#newton-refs)


<a name="newton-roots"></a>
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

<a name="newton-square-roots"></a>
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


<a name="newton-program"></a>
## Newton's Method for Finding Square Roots: Program

This can be implemented in a programming language to yield an iterative
method for computing square roots. We can either specify a tolerance (better),
or a number of iterations. Here is a static method for computing
a square root using Newton's method. The user specifies the value of $a$,
the number they want to compute the square root of; $x_0$, the initial guess;
and a tolerance, which controls the number of decimal places of accuracy of the 
final answer.

```java
	/** Compute a square root using Newton's Method, to a specified tolerance.
	 *
	 * @param a Compute the square root of a.
	 * @param x0 Initial guess.
	 * @param tol Tolerance (stopping criteria).
	 */
	public static double nmsqrttol(double a, double x0, double tol) { 
		double xi, xip1, err;
		xi = xip1 = x0;
		err = x0;
		while(err > tol) { 
			xip1 = xi - (xi*xi-a)/(2*xi);
			err = Math.abs( xip1 - xi );
			xi = xip1;
		}
		return xip1;
	}
```

(There is no check for infinite loops because our function is a smooth
polynomial and Newton's Method will always converge.) 

Here is sample output from a program that varies the tolerance and prints
the corresponding value of the square root that was computed:

```text
$ javac SquareRoot.java && java SquareRoot
Actual value sqrt(2) = 1.4142135623730951
Testing Newton's Method, Specifying Tolerance:
Tol			sqrt(2)
0.1			1.4166666666666667
0.01		1.4142156862745099
0.001		1.4142135623746899
0.0001		1.4142135623746899
1e-05		1.4142135623746899
1e-06		1.4142135623730951
1e-07		1.4142135623730951
1e-08		1.4142135623730951
```

<a name="newton-accuracy"></a>
## Accuracy

Now that we've coded up Newton's Method, we can determine the number of accurate 
digits. There are a couple of ways to do this, but I went with a string comparison 
method. I start with a text file containing thousands of digits of the square root of 2,
then I compute the square root of 2 using Newton's Method. The longest common substring
gives me the number of accurate digits, plus "1.", so if I subtract 2 I get the 
total number of accurate digits after the decimal place. 

```
javac SquareRoot.java && java SquareRoot
Tolerance = 0.1		Number of accurate digits = 2
Tolerance = 0.01		Number of accurate digits = 5
Tolerance = 0.001		Number of accurate digits = 11
Tolerance = 0.0001		Number of accurate digits = 11
Tolerance = 1e-05		Number of accurate digits = 11
Tolerance = 1e-06		Number of accurate digits = 15
Tolerance = 1e-07		Number of accurate digits = 15
Tolerance = 1e-08		Number of accurate digits = 15
Tolerance = 1e-09		Number of accurate digits = 15
Tolerance = 1e-10		Number of accurate digits = 15
Tolerance = 1e-11		Number of accurate digits = 15
Tolerance = 1e-12		Number of accurate digits = 15
Tolerance = 1e-13		Number of accurate digits = 15
Tolerance = 1e-14		Number of accurate digits = 15
```

<a name="newton-speed"></a>
## Speed

It is also important to measure performance, in the form of speed. How fast is 
Newton's Method relative to the built-in square root function in the math library?

Turns out the performance of Newton's Method is much worse than the built-in math library's 
square root function. The Newton's Method defined above is around 100 times slower. 
Here are the results of a simple timing test, in which we compute the square root
10 million times, timing how long it takes, and divide by the number of operations
to yield the time per operation (or rather, as it is slightly easier to grasp, 
the time per 1k operations);:

```
	/** Time Newton's Method.
	 *
	 * How long does it take to achieve 10 digits of accuracy? */
	public static void testTime() { 

		int Nops;
		double a;
		double initialGuess;
		double tol;
		double time;

		Tim tim;

		Nops = 10000000;
		a = 2;
		initialGuess = 1;
		tol = 1E-8;
		tim = new Tim();
		tim.tic();
		for(int i=0; i<Nops; i++) { 
			nmsqrttol(a, initialGuess, tol);
		}
		tim.toc();
		time = 1000*tim.elapsedms()/Nops;
		System.out.println("Newton's Method Time (ms) per 1k operations: "+time);


		Nops = 10000000;
		a = 2;
		tim = new Tim();
		tim.tic();
		for(int i=0; i<Nops; i++) { 
			Math.sqrt(a);
		}
		tim.toc();
		time = 1000*tim.elapsedms()/Nops;
		System.out.println("Math Library Time (ms) per 1k operations: "+time);

	}
```

and the results:

```
javac SquareRoot.java && java SquareRoot
Newton's Method Time (ms) per 1k operations: 0.016
Math Library Time (ms) per 1k operations: 3.0E-4
```

While the accuracy of Newton's Method for square roots may not be that great,
it ain't bad, for 9 lines of code. 

<a name="newton-next"></a>
## Next Steps

In a blog post to follow, we'll compare the speed and accuracy of square root computations using Newton's Method
to an alternative approach involving the continued fraction representation of square roots. This particularly interesting
technique can also be used to solve the Pell equation, a quadratic Diophantine equation of the form:

$$
x^2 - D y^2 = 1
$$

But more on that in a future post...

<a name="newton-refs"></a>
## References

1. Press, William et al. "Numerical Recipes in C." Cambridge Unviersity Press (2007).

2. "SquareRoot.java". Charles Reid. git.charlesreid1.com.
<[https://git.charlesreid1.com/cs/java/src/master/numerics/newtons-method](https://git.charlesreid1.com/cs/java/src/master/numerics/newtons-method)>

