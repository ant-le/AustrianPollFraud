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