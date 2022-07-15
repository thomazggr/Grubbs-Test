from numpy import square, sqrt
from scipy.stats import t
from statistics import mean as mn
from statistics import stdev as stdev


class Grubbs:
    def __init__(self, values: list, samples: list = False, remove: bool = False, alpha: float = 0.05):
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
        results, mean, std, crit = self.z_score(values, crit)

        self.mean = "Mean: {}".format(mean)
        self.std = "Standard deviation: {}".format(std)
        self.critical = "Critical Value(λ): {}".format(crit)

        if samples:
            results["samples"] = samples
        else:
            pass

        if remove:
            rmvd = [x if x is not False and y == "No" else "-"
                    for x, y in zip(results["values"], results["outlier"])]
            if "-" in rmvd:
                rmvd.remove("-")
            else:
                pass

            self.keeps = rmvd
        else:
            pass

        self.results = results

        if results["outlier"].count("Yes") == 0:
            self.outliers = "There are no outliers between all samples"
        elif results["outlier"].count("Yes") == 1:
            self.outliers = "There is 1 outlier between all samples"
        else:
            self.outliers = "There are {} outliers between all samples" \
                .format(results["outlier"].count("Yes"))
        pass

    @staticmethod
    def z_crit(n: int, alpha: float) -> float:
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

    @staticmethod
    def z_score(vals: list, crit: float) -> tuple:
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
        results = {
            "values": vals,
            "zscore": zis,
            "outlier":otls
        }
        return results, mean, std, crit
