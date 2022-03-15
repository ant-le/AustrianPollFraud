// McElreath, R. (2020). Statistical rethinking: 
// A Bayesian course with examples in R and Stan. 
// Chapman and Hall/CRC., Chapter 7,14
data {
  int<lower=0> N;                               // number of observations
  int<lower=0> T;                               // number of time points 
  int<lower=0> K;
  matrix[N, K] x;                               // predictor Vector
  matrix[N, T] d;
  vector[N] y_obs;                              // observed outcome vector
}
parameters {
  vector[T] beta;                               // coefficients for predictors
  vector[K] gamma;
  real<lower=0> sigma;                          // error scale
  vector[N] y_est;                              // estimated outcome vector
}
model {
  y_est ~ normal(x*gamma + d*beta , sigma);     // likelihood
  y_obs ~ normal(y_est, 2);                     // estimating sampling variance
  gamma ~ normal(0, 50);
  beta ~ normal(0, 5);                          // prior for cieffients
  sigma ~ inv_gamma(5,5);                      // prior for error scale
}   