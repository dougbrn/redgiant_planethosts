import pyspeckit
import numpy as np
from astropy import units as u
from astropy.io import fits
from astropy import constants as c
import matplotlib.pyplot as plt
from astropy.convolution import convolve, Box1DKernel
from c_normalize import c_normalize
import glob
import pandas as pd
import warnings
import mplcursors
from contextlib import contextmanager
import sys
import os
warnings.filterwarnings("ignore")


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def calc_ew(file_list, line_list, eqw_out_dir, moog_out_dir):
    # Select Dataset
    files = glob.glob(file_list)

    # Select line list and read into dataframe
    line_df = pd.read_csv(line_list, header=None, delim_whitespace=True)
    lines = line_df[0].tolist()
    print(lines)

    # Calculate Equivalent Widths

    # pars_dict: dictionary of custom parameters for lines that don't exhibit great behavior at default settings
    # key: local continuum range (Angstroms), Sample Region Left, Sample Region Right,
    # Gaussian Amplitude Estimates (in list for multicomponent fits), gaussian center offsets
    # (in list for multicomponent fits), Gaussian Width, selected component
    pars_dict = {'5838.37': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0), '7189.16': (10, 0.23, 0.1, [-0.3], [0], 0.15, 0),
                 '5712.13': (10, 0.5, 0.2, [-0.3, -0.3], [0, -0.2], 0.15, 0),
                 '5698.02': (10, 0.25, 0.7, [-0.3, -0.5], [0, 0.2], 0.15, 0),
                 '5284.1': (10, 1, 0.4, [-0.3, -0.7, -0.3], [0, -0.3, 0.2], 0.15, 0),
                 '5536.58': (10, 0.1, 0.2, [-0.3], [0], 0.15, 0),
                 '5325.56': (10, 0.4, 0.18, [-0.3, -0.1], [0, -0.25], 0.15, 0),
                 '5837.7': (10, 0.55, 0.45, [-0.3, -0.1, -0.2], [0, -0.37, 0.395], 0.15, 0),
                 '5577.03': (10, 0.18, 0.15, [-0.3], [0], 0.15, 0), '5807.78': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
                 '6699.15': (10, 0.17, 0.17, [-0.3], [0], 0.15, 0),
                 '5636.7': (10, 0.15, 0.67, [-0.2, -0.3], [0, 0.4], 0.15, 0),
                 '5635.82': (10, 0.18, 0.6, [-0.3, -0.1], [0, 0.4], 0.15, 0)}

    for file in files:
        line_eqws = []  # Create a list that will be populated by eqw measurements for each line [line,eqw,fitwidth]
        moog_vals = []
        s_hdu = fits.open(file)

        fname = file.split('/')[-1].split('.')[0]
        print(fname)
        out_file = fname + ".ew"

        # Grab the flux and wavelength arrays from the spectrum
        s_data = s_hdu[1].data
        s_flux = s_data['FLUX']
        s_wav = s_data['WAVEL']

        # Calculate Equivalent Width for each line
        for line in lines:
            # Set fitting parameters
            if str(line) in pars_dict.keys():
                key = str(line)
                print("Using Custom Parameters for {}".format(key))

                width = pars_dict[key][0]  # Distance from the line on both sides to sample the local continuum from
                gauss_centhresh_l = pars_dict[key][1]
                gauss_centhresh_r = pars_dict[key][2]
                gauss_amps = pars_dict[key][3]  # list for components
                gauss_cenoffs = pars_dict[key][4]  # list for components
                gauss_width = pars_dict[key][5]
                c_select = pars_dict[key][6]

            else:
                width = 10  # Distance from the line on both sides to sample the local continuum from
                gauss_amps = [-0.2]
                gauss_width = 0.15
                gauss_centhresh_l = 0.2
                gauss_centhresh_r = 0.2
                gauss_cenoffs = [0.0]
                c_select = 0

                # Determine the wavelength range to sample for the local continuum
                lim_l = line - width
                lim_r = line + width

                # Mask the flux and wavelength arrays based on the sampled wavelength range
                wav_mask = (s_wav > lim_l) & (s_wav < lim_r)
                s_localflux = s_flux[wav_mask]
                s_localwav = s_wav[wav_mask]

                # Normalize the local continuum
                yfit, norm, _ = c_normalize(s_localflux, s_localwav, median_replace=False, cheby=True, low_cut=0.99)

                # Load the normalized spectrum into a pyspeckit.Spectrum object
                sp = pyspeckit.Spectrum(data=norm, xarr=s_localwav * u.AA)

                # Define a baseline array for the normalized spectrum (1.0)
                sp.baseline.basespec = np.ones(len(s_localwav))

                # Fit a (multi-component if designated) gaussian to the line
                guesses = []
                for amp, cenoff in zip(gauss_amps, gauss_cenoffs):
                    guesses.append(amp)
                    guesses.append(line + cenoff)
                    guesses.append(gauss_width)

                with suppress_stdout():  # Suppress some annoying info messages
                    sp.specfit(fittype='gaussian', guesses=guesses,
                               exclude=[0, line - gauss_centhresh_l, line + gauss_centhresh_r, line + 5000])
                fwhm = sp.specfit.parinfo[2].value

                # Measure the Equivalent Width of the gaussian line fit against the normalized baseline
                eqw = sp.specfit.EQW(plot=False, continuum_as_baseline=True, xmin=0, xmax=len(norm),
                                     components=True)
                eqw = eqw[c_select] * 1000  # mA

                # calculate broadening (used as a measure for fit quality) in km/s
                broadening = c.c.value*float(fwhm)/float(line)/1000
                line_eqws.append([line, eqw, broadening])

                # Grab line properties for MOOG
                ion = line_df[line_df[0] == line][1].tolist()[0]
                ep = line_df[line_df[0] == line][2].tolist()[0]
                log_gf = line_df[line_df[0] == line][3].tolist()[0]

                moog_vals.append([line, ion, ep, log_gf, eqw])

        # Write line_eqws into an output eqw file
        out_df = pd.DataFrame(line_eqws, columns=["Line", "EQW", "Broadening"])
        out_df.to_csv(eqw_out_dir+out_file, sep=' ', index=False)

        #Generate a file for MOOG input
        clust, star = file.split("/")[-1].split("_")[0:2]
        f_name = clust + "_" + star[0:-3]

        with open(moog_out_dir + f_name + ".txt", "w") as f:
            f.write(f_name + " " + "(generated using the pycalc_ew.py script)" + "\n")
            for row in moog_vals:
                wav, ion, ep, log_gf, eqw = row
                formatted_string = "{:.2f} {:.1f} {:.2f} {:.2f} {:.2f}".format(wav, ion, ep, log_gf, eqw)
                wav, ion, ep, log_gf, ew = formatted_string.split(" ")
                file_line = "  {}{}{}{}{}{}{}{}{}".format(wav, " " * (10 - len(wav)),
                                                          ion, " " * (10 - len(ion)),
                                                          ep, " " * (10 - len(ep)),
                                                          log_gf, " " * ((10 - len(log_gf)) + 20),
                                                          ew, " " * (10 - len(ew)))
                f.write(file_line)
                f.write("\n")


if __name__ == "__main__":
    calc_ew("pydata/oc_rrs/inputs/*wavsoln.fits", "pydata/oc_rrs/inputs/input_lines.lines",
            "pydata/oc_rrs/equiv_widths/", "pydata/oc_rrs/moog_inputs/")

    calc_ew("pydata/ph_ctrl_stars/inputs/*wavsoln.fits", "pydata/ph_ctrl_stars/inputs/input_lines.lines",
            "pydata/ph_ctrl_stars/equiv_widths/", "pydata/ph_ctrl_stars/moog_inputs/")