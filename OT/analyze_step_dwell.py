
from matplotlib import rcParams
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Arial"]
from EM_Algorithm.EM_test_GMM import GMM, plot_EM_results, plot_fit_gauss
from EM_Algorithm.EM_test_Poisson import exp_EM, plot_EM_results_exp, plot_fit_pdf, exp_pdf
from basic.select import get_files, select_folder
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture


def GMM_results(data, n_components, tolerance=10e-5):
    ### fit GMM
    f_save, m_save, s_save, label, data_cluster, BIC, AIC = GMM(data, n_components, tolerance=tolerance)
    ##  plot EM results(mean, std, fractio with iteration)
    # plot_EM_results(m_save, s_save, f_save)
    ##  plot data histogram and its gaussian EM (GMM) results
    plot_fit_gauss(step, f_save[-1,:], m_save[-1,:], s_save[-1,:])

    return f_save[-1,:], m_save[-1,:] ,s_save[-1,:], data_cluster, label, BIC, AIC

def poiEM_results(data, n_components, tolerance=10e-5):
    ##  fit EM
    f_save, tau_save = exp_EM(data, n_components, tolerance=tolerance)
    ##  plot EM results(mean, std, fractio with iteration)
    plot_EM_results_exp([f_save, tau_save], ['fraction', 'dwell time'])
    ##  plot data histogram and its gaussian EM (GMM) results
    plot_fit_pdf(dwell, exp_pdf, [f_save[-1,:], tau_save[-1,:]])

    return f_save[-1,:], tau_save[-1,:]


conc = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
# conc = [0.5, 1.0]

path_folder = select_folder()
all_step = []
all_dwell = []
n_components_g = 2
n_components_p = 1
tolerance = 1e-5

centers = []
stds = []
fractions = []
# name = f'S5S1_{c}
all_tau = []
all_ftau = []
for c in conc:
    path_data = get_files(f'S5S1_{c}*.mat', dialog=False, path_folder=path_folder)
    step = []
    dwell = []
    for path in path_data:
        data = sio.loadmat(path)
        step = np.append(step, data['step'])
        dwell = np.append(dwell, [data['dwell']])

    BICs = []
    BIC_owns = []
    AIC_owns = []
    n_clusters = np.arange(1, 5)
    X = step.reshape(-1,1)
    for c in n_clusters:
        model = GaussianMixture(n_components=c, tol=tolerance)
        model.fit(X)
        label = model.predict(X)
        BICs += [model.bic(X)]
        f, m, s, data_cluster, label_own, BIC_own, AIC_own = GMM(step, n_components=c, tolerance=tolerance)
        BIC_owns += [BIC_own]
        AIC_owns += [AIC_own]

    plt.figure()
    plt.plot(n_clusters, BICs,'o')
    plt.title('BIC')
    plt.xlabel('n_components')
    plt.ylabel('BIC')

    plt.figure()
    plt.plot(n_clusters, BIC_owns,'o')
    plt.title('BIC_owns')
    plt.xlabel('n_components')
    plt.ylabel('BIC_owns')
    
    plt.figure()
    plt.plot(n_clusters, AIC_owns,'o')
    plt.title('AIC_owns')
    plt.xlabel('n_components')
    plt.ylabel('AIC_owns')
    
    all_step += [step]
    all_dwell += [dwell]
    ### get GMM results
    n_components_g = n_clusters[np.argmin(AIC_owns)]
    # n_components_g = 2
    f, m, s, data_cluster, label_own, BIC_own, AIC_own= GMM_results(step, n_components_g, tolerance=tolerance)
    # plt.figure()
    # for data in data_cluster:
    #     plt.plot(data, np.zeros(len(data)), 'o')

    centers += [m]
    stds += [s]
    fractions += [f]

    ### get poisson EM results
    # f_tau, tau = poiEM_results(dwell, n_components_p, tolerance=10e-5)
    # all_tau += [tau]
    # all_ftau += [f_tau]




