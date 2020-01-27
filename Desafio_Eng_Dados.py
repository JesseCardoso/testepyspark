Quest�es Teoricas:

Qual o objetivo do comando cache em Spark?
R: Performance. O Comando cache ajuda a melhorar a efici�ncia do c�digo, permite que resultados intermedi�rios de opera��es lazy 
possam ser armazenados e reutilizados repetidamente. 

O mesmo c�digo implementado em Spark � normalmente mais r�pido que a implementa��o equivalente em MapReduce. Por qu�?
R: Sim. A principal diferen�a entre eles est� no processamento: o Spark pode fazer isso na mem�ria, 
enquanto o Hadoop MapReduce precisa ler e gravar em um disco. Sendo 100 vezes mais r�pido.

Qual � a fun��o do SparkContext ?
R: Tem a fun��o principal � estabelecer conex�o e v�rias opera��es paralelas nos n�s de trabalho (Clusters). E coleta os resultados das opera��es. 
Os n�s de trabalho leem e gravam dados do Sistema de Arquivos Distribu�do do Hadoop. Os n�s de trabalho tamb�m armazenam dados transformados na mem�ria em 
cache com RDDs (Conjuntos de Dados Distribu�do Resiliente).

Explique com suas palavras o que � Resilient Distributed Datasets (RDD)?
R: � uma cole��o de objetos, distribu�da e imut�vel, cada conjunto de dado no RDD�s � dividido em parti��es logicas, que podem ser computadas 
em diferentes nodes de cluster, RDD�s podem ser criadas a partir do Hadoop (arquivos no HDFS), atrav�s da transforma��o de outros RDD�s, 
a partir de banco de dados (relacionais e n�o-relacionais) ou a partir de arquivos locais.

GroupByKey � menos eficiente que reduceByKey em grandes dataset. Por qu�?
R: groupByKey faz o agrupamento em conjunto de dados de pares. Agrupando para executar uma agrega��o sobre cada chave, 
j� o reduceByKey produzir� um desempenho muito melhor, pois retorna um conjunto de dados onde os valores para cada chave s�o agregados usando a fun��o
reduce reduzida.

Explique o que o c�digo Scala abaixo faz ?
R: L� um arquivo especifico no HDFS, executa quebra de linha por espa�o (" "), processa a contagem de palavras em MapReduce e salva o retorno (counts) em arquivo no HDFS.

Quest�es na pratica PYSPARK:-

# 1- N�mero de hosts �nicos.

from pyspark import SparkContext, SparkConf
sc = SparkContext.getOrCreate()
FileJulRDD = sc.textFile("/user/jcs/acess_log_Jul95")
FileAugRDD = sc.textFile("/user/jcs/acess_log_Aug95")
host = fileJulRDD.flatMap(lambda x: x.split(' '))

#Map-Reduce da contagem
testcount = host.map(lambda x:(x,1)) \
.reduceByKey(lambda x, y: x + y) \
.map(lambda x: (x[1], x[0])).sortByKey(False)

#Imprime o resultado
for word in testcount.collect():
    print(word)


    
fileJulRDD.map(lambda x: x[0]).distinct().count()
 # resultados: 81.983

fileAugRDD.map(lambda x: x[0]).distinct().count()
 # resultados: 75.060

# 2- O total de erros 404.
fileJulRDD.filter(lambda x: '404 -' in x).count()
 # resultados: 10.847
 
fileAugRDD.filter(lambda x: '404 -' in x).count()
 # resultados: 10.058

# 3- Os 5 URLs que mais causaram erro 404.

from pyspark.sql.functions import *
import pyspark.sql
from pyspark.sql.types import IntegerType

# criando um dataframe
dfAug = spark.createDataFrame(fileAugRDD)
dfJul = spark.createDataFrame(fileJulRDD)

# define��o de colunas 
dfAug = dfAug.select(col("_1").alias("Host"), col("_2").alias("Timestamp"),col("_3").alias("Requisicao"),col("_4").alias("retorno"),col("_5").alias("bytes"))
dfAug.show()

dfJul = dfJul.select(col("_1").alias("Host"), col("_2").alias("Timestamp"),col("_3").alias("Requisicao"),col("_4").alias("retorno"),col("_5").alias("bytes"))
dfJu.show()

#4- Quantidade de erros 404 por dia.

# converte a tabela p/ instru��o SQL
dfJul.createOrReplaceTempView('temp_Jul')
dfAug.createOrReplaceTempView('temp_Aug')

spSession.sql("select Host,retorno, count(retorno)as qtd from temp_Aug where retorno = '404 -' group by Host,retorno having count() order by qtd desc ").show()
spSession.sql("select Host,retorno, count(retorno)as qtd from temp_Jul where retorno = '404 -' group by Host,retorno having count() order by qtd desc ").show()

# 5- O total de bytes retornados
spSession.sql("select bytes, sum(bytes) soma from temp_Aug group by bytes having count()").show()