#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @package extractSeqFastaFromLen.py
# @author Sebastien Ravel

"""
	The extractSeqFastaFromLen script
	=================================
	:author: Sebastien Ravel
	:contact: sebastien.ravel@cirad.fr
	:date: 08/07/2016
	:version: 0.1

	Script description
	------------------

	This Programme filter sequences by length

	Example
	-------

	>>> # Keep sequences greater than 1000
	>>> extractSeqFastaFromLen.py -f sequences.fasta -l 1000 -o sequence_Sup1000.fasta -k g
	>>> # Keep sequences lower than 1000
	>>> extractSeqFastaFromLen.py -f sequences.fasta -l 1000 -o sequence_Inf1000.fasta -k l

	Help Programm
	-------------

	optional arguments:
		- \-h, --help
						show this help message and exit
		- \-v, --version
						display extractSeqFastaFromLen.py version number and exit

	Input mandatory infos for running:
		- \-f <filename>, --fasta <filename>
						fasta files
		- \-l <int>, --len <int>
						lensize cutoff
		- \-o <filename>, --out <filename>
						name of output file
		- \-k <g/greater/l/lower>, --keep <g/greater/l/lower>
						choice keep sequences size greater than -l (g/greater) or keep lower (l/lower)

"""


##################################################
## Modules
##################################################
#Import MODULES_SEB
import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))+"/"
sys.path.insert(1,current_dir+'../modules/')
from module_Flo import fasta2dict,lenSeq2dict

## Python modules
import argparse
from time import localtime, strftime
## BIO Python modules
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

##################################################
## Variables Globales
version="0.1"
VERSION_DATE='31/03/2015'
debug="False"
#debug="True"


##################################################
## Main code
##################################################
if __name__ == "__main__":

	# Initializations
	start_time = strftime("%d-%m-%Y_%H:%M:%S", localtime())
	# Parameters recovery
	parser = argparse.ArgumentParser(prog='extractSeqFastaFromLen.py', description='''This Programme filter sequences by length''')
	parser.add_argument('-v', '--version', action='version', version='You are using %(prog)s version: ' + version, help=\
						'display extractSeqFastaFromLen.py version number and exit')


	filesreq = parser.add_argument_group('Input mandatory infos for running')
	filesreq.add_argument('-f', '--fasta', metavar="<filename>",type=str, required=True, dest = 'fastaFile', help = 'Fasta files')
	filesreq.add_argument('-o', '--out', metavar="<filename>", required=True, dest = 'paramoutfile', help = 'Name of output')


	files = parser.add_argument_group('Input infos for running with default values')
	files.add_argument('-k', '--keep', metavar="<g/greater/l/lower>",type=str, required=False, dest = 'keep', default ='None', help = 'Choice keep sequences size greater than -l (g/greater) or keep lower (l/lower)')
	files.add_argument('-l', '--len', metavar="<int>",type=int, required=False, dest = 'lenSize',default = 500, help = 'Lensize cutoff')
	# Check parameters
	args = parser.parse_args()

	#Welcome message
	print("#################################################################")
	print("#        Welcome in extractSeqFastaFromLen (Version " + version + ")          #")
	print("#################################################################")
	print('Start time: ', start_time,'\n')

	# R??cup??re le fichier de conf passer en argument
	fastaFile =  os.path.abspath(args.fastaFile)
	outputfilename =  os.path.abspath(args.paramoutfile)
	lenSize = args.lenSize
	keep = args.keep

	output_handle = open(outputfilename, "w")

	dicoSize = lenSeq2dict(fastaFile)
	dicoFasta = fasta2dict(fastaFile)
	filename = fastaFile.split('/')[-1].replace('.fasta','')
	nbTotal = len(dicoFasta.keys())

	count=1
	for ID in sorted(dicoSize.keys(), key=dicoSize.get, reverse=True):
		lenSeq = dicoSize[ID]
	
		sequence = dicoFasta[ID]
		strain = outputfilename.split('/')[-1].split('_')[0].replace('.fasta','')
		seqName = f"Scaffold_{count}"
		#seqName = '%s_%s'%(strain,seqName)
		descrip = "length={}".format(lenSeq)
		if str(sequence.seq).count('N') < (len(str(sequence.seq)) - 20) :
			if keep == 'g' and lenSeq >= lenSize or (keep == 'l' and lenSeq <= lenSize):
					record = SeqRecord(sequence.seq,id=seqName,name=seqName, description='')
					SeqIO.write(record,output_handle, "fasta")
					#SeqIO.write(sequence,output_handle, "fasta")
					count += 1
			elif keep == 'None' : 
					record = SeqRecord(sequence.seq,id=seqName,name=seqName, description='')
					SeqIO.write(record,output_handle, "fasta")
					#SeqIO.write(sequence,output_handle, "fasta")
					count += 1
		else :
			print(ID +' contains only N, so this scaffolds is removed')
			
		
	print("\n\nExecution summary:")

	print("  - Outputting \n\
	Il y a %i Sequences\n\
	les sequences sont ajouter dans le fichier %s" %(count,outputfilename))
	print("\nStop time: ", strftime("%d-%m-%Y_%H:%M:%S", localtime()))
	print("#################################################################")
	print("#                        End of execution                       #")
	print("#################################################################")




