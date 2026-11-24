# Methodological grounding — descriptive analysis

## 1. Method

Descriptive statistics of central tendency and dispersion for a single numeric variable: arithmetic
mean, median, sample standard deviation, minimum and maximum, plus a count of missing cells.

This is textbook descriptive statistics; no inferential claim is made. The median is reported
alongside the mean because their divergence is the cheapest available signal of skew or outliers.

## 2. Operationalisation

| Concept | Variable | Decision | Alternative rejected | Reason |
|---|---|---|---|---|
| central tendency | mean, median | both reported | mean only | median resists outliers and reveals skew |
| dispersion | sample stdev (n−1) | sample, not population | population stdev | the data is treated as a sample |
| missing | count per column | counted, excluded from statistics | imputation | imputation is a modelling decision, not descriptive |

## 3. Epistemic status

- **Established**: the reported statistics describe this file.
- **Interpretation**: divergence between mean and median suggests skew.
- **Hypothesis**: nothing about the population is claimed.
- **Normative**: none.

## 4. Assumptions and validity domain

- Values are on a numeric scale where a mean is meaningful. For ordinal scales the median alone is
  defensible; the mean is reported but should not be read as a magnitude.
- The missing-data mechanism is not analysed. `missing` counts cells; it does not tell whether they
  are missing at random.

## 5. Known alternatives

Full distributional summaries (quantiles, histograms) are more informative and are the natural next
step; they were left out to keep the example readable and its correctness checkable by reading.

## 6. Bibliography

- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Freedman, D., Pisani, R., & Purves, R. (2007). *Statistics* (4th ed.). W. W. Norton.
