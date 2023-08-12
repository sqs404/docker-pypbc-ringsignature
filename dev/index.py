stored_params = """type a
q 8780710799663312522437781984754049815806883199414208211028653399266475630880222957078625179422662221423155858769582317459277713367317481324925129998224791
h 12016012264891146079388821366740534204802954401251311822919615131047207289359704531102844802183906537786776
r 730750818665451621361119245571504901405976559617
exp2 159
exp1 107
sign1 1
sign0 1
"""
from pypbc import *
import time
import warnings
warnings.filterwarnings("ignore")#忽略警告（pypbc库由于一些问题会提示警告，不影响正常使用）
p=160
q=128
t1 = time.time()
params = Parameters(qbits=p,rbits=q)	# type a
# params = Parameters(param_string=stored_params)	# type a
pairing = Pairing(params)  #实例化双线性对对象
def hash2(point):
    tmp=point[0]^point[1]
    tmp2=str(tmp)
    hashmes=Element.from_hash(pairing,Zr,tmp2)
    return hashmes
def PKIsetup(g,s,pkm):#PKI系统参数生成
    print('PKI参数生成')
    xs=Element.random(pairing,Zr)
    sks=Element(pairing,G1,value=g**pow(xs,-1))
    pks=Element(pairing,G1,value=g**xs)
    return pks,sks
def IBCsetup(g,s,pkm):#IBC系统参数生成
    print('IBC参数生成')
    hashid=Element.from_hash(pairing,Zr,'IDibc')
    sks=Element(pairing, G1, value=g**pow(hashid+s,-1))
    pks=Element(pairing,G1,value=g**hashid+pkm)
    return pks,sks
def CLCsetup(g,s,pkm):#CLC系统参数生成
    print('CLC参数生成')
    hashid = Element.from_hash(pairing, Zr, 'IDclc')
    xs = Element.random(pairing, Zr)
    ds=Element(pairing, G1, value=g**pow(hashid+s,-1))
    dptmp=Element(pairing,G1,value=g**hashid+pkm)
    dp=Element(pairing,G1,value=dptmp**xs)

    hashdp=hash2(dp)

    sks=Element(pairing,G1,value=ds**pow(hashdp+xs,-1))
    pks=Element(pairing,G1,value=dptmp**hashdp+dp)
    return pks,sks
def signature(g,m,sks,num,L,pkl):
    k=[]
    vi=[]

    for i in range(num):#随机生成一堆随机shu
        cir = Element.random(pairing, Zr)
        k.append(cir)
    for i in range(num):#计算除去s的所有vi
        vtmp=Element(pairing,G1,g**k[i])
        vi.append(vtmp)
    rs=Element.random(pairing,Zr)
    tmp1u=pairing.apply(g,g)#计算得到g
    tmp2u=Element(pairing,GT,value=pow(tmp1u,rs))#通过计算得到g^r
    tmp3u = pairing.apply(vi[0], pkl[0])
    for i in range(1,num):#循环计算得到双线性对连乘
        tmp3u=Element(pairing,GT,value=tmp3u*pairing.apply(vi[i],pkl[i]))
    u=Element(pairing,GT,value=tmp2u*tmp3u)#最终经过计算得到u

    tmph=str(m)+L+str(u)
    h=Element.from_hash(pairing,Zr,tmph)
    vs=Element(pairing,G1,value=sks**(h+rs))
    vi.append(vs)

    signmes=[vi,u]
    return signmes
def verify(g,m,signmes,num,L,pkl):
    u=signmes[1]
    vi=signmes[0]
    tmph=str(m)+L+str(u)
    h=Element.from_hash(pairing,Zr,tmph)
    e1tmp=pairing.apply(vi[0],pkl[0])
    for i in range(1,num):
        e1tmp=Element(pairing,GT,value=e1tmp*pairing.apply(vi[i],pkl[i]))
    e1=e1tmp
    e2tmp=Element(pairing,GT,value=pow(pairing.apply(g,g),h))
    e2=Element(pairing,GT,value=u*e2tmp)

    # print(e1)
    # print(e2)
    if e1==e2:
        print('Ture：签名正确')
    else:
        print('False：签名错误')

if __name__ == '__main__':

    print('系统建立')  # 系统建立
    m='sqs 的 ringsignature'
    num=10#随机生成num个公钥用作测试(三种加密方式公钥的形式是一样的，这里就随机生成num个这种形式的公钥)
    g = Element.random(pairing, G1)#随机选取一个基点
    s=Element.random(pairing,Zr)
    pkm=Element(pairing,G1,value=g**s)
    #下边的三种系统参数任选，选哪个就调哪个函数
    # pks,sks=PKIsetup(g,s,pkm)
    pks,sks=IBCsetup(g,s,pkm)
    # pks,sks=CLCsetup(g,s,pkm)

    pkl=[]#num个pk构成的一个列表
    L=''#num个pk构成的一个字符串
    for i in range(num):#随机生成一堆公钥（num个）
        cir = Element.random(pairing, G1)
        pkl.append(cir)
        L=L+str(cir)
    L=L+str(pks)#将选定的公钥pks加入L和pkl
    pkl.append(pks)

    print('准备开始签名')
    sigmes=signature(g,m,sks,num,L,pkl)
    print('签名内容:',sigmes)
    print('准备开始验证签名')
    verify(g,m,sigmes,num+1,L,pkl)#num+1表示除了随机生成的还有1个系统提供的真实密钥
    print('验证结束')
    #输出Ture代表验证正确


    cmpbytes=0
    for i in range(num+1):
        cmpbytes=len(str(sigmes[0][i]).encode())+cmpbytes
    cmpbytes = len(str(sigmes[1]).encode()) + cmpbytes
    cmpbytes=len(m.encode())+cmpbytes
    cmpbits=cmpbytes*8
    print(cmpbits)
t2=time.time()
print(t2-t1)
