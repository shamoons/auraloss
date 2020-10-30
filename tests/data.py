import os
import glob
import torch 
import torchaudio
import numpy as np

class LibriMixDataset(torch.utils.data.Dataset):
    """ LibriMix dataset."""
    def __init__(self, root_dir, subset="train", length=16384, noisy=False):
        """
        Args:
            root_dir (str): Path to the preprocessed LibriMix files.
            subset (str, optional): Pull data either from "train", "val", or "test" subsets. (Default: "train")
            length (int, optional): Number of samples in the returned examples. (Default: 40)
            noise (bool, optional): Use mixtures with additive noise, otherwise anechoic mixes. (Default: False)

        """
        self.root_dir = root_dir
        self.subset = subset
        self.length = length
        self.noisy = noisy

        self.last_idx = 0
        self.sample = 0
        self.steps = 0

        # set the mix directory if we want clean or noisy mixes as input
        self.mix_dir = "mix_both" if self.noisy else "mix_clean"

        # get all the files in the mix directory first
        self.files = glob.glob(os.path.join(self.root_dir, self.subset, self.mix_dir, "*.wav"))
        self.hours = 0 # total number of hours of data in the subset

        # loop over files to count total length
        for filename in self.files:
            si, ei = torchaudio.info(filename)
            self.hours += (si.length / si.rate) / 3600 

        # we then want to remove the path and extract just file ids
        self.files = [os.path.basename(filename) for filename in self.files]
        print(f"Located {len(self.files)} examples totaling {self.hours:0.1f} hr in the {self.subset} subset.")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):

        eid = self.files[self.sample]

        # use torchaudio to load them, which should be pretty fast
        s1,    sr = torchaudio.load(os.path.join(self.root_dir, self.subset, "s1", eid))
        s2,    sr = torchaudio.load(os.path.join(self.root_dir, self.subset, "s2", eid))
        noise, sr = torchaudio.load(os.path.join(self.root_dir, self.subset, "noise", eid))
        mix,   sr = torchaudio.load(os.path.join(self.root_dir, self.subset, self.mix_dir, eid))

        # get the length of the current file in samples
        si, ei = torchaudio.info(os.path.join(self.root_dir, self.subset, "s1", eid))

        # choose a random patch of `length` samples for training
        if self.subset == "train":
            start_idx = np.random.randint(0, si.length - self.length - 1)
            stop_idx = start_idx + self.length
        else:
            start_idx = 0
            stop_idx = si.length - 1

        # extract these patches from each sample 
        s1    = s1[0,start_idx:stop_idx].unsqueeze(dim=0)
        s2    = s2[0,start_idx:stop_idx].unsqueeze(dim=0)
        noise = noise[0,start_idx:stop_idx].unsqueeze(dim=0)
        mix   = mix[0,start_idx:stop_idx].unsqueeze(dim=0)

        return s1, s2, noise, mix