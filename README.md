# Integer-LP-using-Gomory-Cuts

<img width="469" alt="image" src="https://github.com/its-archisman/Integer-LP-using-Gomory-Cuts/assets/98551177/434a103e-e309-4ea9-8f5d-9ee3438f83a7"> 

The LP problem is a maximization problem

The constraints are given in the form of
Ax <= b, x >= 0, where x is an integer.

## Approach:
First we convert this problem to one with "=" constaints. To do this, add one separate artificial variable at each constraint and convert it to "=" constraint. How we have a system of "n+m" variables.
The simplex method is done now, and the artificial variables are driven out. On doing this phase-1 of simplex method, we get a basic solution which we can start with.

Now we apply the Gomory-Cut Algorithm.
So accordingly, at each step a cut is added in the form of an extra constraint. It is added to the tableau and we do the dual-simplex method. After doing this once, we arrive to the next basic solution. If 

