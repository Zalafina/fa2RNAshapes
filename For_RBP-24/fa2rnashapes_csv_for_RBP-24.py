# from eden.converter.fasta import sequence_to_eden
# from eden.modifier.rna.annotate_rna_structure import annotate_single
import subprocess as sp
import os
import pdb
import csv
import re

def run_rnashape(sequence):
    #
    cmd = 'echo "%s" | RNAshapes -# %d' % (sequence, 1)
    out = sp.check_output(cmd, shell=True)
    # text = out.strip().split('\r\n')
    text = out.strip()
    shapestr = text.decode().split('\r\n')
    print(shapestr)
    shape = re.split(r"[ ]+", shapestr[1])
    print(shape[1])
    shape_struct = [shape[1], shape[2]]
    return shape[1]
    # print(shapestr)
    # return text

def read_structure(seq_file, seq_filename):
    seq_list = []
    structure_list = []
    # fw = open(seq_file + '.structure', 'w')
    seq = ''
    line_num = 0
    csvfilename = seq_filename + ".csv"
    fname_class = os.path.splitext(seq_filename)[1]
    if ".negatives" == fname_class:
        rnaclass = 0
    elif ".positives" == fname_class:
        rnaclass = 1
    else:
        rnaclass = 0
    with open(seq_file, 'r') as fp:
        with open(csvfilename,"w",encoding='utf-8',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["RNA-Name","RNA-Sequence","RNA-Class","RNA-Shape"])
            for line in fp:
                line_num += 1
                print (line_num)
                # if line_num>=17:
                #     break
                seq = ''
                if line[0] == '>':
                    line = line.strip('\n')
                    line = line.strip('\r')
                    name = line
                else:
                    line = line.strip('\n')
                    line = line.strip('\r')
                    seq = seq + line
                    if len(seq):
                        seq = seq.replace('U', 'T')
                        seq = seq.replace('u', 't')
                        rnashape = run_rnashape(seq)
                        name = name.strip('> ')
                        RNARow = [name, seq, rnaclass, rnashape]
                        writer.writerow(RNARow)

def run_predict_graphprot_data():
    # data_dir = "E:\\work\\papers\\iDeep\\dataset\\RBP-31\\for_test\\fa_files\\"
    data_dir = ".\\fa_files\\"
    filelist = os.listdir(data_dir)
    for x in filelist:
        print(x)

    for protein_file in os.listdir(data_dir):
        protein = os.path.splitext(protein_file)[0]
        read_structure(data_dir + protein_file, protein)

if __name__ == "__main__":  
    # run_predict_graphprot_data()
    run_predict_graphprot_data()
    #sequence = 'TGGAAACATTCCTCAGGTGGTTCATCCAAGGCCCTTTCCACTCTTTCAGCTCACAGCACAGTGGTCCTTTTGTTCTTTGGTCCACCCATGTTTGTGTATAC'
    #encode_struct = run_rnashape(sequence)
    #print encode_struct
