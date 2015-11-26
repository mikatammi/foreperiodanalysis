import numpy as np
from foreperiodanalysis.dataset import GazedataFile
from scipy.signal import medfilt


def get_gazepositions(trialdata):
    left_eye_valid = trialdata['ValidityLeftEye'] < 2
    right_eye_valid = trialdata['ValidityRightEye'] < 2
    both_eyes_valid = left_eye_valid == right_eye_valid
    either_eyes_valid = left_eye_valid | right_eye_valid
    only_left_eye_valid = left_eye_valid == ~both_eyes_valid
    only_right_eye_valid = right_eye_valid == ~both_eyes_valid

    # Create temporary array for filling in the valid gaze points
    tmp_array = np.zeros(shape=(either_eyes_valid.shape[0], 2),
                         dtype=np.float64)

    # Need to create a view on structured array so it is possible
    # to do calculations
    def myview(x): return x.view(dtype=np.float64).reshape(-1, 2)

    def mymean(x): return myview(x[both_eyes_valid]).mean(axis=1)

    # Calculate means for points having data from both left and right eye
    x_means = mymean(trialdata[['XGazePosLeftEye', 'XGazePosRightEye']])
    y_means = mymean(trialdata[['YGazePosLeftEye', 'YGazePosRightEye']])

    # Fill values into temporary array
    tmp_array[both_eyes_valid] = np.vstack((x_means, y_means)).T
    tmp_array[only_left_eye_valid] = myview(
        trialdata[['XGazePosLeftEye', 'YGazePosRightEye']]
                 [only_left_eye_valid])
    tmp_array[only_right_eye_valid] = myview(
        trialdata[['XGazePosRightEye', 'YGazePosRightEye']]
                 [only_right_eye_valid])

    # Return rows with valid data from temporary array
    return tmp_array[either_eyes_valid]


def median_filter(gazepositions):
    # TODO: This does median filtering for separate axis.
    #       Find out possibly more mathematical way to do this.
    return np.vstack((medfilt(gazepositions[:, 0]),
                      medfilt(gazepositions[:, 1]))).T


def extract_variance(gazepositions):
    return median_filter(gazepositions).var(axis=0)


def extract_traveled_distance(gazepositions):
    # TODO: Median filtering might round results to zero
    gz = median_filter(gazepositions)

    gz1 = gz[0:-2]
    gz2 = gz[1:-1]
    diff = gz2 - gz1
    dist = np.sqrt(np.power(diff, 2).sum(axis=1)).sum()

    return dist


def extract_features(trialdata):
    gazepositions = get_gazepositions(trialdata)

    return np.hstack((extract_variance(gazepositions),
                      extract_traveled_distance(gazepositions)))


def process_trial(trialdata):
    return extract_features(trialdata)


def process_gazedata(filename):
    print("Loading %s..." % (filename))
    gaze = GazedataFile(filename)

    # Remove failed trial data
    left_eye_valid = gaze.data['ValidityLeftEye'] < 2
    right_eye_valid = gaze.data['ValidityRightEye'] < 2
    either_eyes_valid = left_eye_valid | right_eye_valid

    gaze.data = gaze.data[either_eyes_valid]
    gaze.data = gaze.data[gaze.data['UserDefined_1'] == 'Face']
    gaze.data = gaze.data[gaze.data['TrialId'] != -1]

    trialids = np.unique(gaze.data['TrialId'])

    return dict(zip(trialids,
                map(process_trial,
                    map(lambda i: gaze.data[gaze.data['TrialId'] == i],
                        trialids))))
