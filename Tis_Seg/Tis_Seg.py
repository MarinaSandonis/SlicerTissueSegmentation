import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# Tis_Seg
#

class Tis_Seg(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Tissue Segmentation (Tis_Seg)"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Segmentation"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Rafael Cabeza Laguna (UPNA), Fernando Idoate Saralegui (Mutua Navarra), Marina Sandonís Fernández (UPNA)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    
    self.parent.helpText = """
This is a scripted loadable module bundled in the SlicerTissueSegmentation extension. It gets the 2D/3D segmentation of the abdomen and the thigh from MR images.

See more information in <a href="https://github.com/organization/projectname#Tis_Seg">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
    Contact: marinasandfer@gmail.com and  rcabeza@unavarra.es

"""


#
# Tis_SegWidget
#

class Tis_SegWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually Fand added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/Tis_Seg.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = Tis_SegLogic()

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    self.ui.inputSelectorWater.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIInputs)
    self.ui.inputSelectorFat.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIInputs)
    self.ui.MasterVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputSelector_l.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.segmentation_l.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputSelector_r.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.segmentation_r.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.NumberOfPartitions.connect("valueChanged(double)", self.updateParameterNodeFromGUI)
    self.ui.RangeWidget.connect("maximumValueChanged(double)", self.updateParameterNodeFromGUI)
    self.ui.RangeWidget.connect("minimumValueChanged(double)", self.updateParameterNodeFromGUI)    
    self.ui.ProcessIncompleteCheckBox.connect("toggled(bool)", self.updateParameterNodeFromGUI)

    self.ui.inputSelectorWater_Abdo.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIAbdo)
    self.ui.inputSelectorFat_Abdo.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIAbdo)
    self.ui.inputSelectorROI.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIAbdo)
    self.ui.outputSelector_Abdo.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIAbdo)
    self.ui.segmentation_Abdo.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUIAbdo)
    self.ui.NumberOfPartitions_Abdo.connect("valueChanged(double)", self.updateParameterNodeFromGUIAbdo)
    self.ui.RangeWidget_Abdo.connect("maximumValueChanged(double)", self.updateParameterNodeFromGUIAbdo)
    self.ui.RangeWidget_Abdo.connect("minimumValueChanged(double)", self.updateParameterNodeFromGUIAbdo)    

    # Buttons
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.ui.applyButtonAbdo.connect('clicked(bool)', self.onApplyButtonAbdo)


    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()

    #Tooltips

    self.ui.inputSelectorWater_Abdo.setToolTip ('Pick the water input image')
    self.ui.inputSelectorFat_Abdo.setToolTip ('Pick the fat input image')
    self.ui.outputSelector_Abdo.setToolTip("Select the volume where the color label map will be saved. Resets label map volumes on each run")
    self.ui.inputSelectorROI.setToolTip("Pick the ROI input segmentation")
    self.ui.segmentation_Abdo.setToolTip("Select the volume where the color segmentation will be saved")
    self.ui.NumberOfPartitions_Abdo.setToolTip('Select the number of partitions on which the volume will be analysed')
    self.ui.RangeWidget_Abdo.setToolTip('Select the number of slices of the image to be segmented. Both end slices are included')

    self.ui.inputSelectorWater.setToolTip ('Pick the water input image')
    self.ui.inputSelectorFat.setToolTip ('Pick the fat input image')
    self.ui.outputSelector_l.setToolTip("Select the volume where left thigh color label map will be saved. Resets label map volumes on each run")
    self.ui.outputSelector_r.setToolTip("Select the volume where right thigh color label map will be saved. Resets label map volumes on each run")
    self.ui.segmentation_l.setToolTip("Select the volume where left thigh color segmentation will be saved")
    self.ui.segmentation_r.setToolTip("Select the volume where right thigh color segmentation will be saved")
    self.ui.NumberOfPartitions.setToolTip('Select the number of partitions on which the volume will be analysed')
    self.ui.RangeWidget.setToolTip('Select the number of slices of the image to be segmented. Both end slices are included')
    self.ui.ProcessIncompleteCheckBox.setToolTip('If the box is checked, incomplete thighs will be segmented even though the results are not 100% accurate')
    self.ui.MasterVolumeSelector.setToolTip("In case the images don't have the same spatial information, a master volume should be selected")

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.logic.installRequiredPythonPackages()
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())
    
  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)


    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    self.ui.inputSelectorWater.setCurrentNode(self._parameterNode.GetNodeReference("InputVolumeW"))
    self.ui.inputSelectorFat.setCurrentNode(self._parameterNode.GetNodeReference("InputVolumeF"))
    self.ui.MasterVolumeSelector.setCurrentNode(self._parameterNode.GetNodeReference("MasterVolume"))
    self.ui.outputSelector_l.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume_l"))
    self.ui.segmentation_l.setCurrentNode(self._parameterNode.GetNodeReference("Segmentation_l"))
    self.ui.outputSelector_r.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume_r"))
    self.ui.segmentation_r.setCurrentNode(self._parameterNode.GetNodeReference("Segmentation_r"))
    self.ui.NumberOfPartitions.value = float(self._parameterNode.GetParameter("numberOfPartitions"))
    self.ui.RangeWidget.maximumValue= float(self._parameterNode.GetParameter("MaxSliceRange"))
    self.ui.RangeWidget.minimumValue= float(self._parameterNode.GetParameter("MinSliceRange"))
    self.ui.ProcessIncompleteCheckBox.checked = (self._parameterNode.GetParameter("Incomplete") == "true")

    self.ui.inputSelectorWater_Abdo.setCurrentNode(self._parameterNode.GetNodeReference("InputVolumeW_Abdo"))
    self.ui.inputSelectorFat_Abdo.setCurrentNode(self._parameterNode.GetNodeReference("InputVolumeF_Abdo"))
    self.ui.inputSelectorROI.setCurrentNode(self._parameterNode.GetNodeReference("InputVolumeROI"))
    self.ui.outputSelector_Abdo.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume_Abdo"))
    self.ui.segmentation_Abdo.setCurrentNode(self._parameterNode.GetNodeReference("Segmentation_Abdo"))
    self.ui.NumberOfPartitions_Abdo.value = float(self._parameterNode.GetParameter("numberOfPartitions_Abdo"))
    self.ui.RangeWidget_Abdo.maximumValue= float(self._parameterNode.GetParameter("MaxSliceRange_Abdo"))
    self.ui.RangeWidget_Abdo.minimumValue= float(self._parameterNode.GetParameter("MinSliceRange_Abdo"))

    # Update buttons states and tooltips
    if  self._parameterNode.GetNodeReference("OutputVolume_r") and self._parameterNode.GetNodeReference("OutputVolume_l") and\
        self._parameterNode.GetNodeReference("Segmentation_r") and self._parameterNode.GetNodeReference("Segmentation_l"):
      self.ui.applyButton.toolTip = "Compute output volume"
      self.ui.applyButton.enabled = True
    else:
      self.ui.applyButton.toolTip = "Select output volume node"
      self.ui.applyButton.enabled = False

    if  self._parameterNode.GetNodeReference("OutputVolume_Abdo") and self._parameterNode.GetNodeReference("Segmentation_Abdo"):
      self.ui.applyButtonAbdo.toolTip = "Compute output volume"
      self.ui.applyButtonAbdo.enabled = True
    else:
      self.ui.applyButtonAbdo.toolTip = "Select output volume node"
      self.ui.applyButtonAbdo.enabled = False

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def changeRangeWidgetMaximum(self, input, range):
    """
    This method is called when the user select the input image.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """
    import sitkUtils
    fat_img=sitkUtils.PullVolumeFromSlicer(input)
    aux = fat_img.GetSize()
    max = float (aux[2]-1)
    range.maximum=max
    
  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """
  
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch
    self._parameterNode.SetNodeReferenceID("MasterVolume", self.ui.MasterVolumeSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputVolume_l", self.ui.outputSelector_l.currentNodeID)
    self._parameterNode.SetNodeReferenceID("Segmentation_l", self.ui.segmentation_l.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputVolume_r", self.ui.outputSelector_r.currentNodeID)
    self._parameterNode.SetNodeReferenceID("Segmentation_r", self.ui.segmentation_r.currentNodeID)
    self._parameterNode.SetParameter("numberOfPartitions", str(self.ui.NumberOfPartitions.value))
    self._parameterNode.SetParameter("MaxSliceRange",str(self.ui.RangeWidget.maximumValue))
    self._parameterNode.SetParameter("MinSliceRange", str(self.ui.RangeWidget.minimumValue))
    self._parameterNode.SetParameter("Incomplete", "true" if self.ui.ProcessIncompleteCheckBox.checked else "false")
    
    self._parameterNode.EndModify(wasModified)

    if self.ui.inputSelectorFat.currentNodeID=="" or self.ui.inputSelectorWater.currentNodeID=="" :
     
      return

    else:
      self.changeRangeWidgetMaximum(self.ui.inputSelectorFat.currentNodeID, self.ui.RangeWidget)


  def updateParameterNodeFromGUIInputs(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """
    import sitkUtils

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch
    self._parameterNode.SetNodeReferenceID("InputVolumeW", self.ui.inputSelectorWater.currentNodeID)
    self._parameterNode.SetNodeReferenceID("InputVolumeF", self.ui.inputSelectorFat.currentNodeID)
    self._parameterNode.EndModify(wasModified)

    if self.ui.inputSelectorFat.currentNodeID=="" or self.ui.inputSelectorWater.currentNodeID=="" :
      return
    else:
      fat_img = sitkUtils.PullVolumeFromSlicer(self.ui.inputSelectorFat.currentNodeID)
      water_img = sitkUtils.PullVolumeFromSlicer(self.ui.inputSelectorWater.currentNodeID)
      if fat_img.GetSize() != water_img.GetSize() or \
              fat_img.GetSpacing() != water_img.GetSpacing()  or \
              fat_img.GetDirection() != water_img.GetDirection() or \
              fat_img.GetOrigin() != water_img.GetOrigin():
        if fat_img.GetSize() == water_img.GetSize():
            msgBox = qt.QMessageBox()
            msgBox.setText("The images don't have the same spatial reference.")
            msgBox.setInformativeText("Select a master volume")
            msgBox.setIcon(qt.QMessageBox.Warning)
            msgBox.setWindowTitle('WARNING')
            ret = msgBox.exec_()
            self.ui.MasterVolumeSelector.enabled = True
            wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch
            self._parameterNode.SetNodeReferenceID("MasterVolume", self.ui.MasterVolumeSelector.currentNodeID)
            self._parameterNode.EndModify(wasModified)

        else:
            self.ui.MasterVolumeSelector.setCurrentNode(None)
            self.ui.MasterVolumeSelector.enabled = False
            wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch
            self._parameterNode.SetNodeReferenceID("MasterVolume", self.ui.MasterVolumeSelector.currentNodeID)
            self._parameterNode.EndModify(wasModified)
      else:
        self.ui.MasterVolumeSelector.setCurrentNode(None)
        self.ui.MasterVolumeSelector.enabled = False
        wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch
        self._parameterNode.SetNodeReferenceID("MasterVolume", self.ui.MasterVolumeSelector.currentNodeID)
        self._parameterNode.EndModify(wasModified)

  def updateParameterNodeFromGUIAbdo(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch
    self._parameterNode.SetNodeReferenceID("InputVolumeW_Abdo", self.ui.inputSelectorWater_Abdo.currentNodeID)
    self._parameterNode.SetNodeReferenceID("InputVolumeF_Abdo", self.ui.inputSelectorFat_Abdo.currentNodeID)
    self._parameterNode.SetNodeReferenceID("InputVolumeROI", self.ui.inputSelectorROI.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputVolume_Abdo", self.ui.outputSelector_Abdo.currentNodeID)
    self._parameterNode.SetNodeReferenceID("Segmentation_Abdo", self.ui.segmentation_Abdo.currentNodeID)
    self._parameterNode.SetParameter("numberOfPartitions_Abdo", str(self.ui.NumberOfPartitions_Abdo.value))
    self._parameterNode.SetParameter("MaxSliceRange_Abdo",str(self.ui.RangeWidget_Abdo.maximumValue))
    self._parameterNode.SetParameter("MinSliceRange_Abdo", str(self.ui.RangeWidget_Abdo.minimumValue))
    
    self._parameterNode.EndModify(wasModified)

    if self.ui.inputSelectorFat_Abdo.currentNodeID=="" or self.ui.inputSelectorWater_Abdo.currentNodeID=="":
      return
    else:
      
      self.changeRangeWidgetMaximum(self.ui.inputSelectorFat_Abdo.currentNodeID, self.ui.RangeWidget_Abdo)

      
  
  def onApplyButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    self.ui.applyButton.text = 'Working...'
    self.ui.applyButton.setEnabled(False)
    slicer.app.processEvents()

    logic = Tis_SegLogic()
    logic.process(self.ui.inputSelectorWater.currentNode(), self.ui.inputSelectorFat.currentNode(),  \
      self.ui.outputSelector_l.currentNode(), self.ui.segmentation_l.currentNode(),\
      self.ui.outputSelector_r.currentNode(), self.ui.segmentation_r.currentNode(),\
      self.ui.NumberOfPartitions.value, self.ui.RangeWidget.maximumValue, self.ui.RangeWidget.minimumValue,\
      self.ui.ProcessIncompleteCheckBox.checked, self.ui.MasterVolumeSelector.currentNode(),  showResult=True) 

    self.ui.applyButton.text = 'Apply'
    self.ui.applyButton.setEnabled(True)
    slicer.app.processEvents()

  def onApplyButtonAbdo(self):
      """
      Run processing when user clicks "Apply" button.
      """
      self.ui.applyButtonAbdo.text = 'Working...'
      self.ui.applyButtonAbdo.setEnabled(False)
      slicer.app.processEvents()

      logic = Tis_SegLogic()
      logic.processAbdo(self.ui.inputSelectorWater_Abdo.currentNode(), self.ui.inputSelectorFat_Abdo.currentNode(),\
        self.ui.inputSelectorROI.currentNode(),self.ui.outputSelector_Abdo.currentNode(), self.ui.segmentation_Abdo.currentNode(),\
        self.ui.NumberOfPartitions_Abdo.value, self.ui.RangeWidget_Abdo.maximumValue, self.ui.RangeWidget_Abdo.minimumValue, showResult=True) 

      self.ui.applyButtonAbdo.text = 'Apply'
      self.ui.applyButtonAbdo.setEnabled(True)
      slicer.app.processEvents()

  #
# Tis_SegLogic
#

class Tis_SegLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  def installRequiredPythonPackages(self):
    try: 
      import skimage as sk
    except: 
      slicer.util.pip_install('scikit-image')
    try:
      import sklearn as skl
    except: 
      slicer.util.pip_install('scikit-learn')
    try: 
      from tisseglibrary import tisseglibrary
    except: 
      slicer.util.pip_install('TisSegLibrary')

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("numberOfPartitions"):
      parameterNode.SetParameter("numberOfPartitions", "10.0")
    if not parameterNode.GetParameter("MinSliceRange"):
      parameterNode.SetParameter("MinSliceRange", "20.00")
    if not parameterNode.GetParameter("MaxSliceRange"):
      parameterNode.SetParameter("MaxSliceRange", "60.00")
    if not parameterNode.GetParameter("Incomplete"):
      parameterNode.SetParameter("Incomplete", "false")


    if not parameterNode.GetParameter("numberOfPartitions_Abdo"):
      parameterNode.SetParameter("numberOfPartitions_Abdo", "10.0")
    if not parameterNode.GetParameter("MinSliceRange_Abdo"):
      parameterNode.SetParameter("MinSliceRange_Abdo", "20.00")
    if not parameterNode.GetParameter("MaxSliceRange_Abdo"):
      parameterNode.SetParameter("MaxSliceRange_Abdo", "60.00")
    
  def getsegmentation_Abdo(self, inputVolumeW_Abdo, inputVolumeF_Abdo, inputVolumeROI , OutputVolume_Abdo, Segmentation_Abdo,  numberOfPartitions_Abdo, RangeSlice_Abdo):
      '''
      Compute the segmentation of the abdomen
      '''
      import sitkUtils
      from tisseglibrary import tisseglibrary

      if inputVolumeF_Abdo is None or inputVolumeW_Abdo is None or inputVolumeROI is None:
        slicer.util.errorDisplay('Select the input images') 

      else : 
        #Leemos las imágenes
        fat_img=sitkUtils.PullVolumeFromSlicer(inputVolumeF_Abdo)
        water_img=sitkUtils.PullVolumeFromSlicer(inputVolumeW_Abdo)

        referenceVolumeNode = inputVolumeF_Abdo
        labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")
        inputVolumeROI.SetReferenceImageGeometryParameterFromVolumeNode(referenceVolumeNode)
        slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(inputVolumeROI, labelmapVolumeNode, referenceVolumeNode)
        roi_img = sitkUtils.PullVolumeFromSlicer(labelmapVolumeNode)
        slicer.mrmlScene.RemoveNode(labelmapVolumeNode)

        #Comprobamos el número de particiones y el rango
        if numberOfPartitions_Abdo > (RangeSlice_Abdo[1]-RangeSlice_Abdo[0]):
          slicer.util.errorDisplay ('The number of partitions is greater than the selected range of slices')
        else:
          
          classImage2_img = tisseglibrary.AbdomenSegmentation(fat_img, water_img, roi_img, RangeSlice_Abdo, numberOfPartitions_Abdo)
          
          sitkUtils.PushVolumeToSlicer(classImage2_img, OutputVolume_Abdo)

          slicer.util.setSliceViewerLayers(background=OutputVolume_Abdo)

          tisseglibrary.ColorSegmentation_Abdo(OutputVolume_Abdo, Segmentation_Abdo)


  def getsegmentation(self, inputVolumeW, inputVolumeF,  outputVolume_l, Segmentation_l, outputVolume_r, Segmentation_r, RangeSlice, numberOfPartitions, incomplete, MasterVolume ):
    '''
    Compute the segmentation of the thights

    '''
    import sitkUtils
    from tisseglibrary import tisseglibrary

    if inputVolumeF is None or inputVolumeW is None:
  
      slicer.util.errorDisplay('Select the input images') 

    else:
        #Leemos las imágenes
        fat_img=sitkUtils.PullVolumeFromSlicer(inputVolumeF)
        water_img=sitkUtils.PullVolumeFromSlicer(inputVolumeW)
       
        if MasterVolume is not None:
          master_img=sitkUtils.PullVolumeFromSlicer(MasterVolume)
          fat_img.CopyInformation(master_img)
          water_img.CopyInformation(master_img)


        #Comprobamos el número de particiones y el rango
        if numberOfPartitions > (RangeSlice[1]-RangeSlice[0]):
          #self.delayDisplay('ERROR: número de particiones mayor que el rango de slices seleccionado', 10000)
          slicer.util.errorDisplay ('The number of partitions is greater than the selected range of slices')
        
        else:
          
          out_l, out_r , right_full_Q, left_full_Q, sum_left, sum_right= tisseglibrary.ThighSegmentation(fat_img, water_img, 
                                                                          RangeSlice, numberOfPartitions, incomplete)

          if left_full_Q == True and right_full_Q == False:
            print('entra en 1')
            if incomplete == False:
              slicer.util.infoDisplay("Incomplete right thigh. \nTo have them processed check the box")
              sitkUtils.PushVolumeToSlicer(out_r , outputVolume_r)
              slicer.util.setSliceViewerLayers(background=outputVolume_r)
              
            else:
    
              sitkUtils.PushVolumeToSlicer(out_r , outputVolume_r)
              slicer.util.setSliceViewerLayers(background=outputVolume_r)
              tisseglibrary.ColorSegmentation(outputVolume_r, '_r', Segmentation_r)

            sitkUtils.PushVolumeToSlicer(out_l, outputVolume_l)
            slicer.util.setSliceViewerLayers(background=outputVolume_l)
            tisseglibrary.ColorSegmentation(outputVolume_l, '_l', Segmentation_l)
            

          elif left_full_Q == False and right_full_Q == True:
            print('entra en 2')
            if incomplete == False:
              slicer.util.infoDisplay("Incomplete left thigh. \nTo have them processed check the box")
              sitkUtils.PushVolumeToSlicer(out_l , outputVolume_l)
              slicer.util.setSliceViewerLayers(background=outputVolume_l)

            else:
              sitkUtils.PushVolumeToSlicer(out_l , outputVolume_l)
              slicer.util.setSliceViewerLayers(background=outputVolume_l)
              tisseglibrary.ColorSegmentation(outputVolume_l, '_r', Segmentation_l)

            
            sitkUtils.PushVolumeToSlicer(out_r , outputVolume_r)
            slicer.util.setSliceViewerLayers(background=outputVolume_r)
            tisseglibrary.ColorSegmentation(outputVolume_r, '_r', Segmentation_r)

          elif left_full_Q == True and right_full_Q == True:
            
            sitkUtils.PushVolumeToSlicer(out_l , outputVolume_l)
            slicer.util.setSliceViewerLayers(background=outputVolume_l)
            tisseglibrary.ColorSegmentation(outputVolume_l, '_l', Segmentation_l)

            sitkUtils.PushVolumeToSlicer(out_r , outputVolume_r)
            slicer.util.setSliceViewerLayers(background=outputVolume_r)
            tisseglibrary.ColorSegmentation(outputVolume_r, '_r', Segmentation_r)

            
          elif left_full_Q == False and right_full_Q == False:
            if incomplete == True:
          
              if sum_left ==0 and sum_right!=0:
                slicer.util.infoDisplay("Thighs could not be divided")
                
                sitkUtils.PushVolumeToSlicer(out_r, outputVolume_r)
                slicer.util.setSliceViewerLayers(background=outputVolume_r)
                tisseglibrary.ColorSegmentation(outputVolume_r, '', Segmentation_r)
                
                sitkUtils.PushVolumeToSlicer(out_l , outputVolume_l)
                slicer.util.setSliceViewerLayers(background=outputVolume_l)

              elif sum_right==0 and sum_left!=0:
                slicer.util.infoDisplay("Thighs could not be divided")
                sitkUtils.PushVolumeToSlicer(out_l, outputVolume_l)
                slicer.util.setSliceViewerLayers(background=outputVolume_l)
                tisseglibrary.ColorSegmentation(outputVolume_l, '', Segmentation_l)

                sitkUtils.PushVolumeToSlicer(out_r , outputVolume_r)
                slicer.util.setSliceViewerLayers(background=outputVolume_r)
              
              elif sum_right!=0 and sum_left!=0:
                sitkUtils.PushVolumeToSlicer(out_l, outputVolume_l)
                slicer.util.setSliceViewerLayers(background=outputVolume_l)
                tisseglibrary.ColorSegmentation(outputVolume_l, '', Segmentation_l)

                sitkUtils.PushVolumeToSlicer(out_r, outputVolume_r)
                slicer.util.setSliceViewerLayers(background=outputVolume_r)
                tisseglibrary.ColorSegmentation(outputVolume_r, '', Segmentation_r)

            else:
              slicer.app.processEvents()
              slicer.util.infoDisplay("Incomplete thighs \nTo have them processed check the box")
            
      
        return outputVolume_l, Segmentation_l, outputVolume_r, Segmentation_r
        
  def process(self, inputVolumeW, inputVolumeF , outputVolume_l, Segmentation_l, outputVolume_r, Segmentation_r, numberOfPartitions, MaxSliceRange, MinSliceRange , incomplete , MasterVolume, showResult=True):
    """
    Run the actual algorithm
    """

    RangeSlice = [MinSliceRange, MaxSliceRange+1]

    outputVolume_r.CreateDefaultDisplayNodes()
    displayOutput_r = outputVolume_r.GetDisplayNode()
    displayOutput_r.SetAndObserveColorNodeID("vtkMRMLColorTableNodeFileGenericColors.txt")

    outputVolume_l.CreateDefaultDisplayNodes()
    displayOutput_l = outputVolume_l.GetDisplayNode()
    displayOutput_l.SetAndObserveColorNodeID("vtkMRMLColorTableNodeFileGenericColors.txt")

    self.getsegmentation(inputVolumeW, inputVolumeF, outputVolume_l, Segmentation_l, outputVolume_r, Segmentation_r, RangeSlice, numberOfPartitions, incomplete, MasterVolume)


    return True

  def processAbdo(self, inputVolumeW_Abdo, inputVolumeF_Abdo, inputVolumeROI, OutputVolume_Abdo, Segmentation_Abdo, numberOfPartitions_Abdo, MaxSliceRange_Abdo, MinSliceRange_Abdo , showResult=True):
    """
    Run the actual algorithm
    """
    import numpy as np

    RangeSlice_Abdo = np.array([MinSliceRange_Abdo, MaxSliceRange_Abdo+1]).astype(np.int32)

    OutputVolume_Abdo.CreateDefaultDisplayNodes()
    displayOutput_Abdo = OutputVolume_Abdo.GetDisplayNode()
    displayOutput_Abdo.SetAndObserveColorNodeID("vtkMRMLColorTableNodeFileGenericColors.txt")

    self.getsegmentation_Abdo(inputVolumeW_Abdo, inputVolumeF_Abdo,  inputVolumeROI, OutputVolume_Abdo, Segmentation_Abdo, numberOfPartitions_Abdo,  RangeSlice_Abdo)


    return True

#
# Tis_SegTest
#

class Tis_SegTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Tis_Seg1()

  def test_Tis_Seg1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test", 10000)
    self.delayDisplay('Test passed', 10000)
