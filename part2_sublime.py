#Part 2 
#(1) Write a function to evaluate the emission parameters based on data set X and Y

#Input: Directory of files (datafile_dir)
#Output: X data set and Y data set (X,Y)
#####################################################################
def get_XY(datafile_dir):
    f = open(datafile_dir)
    f_content = f.read()
    X = []
    Y = []
    xi = []
    yi = []
    
    for data_pair in f_content.split('\n'):
        
        if data_pair == '':
            if (xi != []):
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
    f = open(datafile_dir)
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
                count_y_dic[state] = count_y_dic[state]+1
                em_dic[key] = 1/float(count_y_dic[state])#Fix the problem where the word doesn't have certain states
            else:
                em_dic[key] =float(count_x_y_dic[key])/float(count_y_dic[state])
            #print (key, em_dic[key])
    
    return (em_dic,count_y_dic)
        
#####################################################################    
#Part 2 2) Helper function to include non-appeared word in the test set
#Input: emission parameters, and count of y , a new word
#Output: updated emission parameters and count of y
def set_default_parameter(em_dic,count_y_dic,xi):
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    for state in T:
        key = (xi,state)
        count_y_dic[state] = count_y_dic[state]+1
        em_dic[key] = 1/float(count_y_dic[state])
    return (em_dic,count_y_dic)
       
    
#####################################################################        

#Part 2 3)

#Helper function: Get the optimal y labels for the x sequence
#Input: evaluation file directory, and trained emission parameters
#Output: predicted y sequence
def get_y_predict(em_dic,count_y_predict,x_test):
    
    y_predict = []
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    
    for xm in x_test:
        ym = []
        
        for xi in xm:
            temp = 0
            yi = 'O'
            
            if (xi,'O') not in em_dic:
                em_dic,count_y_predict = set_default_parameter(em_dic,count_y_predict,xi)
            
            for state in T:
                if em_dic[xi,state] >= temp:
                    temp = em_dic[xi,state]
                    yi = state
            #print (xi,yi)
            ym.append(yi)
        y_predict.append(ym) 
    return y_predict



############################################################################
#Function: To write the predictions into a file 
#Input: data_file_dir,devout_dir,devin_dir
def output_prediction(data_file_dir,devin_dir,devout_dir):
    X,Y = get_XY(data_file_dir)
    em_dic,count_y_predict = train_emission_param(X,Y)
    x_test = get_X(devin_dir)
    y_predict = get_y_predict(em_dic,count_y_predict,x_test)
    f_out = open(devout_dir,'w')
    for i in range(len(x_test)):
        xi = x_test[i] 
        yi = y_predict[i]
        f_out.write('\n')
        for j in range(len(xi)):
            f_out.write(xi[j]+" "+yi[j]+"\n")
    f_out.close()

############################################################################
#Fuction: to evaluate the performance of algorithm
def evaluate_para(data_file_dir, devin_dir, devout_dir):
    X,Y = get_XY(data_file_dir)
    em_dic,count_y_predict = train_emission_param(X,Y)
    x_test = get_X(devin_dir)
    y_predict = get_y_predict(em_dic,count_y_predict,x_test)
    predicted = get_predicted_entities(x_test,y_predict)
    observed = get_gold_entities(devout_dir)
    
    correct_sentiment = 0
    correct_entity = 0

    total_observed = 0.0
    total_predicted = 0.0

    #For each Instance Index example (example = 0,1,2,3.....)
    for example in observed:
        observed_instance = observed[example]
        predicted_instance = predicted[example]

        #Count number of entities in gold data
        total_observed += len(observed_instance)
        #Count number of entities in prediction data
        total_predicted += len(predicted_instance)

        #For each entity in prediction
        for span in predicted_instance:
            span_begin = span[1]
            span_length = len(span) - 1
            span_ne = (span_begin, span_length)
            span_sent = span[0]

            #For each entity in gold data
            for observed_span in observed_instance:
                begin = observed_span[1]
                length = len(observed_span) - 1
                ne = (begin, length)
                sent = observed_span[0]

                #Entity matched
                if span_ne == ne:
                    correct_entity += 1
                    

                    #Entity & Sentiment both are matched
                    if span_sent == sent:
                        correct_sentiment += 1

    print()
    print('#Entity in gold data: %d' % (total_observed))
    print('#Entity in prediction: %d' % (total_predicted))
    print()

    prec = correct_entity/total_predicted
    rec = correct_entity/total_observed
    printResult('Entity', correct_entity, prec, rec)
    print()

    prec = correct_sentiment/total_predicted
    rec = correct_sentiment/total_observed
    printResult('Sentiment',correct_sentiment, prec, rec)
############################################################################    
def get_predicted_entities(x_test,y_predict):
    entity_list =[]
    for k in range(len(y_predict)):
        ym = y_predict[k]
        entity_sublist = []
        entity = ''
        flag = 0
        sentiment = 'O' 
        for i in range(len(ym)):
            
            if ym[i] == 'O':
                yi = ym[i]
            elif ym[i] != 'O':
                yi = ym[i].split('-')[1]
            
            if yi != 'O' and yi != sentiment:
                if sentiment != 'O':
                    element = (entity,sentiment)
                    entity_sublist.append(element)
                entity = x_test[k][i]
                sentiment = yi
                flag = 1 
            elif yi != 'O' and flag == 1 and yi == sentiment:
                entity = entity + ' ' + x_test[k][i]
            elif yi == 'O' and flag == 1:
                element = (entity,sentiment)
                entity_sublist.append(element)
                flag = 0
                sentiment = 'O'
        if(entity_sublist != []):
            entity_list.append(entity_sublist)
    print (entity_list)
    return entity_list

############################################################################       
def get_gold_entities(devout_dir):  
    X_gold,Y_gold = get_XY(devout_dir)
    gold_entity_list = []
    for k in range(len(Y_gold)):
        ym = Y_gold[k]
        gold_entity_sublist = []
        entity = ''
        flag = 0
        sentiment = 'O'
        for i in range(len(ym)):
            yi = ym[i]
            if yi == 'B-neutral' or yi == 'B-negative' or yi == 'B-positive':
                entity = X_gold[k][i]
                sentiment = yi.split('-')[1]
                flag = 1 
            elif yi == 'O' and flag ==1:
                element = (entity,sentiment)
                gold_entity_sublist.append(element)
                flag = 0
            elif flag == 1 and yi !='O':
                entity = entity + ' '+ X_gold[k][i]
        if(gold_entity_sublist != []):
            gold_entity_list.append(gold_entity_sublist)
   
    print ('gold_entity_list:\n',gold_entity_list)
    return gold_entity_list
    


#########################Testing PART 2############################################
#output_prediction('SG/train','SG/dev.in','SG/dev.P2.out')        
     
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
        for f in range(len(yi)-1):
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
            if t == len(yi):
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
                tp_dic[key] = count_yf_yt[key]/count_y_dic[state_from]
    
    print (tp_dic)
    return tp_dic

######################### viterbi ###########################################

def viterbi(data_file_dir,test_data_dir):
    em = train_emission_param(data_file_dir)
    tran = train_tran_param(data_file_dir)
    x_test =get_X(test_data_dir)
    T = ['O', 'B-positive', 'I-positive','B-negative','I-negative','B-neutral','I-neutral']
    y_predict =[]
    for xm in x_test:
        ym = []
        #base case
        temp = []
        for state_first in range(len(T)):
            key_em = (xm[0],T[state_first])
            key_tra = ('START',T[state_first])
            if key_em not in em:
                default = get_default_parameter(em,key_em[0])
                score = 1*default[T[state_to]]*tran[key_tra]
            else :
                score = 1 * em[key_em]*tran[key_tra]
            element_temp = ('START',state_first,score)
            temp.append(element_temp)
      
        #moving forward recursivly
        ym.append(temp)
        print (0)
        print (ym)
        temp = []
        for i in range(len(xm)-1):
            i=i+1
            for state_to in range(len(T)):
                max_score = 0
                max_state_from = 'O'
                for state_from in range(len(T)):
                    key_em = (xm[i],T[state_to])
                    key_tra = (T[state_from],T[state_to])
                   
                    if key_em not in em:
                        default = get_default_parameter(em,key_em[0])
                        score = ym[i-1][state_from][2]*default[T[state_to]]*tran[key_tra]
                    else :
                        score = ym[i-1][state_from][2]*em[key_em]*tran[key_tra]
                    if score >=max_score:
                        max_score = score
                        max_state_from = state_from
                element_temp = (max_state_from,state_to,max_score)
                temp.append(element_temp)
            print (i)
            print (ym)
            ym.append(temp)
            temp = []
        # final case 
        temp =[]
        max_score =0 
        max_state = 'O'
        for state_from in range(len(T)):
            final_layer = len(T)
            score = ym[final_layer][state_from][2]* tran[(T[state_from],'STOP')]
            if score >= max_score:
                max_score = score
                max_state = state_from
        key = (max_state,'STOP',max_score)
        temp.append(key)
        ym.append(temp)
        #backtracking 
        y1 = max_state
        ym_predict_num =[]
        for i in range(len(xm),0,-1):
            y2 = y1
            ym_predict_num.append(y2)
            y1 = ym[i][y2][1]
        ym_predict_lable =[]
        t_dic ={0:'O', 1:'B-positive', 2:'I-positive',3:'B-negative',4:'I-negative',5:'B-neutral',6:'I-neutral'}
        for i in ym_predict_num:
            y = t_dic[i]
            ym_predict_lable.append(y)
        y_predict.append(ym_predict_lable)
    print (y_predict)
    return y_predict


#########################Testing PART 3############################################
#train_tran_param('EN/train') 
viterbi('EN/train','EN/dev.in')   

              















