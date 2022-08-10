cmake_minimum_required(VERSION 3.13.4)

project(TissueSegmentation)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/TissueSegmentation")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_CONTRIBUTORS "Rafael Cabeza Laguna (UPNA), Fernando Idoate Saralegui (Mutua Navarra), Marina Sandonís Fernández (UPNA)")
set(EXTENSION_DESCRIPTION "It gets the 2D/3D segmentation of the abdomen and the thigh from MR images")
set(EXTENSION_ICONURL "https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/TissueSegmentation.jpg")
set(EXTENSION_SCREENSHOTURLS "https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/Outputs.png https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/SegmentEditor.png https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/SlicerCapture.gif https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/inputs.png https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/module.png")
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