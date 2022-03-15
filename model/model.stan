// McElreath, R. (2020). Statistical rethinking: 
// A Bayesian course with examples in R and Stan. 
// Chapman and Hall/CRC., Chapter 7,14
data {
  int<lower=0> N;                           // number of observations
  int<lower=0> T;                           // number of time points 
  int time[N];                              // Time Point vector 
  vector[N] x;                              // predictor Vector
  vector[N] y_obs;                          // observed outcome vector
}
parameters {
  vector[T] alpha;                          // Intercept
  vector[T] beta;                           // coefficients for predictors
  vector<lower=0>[T] sigma;                 // error scale
  vector[N] y_est;                          // estimated outcome vector
}
model {
  for (i in 1:N){
    y_est[i] ~ normal(x[i] * beta[time[i]] + alpha[time[i]], sigma[time[i]]); // likelihood
  }
  y_obs ~ normal(y_est, 2);                // estimating sampling variance
  alpha ~ normal(0, 5);                    // Intercept prior
  beta ~ normal(0, 5);                     // prior for cieffients
  sigma ~ inv_gamma(5, 5);
}   