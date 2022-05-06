'''
Sunjq:
问题:
需要一些接口完成列表和消息传递
需不需要停止这个节点的功能?节点在那些地方需要挂起?
''' 

import json
import datetime
from datatype import input_instruction, passed_instruction
from datatype import passed2json
from datatype import json2passed

'''
数据结构常量
'''
TPROPOSAL_ACCEPTOR_1 = 0
TPROPOSAL_ACCEPTOR_2 = 1
TACCEPTOR_PROPOSAL_1 = 2
TACCEPTOR_PROPOSAL_2 = 3
TACCEPTOR_LEARNER = 4
TLEARNER_LEARNER = 5

PDATA = 0
PACCOUNT = 1
#这里定义了数据和账户存储的表号

TADD = 1024
TDELETE = 1025
TBROWSE = 1026
TSIGNUP = 1027
TLOGIN = 1028

'''
节点常量
'''
NMAXNODENO = 2  #最大节点编号
NMAJORITY = (NMAXNODENO + 1)//2 + 1
nodeNo = 0
roundNo = 0  #轮次编号
roundFlag = 0  #进入下一轮 L给P,A提示

class Proposer:
    '''
    Sunjq:
    Proposer的任务
    从Ins消息队列里取一条指令,或者增加上一条指令优先级
    发送prepare
    如果得到多数accept,发送propose,否则停止
    等待节点通知轮次结束
    开始下一个轮次

    Note:
    提案编号为3位优先级+20(8+6+6)位Ins时间戳
    '''

    def __init__(self):
        self.priority = 0
        self.rejected = False
        self.propNo = ''
        self.instruction = input_instruction
        self.propAccepted = False

    '''
    main func
    '''
    def Prepare(self):
        #准备prepare请求的内容
        self.Gen_PropNo()
        prepare_request = passed_instruction
        prepare_request.type = TPROPOSAL_ACCEPTOR_1
        prepare_request.source = nodeNo
        prepare_request.round = roundNo
        prepare_request.number = self.propNo
        prepare_request.accepted = False
        prepare_request.content = ''
        #向其他节点发送prepare请求
        for tgt in range(0,NMAXNODENO):
            if tgt != nodeNo:
                prepare_request.target = tgt
                self.Pass_Instruction(prepare_request)

    def Propose(self):
        #准备propose请求的内容
        propose_request = passed_instruction
        propose_request.type = TPROPOSAL_ACCEPTOR_2
        propose_request.source = nodeNo
        propose_request.round = roundNo
        propose_request.number = self.propNo
        propose_request.accepted = False
        propose_request.content = self.instruction
        #向其他节点发送propose请求
        for tgt in range(0,NMAXNODENO):
            if tgt != nodeNo:
                propose_request.target = tgt
                self.Pass_Instruction(propose_request)

    def Listen_Response(self):
        '''
        监听Acceptor的回复消息,直到把该prepare的回复消息处理完
        如果得到大多数的同意,则进入Propose
        否则,避让,等待轮次结束
        '''
        acceptNum = 0
        if acceptNum >= NMAJORITY:
            self.propAccepted = True
        else: 
            self.propAccepted = False

    
    '''
    helper func
    '''
    def Gen_PropNo(self): #将整数priority和字符串timestamp合并
        strPriority = '%03d' % self.priority
        strTime = str(datetime.datetime.now())
        timeStamp = strTime[0:4]+strTime[5:7]+strTime[8:10]\
            +strTime[11:13]+strTime[14:16]+strTime[17:19]+strTime[20:26]
        strPriority += timeStamp
        self.propNo = strPriority
    
    def Pass_Instruction(self,passIns: passed_instruction):  #发送格式消息
        pass

    def Get_Next_Ins(self):  #从Ins列表中取下一个指令
        pass

    def Get_Next_Response(self):  #从Response列表中取下一个消息
        pass

def main():  #在节点的一个线程中执行
    proposer = Proposer
    while 1:
        #新一轮次开始，检查上一提案的状态
        if proposer.rejected:
            proposer.rejected = False
            proposer.priority += 1
        else:
            proposer.instruction = proposer.Get_Next_Ins()
            proposer.priority = 0
        proposer.Prepare()
        proposer.Listen_Response()
        if proposer.propAccepted:
            proposer.Propose()
        while roundFlag == 0:  #等待当前轮次结束
            pass
