from pyamaze import *
m=15
n=10
a=maze(m,n)
# a.CreateMaze(m,n,loadMaze='maze--2023-03-30--18-11-10.csv')
a.CreateMaze(m,n, loopPercent=100)
bb=agent(a,1,1,shape='arrow',footprints=True,color='yellow')

dic=a.maze_map
# print(dic)
from random import *
Total_population=500
Choromosomes=n-2
fit,inf=0,0
WL,WT,WF=2,2,3
sol=0
iterations=0

def Turns(x):
    turns=0
    for j in range ((n)-1):        
        if x[j]!=x[j+1]:
            turns+=1
    return turns
def Population(x):
    y=[]
    z= [randint(1,m)  for _ in range (x)]
    z.insert(0,1) ; z.append(m)
    direc_bit= [randint(0,1) for _ in range (2)]
    c=Turns(z) ; y=[z]+[direc_bit]
    return y,c
def Solution_found(x):
    for i in range(Total_population):
        if (x[i]==0):
            return 1
        else:
            return 0

def infeasible_steps(x):
    path=[]
    path.append((1,1))
    if m!=n:
        direction[0]=0
    select= direction[0] ^ direction[1]
    a,k,inf=(1,1),1,0
    for g in range(len(pop)-1):
        y=g+1
        Boundary=(pop[g+1]+1) if pop[g+1] >pop[g] else (pop[g+1]-1)
        while k!=Boundary:
            if direction[0]==0:
                b=(k,y+select)
            else:
                b=(y+select,k)
            if b not in ((1,1),(m,n)):
                path.append(b)
                if b[0]-a[0]!=0:
                    if b[0]-a[0]>0:
                        if dic[a]["S"]==0:
                            inf+=1
                    else:
                        if dic[a]['N']==0:
                            inf+=1
                elif b[1]-a[1]!=0:
                    if b[1]-a[1]>0:
                        if dic[a]["E"]==0:
                            inf+=1
                    else:
                        if dic[a]['W']==0:
                            inf+=1
            a=b
            if pop[g+1]>pop[g]:
                k+=1
            else:
                k-=1
        if pop[g+1]>pop[g]:
            k-=1
        else:
            k+=1     
    path.append((m,n))
    # print(path)
    return inf,path,len(path)
def fit(x,y,z):
    inf_min=0
    fitt=[]
    for i in range(Total_population):
        fitness=0
        f_t=1-(y[i]-min(y))/(max(y)-min(y))
        f_l=1-(z[i]-min(z))/(max(z)-min(z))
        f_inf=1-(x[i]-inf_min)/(max(x)-inf_min)
        fitness=(100*WF*f_inf)*((WL*f_l)+(WT*f_t))/(WL+WT)
        fitt.append(fitness)
    return fitt

def Mutation(x):
    a=[]
    for i in range(int(Total_population/2),Total_population):
        Chr=x[i]
        new_ind=randint(1,n-2)
        new_chr=randint(1,m)
        Chr[new_ind]=new_chr
        a.append(Chr)
    return a
    
def Cross_over(x):
    chr = x
    cross_point= randint(2,n-2)
    # print(cross_point)
    halfOf_pop =int(Total_population/2)
    for i in range(halfOf_pop):
        x[i+halfOf_pop][:cross_point] = x[i][:cross_point]      
        x[i+halfOf_pop][cross_point:], x[i][cross_point:] = x[i][cross_point:], x[i+halfOf_pop][cross_point:]
    return x
while(iterations < 10000):
    print(f'Generations: {iterations}')
    # i,Flag=0,0
    # while(i==iterations and Flag==0):
    infeasible_step,path,turns,pp,all_path=[],[],[],[],[]
    for _ in range(Total_population):
            aa,e=Population(Choromosomes)
            # print(aa)
            # pop,dir=a
            pop,direction=aa
            pp.append(aa)
            # print(p)
            b=infeasible_steps(aa)
            # print(b[1],b[2])
            infeasible_step.append(b[0]) ; path.append(b[2]) ; turns.append(e) ; all_path.append(b[1])
            # print(b[1])
    # print(pp)
    # print(c)
    # print(f"\n\n{all_path}")
    # print(f)
    # print(p)
    # path1=p

    Actual_fitness=fit(infeasible_step,turns,path)
    
    z=list(zip(pp,infeasible_step))
    d=sorted(z,key= lambda x: x[1])
    y=list(zip(all_path,infeasible_step))
    sorted_path=sorted(y,key= lambda x: x[1])
    
    # "pp" after buble sorting is "pop"
    sort_pop=[x[0] for x in d ]
    # print(sort_pop)
    sort_inf=[x[1] for x in d ]
    sort_path=[x[0] for x in sorted_path ]
    # print(f"\n\n{pop}")
    # print(f"\n\n{sort_inf}")
    # print(f"\n\n{sort_path}")

    chr=[dd for dd,ee in sort_pop]
    # print(cc)
    direction_bits=[ee for dd,ee in sort_pop]
    # print(ff)
    # print(Solution_found(infeasible_steps))
    s = Solution_found(sort_inf)
    # print(s)
    sol_path = sort_path[0]
    if s==1:
        break
    g=Cross_over(chr)
    # print(g)
    muted_chromosomes=Mutation(g)
    # print(ww)
    iterations += 1
    with open('data_3.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([min(infeasible_step), min(turns),min(path),max(Actual_fitness),iterations])
if s==1:
    a.tracePath({bb:sol_path})
    a.run()
else:
    print('Solution not found!')
#endProgram