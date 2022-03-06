# CS/INFO 5304 Assignment 1: Data Preparation

Chenran Ning (cn257)

This project is a coure project in `Data Science in the wild` from Cornell Tech.
## Question 1: Extract, Transform Load (ETL) (34 points)

### Step 1: Load data (3 points)

```python
spark_df = spark.read.load(filepath, format=format)
```

### Step 2: Make test example (6 points)

`brfss`and`nhis`files:

```json
{"SEX":2.0,"_LLCPWT":1,"_AGEG5YR":11.0,"_IMPRACE":1.0}
{"SEX":1.0,"_LLCPWT":2,"_AGEG5YR":6.0,"_IMPRACE":1.0}
{"SEX":2.0,"_LLCPWT":2,"_AGEG5YR":10.0,"_IMPRACE":5.0}
{"SEX":2.0,"_LLCPWT":1,"_AGEG5YR":1.0,"_IMPRACE":1.0}
{"SEX":2.0,"_LLCPWT":1,"_AGEG5YR":11.0,"_IMPRACE":1.0}
```

```csv
SEX,MRACBPI2,HISPAN_I,AGE_P,DIBEV1
,1,12,65,2
2,1,12,19,2
1,1,12,45,1
2,1,0,67,1
1,1,12,,2
```

```
{"SEX":2.0,"_LLCPWT":1,"_AGEG5YR":1.0,"_IMPRACE":1.0}
2,1,12,19,2
{"SEX":1.0,"_LLCPWT":2,"_AGEG5YR":6.0,"_IMPRACE":1.0}
1,1,12,45,1
{"SEX":2.0,"_LLCPWT":2,"_AGEG5YR":10.0,"_IMPRACE":5.0}
2,1,0,67,1

```

The joint set is :

```
SEX,_LLCPWT,_AGEG5YR,_IMPRACE,DIBEV1
2.0,1,1.0,1.0,2
1.0,2,6.0,1.0,1
2.0,2,10.0,5.0,1

```

In file `brfss`:

- SEX

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305201358261.png" alt="image-20220305201358261" style="zoom: 33%;" />

- _LLCPWT

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305201641044.png" alt="image-20220305201641044" style="zoom:33%;" />

- _AGEG5YR

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305201715857.png" alt="image-20220305201715857" style="zoom:50%;" />

- _IMPRACE

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305201737400.png" alt="image-20220305201737400" style="zoom:50%;" />

In `nhis` file:

- SEX

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305201835667.png" alt="image-20220305201835667" style="zoom:33%;" />

- MRACBPI2

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305202016632.png" alt="image-20220305202016632" style="zoom:50%;" />

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305201737400.png" alt="image-20220305201737400" style="zoom:50%;" />

- HISPAN_I

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305202054736.png" alt="image-20220305202054736" style="zoom:50%;" />

- AGE_P

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305202121575.png" alt="image-20220305202121575" style="zoom:50%;" />

- DIBEV1

<img src="/Users/chty627/Desktop/Cornell/Second Term/DS in the wild/assignment 1/CS-INFO-5304-Assignment-1-Data-Preparation/${img}/image-20220305202211101.png" alt="image-20220305202211101" style="zoom:50%;" />

### Step 3: Map data (12 points) 

```python
spark-submit p1.py test_brfss.json test_nhis.csv no
spark-submit p1.py brfss_input.json nhis_input.csv no
```



## Question 2: Dealing with messy and missing data (40 points)



## Question 3: Outlier Detection (10 points)

## Question 4: Data Visualization (10 points)