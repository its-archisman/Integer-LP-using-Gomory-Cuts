from fractions import Fraction as fr
from copy import deepcopy
import numpy as np
from time import time
def printlist_vec(a):
    for i in range(len(a)):
        print(a[i],end=" ")
    print()
def printlist(a):
    for i in range(len(a)):
        for j in range(len(a[0])):
            print(a[i][j],end=" ")
        print()
def simplex(a,x_basic):    # a is the entire tableau (numpy array). Note: Every element should be in float
    # m = no. of rows-1
    # n = no. of columns-1
    # x_basic stores the indexes of the basic variables (0-indexed), ie if x0, x3, x4 are in the basis, x_basic=[0,3,4]
    # a[0,0] stores the cost
    # the entire first column, ie a[1,0] to a[m,0] stores the basic variables
    # the first row stores the values of reduced costs (all of which has to be omade non-negative)
    # print(a)
    m=len(a)-1
    n=len(a[0])-1
    rc=a[0,1:]  # Stores the reduced costs
    while not (rc>=0).all():
        # print(a)
        store=0
        for i in range(len(rc)):
            if rc[i]<0:
                store=i
                break
        pivot=[float('inf'),store+1]   # Pivot index
        
        min=float('inf')
        for i in range(1,m+1):  # Iterates in [1, 2, ..., m+1]
            if a[i,pivot[1]]<=0:
                continue
            k=a[i,0]/a[i,pivot[1]]
            if k<min:
                min=k
            min_ind=float('inf')
            # Now by bland's rule, we need to identify the variable with the minimum index.
            for i in range(1,m+1):
                if a[i,pivot[1]]<=0:
                    continue
                if a[i,0]==a[i,pivot[1]]*min and x_basic[i-1]<min_ind:
                    pivot[0]=i
                    min_ind=x_basic[i-1]
                
        # Now we have the pivot index
        x_basic[pivot[0]-1]=pivot[1]-1

        # Now doing the row operations
        a[pivot[0]]=a[pivot[0]]/a[pivot[0],pivot[1]]
        for i in range(0,m+1):
            if i==pivot[0]:
                continue
            a[i]=a[i]-a[i,pivot[1]]*a[pivot[0]]
        rc=a[0,1:]
    return [a,x_basic]
def dual_simplex(a,x_basic):
    m=len(a)-1
    n=len(a[0])-1
    rc=a[1:,0]
    while not (rc>=0).all():
        # print(a)
        store=0
        for i in range(len(rc)):
            if rc[i]<0:
                store=i
                break
        pivot=[store+1,float('inf')]   # Pivot index
        
        min=float('inf')
        for i in range(1,n+1):  # Iterates in [1, 2, ..., m+1]
            if a[pivot[0],i]>=0:
                continue
            k=a[0,i]/abs(a[pivot[0],i])
            if k<min:
                min=k
                pivot[1]=i
            if min==float('inf'):
                break
        x_basic[pivot[0]-1]=pivot[1]-1

        # Now doing the row operations
        a[pivot[0]]=a[pivot[0]]/a[pivot[0],pivot[1]]
        for i in range(0,m+1):
            if i==pivot[0]:
                continue
            a[i]=a[i]-a[i,pivot[1]]*a[pivot[0]]
        rc=a[1:,0]
    # printlist(a)
    return [a,x_basic]
def gomory(input):
    # Taking input from file and setting up the problem
    lst=[]
    with open(input, 'r') as f:
        for line in f:
            # process each line here
            lst.append([int(i) for i in line.split()])
    
    b=lst[1]
    m=len(b)
    c=np.array(lst[2])
    n=len(c)
    N=n
    a=[]
    for i in range(3,3+m):
        a.append(lst[i])
        a[i-3]=[fr(x,1) for x in a[i-3]]
    # printlist(a)
    # return
    temp=[fr(0)]*m
    c=[-i for i in c]
    c=np.append(c,temp)
    for i in range(0,m):
        temp[i]=fr(1)
        for _ in temp:
            a[i].append(_)
        temp[i]=0
    for i in range(len(b)):
        if b[i]<0:
            b[i]*=-1
            a[i]=[-1*x for x in a[i]]
    n+=m
    # printlist(a)
    # return
    intial_arr=deepcopy(a)
    # Now adding the m auxiliary variables
    temp=[fr(0)]*m
    c=np.append(c,temp)
    for i in range(0,m):
        temp[i]=fr(1)
        for _ in temp:
            a[i].append(_)
        temp[i]=fr(0)
    a=np.array(a)

    aux_index=list(range(n,n+m))
    aux_cost=np.array([fr(0)]*(n+m))
    for i in range(m):
        aux_cost[n+i]=fr(1)
    aux_cb=np.array([fr(1)]*m)     # We have the auxiliary cost vector

    table=[]    # This tableau will have m+1 rows and n+1 columns
    for i in range(m+1):
        lst=[fr(0)]*(n+m+1)
        table.append(lst)
    table=np.array(table)
    table[0,0]=-np.matmul(aux_cb,np.transpose(b))
    table[0,1:]=aux_cost-np.matmul(aux_cb,a)
    table[1:,0]=np.transpose(b)
    table[1:,1:]=a
    t_index=deepcopy(aux_index)
    result=simplex(table,t_index)
    cb_i=deepcopy(result[1])
    
    for point in range(len(result[1])): 
        
        if result[1][point] in aux_index:
            flag=-1
            printlist(table)
            # An auxiliary variable is still there in the basis
            for _ in range(0,n):
                if table[point+1][_+1]!=0:
                    flag=_+1
                    break
            if flag!=-1:
                pivot=[point+1,flag]  # Selecting the new pivot
                # print("Pivot",pivot)
                cb_i[pivot[0]-1]=pivot[1]-1
                # print("Hello")
                # Now doing the row operations
                table[pivot[0],:]=table[pivot[0],:]/table[pivot[0],pivot[1]]
                for i in range(0,len(table[0])):
                    
                    if i==pivot[0]:
                        continue
                    table[i,:]=table[i,:]-table[i,pivot[1]]*table[pivot[0],:]
            else:
                temp=[]
                # The constraint is a redundant one and can be moved out
                for p in range(len(table)):
                    if p==point+1:
                        continue
                    lst=[]
                    for q in range(len(table[0])):
                        if q==result[1][point]+1:
                            continue
                        lst.append(table[p][q])
                    temp.append(lst)
                table=np.array(temp)
                cb_i.pop(point)
    
    table=table[0:,0:n+1]
    c=c[0:n]
    # print("\nAfter driving out method finishes. Indexes of basis= ",cb_i)
    # printlist(table)
    a=intial_arr
    xB=[fr(0)]*(len(cb_i))
    cb=[fr(0)]*(len(cb_i))
    for i in range(len(cb_i)):
        xB[i]=table[i+1,0]
        cb[i]=c[cb_i[i]]
    xB=np.array(xB)
    # print(xB)
    # return
    A=table[1:,1:]
    # print(BA)
    table[0,0]=-np.matmul(cb,np.transpose(xB))
    table[0,1:]=c-np.matmul(cb,A)
    # printlist(table)
    simplex(table,cb_i)
    print("\nTableau with initial solution. Indexes of basis= ", cb_i)
    printlist(table)
    row=1
    count=0
    while row<len(table):
        # if table[row,0]%1==0:   # If a variable is integral
        #     row+=1
        #     continue
        max=0
        for i in range(1,len(table)):
            val=table[i,0]%1
            if val>max:
                row=i
                max=val
        if max==0:
            break
        # Now we have a row which is a cut
        temp=deepcopy(table)
        temp=temp.tolist()
        for _ in range(0,len(temp)):
            temp[_].append(0)
        # printlist(temp)
        lst=[fr(0)]*(n+2)
        for j in range(0,len(table[0])):
            lst[j]=-(table[row,j]%1)
        lst[n+1]=fr(1)
        # lst[0]=-(table[row,0]%1)
        temp.append(lst)
        table=np.array(temp)
        cb_i.append(n)
        # print("Reduced costs ",float(table[0,0]))
        dual_simplex(table, cb_i)
        n+=1
        row=1
        if count%100==0:
            print(count)
            print(float(table[0][0]))
        count+=1
    
    optimal_v=[0]*N
    for i in range(len(cb_i)):
        if cb_i[i]<N:
            optimal_v[cb_i[i]]=int(table[1+i,0])
    # print("\nFinal tableau. Index of basis=",cb_i)
    # printlist(table)
    # # printlist()
    # print("\nOptimal solution=",optimal_v,"\nOptimal cost=",int(table[0,0]))
    # print("No. of cuts= ",count)
    return optimal_v

st=time()
print(gomory("input.txt"))
print("\nTime taken= ",time()-st)
