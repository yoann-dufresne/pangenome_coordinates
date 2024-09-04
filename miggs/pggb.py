from miggs.run_cmds import run_cmd



class PGGB:
    
    def __init__(self, dataset, tmp_dir, output, bindir):
        self.dataset = dataset
        self.tmp_dir = tmp_dir
        self.output = output
        self.bin_dir = bindir
        
    def construct(self):
        run_cmd()
        raise NotImplementedError
    
    def coordinates(self):
        raise NotImplementedError
        