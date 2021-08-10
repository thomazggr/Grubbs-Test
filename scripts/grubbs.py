from numpy import square, sqrt
from pandas import DataFrame
from scipy.stats import t
from statistics import mean as mn
from statistics import stdev as stdev

class Grubbs:
    def z_crit(self, n: int, alpha: float) -> float:
        """ Gets both degress of freedom and alpha selected by user
        which is then used to get t critical value using Scipy t ppf
        Also there is a possibility to use one-tailed test to find critical value

        Parameters
        ----------
        n : int
            Degrees of freedom passed automatically to the function
        alpha : float
            Alpha value to be used in the t critical value finding passed by the user
        Returns
        -------
        float
            Absolute value for the z critical value used to compare between z score of each sample 
        """
        t_crit = t.ppf(alpha / (2 * n), n - 2)
        num = (n - 1) * t_crit
        den = sqrt(n * (n - 2 + square(t_crit)))
        val_crit = num / den
        return abs(val_crit)

    def z_score(self, vals: list, crit: float) -> DataFrame:
        """ Recieves values and critical z value to be compared with

        Parameters
        ----------
        vals : list
            List of sample values
        crit : float
            Critical z score to be used to compare with values
        Returns
        -------
        pd.DataFrame
            Dataframe with all data from z score and outlier results 
        """
        mean = mn(vals)
        std = stdev(vals)
        zis = [(abs(mean - v) / std) for v in vals]
        otls = ["No" if z < crit else "Yes" for z in zis]
        results = DataFrame(data={"Values":vals, "Z-score": zis, "Outlier?":otls})
        self.mean = "Mean: {}".format(mean)
        self.std = "Standard deviation: {}".format(std)
        self.critical = "Critical Value(λ): {}".format(crit)
        return results

    def test(self, values: list, samples: list = False, remove: bool = False, alpha: float = 0.05) -> str:
        """Recieves a list of values used in graph and identify outliers

        Parameters
        ----------
        values : list
            List of values from individual values for graph/statistics
        samples: list
            List with the samples' names to be used as index
        Returns
        -------
        list
            List with new values removing outliers, or indexes to be removed from main table (?)
        """
        self.values = values
        self.alpha = alpha
        crit = self.z_crit(len(values), alpha)
        results = self.z_score(values, crit)
        
        if samples: results["Samples"] = samples
        else: pass

        if remove: 
            rmvd = [x if x is not False and y == "No" else "-" 
                    for x, y in zip(results["Values"], results["Outlier?"])]
            if "-" in rmvd:
                rmvd.remove("-")
            else: pass

            self.keeps = rmvd
        else: 
            pass
        self.results = results
        
        if results["Outlier?"].value_counts()["Yes"] == 0:
            return "There are no outliers between all samples"
        elif results["Outlier?"].value_counts()["Yes"] == 1:
            return "There is 1 outlier between all samples"
        else:
            return "There are {} outliers between all samples".format(results["Outlier?"].value_counts()["Yes"])