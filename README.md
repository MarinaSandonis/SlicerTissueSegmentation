
# SlicerTissueSegmentation
TissueSegmentation is a 3D Slicer extension designed to provide access to tools for segmenting different tissues of the thigh and abdomen 
1.	Select the module
![alt text](https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/module.png?raw=true)
<br>
<br>
3.	Select the anatomical region to segment
<br>
<br>
![alt text](https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/inputs.png?raw=true)
<br>
<br>
5.	Introduce the input parameters and images
    a.	Introduce the water and fat MRI 
    b.	Introduce the input parameters that are solicited
    In the abdomen case, a ROI segmentation is required too. To obtain that ROI, the 'Segment Editor' module should be used.
      - Create a new segmentation and select a master volume
      - Add a new segment 
      - Making use of the 'Draw 'tool, a segmentation of the area contained within the outer edge of the visceral fat (VAT) should be created.
      
      In case a 3D segmentation is wanted to be done, the first and last slice of the range of the image that is going to be analyzed should be marked manually. 
      The other slices are marked automatically using the ‘Fill between slices’ tool. It is recommended to mark some intermediate slices manually if the anatomical
      characteristics of the image change.  
<br>
<br>
![alt text](https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/Segment Editor.png?raw=true)
<br>
<br>
4.	Create the output volumes and segmentations
![alt text](https://github.com/MarinaSandonis/SlicerTissueSegmentation/blob/main/images/Outputs.png?raw=true)
<br>
<br>

