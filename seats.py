import datetime


#座位列表，图书馆一共有100个座位，座位号分别为1到100。
seat_list = [i+1 for i in range(100)]


#此函数接受两个时间段作为输入，判断这两个时间段是否交叉。
#输入要求：需要保证两个时间段本身的endtime晚于starttime。
def timejunc(starttime1,endtime1,starttime2,endtime2):
    if endtime1 <= starttime2:
        return False            #不交叉
    if starttime1 >= endtime2:
        return False            #不交叉
    return True             #交叉