from pathlib import Path
import re
from gs.utils.log import get_std_logger
from gs.utils.meta_file import get_range
from .model import Batch, Config
from .enums import BatchHealth

log = get_std_logger(__name__)


class FileHandler():

    @staticmethod
    def generate_config(path: Path):
        indx = int(path.stem.split('_')[1])
        return Config(name=path.stem, path=path, index=indx)

    def __init__(self, meta_path: str):
        meta_path = Path(meta_path).resolve(strict=True)
        self.output_dir = meta_path.parent
        self.range = get_range(meta_path)
        self.batches = []
        
        # To implement validation

        # Globbing all frames from each folders
        # key=lambda f: int(re.search(r'\d+', f.name).group()
        for r in self.range:
            # Extracting batches
            _dir_path = self.output_dir/f'{r[0]}_{r[1]}'
            _batch = Batch(path=_dir_path, rng=r, length=(r[1]-r[0]+1))

            log.debug("Processing %s", str(_dir_path))

            #Extracting all files
            _all_frame = list(_dir_path.glob('*.xyz'))
            log.debug("Globbed %d frames", len(_all_frame))
            
            _labeled_frames = [FileHandler.generate_config(f) for f in _all_frame if f.name.startswith("gframe_")]
            _unlabled_frames = [FileHandler.generate_config(f) for f in _all_frame if f.name.startswith("frame_")]

            _len_lab = len(_labeled_frames)
            _len_unlab = len(_unlabled_frames)

            log.debug("Filtered %d unlabeled frames", _len_unlab)
            log.debug("Filtered %d labled frames", _len_lab)

            if _len_lab==_len_unlab:
                _batch.health=BatchHealth.success
            elif _len_lab>0 and _len_lab<_len_unlab:
                _batch.health=BatchHealth.bad
            elif _len_lab==0:
                _batch.health=BatchHealth.ok
            else:
                _batch.health=BatchHealth.error
                log.warning("Unexpeced number of %d labelled frames in %s", _len_lab, str(_dir_path))

            log.info("Batch status=%s for %s", str(_batch.health.name), str(_dir_path))

            #Storing back those frames
            _batch.configs = _unlabled_frames
            _batch.gconfigs = _labeled_frames

            # Appending the bactch
            self.batches.append(_batch)
            
    def files_health(self):
        '''Returns an array of file health for each batch
        '''
        status = [b.health for b in self.batches]
        log.debug("Batch health status %s", str(status))
        return status
    
    def get_batches(strict: bool = True):
        '''Returns list of all configs '''
        ...

    def __str__(self):
        dir_path = "Output dir: "+str(self.output_dir)
        range = "Batches: "+str(self.range)

        batches = []

        for batch in self.batches:    
            cfg = []
            gcfg = []
            for c in batch.configs:
                cfg.append("\t\t"+f"-{c.name}")
            for c in batch.gconfigs:
                gcfg.append("\t\t"+f"-{c.name}")

            cfg_str = "\n".join(cfg)
            gcfg_str = "\n".join(gcfg)

            btch_str = f'Batch range={batch.rng} len={batch.length} status={batch.health.name}' + "\n\tconfigs:\n" + cfg_str + "\n\tgconfigs:\n" + gcfg_str

            batches.append(btch_str)
        
        return dir_path + "\n" + range + "\n" + "\n".join(batches)

# if __name__=="__main__":
#     fh = FileHandler(r'C:\Users\singh\Desktop\gauss_ase\dataset\out\meta.json')