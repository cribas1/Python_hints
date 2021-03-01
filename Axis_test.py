import pdb;
x_axis = 6
y_axis = 8
for x in range(x_axis):
    print("")
    for y in range(y_axis):
        if y == y_axis:
            print(y)
        else:
            print(y,end=" ")
            pdb.set_trace() #continue, step, next