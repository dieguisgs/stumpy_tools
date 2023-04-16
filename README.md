# stumpy_tools
Time Series Analysis using STUMPY patterns detection over a subsequences of a sequence

# Use Example
Starting from a Time Series DataFrame `df`

![TimeSeriesDataFrame](imgs/df.jpg)

Creation of the Similar Pattern Class

```python
patterns=SimilarPattern(df,24)
```

- If the DataFrame inserted has several columns a scateckd proccess compute the 2D array into 1D, turning columns registers to only one column,a dding more registers. Otherwise the sequence is a simply one, so the pattern is not taking into account other variables, just one, the given. 
- The second argument indicates the period of the subsequence to be compute. For 2D (several column DataFrame) Hidely the subsequence distnace computes as 24*nº columns

Once created the SimilarPattern object, the methods arises. Firstly with `.get_similar_patter(date)`

```python 
patterns.get_similar_pattern('2023-01-26')
```

```python
['2023-01-18']
```


The most similar date subsequence is shown. Sometimes some dates cant compute similarities. It depends on the data. 

```python
pattern.plot_similar_pattern('2023-01-26')
```

![TimeSeriesDataFrame](imgs/plot.jpg)

Motifs can be get as following attribute when some method using date is computed

```python
pattern.seek_motif
```


Also the overall matrix profile could be compute as:

```python 
pattern.get_matrix_profile```




----------
Citations
----------
    S.M. Law, (2019). STUMPY: A Powerful and Scalable Python Library for Time Series Data Mining. Journal of Open Source Software, 4(39), 1504.







