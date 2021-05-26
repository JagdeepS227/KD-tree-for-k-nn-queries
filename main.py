import csv
import random
from collections import deque
import math
import time
Null=None
class Root_Node:
    def __init__(self,x_max=0,x_min=0,y_max=0,y_min=0,split_axis='x',split_value=0):
        self.x_max=x_max
        self.x_min=x_min
        self.y_max=y_max
        self.y_min=y_min
        self.split_axis=split_axis
        self.split_value=split_value
        self.right=Null
        self.left=Null
        self.leaf=Null


class Internal_Node:
    def __init__(self,split_axis='x',split_value=0,which_child='r'):
        self.split_axis=split_axis
        self.split_value=split_value
        self.parent=Null
        self.which_child=which_child
        self.right=Null
        self.left=Null


class Leaf_Node:
    def __init__(self,data_arr,num_data_points=1):
        self.num_data_points=num_data_points
        self.data_arr=data_arr
        self.parent=Null



###############   RETURNS 1 FOR Y-AXIS AND 0 FOR X-AXIS 
def find_widest_spread_axis(arr):
    x_arr=[]
    y_arr=[]
    for i in arr:
        x_arr.append(i[0])
        y_arr.append(i[1])
    x_arr.sort()
    y_arr.sort()
    x_dif=x_arr[-1]-x_arr[0]
    y_dif=y_arr[-1]-y_arr[0]
    if x_dif>=y_dif:
        return 0
    return 1


#
def select_median(arr_temp,n):
    #print(type(n))
    arr_temp.sort()
    if n % 2==1:
        return arr_temp[int(n//2)+1]
    else:
        #print(n)
        return arr_temp[int(n/2)]

def find_rectangle_enclosing_data(arr):
    x_arr=[]
    y_arr=[]
    for i in arr:
        x_arr.append(i[0])
        y_arr.append(i[1])

    x_arr.sort()
    y_arr.sort()
    return x_arr[-1],x_arr[0],y_arr[-1],y_arr[0]


################################### KD TREE CLASS #####################################


class KD_TREE:
    def __init__(self):
        self.root=Null
        self.number_points_in_tree=0
        self.height=0
        self.flag_hash={}
        
    def build_recur(self,inp_arr,alpha):
        self.root=self.kd_build_recursive(Null,inp_arr,0,alpha,'left')

        
    def kd_build_recursive(self,current_node,arr,depth,alpha,which_child):
        if len(arr)<=alpha and depth>0:
            node2=Leaf_Node(arr,len(arr))
            node2.parent=current_node        
            self.flag_hash[node2]=False        
            if depth>self.height:
                self.height=depth
            return node2
        elif len(arr)<=alpha and depth==0:
            x_max,x_min,y_max,y_min=find_rectangle_enclosing_data(arr)
            node2=Root_Node(x_max,x_min,y_max,y_min)
            self.flag_hash[node2]=False
            node3=Leaf_Node(arr,len(arr))
            self.flag_hash[node3]=False
            node3.parent=node2
            node2.leaf=node3
            return node2
        else:
            #axis=0 means X-AXIS     x=1 means Y-AXIS 
            
            axis=find_widest_spread_axis(arr)
            temp=[]
            
            for point in arr:
                temp.append(point[axis])
            
            median=select_median(temp,len(temp))
            #dividing points into left and right partition
            left_temp=[]
            right_temp=[]
            for point in arr:    
                if point[axis] >= median:
                    right_temp.append(point)
                if point[axis] < median:
                    left_temp.append(point)
            if len(left_temp)==len(arr) and depth>0 :
                node2=Leaf_Node(left_temp,len(left_temp))

                if depth>self.height:
                    self.height=depth
                return node2
            if len(right_temp)==len(arr) and depth>0 :
                node2=Leaf_Node(right_temp,len(right_temp))            
                if depth>self.height:
                    self.height=depth
                return node2
                


            if depth==0:
                if len(left_temp)==len(arr) :
                    node2=Root_Node(x_max,x_min,y_max,y_min)
                    self.flag_hash[node2]=False
                    node2.split_axis=axis
                    node2.split_value=median
                    node3=Leaf_Node(left_temp,len(left_temp))

                    if depth>self.height:
                        self.height=depth
                    return node2
                if len(right_temp)==len(arr) :
                    node2=Root_Node(x_max,x_min,y_max,y_min)
                    self.flag_hash[node2]=False
                    node2.split_axis=axis
                    node2.split_value=median
                    node3=Leaf_Node(right_temp,len(right_temp))
                
                    if depth>self.height:
                        self.height=depth
                    return node2

                x_max,x_min,y_max,y_min=find_rectangle_enclosing_data(arr)
                node2=Root_Node(x_max,x_min,y_max,y_min)
                self.flag_hash[node2]=False
                node2.split_axis=axis
                node2.split_value=median
                
                
                if left_temp!=[]:
                    #print(left_temp)
                    node2.left=self.kd_build_recursive(node2,left_temp,depth+1,alpha,'left')
                if right_temp !=[]:
                    node2.right=self.kd_build_recursive(node2,right_temp,depth+1,alpha,'right')
                return node2

            middle_node=Internal_Node(axis,median,which_child)
            self.flag_hash[middle_node]=False
            middle_node.parent=current_node
            if left_temp != []:
                #print(left_temp)
                middle_node.left = self.kd_build_recursive(middle_node,left_temp,depth + 1,alpha,'left')
            if right_temp != []:
                middle_node.right = self.kd_build_recursive(middle_node,right_temp,depth + 1,alpha,'right')

            return middle_node
            
def distance_btw_points(p1,p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

def find_k_est_closestpts(point,k,arr,est_pts):
    
    if est_pts!=[] :
        for x in est_pts:
            arr.append(x)
        arr.sort( key = lambda p: math.sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2) )
        if len(arr)>=k:
            return arr[:k]
        else:
            return arr
    
    arr.sort(key = lambda p: math.sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2) )
    if len(arr)>=k:
        return arr[:k]
    else:
        return arr
        

def traversetree_find_estimation_points(tree,root_node,point,k,est_pts):
    if root_node in tree.flag_hash and isinstance(root_node,Internal_Node):
        tree.flag_hash[root_node]=True
    if isinstance(root_node,Leaf_Node):
        
        return find_k_est_closestpts(point,k,root_node.data_arr,est_pts),root_node

    if root_node.split_value<point[root_node.split_axis]:
        rs=traversetree_find_estimation_points(tree,root_node.right,point,k,est_pts)
        return rs
    else:
        rs=traversetree_find_estimation_points(tree,root_node.left,point,k,est_pts)
        return rs
    

def calculate_area_backtracking(node,flag,area):
    if isinstance(node,Root_Node):
        if False in flag:
            if flag[0]==False:
                area[0]=int(node.x_max)
                flag[0]=True             
            if flag[1]==False:
                area[1]=int(node.x_min)
                flag[1]=True             
            if flag[2]==False:
                area[2]=int(node.y_max)
                flag[2]=True             
            if flag[3]==False:
                area[3]=int(node.y_min)
                flag[3]=True             
    else:
        parent_node2=node.parent
        if isinstance(parent_node2,Root_Node):
            return calculate_area_backtracking(parent_node2,flag,area)
        if False in flag:
            if parent_node2.split_axis==0 and parent_node2.which_child=='left' and flag[0]==False:
                area[0]=int(parent_node2.split_value)
                flag[0]=True             
            elif parent_node2.split_axis==0 and parent_node2.which_child=='right' and flag[1]==False:
                area[1]=int(parent_node2.split_value)
                flag[1]=True
            elif parent_node2.split_axis==1 and parent_node2.which_child=='left' and flag[2]==False:
                area[2]=int(parent_node2.split_value)
                flag[2]=True
            elif parent_node2.split_axis==1 and parent_node2.which_child=='right' and flag[3]==False:
                area[3]=int(parent_node2.split_value)
                flag[3]=True
            return calculate_area_backtracking(parent_node2,flag,area)
    return area

def go_down_node(area,point,est_pts):
    min_dis_area_pt=0
    x=abs(point[0]-area[0])
    if abs(point[0]-area[1])<x:
        x=abs(point[0]-area[1])
    y=abs(point[1]-area[2])
    if abs(point[1]-area[3])<y:
        y=abs(point[1]-area[3])
    if abs(point[0]-area[0])+abs(point[0]-area[1])!=abs(area[0]-area[1]) and abs(point[1]-area[2])+abs(point[1]-area[3])!=abs(area[2]-area[3]):
        min_dis_area_pt=math.sqrt((x**2)+(y**2))
    else:
        if x<y:
            min_dis_area_pt=x
        else:
            min_dis_area_pt=y
    est_pts.sort(key = lambda p: math.sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2) )
    if math.sqrt((est_pts[-1][0]-point[0])**2+(est_pts[-1][1]-point[1])**2)>min_dis_area_pt:
        return True
    return False


def backtrack(tree,est_pts,node,k,point):
    #print(type(node))

    if  isinstance(node,Leaf_Node):
        #print("P")
        if  tree.flag_hash[node]==False :
            est_pts=find_k_est_closestpts(point,k,node.data_arr,est_pts)
            #print(est_pts,"HJ")
            tree.flag_hash[node]=True
            n1=node.parent
            fg=0
            if n1.left!=Null and n1.right!=Null:
                if (tree.flag_hash[n1.left] and tree.flag_hash[n1.right]):
                    tree.flag_hash[n1]=True
            if n1.left==Null and n1.right!=Null:
                if tree.flag_hash[n1.right]==True:
                    tree.flag_hash[n1]=True
            if n1.right==Null and n1.left!=Null:
                if tree.flag_hash[n1.left]==True:
                    tree.flag_hash[n1]=True
                    
            return backtrack(tree,est_pts,node.parent,k,point)
        else:
            return backtrack(tree,est_pts,node.parent,k,point)
    else:
        flag=[False,False,False,False]
        area=[0,0,0,0]
        est_pts=res
        node_area=calculate_area_backtracking(node,flag,area)

        if go_down_node(node_area,point,est_pts) and not isinstance(node,Leaf_Node) and tree.flag_hash[node]==False:
            #print("KLK")
            if isinstance(node,Root_Node) and tree.flag_hash[node.left]==True and  tree.flag_hash[node.right]==True:            
                #print("NN")
                

                return est_pts
            flg=0
            if node.left in tree.flag_hash.keys():
                flg=1
                if tree.flag_hash[node.left]==False:
                    #print("II")
                    return backtrack(tree,est_pts,node.left,k,point)
                

            if node.right in tree.flag_hash.keys() :
                if tree.flag_hash[node.right]==False:
                    #print("K")
                    #print(est_pts)
                    tree.flag_hash[node]=True
                    return backtrack(tree,est_pts,node.right,k,point)
                else:
                    n1=node.parent
                    fg=0
                    if n1.left!=Null and n1.right!=Null:
                        if (tree.flag_hash[n1.left] and tree.flag_hash[n1.right]):
                            tree.flag_hash[n1]=True
                    if n1.left==Null and n1.right!=Null:
                        if tree.flag_hash[n1.right]==True:
                            tree.flag_hash[n1]=True
                    if n1.right==Null and n1.left!=Null:
                        if tree.flag_hash[n1.left]==True:
                            tree.flag_hash[n1]=True
                    tree.flag_hash[node]=True
                    return backtrack(tree,est_pts,node.parent,k,point)
            else:
                if isinstance(node,Root_Node):
                    #print("UUU")
                    return est_pts
                
                return backtrack(tree,est_pts,node.parent,k,point)
        else:
            if isinstance(node,Root_Node):
                
                #print("KK")

                return est_pts
            #print("OO")
            tree.flag_hash[node]=True
            return backtrack(tree,est_pts,node.parent,k,point)
        #print("HEre")
        return est_pts

    

def KN_query_algo(tree,root_node,point,k):
    est_pts,node_leaf=traversetree_find_estimation_points(tree,root_node,point,k,[])
    est_pts.reverse()
    #print(est_pts)
    est_pts=backtrack(tree,est_pts,node_leaf.parent.parent,k,point)
    #print(est_pts)
    return est_pts


def naive_query(arr,point,k):
    res=find_k_est_closestpts(point,k,arr,[])
    print(res,"Y")
    return res






def show_tree(nd):
    
    print(nd.left)
    print(nd.left.left)
    print(nd.left.right)
    print(nd.right)
    print(nd.leaf)
        
    print("###################")
        
    q = deque()
    q.append(nd)
    print(nd)
    while q:
        print("W")
        node = q.popleft()
        #print(node)
        if isinstance(node,Leaf_Node):            
            print(node.data_arr,"  ")
        else:
            print("split-V",node.split_value,"   split-axis: ",node.split_axis)
        if not isinstance(node,Leaf_Node):
            print("Q")
            if node.left:
                q.append(node.left )
            if  node.right:
                q.append(node.right)







def do_match(arr1,arr2):
    for i in arr1:
        if i not in arr2:
            return False
    return True







def createRandomSortedList(num, start = 1, end = 100): 
    arr = [] 
    tmp = random.randint(start, end) 
    for x in range(num): 
        while tmp in arr: 
            tmp = random.randint(start, end) 
        arr.append(tmp) 
    arr.sort() 
    return arr 


def generate_data():
    print("Enter number of records you want to generate ")
    n=int(input())
    print("Enter name for output file (without extension)")
    name=input()
    writer = csv.writer(open(name+'.csv', 'w'))
    x=["id","x-coordinate","y-coordinate"]
    writer.writerow(x)
    lsa=createRandomSortedList(n,1,n)
    for a in lsa:
        x=random.randint(0,400)
        y=random.randint(0,400)
        sd=[a,x,y]
        writer.writerow(sd)
    print("File "+name+".csv created successfully !!")




def read_data():
    print("Enter name of csv file with extension:")
    name=input()
    try:
        reader = csv.reader(open(name, 'r'))
    except:
        print("Ooops No such file Exist !!!")
        print('\n')
        add_records_csv()
    i=0
    rec=[]
    for row in reader:
        if i>0:
            xc=(int(row[1]),int(row[2]))
            rec.append(xc)
        else:
            i=i+1
    return rec


#generate_data()
#pts=[(1,2),(4,5),(7,8),(1,9),(2,10)]
rce=read_data()
alfa=100
res=naive_query(rce,(8,5),alfa)
strt_time=time.time()
tree=KD_TREE()
tree.number_points_in_tree=len(rce)
#print("Enter value of k")
#k=int(input())
tree.build_recur(rce,8)

nd=tree.root
#show_tree(nd)
#show_tree(nd)
points=KN_query_algo(tree,nd,(80,90),100)
time_dif=time.time()-strt_time
print(points,"WWWW")
print(res,"RRRR")
print(do_match(points,res))
print("time: ",time_dif)
