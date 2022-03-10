// McElreath, R. (2020). Statistical rethinking: 
// A Bayesian course with examples in R and Stan. 
// Chapman and Hall/CRC., Chapter 7,14
data {
  int<lower=0> N;                          // number of data items
  int<lower=0> K;                          // number of predictors
  matrix[N, K] x;                          // predictor matrix
  vector[N] y_obs;                         // observed outcome vector
}
parameters {
  real alpha;                              // intercept
  vector[K] beta;                          // coefficients for predictors
  real<lower=0> sigma;                     // error scale
  vector[N] y_est;                         // estimated outcome vector
}
model {
  y_est ~ normal(x * beta + alpha, sigma); // likelihood
  y_obs ~ normal(y_est, 2);                // estimating sampling variance
  alpha ~ normal(0,5);                     // prior for intercept
  beta ~ normal(0, 5);                     // prior for cieffients
  sigma ~ inv_gamma(5,5);                  // prior for error scale
}   