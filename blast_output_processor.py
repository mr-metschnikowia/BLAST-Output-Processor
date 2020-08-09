def get_data():
    import os
    folder = input('Folder in which BLAST outputs are prepared:')
    global array
    array = []
    for file in os.listdir(folder):
        path = folder + '\\' + file
        # loops through each file in folder path = file path
        with open(path, 'r') as f:
            lines = f.readlines()
            s = -1
        # file is read
        for line in lines:
            find_end = line.find('Alignments:')
            if find_end >= 0:
                break
            else:
                s += 1
        # finds where hit table ends
        ref_line = lines[1]
        ref_line = ref_line.upper()
        genes = ['PUL1', 'PUL2', 'PUL3', 'PUL4', 'EFSPT4']
        k = 0
        for i in range(5):
            gene = genes[k]
            search = ref_line.find(gene)
            if search >= 0:
                ref = gene
                break
            elif k == 4:
                ref = 'unknown gene'
            else:
                k += 1
        # reads job title providing query gene
        global title_line
        title_line = lines[8]
        def find_qc(x):
            global qc
            qc_start = title_line.find('cover')
            qc_end = title_line.find('cover') + 3
            qc = x[qc_start:qc_end]
            qc = "".join([i for i in qc if i.isalnum()])
        # retrieves query cover based on position of column title
        def find_id(x):
            global title_line
            global id
            id_start = title_line.find('Ident')
            id_end = title_line.find('Ident') + 5
            id = x[id_start:id_end]
        # retrieves percentage identity based on position of column title
        def find_acc(x):
            global title_line
            global acc
            acc_start = title_line.find('Accession')
            acc_end = title_line.find('Accession') + 14
            acc = x[acc_start:acc_end]
            split_em_up = acc.split(' ')
            acc = split_em_up[0]
        # retrieves accession code based on position of column title
        row = []
        x = 0
        for i in lines:
            line = lines[x]
            x += 1
            if x > 9 and x < s:
                find_qc(line)
                find_id(line)
                find_acc(line)
                row.append(ref),row.append(qc), row.append(id), row.append(acc)
                array.append(row)
                row = []
        # iterates through each line of the file
        # query cover, percentage identity and accession code are obtained for each row in hit table
        # information for each row is stored in array with reference gene
    print(array)
    with open('master_table.txt','a') as master:
        master.writelines([" ".join(i) + "\n" for i in array])
    # array is transformed into .txt file with each line representing a row on the hit table

if __name__ == "__main__":
    get_data()

# function is called









