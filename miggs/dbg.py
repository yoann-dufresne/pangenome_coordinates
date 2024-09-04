from os import path, makedirs
from miggs.run_cmds import run_cmd



class DBG:
    def __init__(self, tmp_dir, output, bindir):
        # Binaries
        if bindir is None:
            self.ggcat = 'ggcat'
            self.sshash = 'sshash'
        else:
            self.ggcat = path.abspath(path.join(bindir, 'ggcat', 'target', 'release', 'ggcat'))
            self.sshash = path.abspath(path.join(bindir, 'sshash', 'build', 'sshash'))
        # Data directories
        self.tmp_dir = tmp_dir
        self.output = path.join(output, 'dbg')
        makedirs(self.output)
        
    def construct(self, input_fasta, dry_run=False):
        # Construct the De Bruijn graph
        run_cmd(f'{self.ggcat} build -k 31 -e -s 1 --threads-count 8 -c --keep-temp-files -o {path.join(self.output, "ggcat.fa")} -l {input_fasta} --temp-dir {self.tmp_dir}', dry_run=dry_run)
        
        # index the kmers
        run_cmd(f'{self.sshash} build -i {path.join(self.output, "ggcat.fa")} -k 31 -m 21 -o {path.join(self.output, "ggcat.sshash")} -d {self.tmp_dir} --verbose', dry_run=dry_run)


    def get_coordinates(self):
        print("Getting coordinates")
        raise NotImplementedError
    
    
    
    
    
# input_file=$1
# output_name=$2
# output_folder=$3
# temp_folder=$4
# cores=$5
# max_mem=$6
# kmer_size=$7

# home=/pasteur/zeus/projets/p02/seqbio/fandreac
# module load ggcat
# sshash=$home/tools/exp_sshash/build/sshash
# take_time='/usr/bin/time -v'

# cd $output_folder

# $take_time ggcat build -k $kmer_size -e -s 1 -m $max_mem --threads-count $cores --keep-temp-files -o $output_name.fa -l $input_file --temp-dir $temp_folder

# $take_time $sshash build -i $output_name.fa -k $kmer_size -m 21 -o $output_name.sshash -d $temp_folder --verbose

# while IFS= read -r haplotype; do
#     $take_time $sshash query -i $output_name.sshash -q $haplotype >> $output_name.paths
# done < $input_file