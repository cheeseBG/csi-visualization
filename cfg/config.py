'''
    Configuration of Extractor and plot parameters
'''
# Setting this option to True removes Null Subcarriers.
# Null subcarriers have arbitrary values, and are used to
# help WiFi co-exist with other wireless technologies.
# https://www.oreilly.com/library/view/80211ac-a-survival/9781449357702/ch02.html
remove_null_subcarriers = True

# Pilot subcarriers are used to control the WiFi link,
# while other subcarriers carry data. I found pilot
# subcarriers sometimes have inconsistent CSI compared
# to the rest, and so I remove them. You may not necessarily
# face such issues.
remove_pilot_subcarriers = False

EXTRACTOR_CONFIG = {
    'wifi_chip': 'bcm43455c0',  # Raspberry Pi B3+ / B4
    'band': '2.4GHz',
    'bandwidth': '20MHz'
}

PLOT_PARAMETER = {

}


NULL_PILOT_SUBCARRIER = {
    'null_20': ['_' + str(x+32) for x in  [-32, -31, -30, -29, 31,  30,  29,  0]],

    'null_40': ['_' + str(x+32) for x in  [-64, -63, -62, -61, -60, -59, -1, 63,  62,  61,  60,  59,  1,  0]],

    'null_80': ['_' + str(x+32) for x in  [-128, -127, -126, -125, -124, -123, -1, 127,  126,  125,  124,  123,  1,  0]],

    'null_160': ['_' + str(x+32) for x in  [-256, -255, -254, -253, -252, -251, -129, -128, -127, -5, -4, -3, -2, -1,
                          255,  254,  253,  252,  251,  129,  128,  127,  5,  4,  3,  3,  1,  0]]

    'pilot_20': ['_' + str(x+32) for x in  [-21, -7, 21,  7]],

    'pilot_40': ['_' + str(x+32) for x in  [-53, -25, -11, 53,  25,  11]],

    'pilot_80': [x+128 for x in [-103, -75, -39, -11, 103,  75,  39,  11]],

    'pilot_160': [x+256 for x in [-231, -203, -167, -139, -117, -89, -53, -25, 231,  203,  167,  139,  117,  89,  53,  25]]
}
