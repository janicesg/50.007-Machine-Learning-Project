#Part 2 
#(1) Write a function to evaluate the emission parameters based on data set X and Y

#Input: Directory of files
#Output: X data set and Y data set

def get_XY(datafile_dir):
    f=open(datafile_dir)
    f_content=f.read()
    X = []
    Y = []
    xi = []
    yi = []
    
    for data_pair in f_content.split('\n'):
        
        if data_pair=='':
            X.append(xi)
            Y.append(yi)
            xi = []
            yi = []
            
        else:
            xij,yij = data_pair.split(" ")
            xi.append(xij)
            yi.append(yij)
            
    return (X,Y)

#Input: Dataset X and Y
#Output: Emission parameters based on Dataset X and Y
def train_emission_param(X,Y):
    o_unique = []
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    
    for xi in X:
        
        for o in xi:
            if o not in o_unique:
                o_unique.append(o)
        
    #print (o_unique)
    count_y_dic = {'O':0, 'B-positive':0, 'I-positive':0,'B-negative':0,'I-negative':0,'B-neutral':0,'I-neutral':0}
    count_x_y_dic = {}
    em_dic = {}
    for i in range(len(X)):
        xi = X[i]
        yi = Y[i]
        
        for j in range(len(xi)):
            key = (xi[j],yi[j])
            key_deno = yi[j]
            origin = count_y_dic[key_deno] 
            count_y_dic[key_deno] = origin + 1
            
            if key not in count_x_y_dic:
                count_x_y_dic[key] = 1
            else:
                value = count_x_y_dic[key]
                count_x_y_dic[key] = value + 1
   
    for o in o_unique:
        
        for state in T:
            key = (o,state)
            if key not in count_x_y_dic:
                em_dic[key] = 1/float(count_y_dic[state]+1)#Fix the problem where the word is not in the training set
            else:
                em_dic[key] =float(count_x_y_dic[key])/float(count_y_dic[state])
            print (key, em_dic[key])
    print ('hi')
    
    return em_dic
                
(X,Y)=get_XY('EN/train')
train_emission_param(X,Y)

#Part 2 3) Get the optimal y labels for the x sequence
def evaluate_para(data_file_dir,eval_file_dir):
    X,Y = get_XY(data_file_dir)
    em_dic = train_emission_param()
    


