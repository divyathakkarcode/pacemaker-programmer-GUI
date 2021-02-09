# Program to check if the parameter inputs are within the valid ranges. Returns 'True' if the input
# is valid, otherwise returns 'False'

# Lower Rate Limit 
def checkLRL (value):
    try:
        if 30<=int(value)<=175:
            return True
    except:
        return False

# Upper Rate Limit
def checkURL (value):
    try:
        if 50<=int(value)<=175:
            return True
    except:
        return False

# Maximum Sensor Rate
def checkMSR (value):
    try:
        if 50<=int(value)<=175:
            return True
    except:
        return False

# Fixed AV Delay
def checkFAVD (value):
    try:
        if 70<=int(value)<=300:
            return True
    except:
        return False

# Atrial/Ventricular Amplitude
def checkAmp (value):
    try:
        if 0 < float(value) <= 5:
            return True
    except:
        return False

# Atrial/Ventricular Pulse Width
def checkPW (value):
    try:
        if 1<=int(value)<=30:
            return True
    except:
        return False

# Atrial/Ventricular Refractory Period
def checkRP (value):
    try:
        if 150<=int(value)<=500:
            return True
    except:
        return False

# Activity Threshold
def checkAT (value):
    if value in ["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"]:
        return True
    return False

# Reaction Time
def checkReactTime (value):
    try:
        if 10<=int(value)<=50:
            return True
    except:
        return False

# Response Factor
def checkRF (value):
    try:
        if 1<=int(value)<=16:
            return True
    except:
        return False

# Recovery Time
def checkRecovTime (value):
    try:
        if 2<=int(value)<=16:
            return True
    except:
        return False

