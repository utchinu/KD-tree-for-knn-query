#There are no beautiful surfaces without a terrible depth

import random as rd
import math
import heapq as hq
import time
import matplotlib.pyplot as plt 

class node:
    def __init__(self):
        self.axis="None"
        self.axis_value=0
        self.p_left=-1
        self.p_right=-1
        self.p_par=-1
        self.data=[]

class root_tree:
    root_node=0
    x_max=-1e18
    x_min=1e18
    y_max=-1e18
    y_min=1e18

nodes=[]
nodes_order=[]
alpha=30
points=[]
nodes_cnt=0
root=root_tree()
k=0
knn=[]

def create_dataset(sz):
    global points
    for i in range(0,sz):
        x=rd.randint(0,400)
        y=rd.randint(0,400)
        point={}
        point['x']=x
        point['y']=y
        point['p_id']=i
        points.append(point)


def create_node(par):
    global nodes,nodes_cnt
    n=node()
    n.p_par=par
    nodes.append(n)
    nodes_cnt+=1

def input_dataset(sz):
    global points
    for i in range(0,sz):
        x=int(input())
        y=int(input())
        point={}
        point['x']=x
        point['y']=y
        point['p_id']=i
        points.append(point)    

def add_input(x,y):
    global points
    point={}
    point['x']=x
    point['y']=y
    point['p_id']=len(points)
    points.append(point)      

def show_tree():
    global nodes_order,nodes
    print("Showing nodes in the order of execution")
    for i in nodes_order:
        print(i,nodes[i].axis,nodes[i].axis_value)

def naive_search(x,y):
    global k,points
    t_points=[]
    for point in points:
        dist=calc_sqrt(point['x'],point['y'],x,y)
        id=point['p_id']
        t_points.append((dist,id))

    t_points=sorted(t_points)
    #print(t_points)
    for i in range(0,k):
        p=t_points[i][1]
        print(points[p]['x'],points[p]['y'])
    
    

def start():
    global points,root,alpha,k,nodes_cnt,nodes,nodes_order,knn
    while(1):
        print("1:Input the dataset")
        print("2:Create the dataset")
        print("3:Build tree")
        print("4:Show tree")
        print("5:Naive query")
        print("6:kd tree query")
        print("7:Get graph of execution time")
        print("Any other number to exit")
        choice=int(input())

        if choice==1:
            points.clear()
            print("Enter size of the dataset")
            sz=int(input())
            input_dataset(sz)
        elif choice==2:
            points.clear()
            print("Enter size of the dataset")
            sz=int(input())
            create_dataset(sz)
        elif choice==3:
            nodes.clear()
            nodes_order.clear()
            nodes_cnt=0
            print("Enter the value of alpha")
            alpha=int(input())
    
            create_node(-1)

            for point in points:
                x=point['x']
                y=point['y']
                root.x_max=max(root.x_max,x)
                root.y_max=max(root.y_max,y)
                root.x_min=min(root.x_min,x)
                root.y_min=min(root.y_min,y)

            build(0,root.x_max,root.x_min,root.y_max,root.y_min)
        elif choice==4:
            show_tree()
        elif choice==5:
            print("Enter the query point(x,y)")
            x=int(input())
            y=int(input())
            print("Enter the value of k")
            k=int(input())
            naive_search(x,y)
        elif choice==6:
            knn.clear()
            print("Enter the query point(x,y)")
            x=int(input())
            y=int(input())
            print("Enter the value of k")
            k=int(input())
            dfs(0,x,y,root.x_max,root.x_min,root.y_max,root.y_min)
            for i in knn:
                print(points[i[1]]['x'],points[i[1]]['y'])                
        elif choice==7:
            print("Enter the value of alpha")
            alpha=int(input())
            k_arr=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,150,180,200,300]
            y_arr=[]
            for each in k_arr:
                k=each
                tot_time=0
                for i in range(1,10000):
                    start_time=time.time()
                    x=rd.randint(0,400)
                    y=rd.randint(0,400)
                    knn.clear()
                    dfs(0,x,y,root.x_max,root.x_min,root.y_max,root.y_min)
                    end_time=time.time()
                    tot_time+=end_time-start_time
                avg_time=tot_time/10000
                y_arr.append(avg_time)
            plt.plot(k_arr,y_arr)
            plt.xlabel('k -values') 
            plt.ylabel('execution time')
            plt.show()
        else:
            break     



def calc_sqrt(px,py,qx,qy):
    return(math.sqrt((px-qx)*(px-qx)+(py-qy)*(py-qy)))

def get_distance(x_max,x_min,y_max,y_min,px,py):
    dist=0
    if (px<=x_min and py<=y_min):
        dist=calc_sqrt(px,py,x_min,y_min)
    elif (px<=x_min and py>=y_max):
        dist=calc_sqrt(px,py,x_min,y_max)
    elif (px>=x_max and py<=y_min):
        dist=calc_sqrt(px,py,x_max,y_min)
    elif (px>=x_max and py>=y_max):
        dist=calc_sqrt(px,py,x_max,y_max)
    elif (py<y_min and px>x_min and px<x_max):
        dist=y_min-py
    elif (py>y_max and px>x_min and px<x_max):
        dist=py-y_max
    elif (px<x_min and py>y_min and py<y_max):
        dist=x_min-px
    elif (px>x_max and py>y_min and py<y_max):
        dist=px-x_max                             

    return(dist)

def build(cur_node,x_max,x_min,y_max,y_min):
    nodes_order.append(cur_node)
    global points,nodes,nodes_cnt,alpha
    points_x=[]
    points_y=[]

    for point in points:
        px=point['x']
        py=point['y']
        if px>=x_min and px<=x_max and py>=y_min and py<=y_max :
            points_x.append(point)
            points_y.append(point)
    
    points_x=sorted(points_x,key=lambda i:i['x'])
    points_y=sorted(points_y,key=lambda i:i['y'])


    if len(points_x) <=alpha:
        #cur node is leaf
        #print("c",cur_node)
        nodes[cur_node].p_left=-1
        nodes[cur_node].p_right=-1
        for i in points_x:
            nodes[cur_node].data.append(i['p_id'])
        return
    
    l=len(points_x)
    d1=points_x[l-1]['x']-points_x[0]['x']
    d2=points_y[l-1]['y']-points_y[0]['y']


    #print(points_x)
    #print(points_y)

    if d1>d2:
        cur=int((l-1)/2)
        while(cur<l)and points_x[cur]['x']==points_x[int((l-1)/2)]['x'] :
            cur+=1
        if cur==l:
            #print("a")
            nodes[cur_node].p_left=-1
            nodes[cur_node].p_right=-1
            for i in points_x:
                nodes[cur_node].data.append(i['p_id'])
            return
        cur-=1
        nodes[cur_node].axis='x'
        nodes[cur_node].axis_value=points_x[cur]['x']
        #print(nodes_cnt)
        create_node(cur_node)
        create_node(cur_node)

        #print("for node",cur_node,"creating 2 child nodes",nodes_cnt-2,nodes_cnt-1,nodes_cnt)

        nodes[cur_node].p_left=nodes_cnt-2
        nodes[cur_node].p_right=nodes_cnt-1

        px=points_x[cur]['x']
        build(nodes[cur_node].p_left,px,x_min,y_max,y_min)
        build(nodes[cur_node].p_right,x_max,px+1,y_max,y_min)

    else:
        cur=int((l-1)/2)
        while(cur<l)and points_y[cur]['y']==points_y[int((l-1)/2)]['y'] :
            cur+=1
        if cur==l:
            #print("b")
            nodes[cur_node].p_left=-1
            nodes[cur_node].p_right=-1
            for i in points_y:
                nodes[cur_node].data.append(i['p_id'])
            return
        cur-=1
        nodes[cur_node].axis='y'
        nodes[cur_node].axis_value=points_y[cur]['y']

        #print(nodes_cnt)
        create_node(cur_node)
        create_node(cur_node)

        nodes[cur_node].p_left=nodes_cnt-2
        nodes[cur_node].p_right=nodes_cnt-1

        #print("for node",cur_node,"creating 2 child nodes",nodes_cnt-2,nodes_cnt-1,nodes_cnt)

        py=points_y[cur]['y']
        build(nodes[cur_node].p_left,x_max,x_min,py,y_min)
        build(nodes[cur_node].p_right,x_max,x_min,y_max,py+1)        

    return


def dfs(cur_node,px,py,x_max,x_min,y_max,y_min):
    global k,points,nodes,knn

    if nodes[cur_node].p_left==-1 and nodes[cur_node].p_right==-1:

        t_points=[]
        for i in nodes[cur_node].data :
            dist=calc_sqrt(px,py,points[i]['x'],points[i]['y'])
            t_points.append((dist,i))
        t_points=sorted(t_points)

        if len(knn)<k:
            index=0
            while(index<len(t_points) and len(knn)<k):
                hq.heappush(knn,(-t_points[index][0],t_points[index][1]))
                index+=1
            while index<len(t_points) and knn[0][0] < -t_points[index][0] :

                hq.heappop(knn)
                hq.heappush(knn,(-t_points[index][0],t_points[index][1]))
                index+=1
        
        else:

            index=0
            while index<len(t_points) and knn[0][0] < -t_points[index][0] :

                hq.heappop(knn)
                hq.heappush(knn,(-t_points[index][0],t_points[index][1]))
                index+=1
        return

    else:
        axis=nodes[cur_node].axis
        axis_value=nodes[cur_node].axis_value

        if axis=="x":
            if px<=axis_value:
                #Left of axis_value
                dfs(nodes[cur_node].p_left,px,py,axis_value,x_min,y_max,y_min)
                #right of axis value    
                dist=get_distance(x_max,axis_value+1,y_max,y_min,px,py)
                if (len(knn)<k) or dist<abs(knn[0][0]):
                    dfs(nodes[cur_node].p_right,px,py,x_max,axis_value+1,y_max,y_min)
            else:
                #Right of axis value
                dfs(nodes[cur_node].p_right,px,py,x_max,axis_value+1,y_max,y_min)
                #left of axis value
                dist=get_distance(axis_value,x_min,y_max,y_min,px,py)
                if (len(knn)<k) or dist<abs(knn[0][0]):
                    dfs(nodes[cur_node].p_left,px,py,axis_value,x_min,y_max,y_min)

        else:
            if py<=axis_value:
                #left of axis value
                dfs(nodes[cur_node].p_left,px,py,x_max,x_min,axis_value,y_min)
                #right of axis value
                dist=get_distance(x_max,x_min,y_max,axis_value+1,px,py)
                if (len(knn)<k) or dist <abs(knn[0][0]):
                    dfs(nodes[cur_node].p_right,px,py,x_max,x_min,y_max,axis_value+1)

            else:
                #right of axis value
                dfs(nodes[cur_node].p_right,px,py,x_max,x_min,y_max,axis_value+1)
                #left of axis value
                dist=get_distance(x_max,x_min,axis_value,y_min,px,py)
                if (len(knn)<k) or dist <abs(knn[0][0]):
                    dfs(nodes[cur_node].p_left,px,py,x_max,x_min,axis_value,y_min)

    return                                                


start()