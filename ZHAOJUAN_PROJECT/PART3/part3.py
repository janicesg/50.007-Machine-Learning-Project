#Part 3 code here
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
#output_prediction('SG/train','SG/dev.in','SG/dev.P2test.out','part2')        
     
######################### PART 3###########################################

     
def train_tran_param(data_file_dir):
    X,Y = get_XY(data_file_dir)
    tp_dic = {}
    T = ['START','O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral','STOP']
    count_y_dic = {'START':0,'O':0, 'B-positive':0, 'I-positive':0,'B-negative':0,'I-negative':0,'B-neutral':0,
                   'I-neutral':0,'STOP':0}
    count_yf_yt = {}
    tp_dic = {}
    for yi in Y:
        count_y_dic['START'] +=1
        yi1 = yi[0]
        key =('START', yi1)
        if key not in count_yf_yt:
            count_yf_yt[('START',yi1)] = 1
        else:
            count_yf_yt[('START',yi1)] += 1
        for f in range(1,len(yi)-1):
            t = f + 1 
            yf = yi[f]
            yt = yi[t]
            key = (yf,yt)
            if key not in count_yf_yt:
                count_yf_yt[key] = 1
            else:
                 count_yf_yt[key] = count_yf_yt[key] +1
            if yf not in count_y_dic:
                count_y_dic[yf] = 1
            else:
                count_y_dic[yf] +=1
            if t == (len(yi)-1):
                count_y_dic[yt] +=1
                key = (yi[t],'STOP')
                if key not in count_yf_yt:
                    count_yf_yt[key] = 1
                else:
                    count_yf_yt[key] +=1
                count_y_dic['STOP'] +=1
         
    for state_from in T[:8]:
        for state_to in T[1:9]:
            key = (state_from,state_to)
            if key not in count_yf_yt:
                tp_dic[key] = 0
            else:
                tp_dic[key] = float(count_yf_yt[key])/float(count_y_dic[state_from])
         
    return tp_dic


######################### viterbi ###########################################
def viterbi(em,tran,x_test):

    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    y_predict =[]
    for xm in x_test:
        ym = []
        #base case
        temp = []
        for state_first in range(len(T)):
            key_em = (xm[0],T[state_first])
            key_tra = ('START',T[state_first])
            score =0
            if key_em not in em : 
                default = get_default_parameter(em)
                if tran[key_tra] != 0:
                    score = math.log(1.0*default[T[state_first]]*tran[key_tra])
                else:
                    score = -1000000000
            else :
                if em[key_em] == 0 or tran[key_tra] == 0:
                    score = -1000000000
                else:
                    score = math.log(1.0 * em[key_em]*tran[key_tra])
            element_temp = ('START',state_first,score)
            temp.append(element_temp)
      
        #moving forward recursivly
        ym.append(temp)
        temp = []
        for i in range(len(xm)-1):
            i=i+1
            for state_to in range(len(T)):
                max_score = -100000000000
                max_state_from = 0
                for state_from in range(len(T)):
                    key_em = (xm[i],T[state_to])
                    key_tra = (T[state_from],T[state_to])
                   
                    if key_em not in em:
                        default = get_default_parameter(em)
                        if tran[key_tra]!=0:
                            score = float(ym[i-1][state_from][2])+math.log(float(default[T[state_to]]))+math.log(float(tran[key_tra]))
                        else:
                            score = -100000000
                    else :
                        if em[key_em] == 0 or tran[key_tra]==0:
                            score = float(ym[i-1][state_from][2])+float(-10000000)
                        else:
                            score = float(ym[i-1][state_from][2])+math.log(float(em[key_em]))+math.log(float(tran[key_tra]))
                    if score >=max_score:
                        max_score = score
                        max_state_from = state_from
                element_temp = (max_state_from,state_to,max_score)
                temp.append(element_temp)
            ym.append(temp)

            temp = []
        # final case 
        max_score =-10000000000
        max_state = 0
        for state_from in range(len(T)):
            final_layer = len(xm)
            if tran[(T[state_from],'STOP')] != 0:
                score = float(ym[final_layer-1][state_from][2])+ math.log(float(tran[(T[state_from],'STOP')]))
            if score >= max_score:
                max_score = score
                max_state = state_from
        key = (max_state,'STOP',max_score)
        temp.append(key)
        ym.append(temp)
    
        #backtracking 
        y1 = max_state
        ym_predict_num =[]
        for i in range(len(xm)-1,-1,-1):
            y2 = y1
            ym_predict_num.append(y2)
            y1 = ym[i][y2][0]
        ym_predict_lable =[]
        t_dic ={0:'O', 1:'B-positive', 2:'I-positive',3:'B-negative',4:'I-negative',5:'B-neutral',6:'I-neutral'}
        for i in range(len(ym_predict_num)-1,-1,-1):
            y = t_dic[ym_predict_num[i]]
            ym_predict_lable.append(y)
        y_predict.append(ym_predict_lable)
    return y_predict

#########################Testing PART 3############################################


#output_prediction('EN/train','EN/dev.in','EN/dev.P3.out','v')        
#output_prediction('ES/train','ES/dev.in','ES/dev.P3.out','v')   
#output_prediction('CN/train','CN/dev.in','CN/dev.P3.out','v')   
#output_prediction('SG/train','SG/dev.in','SG/dev.P3.out','v')   
