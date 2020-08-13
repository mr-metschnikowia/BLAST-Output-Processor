def get_data():
    import os
    folder = r'C:\Users\Rhino\PycharmProjects\sfam\blast_outputs'
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
        range_1_lines = []
        gene_starts = []
        gene_ends = []
        count_1 = 0
        for line in lines:
            find_range_1 = line.find('Range 1:')
            if find_range_1 >= 0:
                range_1_lines.append(count_1)
                count_1 += 1
            else:
                count_1 += 1
        for line in range_1_lines:
            range_line = lines[line].strip()
            range_line = range_line[len('Range 1: '):len(range_line)]
            range_line = range_line.split(' to ')
            gene_start = range_line[0]
            gene_starts.append(gene_start)
            gene_end = range_line[1]
            gene_ends.append(gene_end)
        # obtains gene start and gene end for each hit
        program_line = lines[2]
        program = program_line[len('Program: '):len(program_line) - 2]
        # obtain program
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
        count_2 = 0
        for i in lines:
            line = lines[x]
            x += 1
            if x > 9 and x < s:
                find_qc(line)
                find_id(line)
                k = float(id) * float(qc)/10000
                k = str(k)
                find_acc(line)
                row.append(program), row.append(ref), row.append(acc), row.append(id), row.append(qc), row.append(k), row.append(gene_starts[count_2]), row.append(gene_ends[count_2])
                count_2 += 1
                array.append(row)
                row = []
        # iterates through each line of the file
        # program, reference, accession, % id, coverage, k, gene start and gene end are obtained for each row in hit table
        # information for each row is stored in array
    print(array)
    header = 'program reference accession %id coverage k start end \n'
    with open('master_table.txt', 'a') as master:
        master.write(header)
        master.writelines([" ".join(i) + "\n" for i in array])
    # array is transformed into .txt file with each line representing a row on the hit table + header

if __name__ == "__main__":
    get_data()

# function is called
