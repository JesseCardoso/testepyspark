Questões Teoricas:

Qual o objetivo do comando cache em Spark?
R: Performance. O Comando cache ajuda a melhorar a eficiência do código, permite que resultados intermediários de operações lazy 
possam ser armazenados e reutilizados repetidamente. 

O mesmo código implementado em Spark é normalmente mais rápido que a implementação equivalente em MapReduce. Por quê?
R: Sim. A principal diferença entre eles está no processamento: o Spark pode fazer isso na memória, 
enquanto o Hadoop MapReduce precisa ler e gravar em um disco. Sendo 100 vezes mais rápido.

Qual é a função do SparkContext ?
R: Tem a função principal é estabelecer conexão e várias operações paralelas nos nós de trabalho (Clusters). E coleta os resultados das operações. 
Os nós de trabalho leem e gravam dados do Sistema de Arquivos Distribuído do Hadoop. Os nós de trabalho também armazenam dados transformados na memória em 
cache com RDDs (Conjuntos de Dados Distribuído Resiliente).

Explique com suas palavras o que é Resilient Distributed Datasets (RDD)?
R: É uma coleção de objetos, distribuída e imutável, cada conjunto de dado no RDD´s é dividido em partições logicas, que podem ser computadas 
em diferentes nodes de cluster, RDD´s podem ser criadas a partir do Hadoop (arquivos no HDFS), através da transformação de outros RDD´s, 
a partir de banco de dados (relacionais e não-relacionais) ou a partir de arquivos locais.

GroupByKey é menos eficiente que reduceByKey em grandes dataset. Por quê?
R: groupByKey faz o agrupamento em conjunto de dados de pares. Agrupando para executar uma agregação sobre cada chave, 
já o reduceByKey produzirá um desempenho muito melhor, pois retorna um conjunto de dados onde os valores para cada chave são agregados usando a função
reduce reduzida.

Explique o que o código Scala abaixo faz ?
R: Lê um arquivo especifico no HDFS, executa quebra de linha por espaço (" "), processa a contagem de palavras em MapReduce e salva o retorno (counts) em arquivo no HDFS.

Questões na pratica PYSPARK:-

# 1- Número de hosts únicos.

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

# 2- Total de erros 404.

fileJulRDD.map(lambda x: x[0]).distinct().count()
#total distintos no arquivo Julho
fileAugRDD.map(lambda x: x[0]).distinct().count()
#total distintos no arquivo Julho

fileJulRDD.filter(lambda x: '404 -' in x).count()
 
fileAugRDD.filter(lambda x: '404 -' in x).count()

# 3- Os 5 URLs que mais causaram erro 404.
# Bibliotecas e Classes necessárias para conversão file para tabela sql;
from pyspark.sql.functions import *
import pyspark.sql
from pyspark.sql.types import IntegerType

# criando um dataframe
dfAug = spark.createDataFrame(fileAugRDD)
dfJul = spark.createDataFrame(fileJulRDD)

# defineção de colunas 
dfAug = dfAug.select(col("_1").alias("Host"), col("_2").alias("Timestamp"),col("_3").alias("Requisicao"),col("_4").alias("retorno"),col("_5").alias("bytes"))
dfAug.show()

dfJul = dfJul.select(col("_1").alias("Host"), col("_2").alias("Timestamp"),col("_3").alias("Requisicao"),col("_4").alias("retorno"),col("_5").alias("bytes"))
dfJul.show()

#4- Quantidade de erros 404 por dia.

# converte a tabela p/ instrução SQL
dfJul.createOrReplaceTempView('temp_Jul')
dfAug.createOrReplaceTempView('temp_Aug')

spSession.sql("select 
                Host,retorno, count(retorno)as qtd from temp_Aug 
              where 
                retorno = '404 -' 
              group by 
                Host,retorno having count() 
              order by 
                qtd desc ").show()
spSession.sql("select 
                    Host,retorno, count(retorno)as qtd from temp_Jul 
                where 
                    retorno = '404 -' 
                group by 
                    Host,retorno having count() 
                order by 
                    qtd desc ").show()

# 5- O total de bytes retornados
spSession.sql("select 
                    bytes, sum(bytes) soma 
                from 
                    temp_Aug 
                group by 
                    bytes 
                having count()").show()
