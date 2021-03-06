import pyspeckit
import numpy as np
from astropy import units as u
from astropy.io import fits
from astropy import constants as c
from c_normalize import c_normalize
import glob
import pandas as pd
import warnings
from contextlib import contextmanager
import sys
import os
import yaml
from dask import compute, delayed
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


def ew_line_calc(line, file, s_flux, s_wav, pars_dict, line_df):
    # Set fitting parameters
    if (str(line) == '7189.16') and ('ngc2204' in file):
        return [line] + [np.nan]*5 +[2]

    # Grab line properties for MOOG
    ion = line_df[line_df[0] == line][1].tolist()[0]
    ep = line_df[line_df[0] == line][2].tolist()[0]
    log_gf = line_df[line_df[0] == line][3].tolist()[0]
    # debugging -----
    print(f"Line: {str(np.round(float(line), 2))}")
    #print(list(pars_dict.keys())[np.where(abs(line_wavs - float(line)) < 0.2)[0][0]])
    #print(str(line) in pars_dict.keys())
    # ---------------
    if str(np.round(float(line), 2)) in np.array(list(pars_dict.keys())):
        key = str(np.round(float(line), 2))
        print(key)

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

    # Don't try to fit if line lies in an order edge (flux is zeroes)
    order_edges = s_localwav[s_localflux == 0.0]
    if len(order_edges) > 0:
        if min(order_edges) <= line <= max(order_edges):
            return [line] + [np.nan]*5 +[1]


    # Normalize the local continuum
    try:
        yfit, norm, _ = c_normalize(s_localflux, s_localwav, median_replace=False, cheby=True, low_cut=0.97)
    except ValueError:
        print(f"Bad c_normalize for {line}")
        log_message = 'Bad c_normalize fit'
        return [line, ion, ep, log_gf, 0, 0, 1, log_message]

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
    fwhm = sp.specfit.parinfo["WIDTH0"].value




    # Measure the Equivalent Width of the gaussian line fit against the normalized baseline
    eqw = sp.specfit.EQW(plot=False, continuum_as_baseline=True, xmin=0, xmax=len(norm),
                         components=True)
    eqw = eqw[c_select] * 1000  # mA

    # calculate broadening (used as a measure for fit quality) in km/s
    broadening = c.c.value * float(fwhm) / float(line) / 1000


    dq_flag = 0  # Flag for measurement quality, 0=Good, 1=Omit (log), 2=Omit (Don't log), 3=Warn
    log_message = ''
    # Omit Measurements that return ridiculous EQWs
    if (eqw <= 3.0) or (eqw > 500.0):
        dq_flag = 1
        log_message+=" EQW outside of expected range (<=3 or >500)"
    # Flag measurements that return EQWs that are higher than we'd typically expect
    elif eqw > 300:
        dq_flag = 3
        log_message+=" EQW > 300 "

    # get the fwhm values for secondary fits
    if len(gauss_amps) > 1:
        for idx in range(len(gauss_amps)):  # sample the number of fits
            if idx == 0:
                continue
            if sp.specfit.parinfo[f"WIDTH{idx}"].value > 0.2:  # width cutoff of 20.0 mA, we expect ~15.0 mA
                dq_flag = 1
                log_message+=" , A secondary fit exceeded the fwhm limit, the fit is likely poor as a result"

    return [line, ion, ep, log_gf, eqw, broadening, dq_flag, log_message]


def calc_ew(file_list, line_list, eqw_out_dir, moog_out_dir, log = True):
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
    pars_dict = yaml.load(open('line_pars.yml'))

    # If log is enabled, create a log of omitted and warning-incurred measurements for tracking in post
    if log:
        log_file = open(moog_out_dir + "../runlog.txt", "w")

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
        inputs = zip(lines, )
        values = [delayed(ew_line_calc)(line[0], file, s_flux, s_wav, pars_dict, line_df) for line in inputs]
        results = np.array(compute(*values, scheduler='processes'))

        dq_flags = np.array([row[6] for row in results],dtype='int32')


        # Omit Lines if they have the omit flag set (not logged)
        results = results[dq_flags != 2]
        dq_flags = np.array(dq_flags[dq_flags != 2])

        # Omit Lines if they have the omit flag set (logged)
        masked_results = results[dq_flags != 1]
        #import pdb;pdb.set_trace()
        # Check broadening for all lines -- update DQ flags if outliers are present

        broadening = np.array([float(row[5]) for row in masked_results])
        #import pdb; pdb.set_trace()
        sigma = 1
        broad_mask = abs(broadening - np.mean(broadening)) > sigma * np.std(broadening)

        flagged_results = []
        for row, mask_bool in zip(masked_results, broad_mask):
            if mask_bool:
                row[6] = 1  # omit broadening outliers
                row[7]+=" , primary fwhm is a broadening outlier compared to rest of star "
            flagged_results.append(row)

        # Grab values for EQW and MOOG files
        line_eqws = [[row[0], row[4], row[5]] for row in flagged_results]
        moog_vals = [row[0:5] for row in flagged_results]

        # Write line_eqws into an output eqw file
        out_df = pd.DataFrame(line_eqws, columns=["Line", "EQW", "Broadening"])
        out_df.to_csv(eqw_out_dir+out_file, sep=' ', index=False)

        # Generate a file for MOOG input
        clust, star = file.split("/")[-1].split("_")[0:2]
        f_name = clust + "_" + star[0:-3]

        with open(moog_out_dir + f_name + ".txt", "w") as f:
            f.write(f_name + " " + "(generated using the pycalc_ew.py script)" + "\n")
            for row in moog_vals:
                wav, ion, ep, log_gf, eqw = row
                formatted_string = "{:.2f} {:.1f} {:.2f} {:.2f} {:.2f}".format(float(wav), float(ion),
                                                                               float(ep), float(log_gf), float(eqw))

                wav, ion, ep, log_gf, ew = formatted_string.split(" ")
                file_line = "  {}{}{}{}{}{}{}{}{}".format(wav, " " * (10 - len(wav)),
                                                          ion, " " * (10 - len(ion)),
                                                          ep, " " * (10 - len(ep)),
                                                          log_gf, " " * ((10 - len(log_gf)) + 20),
                                                          ew, " " * (10 - len(ew)))
                f.write(file_line)
                f.write("\n")

        if log:
            log_file.write("==========\n")
            log_file.write(f_name+'\n')
            log_file.write("==========\n")
            for row in results:
                if int(row[6]) == 1:
                    log_file.write("Omitted: {} EQW = {} Reason: {}\n".format(row[0], row[4], row[7]))
            for row in flagged_results:
                if int(row[6]) == 3:
                    log_file.write("Warning: {} EQW = {} Reason: {}\n".format(row[0], row[4], row[7]))

    if log:
        log_file.close()


if __name__ == "__main__":
    calc_ew("../pydata/ph_ctrl_stars/inputs/BD*wavsoln.fits", "../pydata/input_lines.lines",
            "../pydata/ph_ctrl_stars/equiv_widths/", "../pydata/ph_ctrl_stars/moog_inputs/")
    """
    # Sample with Known EQWs
    calc_ew("pydata/ew_known/inputs/*wavsoln.fits", "pydata/input_lines.lines",
            "pydata/ew_known/equiv_widths/", "pydata/ew_known/moog_inputs/")
    # Rapid Rotators
    calc_ew("pydata/oc_rrs/inputs/*wavsoln.fits", "pydata/input_lines.lines",
            "pydata/oc_rrs/equiv_widths/", "pydata/oc_rrs/moog_inputs/")
    # Known Planet Hosts
    calc_ew("pydata/ph_ctrl_stars/inputs/*wavsoln.fits", "pydata/input_lines.lines",
            "pydata/ph_ctrl_stars/equiv_widths/", "pydata/ph_ctrl_stars/moog_inputs/")
    # Dupont Data
    calc_ew("pydata/dupont_ph_ctrl/inputs/*wavsoln.fits", "pydata/input_lines.lines",
            "pydata/dupont_ph_ctrl/equiv_widths/", "pydata/dupont_ph_ctrl/moog_inputs/")
    # Standards
    calc_ew("pydata/misc/inputs/*wavsoln.fits", "pydata/input_lines.lines",
            "pydata/misc/equiv_widths/", "pydata/misc/moog_inputs/")
    """





