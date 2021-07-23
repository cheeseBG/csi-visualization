import pandas as pd
import numpy as np
import time

output_df = pd.read_csv('data/outputs.csv', encoding='utf-8', header=None)
output_df = output_df.drop([output_df.columns[0]], axis='columns')  # remove index column
output_df = output_df.drop(0, axis='rows')  # remove column name (first row)
output_df.reset_index(drop=True, inplace=True)

output_df.columns -= 1

result_f = open('data/results.txt', 'r', encoding='utf-8')  # MOT

csi_times = output_df[0].tolist()
csi_times = list(map(float, csi_times))

# MOT를 다 읽고, CSI는 한 줄씩 읽기
mot_times = dict()

while result_f:  # MOT
    line = result_f.readline().split()
    if len(line) != 0:
        mot_times[line[0]] = line[1]
    else:
        break

label = []
threshold = 0.5  # error threshold

start = time.time()  # Save start time

for csi_time in csi_times:
    fre = [0, 0]
    flag = 0
    for mot_time in mot_times.keys():

        if abs(csi_time - float(mot_time)) < threshold:
            flag = 1
            fre[int(mot_times[mot_time])] += 1
        elif flag == 1:
            break

    if max(fre) == 0:
        label.append(-1)
    else:
        label.append(fre.index(max(fre)))

print("time :", time.time() - start)
print(label)


# ================ new =========================
'''
  Aftermoon-dev's code
'''
# Datalist에서 Value와 가장 유사한 값을 찾음
def matching_values(datalist, value):
    datalist = list(map(float, datalist))
    value = float(value)
    # Threshold 범위 내의 값만 Numpy Array에 담음
    array = np.asarray(list(filter((lambda x: abs(x - value) < threshold), datalist)))

    # 해당하는 값이 하나 이상이면
    if array.size > 0:
        # 그 중 가장 작은 값의 Index를 리턴
        minvalue = (np.abs(array - value)).argmin()
        return datalist.index(array[minvalue])
    else:
        # 하나도 없다면 -1
        return -1

label2 = {}
csi_times = csi_times
mot_times2 = list(mot_times.keys())

start2 = time.time()
for csi_time in csi_times:
    # 두 값을 비교해 현재 CSI Time과 가장 유사한 MOT Time을 구함
    compare = matching_values(mot_times2, csi_time)

    # -1이면 매칭 실패
    if compare == -1:
        label2[csi_time] = -1
    # 그 외에는 해당하는 MOT Timestamp가 Return 되므로 그 값을 Label에 담음
    else:
        label2[csi_time] = mot_times[mot_times2[compare]]
        del mot_times2[compare]
print("time :", time.time() - start2)
print(label)
# ======================================================