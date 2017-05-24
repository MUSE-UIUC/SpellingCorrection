# find which data are missing

missing_inds = []

for i in range(361):
    in_file_name = 'output/separated_by_revised_type/add/'+str(i)+'_method0.txt'
    try:
        f = open(in_file_name, 'r')
    except:
        missing_inds.append(i)

print('missing indices:',missing_inds)
print('number of missing indices:',len(missing_inds)) # 39
