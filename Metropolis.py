import numpy as np
from math import exp
import matplotlib.pyplot as plt


# Lattice setting
rng = 0
NDims = 2
NSpins = 20
pUpInnit = 0
KIter = 4

# Sytem settings
mu = 1
H = 2
J = 1
kTc = 2 * J * NDims
kT = 1

# Flags
Evolution = 1
logscale = 0


# Intermediate calculations
B = mu * H
totIter = 2 ** KIter * NSpins ** NDims
if Evolution:
    Iter, EIter, mIter = range(totIter), [], []


class Lattice:
    def __init__(self, NDims=2, NSpins=20, pUpInnit=0.5, rng=None, B=0, J=1, kT=1):
        # store constants
        self.rng, self.NDims, self.NSpins = rng,  NDims, NSpins
        self.B, self.J, self.kT = B, J, kT
        assert NDims <= 3, f"Maximum of 2 dimensions supported, {NDims}-D was attempted"

        # main lattice array with initial percentage of spin up
        self.lattice = np.random.default_rng(rng).random(size=[NSpins for i in range(NDims)])
        self.lattice = (self.lattice < pUpInnit).astype(int)
        self.lattice = np.ma.masked_array(data=self.lattice, mask=self.lattice == 0, fill_value=-1).filled()

        '''counts = dict(zip(*np.unique(self.lattice, return_counts=True)))
        print(counts, counts[1] / (NSpins**NDims))
        print(self.lattice, self.lattice.shape)'''

    def Run(self, NIter=4, Evo=0):
        '''
        Execute main Metropolis algorithm
        '''

        # iterate over every spin randomly
        randAcc = np.random.default_rng(self.rng).random(size=NIter)
        randLoc = np.random.default_rng(self.rng).integers(self.NSpins, size=NIter*self.NDims)
        i = 0
        while i < NIter:
            loc = tuple(randLoc[self.NDims*i: self.NDims*(i+1)])

            # energy difference
            # E1 = self.GetEnergy(loc, deep=True)
            # self.FlipSpin(loc)
            # E2 = self.GetEnergy(loc, deep=True)
            # dE = E2 - E1
            dE = - 2 * self.GetEnergy(loc, deep=True)

            # acceptance probability
            # accept = dE < 0 or exp(- dE / kT) > randAcc[i]
            try:
                ans = exp(- dE / kT)
            except OverflowError:
                ans = float('inf')
            pAcc = min(1, ans)
            accept = pAcc > randAcc[i]
            # accept = randAcc[i] <= pAcc
            # if flip accepted, leave spin fipped
            # else flip back
            # if not accept:
            #     self.FlipSpin(loc)
            if accept:
                self.FlipSpin(loc)

            """ if i> 2000:
                locy, locx = loc
                print((locy, locx), self.lattice[locy-1: locy+2, locx-1: locx+2], sep="\n")
                print(f"dE: {dE}\nProb: {ans}\nAccept: {accept}")
                self.ShowLattice()
                a=2 """

            # store results for each iteration
            if Evo != 0:
                EIter.append(self.GetAvgEnergy())
                mIter.append(self.GetAvgMagnetisation())

            i += 1

        return 0

    def ShowLattice(self):
        '''
        Show matrix image of lattice
        '''
        plt.matshow(self.lattice, cmap="binary")
        plt.colorbar()
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
        counts = dict(zip(*np.unique(self.lattice, return_counts=True)))
        return counts


lat = Lattice(NDims=NDims, NSpins=NSpins, rng=rng, pUpInnit=pUpInnit, B=B, J=J, kT=kT)
print("BEFORE")
print(lat.lattice[:5, :5])
print("Avg Energy: ", lat.GetAvgEnergy())
print("Avg Magnetisation: ", lat.GetAvgMagnetisation())
print("Counts: ", lat.GetCounts())
lat.Run(NIter=totIter, Evo=Evolution)
print("-"*30, "AFTER", sep="\n")
print(lat.lattice[:5, :5])
print("Avg Energy: ", lat.GetAvgEnergy())
print("Avg Magnetisation: ", lat.GetAvgMagnetisation())
print("Counts: ", lat.GetCounts())


# plot results
fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True)

ax0.plot(Iter, np.array(EIter) / (J * NDims))
ax0.set_ylabel(r"Average Energy ($\frac{E}{JN_{Dim}}$)")

ax1.plot(Iter, mIter)
ax1.set_ylabel(r"Average Magnetisation ($m$)")
ax1.set_xlabel(r"Iteration no.")


def animate(i):
    pass


if logscale:
    plt.xscale("log")
plt.show()
