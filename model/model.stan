// McElreath, R. (2020). Statistical rethinking: 
// A Bayesian course with examples in R and Stan. 
// Chapman and Hall/CRC., Chapter 7,14
// Note that contratily to the paper, all fixed effects are stored
// in a single matrix x with parameter gamma
data {
  int<lower=0> N;                               // number of observations
  int<lower=0> T;                               // number of time points 
  int<lower=0> K;                               // number of groups
  matrix[N, K] x;                               // predictor Vector
  matrix[N, T] d;
  vector[N] y_obs;                              // observed outcome vector
}
parameters {
  vector[T] beta;                               // coefficients for estimators
  vector[K] gamma;                              // coefficients for fixed effects
  real<lower=0> sigma;                          // error scale
  vector[N] y_est;                              // estimated outcome vector
}
model {
  y_est ~ normal(x*gamma + d*beta, sigma);     // likelihood
  y_obs ~ normal(y_est, 2);                     // estimating sampling variance
  gamma ~ normal(0, 20);                        // fixed effects prior 
  beta ~ normal(0, 2);                          // prior for coeffients
  sigma ~ inv_gamma(5,5);                       // prior for error scale
}   
generated quantities {
  vector[N] y_hat;
  for (i in 1:N){
    y_hat[i] = normal_rng(x[i]*gamma + d[i]*beta, sigma);
  }
}