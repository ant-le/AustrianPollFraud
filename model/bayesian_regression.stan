"""
Bayesian: modeling and imputing missing potential outcomes 
based on their posterior distributions

Bayesian inference considers the observed values of the 
four quantities to be realizations of random variables 
and the unobserved values to be unobserved random variables
"""

data {
  int<lower=1> N;
  int<lower=1> M;
  vector[N] y;
  matrix[M,N] x;
}
parameters {
  real alpha;
  real beta;
  real<lower=0> sigma;
}
model {
  // priors
  alpha ~ normal(0, 10);
  beta ~ normal(0, 10);
  sigma ~ cauchy(0, 2.5); 

  // model
  y ~ normal(x * beta + alpha, sigma);
}