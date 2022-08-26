cmake_minimum_required(VERSION 3.13.4)

project(TissueSegmentation)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/MarinaSandonis/SlicerTissueSegmentation#slicertissuesegmentation")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_CONTRIBUTORS "Marina Sandonís Fernández (UPNA), Fernando Idoate Saralegui (Mutua Navarra), Rafael Cabeza Laguna (UPNA))"
set(EXTENSION_DESCRIPTION "Gets the 2D/3D segmentation of the abdomen and the thigh from MR images")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/MarinaSandonis/SlicerTissueSegmentation/main/TissueSegmentation.jpg")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/MarinaSandonis/SlicerTissueSegmentation/main/images/module.png https://raw.githubusercontent.com/MarinaSandonis/SlicerTissueSegmentation/main/images/inputs.png https://raw.githubusercontent.com/MarinaSandonis/SlicerTissueSegmentation/main/images/Outputs.png https://raw.githubusercontent.com/MarinaSandonis/SlicerTissueSegmentation/main/images/abdomen_segmenattion.png https://raw.githubusercontent.com/MarinaSandonis/SlicerTissueSegmentation/main/images/thigh_segmenattion.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(Tis_Seg)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
