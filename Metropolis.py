from MainAlgo import *


# Lattice setting
rng = 0
NDims = 2
NSpins = 20
pUpInnit = 0.5
KIter = 4

# Sytem settings
mu = 1
H = 0
J = 1
kTc = 2 * J * NDims
kT = 1

# Flags
Evolution = 1
logscale = 0
verbose = 1


# Intermediate calculations
B = mu * H
totIter = 2 ** KIter * NSpins ** NDims
if Evolution:
    Iter = range(totIter)


# Run simulation
lat = Lattice(NDims=NDims, NSpins=NSpins, rng=rng, pUpInnit=pUpInnit, B=B, J=J, kT=kT, Evo=Evolution)
if verbose:
    print("BEFORE")
    print(lat.lattice[:5, :5])
    print("Avg Energy: ", lat.GetAvgEnergy())
    print("Avg Magnetisation: ", lat.GetAvgMagnetisation())
    print("Counts: ", lat.GetCounts())
lat.Run(NIter=totIter)
if verbose:
    print("-"*30, "AFTER", sep="\n")
    print(lat.lattice[:5, :5])
    print("Avg Energy: ", lat.GetAvgEnergy())
    print("Avg Magnetisation: ", lat.GetAvgMagnetisation())
    print("Counts: ", lat.GetCounts())


# Plot results
fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True)
ax0.set_title(rf"Magnetisation evolution ($H={B}$)")

ax0.plot(Iter, np.array(lat.EIter) / (J * NDims))
ax0.set_ylabel(r"Average Energy ($\frac{E}{JN_{Dim}}$)")

ax1.plot(Iter, lat.mIter)
ax1.set_ylim([-1.1, 1.1])
ax1.set_ylabel(r"Average Magnetisation ($m$)")
ax1.set_xlabel(r"Iteration no.")


if logscale:
    plt.xscale("log")
plt.show()
