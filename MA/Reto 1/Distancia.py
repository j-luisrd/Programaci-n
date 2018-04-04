import csv
import time
import datetime
import math
from multiprocessing import Process, Manager
from os import getpid

def open_files(path):
    result = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(row)
    return result

def euclidean_distance(a1, b1, a2, b2):
    return str(math.sqrt(math.pow(float(b2) - float(b1), 2) + math.pow(float(a2) - float(a1), 2)))

def compare(model_data, new_data, position, total, return_dict, id):
    results = []
    for row in new_data:
        i = -1
        x = 0
        while(i == -1 and x < len(model_data)):
            if(model_data[x][0] == row[0]): i = x
            x += 1
            if(i != -1):
                row_model = model_data[i]
                distance = euclidean_distance(row[0], row[1], row_model[0], row_model[1])
                print("{} | {}, distance: {}".format(row_model, row, distance))
                results.append(float(distance))
        print("Percent: {}, PID: {}, proccess: {}".format(round((position*2/ total) * 100, 2), getpid(), str(id)))
        position += 1
    return_dict[id] = results
def prom(distance_data, position, total, return_dict, id):
    prom = 0
    min = distance_data[0]
    for row in distance_data:
        if(row < min): min = row
        prom += row
        percent = (position*2/ total) * 100
        print("Prom, percent: {}, PID: {}".format(round(percent, 2), getpid()))
        position += 1
    return_dict[id] = {'prom': prom, 'min': min}

if __name__ == '__main__':
    humedad_station = sorted(open_files('Humedad_Station.csv'), key=lambda data: data[0])
    humedad_patron = open_files('Humedad_Patron.csv')

    new_data = []
    distance_data = []

    for row in humedad_patron:
        date = row[0].split("/")
        time_info = row[1].split(" ")
        time = time_info[0].split(":")
        if(time_info[1] == "p"):
            hour = 12 - int(time[0])
        else:
            hour = int(time[0])
        time = datetime.datetime(int("20" + date[2]), int(date[1]), int(date[0]), hour, int(time[1])).strftime('%s')
        new_data.append([str(time), row[2]])
        # print(row)

    new_data = sorted(new_data, key=lambda data: data[0])

    manager = Manager()
    return_dict = manager.dict()
    position = 0

    if(len(new_data) % 2 == 0):
        start = len(new_data) // 2
    else:
        start = (len(new_data) - 1) // 2

    p1 = Process(target=compare, args =(humedad_station, new_data[0:start - 1], position, len(new_data), return_dict, 0))
    p2 = Process(target=compare, args =(humedad_station, new_data[start:len(new_data)], position, len(new_data), return_dict, 1))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    for x in return_dict.values():
        for elem in x:
            distance_data.append(elem)

    position = 0
    if(len(distance_data) % 2 == 0):
        start = len(distance_data) // 2
    else:
        start = (len(distance_data) - 1) // 2

    p3 = Process(target=prom, args =(distance_data[0:start - 1], position, len(distance_data), return_dict, 2))
    p4 = Process(target=prom, args =(distance_data[start:len(distance_data)], position, len(distance_data), return_dict, 3))

    p3.start()
    p4.start()
    p3.join()
    p4.join()

    prom = return_dict[2]['prom'] + return_dict[3]['prom']
    if (return_dict[2]['min'] < return_dict[3]['min']):
        min = return_dict[2]['min']
    else:
        min = return_dict[3]['min']

    print("Minimum value: {}".format(min))
    print("Prom: {}".format(str(prom / len(distance_data))))
