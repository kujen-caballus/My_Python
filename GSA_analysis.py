import win32com.client
import pandas as pd
import matplotlib.pyplot as plt


result_filepath = "C:\\Users\\Username\\Documents\\study\\PositiveShell\\result_csv_longterm\\result"

gsaobj = win32com.client.Dispatch("GSA_8_7.ComAuto")

gsaobj.VersionString()

gsaobj.Open("C:\\Users\\Username\Documents\\study\\PositiveShell\\original\\shell_test.gwb")

# gsaobj.GwaCommand("SET, EL_BEAM, 1, 1, 1, 1, 4, 4")
# gsaobj.GwaCommand("ADD, LOAD_GRAVITY,L1,1,1,0,0,-1")
for i in range(1, 3):
    s = i * 0.05 + 0.10
    gsaobj.GwaCommand("ADD,MAT,6,MAT_ELAS_ISO,mymatelial,RED,MT_CONCRETE,6,2.26e+10,0.2,24.0, 1.0e-5, 0, 0 ")
    gsaobj.Delete("RESULTS")
    gsaobj.GwaCommand("SET, PROP_2D.2, 1, Prop2d, , Global , 6, SHELL," + str(s) + ", 0, 100% , 100%, 100%")
    gsaobj.Analyse()
    gsaobj.SaveAs("C:\\Users\\Username\\Documents\\study\\PositiveShell\\result_gwb\\result" + str(i) + ".gwb")
    gsaobj.SaveAs(result_filepath + str(i) + ".csv")

gsaobj.Close()
gsaobj = None

import csv
l_force_filepath       = "C:\\Users\\Username\\Documents\\study\\PositiveShell\\result_longterm_FORCE2D\\force"
l_shearstress_filepath = "C:\\Users\\Username\\Documents\\study\\PositiveShell\\result_longterm_SHEAR2D\\shear"
l_moment_filepath      = "C:\\Users\\Username\\Documents\\study\\PositiveShell\\result_longterm_MOMENT2D\\moment"
#s_nstrress_filepath
#s_shearstress_filepath
#s_moment_filepath
moment2d = []
shear2d  = []
force2d  = []
def csvwriter(result_csv_filepath, stress_csv_filepath, search_string, append_list):
    for i in range(1, 3):
        for l in open(result_csv_filepath + str(i) + ".csv"):
            if search_string in l:
                append_list.append(l.split(","))
                with open(stress_csv_filepath + str(i) +  ".csv", 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    writer.writerows(append_list)

csvwriter(result_filepath,l_moment_filepath,"MOMENT_2D",moment2d)
csvwriter(result_filepath,l_shearstress_filepath,"SHEAR_2D",shear2d)
csvwriter(result_filepath,l_force_filepath,"FORCE_2D",force2d)

mx_max_ls  = []
mx_el_ls = []

my_max_ls  = []
my_el_ls = []

mxy_max_ls = []
mxy_el_ls = []
for i in range(1,3):
    df_moment = pd.read_csv(l_moment_filepath + str(i) + ".csv",names=("TITLE", "EL_LIST", "NOT", "TYPE","My","Mx","Mxy"),index_col=1)
    df_moment_Centre = df_moment.query("TYPE == -1")
    df_mx_max  = df_moment_Centre.loc[df_moment["Mx"].idxmax()]
    df_my_max  = df_moment_Centre.loc[df_moment["My"].idxmax()]
    df_mxy_max = df_moment_Centre.loc[df_moment["Mxy"].idxmax()]
    mx_max_ls.append(df_mx_max["Mx"].max())
    my_max_ls.append(df_my_max["My"].max())
    mxy_max_ls.append(df_mxy_max["Mxy"].max())

#TYPE = NODE_NUMBER -1 = Centre
"""df_moment0 = df_moment.query("index == 0")
df_moment1 = df_moment.query("index == 1")
df_moment2 = df_moment.query("index == 2")
df_moment3 = df_moment.query("index == 3")"""

qx_max_ls  = []
qx_el_ls = []

qy_max_ls  = []
qy_el_ls = []

for i in range(1,3):
    df_shear = pd.read_csv(l_shearstress_filepath + str(i) + ".csv",names=("TITLE", "EL_LIST", "NOT", "TYPE","Qy","Qx"),index_col=1)
    df_shear_Centre = df_shear.query("TYPE == -1")
    df_qx_max  = df_shear_Centre.loc[df_shear["Qx"].idxmax()]
    df_qy_max  = df_shear_Centre.loc[df_shear["Qy"].idxmax()]
    qx_max_ls.append(df_qx_max["Qx"].max())
    qy_max_ls.append(df_qy_max["Qy"].max())
print(qx_max_ls)

nx_max_ls  = []
nx_el_ls = []

ny_max_ls  = []
ny_el_ls = []

nxy_max_ls = []
nxy_el_ls = []
for i in range(1,3):
    df_force = pd.read_csv(l_force_filepath + str(i) + ".csv",names=("TITLE", "EL_LIST", "NOT", "TYPE","Ny","Nx","Nxy"),index_col=1)
    df_force_Centre = df_force.query("TYPE == -1")
    df_nx_max  = df_force_Centre.loc[df_force["Nx"].idxmax()]
    df_ny_max  = df_force_Centre.loc[df_force["Ny"].idxmax()]
    df_nxy_max = df_force_Centre.loc[df_force["Nxy"].idxmax()]
    nx_max_ls.append(df_nx_max["Nx"].max())
    ny_max_ls.append(df_ny_max["Ny"].max())
    nxy_max_ls.append(df_nxy_max["Nxy"].max())

from matplotlib.backends.backend_pdf import PdfPages
x = [150,200]
plt.plot(x, mx_max_ls, label="Mx")
plt.plot(x, my_max_ls, label="My")
plt.legend()
plt.title("MaxMoments")
plt.xlabel("Thickness [mm]")
plt.ylabel("Moment [n*m/m2]")
plt.grid(True)
plt.savefig("Mx.png")
plt.show()


x = [150,200]
plt.plot(x, qx_max_ls, label="Qx")
plt.plot(x, qy_max_ls, label="Qy")
plt.legend()
plt.title("MaxShearStress")
plt.xlabel("Thickness [mm]")
plt.ylabel("Q [n/m]")
plt.grid(True)
plt.savefig("Qx.png")
plt.show()

x = [150,200]
plt.plot(x, nx_max_ls, label="Nx")
plt.plot(x, ny_max_ls, label="Ny")
plt.legend()
plt.title("Force")
plt.xlabel("Thickness [mm]")
plt.ylabel("Force [n/m]")
plt.grid(True)
plt.savefig("Nx.png")
plt.show()