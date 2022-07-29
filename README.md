# FindGBugs
This project consists of two main parts, the first department is bugs_crawler and the second part is bugs_mining.

## bugs_crawler
The files in this folder are used for crawling, and they all end up fetching bugs in the form of <issue, commit>.

* oneRepoIWC.py

  This .py file is based on the full name of the repo to do the crawl only for this repo.


* getIWC.py

  This .py file does a query based on the keywords entered and does a crawl of all the repo's that are queried.

## bugs_mining

### �����﷨�������ͨ��ȱ���ھ򷽷�
This part is to propose a set of automated ways to dig the General Bug from the bugs obtained by the crawler above.It mainly uses python's abstract syntax tree. Based on the abstract syntax tree, a rule-based approach is used to mine the General Bug.
You need to run `clone_repo.py` to clone the Github repo to your own local before digging into the General Bug.
`update_nodes.py` is the starting position for digging the General Bug.

### ���ڴ����޸�ģʽѧϰ��ͨ��ȱ���ھ򷽷�

#### ����Dual-Encoder��ͨ��ȱ���ھ򷽷�

ʹ�����������������ض�Buggy�汾����Ƭ�κ�Fix�汾����Ƭ�ν��б��룬Ȼ��ʹ�õ���ȶ������ƶȼ��㷽��������������������ʾ�����ƶȣ����ͨ�����Բ������ࡣ

![img.png](img.png)

#### ����Cross-Encoder��ͨ��ȱ���ھ򷽷�

����Cross-Encoder��ͨ��ȱ���ھ򷽷����Ƚ�Buggy�汾��Fix�汾���δ������������������ݵ�CodeBERT�У�ͨ��Transformers��CodeBERT����������ṹ���ڲ�ʹ��Self-Attention���ƣ����ڱ���һ��Token��ʱ��ͬʱ�������������ĵ�Token����ע����ͷ����ֱ�Ӷ����δ����Ľ������н�ģ����������δ��������Է�����Ȼ��ͨ�����Բ������ࡣ

![img_1.png](img_1.png)

### ʵ����

���о�ʹ��Hugging Face��Դ��`Transforms`�����ṩ�����ڱ�̺���Ȼ���Ե�Ԥ����ģ��`CodeBERT-base-mlm`���������Ϊ12�㣬ÿ����12����ע��ͷ�����ز�ά����768��ģ�Ͳ���������Ϊ125M������ģ����`CodeSearchNet`�Ĵ������Ͽ������Ԥѵ�������Ĺ��������ֻ��ڴ����޸�ģʽѧϰ��ͨ��ȱ���ھ�ģ��ʹ��AdamW�Ż����Ż���������ز�������Ϊ����_1="0.9" ����_2="0.99" ��?="1e-8" ������Batch����С��Ϊ8��dropoutֵ��Ϊ0.2��`CodeBERT`ģ��ѧϰ����Ϊ "2e-5" ��L2Ȩ��˥��������Ϊ0.01��Ϊ�˱�֤ѵ�����̵��ȶ������Ĳ�����ȼ��ò�����������ݶȷ���Ϊ1�����ڴ����޸�ģʽѧϰ��ͨ��ȱ���ھ򷽷��е�ʵ�����`PyTorch`���ѧϰ��ܣ���NVIDIA GeForce RTX 2060��16G���Կ������ģ��ѵ����ѵ�������в�����ͣ��Early Stopping�����ԣ���ģ������֤��������3��`Epoch`���ܣ���׼ȷ��Ϊָ�꣩û������������ֹѵ�����������֤����������ѵ�ģ�����ڲ��Լ��ϵ�������

ʵ������
![img_2.png](img_2.png)
![img_3.png](img_3.png)