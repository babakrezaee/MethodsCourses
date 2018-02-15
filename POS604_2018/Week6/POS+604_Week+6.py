
# coding: utf-8

# # POS 604: Polimetrics II
# ## Week 6: Multinomial data/ Multinomial models
# 
# There are two major categories of categorical outcomes with more than two possible outcomes:
# * Ordered outcomes: Regime type=\{Democracy, anocracy, autocracy\}; education level=\{High school, undergraduate, Graduate \}
# * Unordered outcomes: Religion=\{Protestant, Catholic, Islam, other \}; Trade agreement=\{ WTO, EU, ASEAN \}

# In[2]:


## Loading stata kernel in jupyter notebook, using python code
import ipystata
from ipystata.config import config_stata
config_stata('C:\Program Files (x86)\Stata14\StataSE-64.exe') 


# For this session, we learn about multinomial models by replicating one of Kathleen Gallagher Cunningham, titled [Understanding strategic choice The determinants of civil war and nonviolent campaign in self-determination disputes](http://journals.sagepub.com/doi/abs/10.1177/0022343313475467)
# 
# Read the abstract of the paper; what is the main argument of this paper?

# In[3]:


get_ipython().run_cell_magic('stata', '', '*Set the format of printed coeffients and p-values\nset cformat %5.2f\nset pformat %5.2f\n*Load th data:\nuse "https://github.com/babakrezaee/MethodsCourses/blob/master/POS604_2018/Week6/JPR%20final.dta?raw=true", clear')


# Variable *strategic2* is the strategy choice of self-determination movements.
# 
# strategic2 is coded as follwo:
# * 0 = conventional politics
# * 1= nonviolent campaign
# * 2= civil war
# * 3= both civil war and nonviolent campaign.
# 
# Let's start with summarizing and plotting this variable:

# In[8]:


get_ipython().run_cell_magic('stata', '', 'des strategic2 \ndisplay("***************************************************************************************************************")\nsum strategic2 if active==1\ndisplay("***************************************************************************************************************")\ntab strategic2 if active==1\ndisplay("***************************************************************************************************************")')


# In[9]:


get_ipython().run_cell_magic('stata', '', 'hist strategic2, freq scheme(plotplain) addlabel ')


# This study investigates the effect of a set of variables on the stratgeic choice of self-detemrination movements between conventional politics and different types of contencious politics.
# The list of regressors:
# * democracy: regime type, dummy variable
# * instab: Political instability is measured as a three or greater point change in the Polity score of the state in the past two years
# * loggdppc: gross domestic product (GDP) per capita (log-transformed), proxy for state capacity
# * logSDsize_relative: relative group population
# * groupcon: geographic concentration
# * kin: transnational kin, whether the SD group has kin in a nearby state.
# * logfactions: measure of group fragmentation, which is a logged measure of the number of organizations making demands related to selfdetermination on behalf of the group each year.
# * indep: independence demands
# * excluded: political exclusion
# * avgecdis: economic grievance, the average level of economic discrimination the group faces measuring less to more discrimination.
# * logpop: population, log transformed
# * last3years_nvcampaign
# * last3years_civilwar1000
# 
# Formally, we want to estimate the below model:
# $$strategic2=\alpha_0~democracy+\alpha_1~instab+\alpha_2~loggdppc+\alpha_3~logSDsize_relative+\alpha_4~groupcon+\alpha_5~kin+$$ 
# $$\alpha_6~logfactions+\alpha_7~indep+\alpha_8~excluded+\alpha_9~avgecdis+\alpha_{10}~logpop+\alpha_{11}~last3years\_nvcampaign+\alpha_{12}~last3years\_civilwar1000+\epsilon$$

# How do you estimate this model? Let's start with an OLD estimation:

# In[10]:


get_ipython().run_cell_magic('stata', '', 'reg strategic2 i.democracy instab loggdppc logSDsize_relative groupcon kin   logfactions indep excluded avgecdis logpop  last3years_nvcampaign last3years_civilwar1000 if active==1, cluster(kgcid)\n\noutreg2 using Cunningham_2013.xls, replace ctitle(OLS)')


# In[11]:


get_ipython().run_cell_magic('stata', '', 'predict e_hat, residuals\nhistogram e_hat, fraction normal kdensity scheme(plotplain)')


# In[12]:


get_ipython().run_cell_magic('stata', '', 'predict y_hat, xb\nhistogram y_hat, fraction scheme(plotplain) xline(0 1 2 3)')


# Since the outcome variable is categorical, we expected to experience some issues after using OLS method for estimation our model. Previous sessions, logit and probit models were discussed in class for categorical outcomes with *exactly* two possible outcomes. Last session, you also learned about ordered logit model. Let's estimate above model using ordered logit estimation method:

# In[13]:


get_ipython().run_cell_magic('stata', '', 'ologit strategic2  i.democracy instab loggdppc logSDsize_relative groupcon kin   logfactions indep excluded avgecdis logpop  last3years_nvcampaign last3years_civilwar1000 if active==1, cluster(kgcid)')


# These results mean,
# $$
# y=\begin{cases} 0~~~~if~~~~y^* \leq 1.85 \\ 1~~~~if~~~~1.85<y^* \leq 2.12 \\ 2~~~~if~~~~2.12<y^* \leq 7.64 \\  
# 3~~~~if~~~~7.64<y^*
# \end{cases}
# $$

# ------------------------------------------------------------------------------
# ### Math behind ordered logit and probit
# The probability of a given observation for ordered logit is:
# 
# $$
# p_{ij}=Pr(y_j=i)=Pr(k_{i-1}<X_j\beta+u\leq k_i)\\
# ~~~~~~=\frac{1}{1+exp(-k_i+X_j\beta)}-\frac{1}{1+exp(-k_{i-1}+X_j\beta)}\\
# $$
# $k_0$ is defined as $-\infty$ and $k_k$ as $+\infty$.
# 
# For ordered probit, the probability of a given observation is 
# 
# $$
# p_{ij}=Pr(y_j=i)=Pr(k_{i-1}<X_j\beta+u\leq k_i)\\
# ~~~~~~=\Phi(k_i-X_j\beta)-\Phi(k_{i-1}-x_j\beta)
# $$
# where $\Phi(.)$ is the cdf of standard normal distribution.
# 
# 
# ------------------------------------------------------------------------------

# Here, we make a critical assumption. Using ologit/oprobit, it is assumed that the association between each pair of outcome groups is the same, know as *proportional odds assumption*. We can brant test to evaluate this assumnption.

# In[14]:


get_ipython().run_cell_magic('stata', '', 'brant')


# In[16]:


get_ipython().run_cell_magic('stata', '', 'hist strategic3, freq scheme(plotplain) addlabel ')


# In[28]:


get_ipython().run_cell_magic('stata', '', 'ologit strategic3  i.democracy instab loggdppc logSDsize_relative groupcon kin   logfactions indep excluded avgecdis logpop  last3years_nvcampaign last3years_civilwar1000 if active==1, cluster(kgcid) nolog')


# In[18]:


get_ipython().run_cell_magic('stata', '', 'brant')


# One implication of the violation of proportional odds assumption is that $p_{ik} \neq p_{ik}$ that is $ x_i\beta_k \neq x_i\beta_k $ for at least one $k$.

# #### ------------------------------------------------------------------------------
# ### Math behind multinomial logit
# 
# For the sake of simplicity, assume there are three categorical outcomes.
# The probability of a given observation for ordered logit is:
# 
# $$
# ln\frac{Pr(Y_i=1)}{Pr(Y_i=3)}=\beta_1.X_i \\
# ln\frac{Pr(Y_i=2)}{Pr(Y_i=3)}=\beta_2.X_i  
# $$
# 
# Then,
# $$
# Pr(Y_i=1)=Pr(Y_i=3)e^{\beta_1.X_i} \\
# Pr(Y_i=2)=Pr(Y_i=3)e^{\beta_2.X_i} \\
# Pr(Y_i=3)=1-Pr(Y_i=1)-Pr(Y_i=2)
# $$
# 
# We can show that,
# 
# $$
# Pr(Y_i=1)=\frac{e^{\beta_1.X_i}}{e^{\beta_1.X_i}+e^{\beta_2.X_i}+e^{\beta_3.X_i}} \\
# Pr(Y_i=2)=\frac{e^{\beta_2.X_i}}{e^{\beta_1.X_i}+e^{\beta_2.X_i}+e^{\beta_3.X_i}} \\
# Pr(Y_i=3)=\frac{e^{\beta_3.X_i}}{e^{\beta_1.X_i}+e^{\beta_2.X_i}+e^{\beta_3.X_i}}
# $$
# 
# (You easily extend above math to an outcome with k unordered categorical variable.)
# 
# 
# We need to estimate above equations. However, there is a problem here. By estimating $\beta_1$, $\beta_2$, and $\beta_3$, the model is unidentified. Why?
# 
# To resolve this issue, we can arbitrarily set one of $\beta_1$, $\beta_2$, and $\beta_3$ to zero. Above probabilities, therefore, can be re-written as follow:
# $$
# Pr(Y_i=1)=\frac{1}{1+e^{\beta_2.X_i}+e^{\beta_3.X_i}} \\
# Pr(Y_i=2)=\frac{e^{\beta_2.X_i}}{1+e^{\beta_2.X_i}+e^{\beta_3.X_i}} \\
# Pr(Y_i=3)=\frac{e^{\beta_3.X_i}}{1+e^{\beta_2.X_i}+e^{\beta_3.X_i}}
# $$
# 
# In fact, given this normalization, you will find the prbability of outcome 2 and 3 relative to the probability of outcome 1, as your base outcome.
# #### ------------------------------------------------------------------------------

# In[27]:


get_ipython().run_cell_magic('stata', '', 'mlogit strategic2  democracy instab loggdppc logSDsize_relative groupcon kin   logfactions indep excluded avgecdis logpop  last3years_nvcampaign last3years_civilwar1000 if active==1, cluster(kgcid) nolog')


# We can change the baseline probability in STATA by adding *base(outcome=0,1,2,...)* as an option to the mlogit estimation:

# In[29]:


get_ipython().run_cell_magic('stata', '', 'mlogit strategic2  democracy instab loggdppc logSDsize_relative groupcon kin   logfactions indep excluded avgecdis logpop  last3years_nvcampaign last3years_civilwar1000 if active==1, cluster(kgcid) base(3) nolog')


# In[26]:


get_ipython().run_cell_magic('stata', '', 'quietly mlogit strategic2  democracy instab loggdppc logSDsize_relative groupcon kin   logfactions indep excluded avgecdis logpop  last3years_nvcampaign last3years_civilwar1000 if active==1, cluster(kgcid)\nquietly margins, at( loggdppc =(3.5(.5)10.5))\nmarginsplot, scheme(plotplain)')

