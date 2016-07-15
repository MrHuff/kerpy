'''
Created on 17 Nov 2015

@author: qinyi
'''
from HSICTestObject import HSICTestObject
import time


class HSICPermutationTestObject(HSICTestObject):

    def __init__(self, num_samples, data_generator, kernelX, kernelY, kernel_width_x=False,
                 kernel_width_y=False, num_rfx=None, num_rfy=None, rff=False,
                 induce_set=False, num_inducex = None, num_inducey = None, num_shuffles=1000, unbiased=True):
        HSICTestObject.__init__(self, num_samples, data_generator, kernelX, kernelY, 
                                kernel_width_x=kernel_width_x,kernel_width_y=kernel_width_y,
                                num_rfx=num_rfx, num_rfy=num_rfy, rff=rff,induce_set=induce_set,
                                 num_inducex = num_inducex, num_inducey = num_inducey)
        self.num_shuffles = num_shuffles
        self.unbiased = unbiased
    
     
    def compute_pvalue(self,data_x=None,data_y=None):
        if data_x is None and data_y is None:
            if not self.streaming and not self.freeze_data:
                start = time.clock()
                self.generate_data()
                data_generating_time = time.clock()-start
                data_x = self.data_x
                data_y = self.data_y
            else:
                data_generating_time = 0.
        else:
            data_generating_time = 0.
        print 'Permutation data generating time passed: ', data_generating_time
        hsic_statistic, null_samples, _, _, _, _, _ = self.HSICmethod(unbiased=self.unbiased,num_shuffles=self.num_shuffles,
                                                                      data_x = data_x, data_y = data_y)
        pvalue = ( sum( null_samples > hsic_statistic ) ) / float( self.num_shuffles )
        return pvalue, data_generating_time