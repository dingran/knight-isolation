import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

d = {'AB_Improved': [97, 116, 103, 147, 178, 154, 178, ],
     'Diff_Agg_0': [91, 105, 95, 141, 169, 148, 185, ],
     'Diff_Agg_0.5': [97, 116, 94, 138, 177, 152, 186, ],
     'Diff_Agg_1': [104, 108, 104, 143, 178, 150, 182, ],
     'Diff_Agg_2.5': [93, 106, 102, 147, 175, 146, 188, ],
     'Diff_Agg_inf': [98, 111, 104, 139, 184, 154, 190, ],
     'TV_Diff_V1': [101, 106, 95, 152, 167, 154, 185, ],
     'TV_Diff_V2': [92, 98, 104, 141, 176, 152, 187, ],
     'LA_Agg_0': [96, 111, 104, 139, 179, 153, 176, ],
     'LA_Agg_0.5': [105, 109, 118, 157, 176, 159, 189, ],
     'LA_Agg_1': [111, 110, 112, 167, 179, 159, 183, ],
     'LA_Agg_2': [99, 111, 116, 148, 172, 154, 178, ],
     'LA_Agg_inf': [103, 106, 107, 147, 182, 164, 181, ],
     'Wall_and_Corner': [88, 101, 91, 143, 174, 145, 190, ],
     }
df2 = pd.DataFrame(d, index=['AB_Improved', 'AB_Center', 'AB_Open', 'MM_Improved', 'MM_Center', 'MM_Open', 'Random'])

df2 = df2 / 200.0 * 100
plt.figure(figsize=(20, 4))
df2.plot.bar()
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 10})
plt.legend(loc='upper left')
plt.tight_layout()
plt.ylim(40, 100)
plt.savefig('overall_tournament.png')

df2 = df2[['AB_Improved', 'LA_Agg_1']]
plt.figure(figsize=(20, 4))
df2.plot.bar()
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 10})
plt.legend(loc='upper left')
plt.tight_layout()
plt.ylim(40, 100)
plt.savefig('best.png')