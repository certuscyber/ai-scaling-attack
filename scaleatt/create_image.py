# This script is based off the Jupyter notebook found in tutorial/jupyter_intro.ipynb by

from utils.plot_image_utils import plot_images_in_actual_size

from scaling.ScalingGenerator import ScalingGenerator
from scaling.SuppScalingLibraries import SuppScalingLibraries
from scaling.SuppScalingAlgorithms import SuppScalingAlgorithms
from scaling.ScalingApproach import ScalingApproach
from attack.QuadrScaleAttack import QuadraticScaleAttack
from attack.ScaleAttackStrategy import ScaleAttackStrategy
from utils.load_image_data import load_image_examples
import scaling.scale_utils as scale_utils
from utils.plot_image_utils import plot_images2
from PIL import Image
from numpy import asarray
import cv2 as cv
import argparse

def setScaling(userArg):
    # Allows user to provide their own scaling
    if type(userArg) is int or type(userArg) is str:
        scaling = float(userArg)
    else:
        scaling = None

    

    if scaling is None:
        scaling = 20

    if scaling < 0 or scaling > 100:
        print("scaling must be between 0 - 100.")
        exit()

    if scaling > 1:
        scaling = scaling / 100

    return scaling

def setAlgorithm(userArg):
    algorithm = userArg
    if algorithm is None:
        algorithm = "N"

    if algorithm.upper() == "N" or algorithm.upper() == "NEAREST":
        scaling_algorithm: SuppScalingAlgorithms = SuppScalingAlgorithms.NEAREST
    elif algorithm.upper() == "BL" or algorithm.upper() == "BILINEAR":
        scaling_algorithm: SuppScalingAlgorithms = SuppScalingAlgorithms.LINEAR
    elif algorithm.upper() == "BC" or algorithm.upper() == "BICUBIC":
        scaling_algorithm: SuppScalingAlgorithms = SuppScalingAlgorithms.CUBIC
    elif algorithm.upper() == "L" or algorithm.upper() == "LANCZOS":
        scaling_algorithm: SuppScalingAlgorithms = SuppScalingAlgorithms.LANCZOS
    elif algorithm.upper() == "A" or algorithm.upper() == "AREA":
        scaling_algorithm: SuppScalingAlgorithms = SuppScalingAlgorithms.AREA
    else:
        scaling_algorithm: SuppScalingAlgorithms = SuppScalingAlgorithms.NEAREST
        
    return scaling_algorithm

def setLibrary(library):

    if library is None:
        library = "T"
    
    if library.upper() == "C" or library.upper() == "OPENCV":
        scaling_library: SuppScalingLibraries = SuppScalingLibraries.CV
    elif library.upper() == "P" or library.upper() == "PILLOW":
        scaling_library: SuppScalingLibraries = SuppScalingLibraries.PIL
    else:
        scaling_library: SuppScalingLibraries = SuppScalingLibraries.TF
    return scaling_library
    

def scaleImage(normalPath, attackPath, scaling):
    normalImage = cv.imread(normalPath)
    attackImage = cv.imread(attackPath)


    # need to convert back to RGB because CV defaults to reading in BGR
    normalImage = cv.cvtColor(normalImage, cv.COLOR_BGR2RGB)
    attackImage = cv.cvtColor(attackImage, cv.COLOR_BGR2RGB)

    # Have to scale down the attack image so it will fit with the original image.
    scaledNormalImage = scale_utils.scale_cv2(normalImage, round(normalImage.shape[0]), round(normalImage.shape[1]))
    # Have to scale down the attack image so it will fit with the original image.
    scaledAttackImage = scale_utils.scale_cv2(attackImage, round(scaledNormalImage.shape[0] * scaling), round(scaledNormalImage.shape[1] * scaling))

    plot_images2(scaledNormalImage, scaledAttackImage)
    return [scaledNormalImage,scaledAttackImage] 

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="The file path to the original source image.", required=True)
    parser.add_argument("-t", "--target", help="The file path to the target image to inject into the source image.", required=True)
    parser.add_argument("-l", "--library", help="The library you would want to generate the malicious image. (C for OpenCV, P for Pillow, T for TensorFlow.) Default is TensorFlow")
    parser.add_argument("-a", "--algorithm", help="The algorithm you would want to generate the malicious image. (N for nearest, BL for bilinear, BC for bicubic, l for lanczos, A for area.) Default is nearest")
    parser.add_argument("-o", "--output", help="The name of the output image. Default output file will be output.png")
    parser.add_argument("-c", "--scaling", help="The percentage of resolution you would like to use when the target image appears in the output file. The higher the value the clear the target image. The default is 20% (Value must be between 0 and 100).")

    args = parser.parse_args()


    scaling_algorithm = setAlgorithm(args.algorithm)

    scaling = setScaling(args.scaling)

    scaling_library = setLibrary(args.library)

    # We support OpenCV, Pillow or TensorFlow (consider that Pillow has a 'secure' scaling behaviour for
    # Linear and Cubic, see Sec. 4.2 USENIX Security'20 paper)
    if args.algorithm.upper() == "A" or args.algorithm.upper() == "AREA":
        print("The Area algorithm is protected against scaling attacks.")
        exit()
    elif (args.library.upper() == "P" and not(args.algorithm.upper() == "N" or args.algorithm.upper() == "NEAREST")):
        print("The Pillow library is protected against scaling attacks if it does not using the nearest scaling algorithm.")
        exit()




    srcImage,attackImage = scaleImage(args.source,args.target, scaling)

    outputName = args.output
    if outputName is None:
        outputName = "output.png"

    scaler_approach: ScalingApproach = ScalingGenerator.create_scaling_approach(
        x_val_source_shape=srcImage.shape,
        x_val_target_shape=attackImage.shape,
        lib=scaling_library,
        alg=scaling_algorithm
    )

    scale_att: ScaleAttackStrategy = QuadraticScaleAttack(eps=1, verbose=False)
    
    result_attack_image, _, _ = scale_att.attack(src_image=srcImage,
                                                target_image=attackImage,
                                                scaler_approach=scaler_approach)

    # Display original image next to attack image
    plot_images_in_actual_size(imgs=[srcImage, result_attack_image], titles=["Source", "Attack"], rows=1)

    

    # To this end, let's scale down the attack image, as we would do in a real machine learning pipeline.
    result_output_image = scaler_approach.scale_image(xin=result_attack_image)

    

    # Proves that when scaled down it looks similar to the target image.
    plot_images_in_actual_size(imgs=[attackImage, result_output_image], titles=["Target", "Output"], rows=1)



    # Create output image
    output = Image.fromarray(result_attack_image)
    output.save(outputName)



if __name__ == "__main__":
    main()