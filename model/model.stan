data {
  int<lower=0> N;       // number of data items
  int<lower=0> K;       // number of predictors
  matrix[N, K] x;       // predictor matrix
  vector[N] y_obs;      // outcome vector
}
parameters {
  real alpha;           // intercept
  vector[K] beta;       // coefficients for predictors
  real<lower=0> sigma;  // error scale
}
model {
  y_obs ~ normal(x * beta + alpha, sigma);   // likelihood
  alpha ~ normal(0, 5);
  beta ~ normal(0, 5);
  sigma ~ inv_gamma(5, 5);   
} 