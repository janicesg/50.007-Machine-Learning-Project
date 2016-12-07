#PART 2 code here
# For testing, scroll down to the last part, uncomment the output_prediction lines, and change the parameters accordingly.



#####################################################################
#Input: Directory of files (datafile_dir)
#Output: X data set and Y data set (X,Y)
import math
def get_XY(datafile_dir):
    f = open(datafile_dir, encoding = "utf-8")
    f_content = f.read()
    X = []
    Y = []
    xi = []
    yi = []
    
    for data_pair in f_content.split('\n'):
        
        if data_pair == '':
            if xi != []:
                X.append(xi)
                Y.append(yi)
                xi = []
                yi = []
            
        else:
            xij,yij = data_pair.split(" ")
            xi.append(xij)
            yi.append(yij)
            
    return (X,Y)
#####################################################################
#Helper function: Get X sequence from a file
#Input: Directory of a file (datafile_dir)
#Output: Array of X sequences (X)
def get_X(datafile_dir):
    f = open(datafile_dir, encoding = "utf-8")
    f_content = f.read()
    X = []
    xi = []
    for data in f_content.split('\n'):
        
        if data == '':
            if (xi != []):
                X.append(xi)
                xi = []
        else:
            xij = data
            xi.append(xij)
    return X


#####################################################################
#Input: Dataset X and Y (X,Y)
#Output: Emission parameters based on Dataset X and Y( em_dic, count_y_dic)
def train_emission_param(data_file_dir):
    X,Y =get_XY(data_file_dir)
    o_unique = []
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    
    for xi in X:
        
        for o in xi:
            if o not in o_unique:
                o_unique.append(o)
   
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
                em_dic[key] = 0
            else:
                em_dic[key] =float(count_x_y_dic[key])/float(count_y_dic[state]+1)
    em_dic[1] = count_y_dic
    return (em_dic)
#train_emission_param('EN/train')
        
#####################################################################    
#Part 2 2) Helper function to include non-appeared word in the test set
#Input: emission parameters, and count of y , a new word
#Output: updated emission parameters and count of y
def get_default_parameter(em_dic):
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    default ={}
    for state in T:
        default[state] = 1/float(em_dic[1][state]+1)
    return (default)


       
    
#####################################################################        

#Part 2 3)

#Helper function: Get the optimal y labels for the x sequence
#Input: evaluation file directory, and trained emission parameters
#Output: predicted y sequence
def get_y_predict(em_dic,x_test):
    
    y_predict = []
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    
    for xm in x_test:
        ym = []
        
        for xi in xm:
            temp = 0
            yi = 'I-negative'
            
            for state in T:
                if (xi,state) not in em_dic:
                    default = get_default_parameter(em_dic)
                    if default[state]>=temp:
                        temp=default[state]
                        yi = state
                else:
                    if em_dic[(xi,state)] >= temp:
                        temp = em_dic[(xi,state)]
                        yi = state
            #print (xi,yi)
            ym.append(yi)
        y_predict.append(ym) 
    return y_predict



############################################################################
#Function: To write the predictions into a file 
#Input: data_file_dir,devout_dir,devin_dir
def output_prediction(data_file_dir,devin_dir,devout_dir,algo):
    x_test = get_X(devin_dir)
    em_v = train_emission_param(data_file_dir)
    tran_v = train_tran_param(data_file_dir)
    if algo=='v':
        y_predict = viterbi(em_v,tran_v,x_test)
    elif  'tt' in algo:
        select = int(algo.split(":")[1])
        y_predict = viterbi_top(em_v,tran_v, x_test,select)
    elif algo == 'p':
        y_predict = perceptron_predict(data_file_dir,x_test)
    else:
        y_predict = get_y_predict(em_v,x_test)
    f_out = open(devout_dir,'w', encoding = "utf-8")
    for i in range(len(x_test)):
        xi = x_test[i] 
        yi = y_predict[i]
        for j in range(len(xi)):
            f_out.write(xi[j]+" "+yi[j]+"\n")
        f_out.write(' \n')
    f_out.close()


#########################Testing PART 2############################################
#output_prediction('EN/train','EN/dev.in','EN/dev.P2.out','part2')        
#output_prediction('ES/train','ES/dev.in','ES/dev.P2.out','part2')   
#output_prediction('CN/train','CN/dev.in','CN/dev.P2.out','part2')   
#output_prediction('SG/train','SG/dev.in','SG/dev.P2.out','part2')   