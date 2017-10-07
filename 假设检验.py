import numpy as np
import math
import xlrd
def sumCount(averageX,miu,sita,n):
    return (averageX-miu)/math.sqrt(sita**2/n)
def fetch(a,b):
    return u>=ua
def result(u,ua):
    if fetch(u, ua):
        print("小概率事件发生")
    else:
        print("符合正态分布")
def linjie(x):
    wb=xlrd.open_workbook("标准正态分布表.xlsx")
    sh=wb.sheet_by_index(0)
    row=0
    flag=1
    while row<sh.nrows:
        col = 0
        while col<sh.ncols:
            if x==sh.cell(rowx=row,colx=col).value:
                linjiezhi=sh.cell(rowx=row,colx=0).value+sh.cell(rowx=0,colx=col).value
                flag=0
                break
            col+=1
        row += 1
    if(flag==1):
        linjiezhi=-1
    print("临界值为:{}".format(linjiezhi))
    return linjiezhi
arerfa=0.05
x=[501.8,502.4,499,500.3,504.5,498.2,505.6]
miu=500
sita=2
n=7
u=sumCount(np.mean(x),miu,sita,n)
u=np.abs(u)
ua=linjie(1-arerfa/2)
if(ua==-1):
    print("临界值异常，请重新分配显著性水平")
else:
    result(u,ua)
