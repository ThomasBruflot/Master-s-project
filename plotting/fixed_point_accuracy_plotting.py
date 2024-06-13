import numpy as np
import matplotlib.pyplot as plt
 
 
x_axis = []
for i in range(4,48):
    x_axis.append(i)
 
accuracy_array = [9.8, 36.88, 69.71, 70.27, 74.15, 74.27, 75.12, 75.71, 75.59, 75.62, 75.65, 75.63, 75.70, 75.72]
for i in range(29):
    accuracy_array.append(75.75)
accuracy_array.append(75.95)
 
 
#x_axis = []
#for i in range(48,4,-1):
#    x_axis.append(i)
#
#
#accuracy_array = [75.9]
#for i in range(29):
#    accuracy_array.append(75.75)
#accuracy_array.append(75.72)
#accuracy_array.append(75.70)
#accuracy_array.append(75.63)
#accuracy_array.append(75.65)
#accuracy_array.append(75.62)
#accuracy_array.append(75.59)
#accuracy_array.append(75.71)
#accuracy_array.append(75.12)
#accuracy_array.append(74.27)
#accuracy_array.append(74.15)
#accuracy_array.append(70.27)
#accuracy_array.append(69.71)
#accuracy_array.append(36.88)
#accuracy_array.append(9.8)
 
 
print(len(accuracy_array))
print(len(x_axis))
 
def visualize_accuracies(accuracy_array,x_axis):
 
    fig, ax = plt.subplots(
    figsize=(6, 5)
    )
    ax.set_xlabel('Fractional precision')
    ax.set_ylabel('Accuracy [%]')
    title_string = 'Accuracy performance of the ASIC SNN on the MNIST dataset during inference with different fractional precision'
    ax.set_title(title_string)
    ax.plot(x_axis, accuracy_array, linestyle='--', marker='o', color='b', label='Accuracy of ASIC SNN in behavioural simulation')
 
    ax.plot(
    [8, 8],
    [accuracy_array[0], max(accuracy_array)],
    #label="75 %",
    color="red",
    linestyle="--",
    linewidth=1,
    )
    ax.text(
    8,
    accuracy_array[-1] * 1.01,
    "Breakdown point",
    color="red",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
 
 
    ax.plot(
    [x_axis[0], max(x_axis)],
    [75, 75],
    #label="75 %",
    color="lightgray",
    linestyle="--",
    linewidth=1,
    )
    ax.plot(
    [x_axis[0], max(x_axis)],
    [75.9, 75.9],
    #label="75 %",
    color="black",
    linestyle="--",
    linewidth=1,
    )
    ax.plot(
    [x_axis[0], max(x_axis)],
    [74, 74],
    color="lightgray",
    linestyle="--",
    linewidth=1,
    )
    ax.text(
    x_axis[-1] * 1.01,
    74,
    "74 %",
    color="lightgray",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
    ax.plot(
    [x_axis[0], max(x_axis)],
    [75.9, 75.9],
    #label="75 %",
    color="black",
    linestyle="--",
    linewidth=1,
    )
    ax.text(
    x_axis[-1] * 1.01,
    75,
    "75 %",
    color="lightgray",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
    ax.text(
    x_axis[-1] * 1.01,
    75.9,
    "75.9 %",
    color="black",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
    # Hide the all but the bottom spines (axis lines)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
 
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")
    ax.spines["bottom"].set_bounds(min(x_axis), max(x_axis))
    # -------------------BEGIN-CHANGES------------------------
    ax.set_xticks(np.arange(min(x_axis), max(x_axis) + 1))
    plt.legend()
    plt.show()
 
 
 
#visualize_accuracies(accuracy_array,x_axis)
 
def visualize_dual_plot(accuracy_array, x_axis):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.subplots_adjust(hspace=0.05)  # adjust space between Axes
 
    #SMALL_SIZE = 8
    #MEDIUM_SIZE = 10
    #BIGGER_SIZE = 18
    #
    #plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    #plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    #plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    #plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    #plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    #plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    #plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
 
    # plot the same data on both Axes
    ax2.set_xlabel('Fractional precision')
    #ax2.set_ylabel('Accuracy [%]')
    fig.text(0.08, 0.5, 'Accuracy [%]', va='center', rotation='vertical', fontsize=10)
    title_string = 'Accuracy performance of the ASIC SNN on the MNIST dataset during inference with different fractional precision'
    ax1.set_title(title_string, size=14)
    ax1.plot(x_axis, accuracy_array, linestyle='--', markersize=3, marker='o', color='b', label='Accuracy of ASIC SNN in behavioural simulation')
    ax2.plot(x_axis, accuracy_array, linestyle='--', markersize=3, marker='o', color='b', label='Accuracy of ASIC SNN in behavioural simulation')
 
 
    # zoom-in / limit the view to different portions of the data
    ax1.set_ylim(67, 80)  # most of the data
    ax2.set_ylim(0, 40)  # outliers only
 
    ax1.plot(
    [8, 8],
    [accuracy_array[0], max(accuracy_array)],
    #label="75 %",
    color="red",
    linestyle="--",
    linewidth=1,
    )
    ax1.text(
    8,
    accuracy_array[-1] * 1.01,
    "Breakdown point",
    color="red",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
    ax2.plot(
    [8, 8],
    [accuracy_array[0], max(accuracy_array)],
    #label="75 %",
    color="red",
    linestyle="--",
    linewidth=1,
    )
 
 
 
    ax1.plot(
    [x_axis[0], max(x_axis)],
    [75, 75],
    #label="75 %",
    color="lightgray",
    linestyle="--",
    linewidth=1,
    )
    #ax1.plot(
    #[x_axis[0], max(x_axis)],
    #[75.9, 75.9],
    ##label="75 %",
    #color="black",
    #linestyle="--",
    #linewidth=1,
    #)
    ax1.plot(
    [x_axis[0], max(x_axis)],
    [74, 74],
    color="lightgray",
    linestyle="--",
    linewidth=1,
    )
    ax1.text(
    x_axis[-1] * 1.01,
    74,
    "74 %",
    color="lightgray",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
 
    ax1.text(
    x_axis[-1] * 1.01,
    75,
    "75 %",
    color="lightgray",
    fontweight="bold",
    horizontalalignment="left",
    verticalalignment="center",
    )
    #ax1.text(
    #x_axis[-1] * 1.01,
    #75.9,
    #"75.9 %",
    #color="black",
    #fontweight="bold",
    #horizontalalignment="left",
    #verticalalignment="center",
    #)
    # hide the spines between ax and ax2
    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    #ax1.xaxis.tick_top()
    #ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()
    ax1.xaxis.set_visible(False)
 
    ax2.xaxis.set_ticks_position("bottom")
    #ax2.spines["bottom"].set_bounds(min(x_axis), max(x_axis))
    # -------------------BEGIN-CHANGES------------------------
    ax2.set_xticks(np.arange(min(x_axis), max(x_axis) + 1))
 
    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)
    # -------------------BEGIN-CHANGES------------------------
    #ax.set_xticks(np.arange(min(x_axis), max(x_axis) + 1))
    #plt.legend()
    plt.show()
 
visualize_dual_plot(accuracy_array, x_axis)