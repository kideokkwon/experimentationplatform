import scipy.stats as stats
import numpy as np

def msprt(alpha, x_c, x_t):
    """
    Performs two-sided sequential test (mSPRT) from Zhao et al., 2019

    Input: 
    - alpha: significance level alpha, usually 0.05
    - x_c: control data
    - x_t: treatment data

    Output: 
    - Confidence Interval
    """
    x_c_bar = np.mean(x_c)
    x_t_bar = np.mean(x_t)
    n_c = len(x_c)
    n_t = len(x_t)

    # variance of the difference in means
    v = (np.var(x_c) / n_c) + (np.var(x_t) / n_t)

    # Z-score corresponding to 1 - alpha/2
    Z_alpha = stats.norm.ppf(1-alpha/2)

    # mixing parameter
    t = (Z_alpha**2) * ((np.var(x_t) + np.var(x_c)) / (n_c + n_t))

    # margin of error of the confidence interval
    me = np.sqrt( ((v*(v+t))/t) * (-2*np.log(alpha/2) - np.log(v/(v+t))))

    # mean difference
    delta = x_t_bar - x_c_bar

    # confidence interval
    return (delta - me, delta + me)

def fixedttest(alpha, x_c, x_t):
    """
    Performs two-sided Welch's t-test

    Input: 
    - alpha: significance level alpha, usually 0.05
    - x_c: control data
    - x_t: treatment data

    Output: 
    - Confidence Interval
    """
    # Welch's t-test
    t_statistic, p_value = stats.ttest_ind(x_t, x_c, equal_var=False)

    # calculate DoF
    degrees_of_freedom = len(x_c) + len(x_t) - 2

    # loc
    loc = (x_t.mean() - x_c.mean())

    # scale
    scale = ((x_t.var() / len(x_t)) + (x_c.var() / len(x_c))) ** 0.5

    # calculate ci's for the diff. in means
    ci_lower, ci_upper = stats.t.interval(1-alpha/2, df=degrees_of_freedom, loc = loc, scale = scale)

    return ci_lower, ci_upper

def check_zero_in_interval(lower, upper):
    """
    significance checker - if significant return 0
    """
    if lower <= 0 <= upper:
        return 0
    else:
        return 1

def msprt_ci(control, treatment, alpha = 0.05):
  """
    Performs two-sided sequential test (mSPRT) from Zhao et al., 2019

    Input: 
    - alpha: significance level alpha, usually 0.05
    - x_c: control data
    - x_t: treatment data

    Output: 
    - Confidence Interval
  """
  control['day'] = control['date'].dt.date.rank(method='dense').astype(int)
  treatment['day'] = treatment['date'].dt.date.rank(method='dense').astype(int)

  # Iterate over each day
  for day in range(1, max(control['day']) + 1):
      # Filter data up to the current day
      x_c = control[control['day'] <= day]['action_count']
      x_t = treatment[treatment['day'] <= day]['action_count']

      # variance of the difference in means
      v = (np.var(x_c) / len(x_c)) + (np.var(x_t) / len(x_t))

      # Z-score corresponding to 1 - alpha/2
      Z_alpha = stats.norm.ppf(1-alpha/2)

      # mixing parameter
      t = (Z_alpha**2) * ((np.var(x_t) + np.var(x_c)) / (len(x_c) + len(x_t)))

      # marin of error term
      me = np.sqrt(((v*(v+t))/t) * (-2*np.log(alpha/2) - np.log(v/(v+t))))

      # sample mean
      e = np.mean(x_t) - np.mean(x_c)

      # ci
      ci_l = e - me
      ci_u = e + me

      # Check if significant
      if ci_u < 0 or ci_l > 0:
          return 1, day, ci_l, ci_u, e  # Significant result found, return 1

  # No significant result found after testing all days
  return 0, day, ci_l, ci_u, e

def welchtest(control, treatment, alpha=0.05):
    """
    run welch t-test
    """

    ## 6. Display Welch's T-Test
    user_data_sums_control = control.groupby('userid')['action_count'].sum()
    user_data_sums_treat = treatment.groupby('userid')['action_count'].sum()

    mean_c = round(user_data_sums_control.mean(),2)
    mean_t = round(user_data_sums_treat.mean(),2)
    relative_lift = round((mean_t - mean_c) / mean_c,2)

    # Perform Welch's t-test
    t_stat, p_value = stats.ttest_ind(user_data_sums_treat,user_data_sums_control, equal_var=False)

    return mean_c, mean_t, relative_lift, p_value