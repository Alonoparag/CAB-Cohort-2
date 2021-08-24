{
 "metadata": {
  "name": "example_tukeyhsd"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "heading",
     "level": 1,
     "metadata": {},
     "source": [
      "Multiple Comparison in OneWay ANOVA"
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "from statsmodels.compatnp.py3k import BytesIO, asbytes   # for python 3 compatibility\n",
      "import numpy as np\n",
      "import statsmodels.stats.multicomp as multi"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 14
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "In the following we have two datasets for which we would like to test whether the response differs across different levels of the explanatory variable."
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "ss = '''\\\n",
      "  43.9  1   1\n",
      "  39.0  1   2\n",
      "  46.7  1   3\n",
      "  43.8  1   4\n",
      "  44.2  1   5\n",
      "  47.7  1   6\n",
      "  43.6  1   7\n",
      "  38.9  1   8\n",
      "  43.6  1   9\n",
      "  40.0  1  10\n",
      "  89.8  2   1\n",
      "  87.1  2   2\n",
      "  92.7  2   3\n",
      "  90.6  2   4\n",
      "  87.7  2   5\n",
      "  92.4  2   6\n",
      "  86.1  2   7\n",
      "  88.1  2   8\n",
      "  90.8  2   9\n",
      "  89.1  2  10\n",
      "  68.4  3   1\n",
      "  69.3  3   2\n",
      "  68.5  3   3\n",
      "  66.4  3   4\n",
      "  70.0  3   5\n",
      "  68.1  3   6\n",
      "  70.6  3   7\n",
      "  65.2  3   8\n",
      "  63.8  3   9\n",
      "  69.2  3  10\n",
      "  36.2  4   1\n",
      "  45.2  4   2\n",
      "  40.7  4   3\n",
      "  40.5  4   4\n",
      "  39.3  4   5\n",
      "  40.3  4   6\n",
      "  43.2  4   7\n",
      "  38.7  4   8\n",
      "  40.9  4   9\n",
      "  39.7  4  10'''\n",
      "\n",
      "#idx   Treatment StressReduction\n",
      "ss2 = '''\\\n",
      "1     mental               2\n",
      "2     mental               2\n",
      "3     mental               3\n",
      "4     mental               4\n",
      "5     mental               4\n",
      "6     mental               5\n",
      "7     mental               3\n",
      "8     mental               4\n",
      "9     mental               4\n",
      "10    mental               4\n",
      "11  physical               4\n",
      "12  physical               4\n",
      "13  physical               3\n",
      "14  physical               5\n",
      "15  physical               4\n",
      "16  physical               1\n",
      "17  physical               1\n",
      "18  physical               2\n",
      "19  physical               3\n",
      "20  physical               3\n",
      "21   medical               1\n",
      "22   medical               2\n",
      "23   medical               2\n",
      "24   medical               2\n",
      "25   medical               3\n",
      "26   medical               2\n",
      "27   medical               3\n",
      "28   medical               1\n",
      "29   medical               3\n",
      "30   medical               1'''\n",
      "\n",
      "#accommodate recfromtxt for python 3.2, requires bytes\n",
      "ss = asbytes(ss)\n",
      "ss2 = asbytes(ss2)\n",
      "\n",
      "\n",
      "dta = np.recfromtxt(BytesIO(ss), names=(\"Rust\",\"Brand\",\"Replication\"))\n",
      "dta2 = np.recfromtxt(BytesIO(ss2), names = (\"idx\", \"Treatment\", \"StressReduction\"))\n",
      "import pandas as pd\n",
      "dta1 = pd.read_csv(BytesIO(ss), delimiter=' +', names=(\"Rust\",\"Brand\",\"Replication\"))"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 15
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "The fo"
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "dta1.head()"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "html": [
        "<div style=\"max-height:1000px;max-width:1500px;overflow:auto;\">\n",
        "<table border=\"1\" class=\"dataframe\">\n",
        "  <thead>\n",
        "    <tr style=\"text-align: right;\">\n",
        "      <th></th>\n",
        "      <th>Rust</th>\n",
        "      <th>Brand</th>\n",
        "      <th>Replication</th>\n",
        "    </tr>\n",
        "  </thead>\n",
        "  <tbody>\n",
        "    <tr>\n",
        "      <th>0</th>\n",
        "      <td> 43.9</td>\n",
        "      <td> 1</td>\n",
        "      <td> 1</td>\n",
        "    </tr>\n",
        "    <tr>\n",
        "      <th>1</th>\n",
        "      <td> 39.0</td>\n",
        "      <td> 1</td>\n",
        "      <td> 2</td>\n",
        "    </tr>\n",
        "    <tr>\n",
        "      <th>2</th>\n",
        "      <td> 46.7</td>\n",
        "      <td> 1</td>\n",
        "      <td> 3</td>\n",
        "    </tr>\n",
        "    <tr>\n",
        "      <th>3</th>\n",
        "      <td> 43.8</td>\n",
        "      <td> 1</td>\n",
        "      <td> 4</td>\n",
        "    </tr>\n",
        "    <tr>\n",
        "      <th>4</th>\n",
        "      <td> 44.2</td>\n",
        "      <td> 1</td>\n",
        "      <td> 5</td>\n",
        "    </tr>\n",
        "  </tbody>\n",
        "</table>\n",
        "</div>"
       ],
       "output_type": "pyout",
       "prompt_number": 16,
       "text": [
        "   Rust  Brand  Replication\n",
        "0  43.9      1            1\n",
        "1  39.0      1            2\n",
        "2  46.7      1            3\n",
        "3  43.8      1            4\n",
        "4  44.2      1            5"
       ]
      }
     ],
     "prompt_number": 16
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "#help(multi.MultiComparison)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 38
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "#What's the nicest, fastest way to get F-test for oneway anova?\n",
      "\n",
      "The F-test in the following regression shows that the null hypothesis that all coefficients are zero, is strongly rejected with a p-value of 1e-33. This means in terms of a one way anova, that we can reject the joint hypothesis that all means of the response are the same across each explanatory variable, in this case the brand.\n",
      "\n",
      "In the following we use Tukey HSD to test each pairwise comparison. We reject that all means are the same, but we would like to know if some pairs of brands have the same mean."
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import statsmodels.formula.api as smf\n",
      "res = smf.ols(\"Rust ~ C(Brand, Treatment(1))\", dta1).fit()\n",
      "print res.summary()"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "                            OLS Regression Results                            \n",
        "==============================================================================\n",
        "Dep. Variable:                   Rust   R-squared:                       0.986\n",
        "Model:                            OLS   Adj. R-squared:                  0.985\n",
        "Method:                 Least Squares   F-statistic:                     866.1\n",
        "Date:                Sat, 05 Apr 2014   Prob (F-statistic):           1.34e-33\n",
        "Time:                        21:32:38   Log-Likelihood:                -90.946\n",
        "No. Observations:                  40   AIC:                             189.9\n",
        "Df Residuals:                      36   BIC:                             196.6\n",
        "Df Model:                           3                                         \n",
        "Covariance Type:            nonrobust                                         \n",
        "===============================================================================================\n",
        "                                  coef    std err          t      P>|t|      [95.0% Conf. Int.]\n",
        "-----------------------------------------------------------------------------------------------\n",
        "Intercept                      43.1400      0.784     55.056      0.000        41.551    44.729\n",
        "C(Brand, Treatment(1))[T.2]    46.3000      1.108     41.782      0.000        44.053    48.547\n",
        "C(Brand, Treatment(1))[T.3]    24.8100      1.108     22.389      0.000        22.563    27.057\n",
        "C(Brand, Treatment(1))[T.4]    -2.6700      1.108     -2.409      0.021        -4.917    -0.423\n",
        "==============================================================================\n",
        "Omnibus:                        0.395   Durbin-Watson:                   2.608\n",
        "Prob(Omnibus):                  0.821   Jarque-Bera (JB):                0.555\n",
        "Skew:                          -0.101   Prob(JB):                        0.758\n",
        "Kurtosis:                       2.459   Cond. No.                         4.79\n",
        "==============================================================================\n",
        "\n",
        "Warnings:\n",
        "[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.\n"
       ]
      }
     ],
     "prompt_number": 39
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "mc = multi.MultiComparison(dta['Rust'], dta['Brand'])\n",
      "res = mc.tukeyhsd()\n",
      "print(res.summary())"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Multiple Comparison of Means - Tukey HSD,FWER=0.05\n",
        "===============================================\n",
        "group1 group2 meandiff  lower    upper   reject\n",
        "-----------------------------------------------\n",
        "  0      1      46.3   43.3155  49.2845   True \n",
        "  0      2     24.81   21.8255  27.7945   True \n",
        "  0      3     -2.67   -5.6545   0.3145  False \n",
        "  1      2     -21.49  -24.4745 -18.5055  True \n",
        "  1      3     -48.97  -51.9545 -45.9855  True \n",
        "  2      3     -27.48  -30.4645 -24.4955  True \n",
        "-----------------------------------------------\n"
       ]
      }
     ],
     "prompt_number": 18
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "mc = multi.MultiComparison(dta1['Rust'], dta1['Brand'])#.values)\n",
      "res = mc.tukeyhsd()\n",
      "print(res.summary())"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Multiple Comparison of Means - Tukey HSD,FWER=0.05\n",
        "===============================================\n",
        "group1 group2 meandiff  lower    upper   reject\n",
        "-----------------------------------------------\n",
        "  0      1      46.3   43.3155  49.2845   True \n",
        "  0      2     24.81   21.8255  27.7945   True \n",
        "  0      3     -2.67   -5.6545   0.3145  False \n",
        "  1      2     -21.49  -24.4745 -18.5055  True \n",
        "  1      3     -48.97  -51.9545 -45.9855  True \n",
        "  2      3     -27.48  -30.4645 -24.4955  True \n",
        "-----------------------------------------------\n"
       ]
      }
     ],
     "prompt_number": 19
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "#vars(res)\n",
      "res.groupsunique\n"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "pyout",
       "prompt_number": 20,
       "text": [
        "Brand\n",
        "0        1\n",
        "18       2\n",
        "29       3\n",
        "38       4\n",
        "Name: Brand, dtype: int64"
       ]
      }
     ],
     "prompt_number": 20
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "Now we can perform the same hypothesis tests for the second data set."
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "#Bug: this doesn't work with recarray, why?\n",
      "#res = smf.ols(\"StressReduction ~ C(Treatment, Treatment(1))\", \n",
      "#              data={'StressReduction':dta2['StressReduction'], 'Treatment':dta2['Treatment']}).fit()\n",
      "res = smf.ols(\"StressReduction ~ Treatment\", dta2).fit()\n",
      "print res.summary()"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "                            OLS Regression Results                            \n",
        "==============================================================================\n",
        "Dep. Variable:        StressReduction   R-squared:                       0.277\n",
        "Model:                            OLS   Adj. R-squared:                  0.223\n",
        "Method:                 Least Squares   F-statistic:                     5.164\n",
        "Date:                Sat, 05 Apr 2014   Prob (F-statistic):             0.0126\n",
        "Time:                        21:52:28   Log-Likelihood:                -42.816\n",
        "No. Observations:                  30   AIC:                             91.63\n",
        "Df Residuals:                      27   BIC:                             95.84\n",
        "Df Model:                           2                                         \n",
        "Covariance Type:            nonrobust                                         \n",
        "=========================================================================================\n",
        "                            coef    std err          t      P>|t|      [95.0% Conf. Int.]\n",
        "-----------------------------------------------------------------------------------------\n",
        "Intercept                 2.0000      0.336      5.951      0.000         1.310     2.690\n",
        "Treatment[T.mental]       1.5000      0.475      3.156      0.004         0.525     2.475\n",
        "Treatment[T.physical]     1.0000      0.475      2.104      0.045         0.025     1.975\n",
        "==============================================================================\n",
        "Omnibus:                        0.893   Durbin-Watson:                   1.385\n",
        "Prob(Omnibus):                  0.640   Jarque-Bera (JB):                0.918\n",
        "Skew:                          -0.293   Prob(JB):                        0.632\n",
        "Kurtosis:                       2.374   Cond. No.                         3.73\n",
        "==============================================================================\n",
        "\n",
        "Warnings:\n",
        "[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.\n"
       ]
      }
     ],
     "prompt_number": 45
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "mc2 = multi.MultiComparison(dta2['StressReduction'], dta2['Treatment'])\n",
      "res2 = mc2.tukeyhsd()\n",
      "print(res2.summary())"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Multiple Comparison of Means - Tukey HSD,FWER=0.05\n",
        "============================================\n",
        "group1 group2 meandiff  lower  upper  reject\n",
        "--------------------------------------------\n",
        "  0      1      1.5     0.3217 2.6783  True \n",
        "  0      2      1.0    -0.1783 2.1783 False \n",
        "  1      2      -0.5   -1.6783 0.6783 False \n",
        "--------------------------------------------\n"
       ]
      }
     ],
     "prompt_number": 21
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "The sample in this example is balanced, all group levels have the same number of observations. We can drop some observations to get an unbalanced sample."
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "mc2s = multi.MultiComparison(dta2['StressReduction'][3:29], dta2['Treatment'][3:29])\n",
      "res2s = mc2s.tukeyhsd()\n",
      "print(res2s.summary())"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Multiple Comparison of Means - Tukey HSD,FWER=0.05\n",
        "============================================\n",
        "group1 group2 meandiff  lower  upper  reject\n",
        "--------------------------------------------\n",
        "  0      1     1.8889   0.6302 3.1476  True \n",
        "  0      2     0.8889  -0.2587 2.0365 False \n",
        "  1      2      -1.0   -2.2309 0.2309 False \n",
        "--------------------------------------------\n"
       ]
      }
     ],
     "prompt_number": 22
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "The test and confidence interval are by default defined for a familywise error rate of alpha=0.05. The FWER can be changed in the call to `tukeyhsd`. The confidence interval becomes larger if we reduce alpha to one percent, however in this case the rejection decision remains unchanged."
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "res2s_001 = mc2s.tukeyhsd(alpha=0.01)\n",
      "print(res2s_001.summary())"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "Multiple Comparison of Means - Tukey HSD,FWER=0.01\n",
        "============================================\n",
        "group1 group2 meandiff  lower  upper  reject\n",
        "--------------------------------------------\n",
        "  0      1     1.8889   0.2662 3.5116  True \n",
        "  0      2     0.8889  -0.5905 2.3683 False \n",
        "  1      2      -1.0   -2.5868 0.5868 False \n",
        "--------------------------------------------\n"
       ]
      }
     ],
     "prompt_number": 23
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "from IPython.display import HTML\n",
      "s = res2s_001.summary().as_html()\n",
      "h = HTML(s); h"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "html": [
        "<table class=\"simpletable\">\n",
        "<caption>Multiple Comparison of Means - Tukey HSD,FWER=0.01</caption>\n",
        "<tr>\n",
        "  <th>group1</th> <th>group2</th> <th>meandiff</th>  <th>lower</th>   <th>upper</th> <th>reject</th>\n",
        "</tr>\n",
        "<tr>\n",
        "     <td>0</td>      <td>1</td>    <td>1.8889</td>  <td>0.2662</td>  <td>3.5116</td>  <td>True</td> \n",
        "</tr>\n",
        "<tr>\n",
        "     <td>0</td>      <td>2</td>    <td>0.8889</td>  <td>-0.5905</td> <td>2.3683</td>  <td>False</td>\n",
        "</tr>\n",
        "<tr>\n",
        "     <td>1</td>      <td>2</td>     <td>-1.0</td>   <td>-2.5868</td> <td>0.5868</td>  <td>False</td>\n",
        "</tr>\n",
        "</table>"
       ],
       "output_type": "pyout",
       "prompt_number": 24,
       "text": [
        "<IPython.core.display.HTML at 0x7739210>"
       ]
      }
     ],
     "prompt_number": 24
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "fig = res2.plot_simultaneous()\n",
      "#Why are the axislabels shifted ?"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "display_data",
       "png": "iVBORw0KGgoAAAANSUhEUgAAAmcAAAF6CAYAAABcEv/JAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAIABJREFUeJzt3Xt8TWe+x/HviiAuETtolCLuREQirkWztUzc0kFRKiid\n1rTEpe2ZVlsVZ8o4hjMtLzNUL2jrckw5VNymdCvTqktRiirTkKgqgkQIIev84dhjRyIRl/0kPu/X\nK6/uy1rP+q1nP7u+eZ61dyzbtm0BAADACD7eLgAAAAD/RjgDAAAwCOEMAADAIIQzAAAAgxDOAAAA\nDEI4AwAAMAjhDCgAHx8f/etf/8r1+dDQUH355Zf5ais4OFjr1q27U6UVGl26dNFHH33k7TIgKTEx\nUT4+PsrKypIkOZ1Ovf/++3f0GJ988omio6PvWHuzZs3S6NGjb6uNvN7HBdGyZUvt3bv3jraJ+w/h\nDPeV4OBglSxZUqdOnfJ4PCIiQj4+Pjpy5Mgtt/n0009r7NixHo/t2bNHjzzySL72tyxLlmXd8nEl\nKTU1VaNGjVKNGjXk7++vOnXqaPTo0Tecn4lWrlypAQMGeLsMSVfHRenSpeXv76/AwEB169ZNycnJ\n+drX5XKpWrVqd7nCO8PlcsnHx0eTJ0++6XY3G5Px8fEqXry4/P395XA41KZNG23evDnPY/fv319r\n1qwpUN3ZXbp0SRMmTNAf/vAHbdy4Uf7+/vL391fZsmXl4+Pjvl+uXLl8v453yssvv6w333zznh4T\nRQ/hDPcVy7JUq1YtLViwwP3Y7t27deHChQIHJG+5dOmSHnvsMe3bt09r1qxRWlqavv76a1WsWFFb\ntmzxdnm5sm1bpn33tWVZWrFihdLS0nTs2DEFBQUpLi7O22XdcXPnzlVoaKjmzZtX4DYsy1K/fv2U\nlpamEydOqG3bturZs+dt1XX58uVb2n7ZsmVq2LChHnzwQbVr105paWlKS0vT999/L0k6e/as0tLS\nlJqaqoceeui2artVMTEx+uKLL3T8+PF7elwULYQz3HdiY2M9/nGaO3euBg4c6BEYsi/rzJkzR+3a\ntbuhrXfffVfz58/X5MmT5e/vr9/+9reSrs7ErF+/XtLVmYZevXqpb9++KleunCIjI/Xdd9/lWJtt\n25o0aZLq1KmjihUr6sknn9Tp06dz3HbevHlKSkrS0qVL1aBBA0lSpUqV9Prrr6tz586SpH379snp\ndMrhcCg0NFSfffaZe/+nn35aL7zwgrp06SJ/f3+1a9dOv/zyi0aOHCmHw6GGDRtq586d7u2Dg4M1\nadIkNWrUSIGBgRoyZIguXrwoSTpz5oy6deumBx54QIGBgYqJidHRo0c9+vONN95QmzZtVLZsWf3r\nX//y6OODBw8qKipK5cuXV6VKldS3b1/3vl999ZWaN2+u8uXLq0WLFvr666892n3zzTfVtm1blStX\nTtHR0e5Zw4yMDMXGxqpixYpyOBxq0aKFfv311xz78nolS5bUE0884bE0dfHiRb388suqUaOGKleu\nrOeff14ZGRlKT09X586d9fPPP7tnao4dO6ZSpUopJSVFkjRhwgQVL15c586dkySNHTvWvRyXW7vX\nrFixQuHh4e4Zqt27d3u8HlOnTlWTJk1Uvnx59e3b1/165CQ9PV2ffvqpZs6cqSNHjmj79u159kVO\nrg/Xvr6+GjhwoH755RedOnXKPXbLlSunRo0a6X//93/d+2V/D/n4+Oivf/2r6tatq/r160uSRo8e\nraCgIAUEBCgsLMwdtrJbtWqVoqKicqztevl9H0vSpk2bVL16dfflCB988IFCQkIUGBioTp06uWfV\nhw0bppdfftlj38cff1xvv/22JMnPz0+RkZF3bJYQ9yfCGe47rVq1Umpqqvbv368rV65o0aJFio2N\n9dgmv0uNzz33nPr3769XXnlFaWlpWrZsmXv/6y1fvlx9+vTR6dOn9dRTT6l79+66cuXKDe1NmzZN\ny5cv15dffqljx47J4XBo2LBhOR77888/V+fOnVW6dOkcn8/MzFRMTIw6deqkEydOaPr06erfv78O\nHDjg3mbx4sWaMGGCTp48qRIlSqhVq1Zq3ry5UlJS1KtXL7344osebc6fP19r167VoUOHdODAAb31\n1luSpKysLD3zzDM6cuSIjhw5olKlSmn48OEe+3788cd67733lJaWpho1anj08dixY9WpUyedOXNG\nR48e1YgRIyRJKSkp6tq1q0aNGqWUlBS9+OKL6tq1q0dgXbBggebMmaNff/1Vly5d0pQpUyRdDd2p\nqalKTk5WSkqKZs2apVKlSuXYV9K//2E/f/68Fi1apNatW7ufe/XVV3Xw4EHt2rVLBw8e1NGjR/Wf\n//mfKlOmjFavXq0qVaq4Z2oefPBBtWjRQi6XS5K0YcMGBQcHa9OmTe77Tqfzpu1K0o4dO/TMM89o\n9uzZSklJ0dChQ/X4448rMzNT0tUxtnjxYq1Zs0Y//fSTvvvuO82ZMyfX81uyZImCgoL08MMPKyYm\nRnPnzs112/y6ePGi5syZo+rVq6tChQqqU6eONm3apNTUVI0bN06xsbE3nUFatmyZtm7dqr1792rN\nmjXauHGjfvzxR509e1aLFy9WhQoVctxvz5497kB3M/l9H69evVpPPfWUlixZokceeUTLli3Tn/70\nJy1dulQnT55Uu3bt1K9fP0lXf6lZsGCBe7ycPHlS69atU//+/d3tNWzYULt27crzuEBuCGe4Lw0Y\nMEDz5s3TP/7xD4WEhKhq1aq31V5ey3TNmjVTz549VaxYMb344ovKyMjI8TqdWbNm6a233lKVKlVU\nvHhxjRs3Tn//+9/dF2pfLyUlRQ8++GCux9y8ebPS09P16quvytfXV+3bt1e3bt08lnR79uypiIgI\nlSxZUj169FCZMmUUGxsry7LUp08f7dixw72tZVkaPny4qlatKofDoddff93dVmBgoHr06CE/Pz+V\nLVtWr732mjZs2OCx79NPP62GDRvKx8dHvr6+HrWWKFFCiYmJOnr0qEqUKKGHH35YkpSQkKD69eur\nf//+8vHxUd++fdWgQQMtX77c3e7gwYNVp04d+fn5qU+fPu7ZvhIlSujUqVP68ccfZVmWIiIi5O/v\nn2Nf2bat7t27y+FwqHz58lq3bp17dsS2bc2ePVv//d//rfLly6ts2bIaM2aMFi5c6H4+u6ioKG3Y\nsEFXrlzR7t27NWLECG3YsEEZGRnatm2bHnnkkTzbfffddzV06FA1b95clmVp4MCBKlmypMe4GTFi\nhCpXriyHw6GYmBiPmc7s5s6dq969e0uSevfurYULF97ycuI1//M//yOHw6Hq1atrx44dWrp0qSSp\nV69eqly5siSpT58+qlu3rr755ptc2xkzZozKly+vkiVLqkSJEkpLS9O+ffuUlZWl+vXru9vK7syZ\nM7m+lrdq0aJF+v3vf6/Vq1erWbNmkqSZM2dqzJgxql+/vnx8fDRmzBjt3LlTSUlJat68uQICAtwf\n4lm4cKHat2+vSpUqudv09/fXmTNn7kh9uD8RznDfsSxLAwYM0CeffJLjkubdcP11L5Zl6aGHHtLP\nP/98w3aJiYnq0aOHHA6HHA6HQkJC5Ovrm+PsQ4UKFXJs45qff/75hgvVa9So4d7Hsiw98MAD7uf8\n/Pw87pcqVcq9FHfN9e1Vr17d3db58+c1dOhQBQcHKyAgQFFRUTp79qxHv97sovnJkyfLtm21aNFC\noaGh+vDDD93nUL169VzPQZLHP+DX1zxgwABFR0erb9++qlq1ql555ZVcw4hlWVq2bJlOnz6tixcv\navr06YqKitKvv/6qEydO6Pz584qMjHS/Lp07d9bJkydzPZ+oqCi5XC59++23aty4sTp06KANGzbo\nm2++UZ06deRwOPJs9/Dhw5o6dar7OYfDoeTk5Hyde3ZJSUlyuVzucNapUydlZGQoISEh13O4mWvL\n7cePH9fnn3+uiIgISVeX2iMiItz17tmz56YfTrl+TLRv317Dhw/XsGHDFBQUpKFDhyotLS3H/RwO\nh1JTUwtUe3bTpk3Tk08+qZCQEPdjhw8fdi/vOxwO9wzetaX6gQMH6uOPP5Z0dUY4+wdbUlNT5XA4\n7kh9uD8RznBfql69umrVqqVVq1bleDFzmTJllJ6e7r7/yy+/5NpWfpZNkpKS3LezsrKUnJysKlWq\n5FjX6tWrdfr0affP+fPnc5wh69Chg9asWaPz58/neMwqVaooKSnJIyAdPnz4tmYJr/8065EjR9xt\nTZ06VQcOHNCWLVt09uxZbdiw4YYL/2/WT0FBQXr33Xd19OhRzZo1Sy+88IIOHTqkqlWr6vDhwx7b\n5vccfH199eabb+r777/XV199pRUrVuTrQnjLstSjRw8VK1ZMmzZtUsWKFVWqVCnt3bvX/ZqcOXPG\nHQ5yOq/WrVvrhx9+0NKlS+V0OtWwYUMdOXJEK1eudC9p5tVu9erV9frrr3uMhXPnzunJJ5/Mte7c\nfPTRR8rKylKXLl304IMPqmbNmsrIyCjQ0qZlWTn+MnP48GE999xzmjFjhlJSUnT69GmFhobe9Bef\n7DXHxcVp27Zt2rt3rw4cOKA///nPOe4XFhbmsTyfm/y8jxcvXqylS5dq2rRp7seqV6+ud99916Pv\n09PT1apVK0lXr1tdtmyZdu3apf3796t79+4ebe7bt09NmjTJsz4gN4Qz3Lfef/99rV+/PsfrkMLD\nw7VkyRJduHBBBw8evOl3PgUFBeX5XUnbt2/X0qVLdfnyZb399tvy8/Nz/4/+er///e/12muvuUPQ\niRMn3Et42Q0YMEDVqlXTE088oR9++EFZWVk6deqUJk6cqFWrVqlVq1YqXbq0Jk+erMzMTLlcLq1Y\nscJ9sf2tzhbatq2//vWvOnr0qFJSUjRhwgR3UDh37pxKlSqlgIAApaSkaPz48Tnun5vFixe7v/Kg\nfPnysixLxYoVU+fOnXXgwAEtWLBAly9f1qJFi7R//35169Ytz3a/+OIL7d69W1euXJG/v7+KFy+u\nYsWK3fT8rv332izatWXYZ599VqNGjdKJEyckXZ1BWbt2raSrr/+pU6c8ZnJKly6tyMhIzZgxw33h\n+sMPP6yZM2e67+fV7rPPPquZM2dqy5Ytsm1b6enpSkhIyHV27Gb9O3fuXMXHx2vXrl3un08//VQr\nV650f3Ahv+3l9nh6erosy1LFihWVlZWlDz/8UHv27Mm1puy2bdumb775RpmZmSpdurT8/Pxyfb26\ndOnisWyem/y8j6tUqaJ169bpnXfe0cyZMyVdfR9OnDjR/aGQa9fAXfPQQw+pWbNmGjhwoHr16qWS\nJUu6n8vIyNC3336rjh075vvcgewIZ7hv1apVS02bNnXfv/63+NGjR6tEiRIKCgrS4MGD3ddh5bTt\nM888o71798rhcOQ4C2dZln77299q0aJFCgwM1CeffKIlS5bk+A/PyJEj9fjjj+s3v/mNypUrp9at\nW+f6tRglSpTQ559/rgYNGqhjx44KCAhQy5YtlZKSolatWql48eL67LPPtGrVKlWqVEnDhw/XRx99\npHr16rnryn5O2Wcysj//1FNP6Te/+Y1q166tunXr6o033pAkjRo1ShcuXFDFihX18MMPq3Pnzjdt\nK7tt27apVatW7k+8Tps2TcHBwapQoYJWrFihqVOnqmLFipoyZYpWrFihwMDAXGu8dv/48ePq3bu3\nAgICFBISIqfTedPvVYuJiZG/v78CAgI0duxYzZs3Tw0bNpQk/dd//Zfq1KmjVq1aKSAgQB07dnTP\n3DRo0ED9+vVTrVq1FBgY6J6diYqK0uXLl9WiRQv3/XPnznl8/93N2o2MjNTs2bM1fPhwBQYGqm7d\nupo3b16u/Zjbxe+bN29WUlKShg0bpgceeMD9ExMTozp16rivccvv65XbcUJCQvTSSy+pdevWqly5\nsvbs2aO2bdvmul/2NlJTU/Xcc88pMDBQwcHBqlixov7jP/4jxxq6deum/fv369ixYznWd01+38fV\nqlXTunXrNGnSJH3wwQfq3r27XnnlFfXt21cBAQFq3LjxDZ++HDRokHbv3n3DmPrss8/Uvn37XK+X\n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\nQmCC\n"
      }
     ],
     "prompt_number": 25
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 25
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 25
    }
   ],
   "metadata": {}
  }
 ]
}