import numpy as np
"""
this file will create a GM(grey prediction machine), and enable user to predict the future data based on current array of data. please note that this 
machine is based on first order differential equation, so it will be good at predicting data with certain trend( growing or minimizing), not very useful
for the periodically changed data( or you can try to break the periodically changed data into parts and use this machine). good for short term future prediction but 
not the long term
"""
class GM_predictor(object):
    def __init__(self,existing_data):
        '''
        this constructor will help initialize a GM_predictor, only need to add the existing_data and then we will store the data for you
        :param existing_data:
                the series data we already have, will try to find the patterns of how the data change
        '''
        self.existingD = existing_data

    def GM11_predict(self,  predictNum):
        '''
            this function will enable the GM_predictor to predict future data based on the existing data with the parameter usedDataNum and predictNum
        :param usedDataNum:
                  the number of data to use in self.existingD, could change according to will, has to be greater or equal to 1
        :param predictNum:
                  the number of data to predict later, predictNum is the length of the predicted data
        :return: result
                  an list of data predicted by GM_predictor
        '''
        #first assuming using all data to do prediction, then make modifications
        oldData_x0 = np.array( self.existingD )   # getting all existing data
        dataSum_x1 = np.cumsum( oldData_x0 )      #summing up the prevoius value, culminate
        halfSum_z1 = (dataSum_x1[ :len(dataSum_x1)-1 ]+ dataSum_x1[ 1: ])/2.0   #shifting is faster than looping
        halfSum_z1 = halfSum_z1.reshape(len(halfSum_z1), 1)  # change halfSum_z1 into array, get ride of the first term because it is none
        coef_b1 = np.append(-halfSum_z1,np.ones_like( halfSum_z1 ), axis= 1)  #according to the fomula, setting coef_b1
        pseudoR_y = oldData_x0[1:].reshape( len(oldData_x0)-1, 1 ) #have to reshape the pseudoR_y into the same shape as coef_b1
        #getting the value of a,b according to the formula
        [ [a],[b] ] = np.dot(np.dot(np.linalg.inv( np.dot(coef_b1.T, coef_b1) ), coef_b1.T), pseudoR_y)
        result= []
        #use the formula, get oldData_x0's every later terms from dataSum_x1's solutions
        for i in range(oldData_x0.shape[0]+1,oldData_x0.shape[0]+predictNum+1):   # index will begin in the end of the existing list and end in the len(existing list)+predictNum
            result.append((oldData_x0[0]-b/a)*np.exp( -a*(i-1) )-( oldData_x0[0]-b/a )*np.exp(-a*( i-2 )))
        return result

