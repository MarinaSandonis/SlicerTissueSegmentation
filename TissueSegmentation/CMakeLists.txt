cmake_minimum_required(VERSION 3.13.4)

project(TissueSegmentation)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/TissueSegmentation")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_CONTRIBUTORS "Rafael Cabeza Laguna (UPNA), Fernando Idoate Saralegui (Mutua Navarra), Marina Sandonís Fernández (UPNA)")
set(EXTENSION_DESCRIPTION "This is a scripted loadable module bundled in the SlicerTissueSegmentation extension. It gets the 2D/3D segmentation of the abdomen and the thigh from MR images.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/TissueSegmentation.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/TissueSegmentation/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(Tis_Seg)
add_subdirectory(TigSegLibrary)
add_subdirectory(TisSeg)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
