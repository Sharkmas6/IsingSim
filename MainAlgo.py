import numpy as np
from math import exp
import matplotlib.pyplot as plt


class Lattice:
    def __init__(self, NDims=2, NSpins=20, pUpInnit=0.5, rng=None, B=0, J=1, kT=1,
                Evo=None):
        # store constants
        self.rng, self.NDims, self.NSpins = rng,  NDims, NSpins
        self.B, self.J, self.kT = B, J, kT
        assert NDims <= 3, f"Maximum of 2 dimensions supported, {NDims}-D was attempted"

        # main lattice array with initial percentage of spin up
        self.lattice = np.random.default_rng(rng).random(size=[NSpins for i in range(NDims)])
        self.lattice = (self.lattice < pUpInnit).astype(int)
        self.lattice = np.ma.masked_array(data=self.lattice, mask=self.lattice == 0, fill_value=-1).filled()

        # prepare energies, magnetisation arrays
        if Evo:
            self.EIter, self.mIter = [], []

    def RunIter(self, Loc=None, Acc=None):
        '''
        Execute single iteration of main Metropolis algorithm
        '''
        Loc = np.random.random(self.NDims) if Loc is None else Loc
        Acc = np.random.random() if Acc is None else Acc

        # energy difference
        dE = - 2 * self.GetEnergy(Loc, deep=True)

        # acceptance probability
        try:
            ans = exp(- dE / self.kT)
        except OverflowError:
            ans = float('inf')
        pAcc = min(1, ans)
        accept = pAcc > Acc

        if accept:
            self.FlipSpin(Loc)

        """ if i> 2000:
            locy, locx = loc
            print((locy, locx), self.lattice[locy-1: locy+2, locx-1: locx+2], sep="\n")
            print(f"dE: {dE}\nProb: {ans}\nAccept: {accept}")
            self.ShowLattice()
            a=2 """

        # store results for each iteration
        if self.EIter is not None:
            self.EIter.append(self.GetAvgEnergy())
            self.mIter.append(self.GetAvgMagnetisation())

    def Run(self, NIter=4):
        '''
        Execute main Metropolis algorithm
        '''

        # iterate over every spin randomly
        randAcc = np.random.default_rng(self.rng).random(size=NIter)
        randLoc = np.random.default_rng(self.rng).integers(self.NSpins, size=NIter*self.NDims)
        i = 0
        while i < NIter:
            loc = tuple(randLoc[self.NDims*i: self.NDims*(i+1)])
            self.RunIter(Loc=loc, Acc=randAcc[i])
            i += 1

        return 0

    def ShowLattice(self, colorbar=True):
        '''
        Show matrix image of lattice
        '''
        plt.matshow(self.lattice, cmap="binary")
        if colorbar: plt.colorbar()
        plt.show()

        return 0

    def GetEnergy(self, loc, deep=False):
        '''
        Get energy of single spin due to external magnetic field and neighbouring spins
        '''
        loc = tuple(loc)

        E = - self.B * self.lattice[loc] if deep else 0  # was sum
        # direct neighbours only (no diagonals)
        for n in range(self.NDims):
            for j in range(-1, 2, 2):
                locNbr = list(loc)
                locNbr[n] = (loc[n] + j) % self.NSpins
                locNbr = tuple(locNbr)

                E -= self.J * self.lattice[loc] * self.lattice[locNbr]

        return E

    def GetAvgEnergy(self):
        '''
        Get average energy of every spin, including magnetic field
        '''

        E = - self.B * self.lattice.sum()
        for n in range(self.NDims):
            loc = [0 for a in range(self.NDims)]
            for i in range(self.NSpins):

                E += self.GetEnergy(tuple(loc), deep=False)
                loc[n] += 1

        return E / self.lattice.size

    def GetAvgMagnetisation(self):
        '''
        Get average magnetisation
        '''

        return np.mean(self.lattice)

    def FlipSpin(self, loc):
        '''
        Flip single spin
        '''

        loc = tuple(loc)
        self.lattice[loc] = - self.lattice[loc]

        return 0

    def GetCounts(self):
        '''
        Get dictionary of counts of spin up/down
        '''
        counts = dict(zip(*np.unique(self.lattice, return_counts=True)))
        return counts