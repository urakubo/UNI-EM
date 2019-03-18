[Japanese version here](Workflow1.ja.md)

- [How to use: Dojo proofreader](HowToUse.md#Dojo-proofreader)
- [How to use: 3D annotator](HowToUse.md#3D-annotator)
- [How to use: 2D DNN](HowToUse.md#2D-DNN)
- [How to use: 3D FFN](HowToUse.md#3D-FFN)
- [How to use: 2D and 3D filters](HowToUse.md#2D-and-3D-filters)
- [Example workflow1: Mitochondria segmentation by use of 2D DNN](Workflow1.md)
- [Example workflow2: Membrane segmentation by use of 3D FFN](Workflow2.md) 

## Example workflow 1: Mitochondria segmentation by use of 2D DNN

Here we try automated mitochondria segmentation of a stack of EM images by use of a 2-dimentional deep neural network (2D DNN). The target EM stack was obtained by Kasthuri et al. ( Cell 162(3):648-61, 2015 ). The target brain region is mouse somatosensory cortex, and they used an automatic tape-collecting ultra-microtome system (ATUM) for SEM imaging (ATUM/SEM).  The EM stack was originally arranged for ISBI 2013 challenge ([SNEMI3D](http://brainiac2.mit.edu/SNEMI3D/)), and we here reuse it. The EM images are open to public under Open Data Commons Attribution License (ODC-By) v1.0. The original images were passed through the Contrast Limited Adaptive Histogram Equalization filter (CLAHE; blocksize 127,　Histogram bins 256, max slope 1.50).

- https://neurodata.io/data/kasthuri15/
- https://opendatacommons.org/licenses/by/1-0/
- http://docs.neurodata.io/kasthuri2015/kasthuri15docs.html

#### Target EM images and ground truth

1. Download the file "Example2DNN.zip" from the link below and unzip it on your UNI-EM installed PC. Copy and paste the unzipped contents to the "data" folder of UNI-EM ([UNI-EM]). Here the training image is stored in "[UNI-EM]/data/_2DNN_training_images", and the ground truth segmentation is stored in "[UNI-EM]/data/_2DNN_ground_truth" (**Fig. 1**). The software Vast lite is recommend to make such ground truth segmentation ( https://software.rc.fas.harvard.edu/lichtman/vast/ ).

	- "Example2DNN.zip": https://www.dropbox.com/s/k1baokh6yz1ucjk/Example2DNN.zip?dl=0
<BR>
<p align="center">
  <img src="Images/Training_GroundTruth.png" alt="2D DNN Training" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 1. Training EM image and mitochondria ground truth segmentation</b> </font>
</p>
<BR>


#### Training and inference

2. Launch UNI-EM.

3. Select "Segmentation → 2DNN" from a UNI-EM dropdown menu to launch a dialogue that is named as 2D DNN (**Fig. 2a**).
	- Select Training tab (**Fig. 2b**).
	- Confirm that "Image Folder" targets [UNI-EM]/data/_2DNN_training_images (**Fig. 2c**), "Segmentation Folder" targets [UNI-EM]/data/_2DNN_ground_truth (**Fig. 2d**), and "Checkpoint Folder" targets [UNI-EM]/data/_2DNN_model_tensorflow (**Fig. 2e**).
	- Select "resnet" from the tab menu in the middle (**Fig. 2f**), and set "N res blocks" as 16 (**Fig. 2g**). This is because Resnet is one of the best network topologies for mitochondria segmentation (Ref 1).
	- Save all parameters by clicking "Save Parameters". The saved parameters are loaded by clicking "Load Parameters".

4. Start Res-net training by clicking the "Execute" button (**Fig. 2h**). Users will see initial and progress messages in the console window (shown below). It takes 6-min for a desktop PC equipped with a NIVIDA GTX1070 GPU. The console window shows a message "saving model" when the training is finished. During and after the training period, users can visually inspect its progression through Tensorboad by selecting "Segmentation → Tensorboard".
```2D DNN Training
        progress  epoch 49  step 1  image/sec 5.2  remaining 6m
        discrim_loss 0.49639216
        gen_loss_GAN 0.41848987
        gen_loss_classic 0.13485438
        recording summary
        progress  epoch 99  step 1  image/sec 5.5  remaining 5m
        discrim_loss 0.69121116
        gen_loss_GAN 0.73412275
        gen_loss_classic 0.13613938
        ...
        ...
        progress  epoch 1999  step 1  image/sec 7.3  remaining 0m
        discrim_loss 0.715416
        gen_loss_GAN 2.1579466
        gen_loss_classic 0.04729831
        saving model
```
5. Select the inference tab in the 2D DNN dialogue (**Fig. 2b**).
	- Confirm that "Image Folder " targets [UNI-EM]/data/_2DNN_test_images, "Output Segmentation Folder" targets [UNI-EM]/data/_2DNN_inference, and "Checkpoint Folder" targets [UNI-EM]/data/_2DNN_model_tensorflow.

6. Start inference by clicking the "Execute" button in the Inference tab. Users will see initial and progress messages in the console window (shown below). Users will see "evaluated image 0099" when Inference is finished.
```2D DNN Inference
        parameter_count = 68334848
        loading all from checkpoint
        evaluated image 0000
        evaluated image 0001
        evaluated image 0002
        ...
        ...
        evaluated image 0097
        evaluated image 0098
        evaluated image 0099
```
7. Confirm that the "Output Segmentation Folder" ( [UNI-EM]/data/_2DNN_inference ) contains 0000.png, 0001.png, ..., 0099.png .

<p align="center">
  <img src="Images/2DNN_Training.png" alt="2D DNN dialog for training" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 2. 2D DNN training dialog</b> </font>
</p>
<BR>


#### Postprocessing: binarization and labeling

8. Select "Plugins → 2D Filters" from the UNI-EM dropdown menu to launch the dialogue "2D Filters" (**Fig. 3**).
	- Select the Binary tab (**Fig. 3a**).
	- Confirm that "Target Folder" targets [UNI-EM]/data/_2DNN_inference (**Fig. 3b**).
	- Confirm that "Output Folder" targets [UNI-EM]/data/_2DNN_segmentation (**Fig. 3c**)。
	- Users will see a thumbnail image in the "Target image" space and manipulate it by the slide bars of Target X, Target Y, and Target Z (**Fig. 3d**). Users will see an example result of binarization by clicking "Obtain sample output" (**Fig. 3e**).

9. Start binarization by clicking the "Execute" button (**Fig. 3f**). Users will see progress messages in the console window as follows.
```2D Binarization
        Target Folder:  [UNI-EM]/data/_2DNN_inference
        Output Folder:  [UNI-EM]/data/_2DNN_segmentation
        No: 0
        No: 1
        ...
        ...
        No: 98
        No: 99
        Binary was executed!
```

10. Select "Plugins → 3D Filters" from the UNI-EM dropdown menu to launch the dialogue "3D Filters".
	- Select the Label tab.
	- Set "Target Folder" as **[UNI-EM]/data/_2DNN_segmentation** . 
	- Set "Output Folder" as **[UNI-EM]/data/_2DNN_segmentation2** .

11. Start labeling by clicking the "Execute" button. Users will see progress messages as follows.
```3D Labeling
        Target Folder:  [UNI-EM]/data/_2DNN_segmentation
        Output Folder:  [UNI-EM]/data/_2DNN_segmentation2
        Loading images ...
        Saving images ...
        Label was executed!
```

<p align="center">
  <img src="Images/2D_Binary.png" alt="Dialog for binarization" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 3. Dialog for binarization</b> </font>
</p>
<BR>

#### Proofreading, annotation, and visualization

12. Select "Dojo → Import EM Stack/Segmentation" from the UNI-EM dropdown menu to launch the dialogue "Import Images & Segments".
	- Set "Source Image Folder" as **[UNI-EM]/data/_2DNN_test_images** .
	- Set "Source Segmentation Folder" as **[UNI-EM]/data/_2DNN_segmentation2** .
	- Create a file folder and set it as "Destination Dojo Folder". Dojo style files will be generated in this folder.

13. Generate the Dojo style files by clicking the "OK" button. The software Dojo will be launched after the file generation (**Fig. 4a**).

14. Inspect successful segmentation visually through manipulating the bottom slice bar (**Fig. 4b**), top Zoom bar (**Fig. 4c**), and top Opacity bar (**Fig. 4d**).

15. Correct erroneous segmentation by entering the mode "Adjust". Click an icon whose shape has a fused two area (**Fig. 4e**). In the adjust mode, users can fill voids by dragging the circled cursor from a filled area. The +/- keys change its radius. Press the Tab key to verify the change, or the Esc key to cancel the change. Users can erase unnecessary areas by dragging the circled cursor after clicking the eraser icon (**Fig. 4f**).

16. Save the segmentation after proofreading. Users can also export the segmentation by selecting "Dojo → Export Segmentation" from the UNI-EM dropdown menu. The export file style is sequential png/tiff images.

17. Select "Annotator → Open" from the UNI-EM dropdown menu to launch the 3D Annotator. Users can visually inspect the 3D shapes of target objects, save 3D images, annotate the target objects, and locate markers (**Fig. 4g**). Refer [3D Annotator](../README.md#3D-Annotator) for detail.

<p align="center">
  <img src="Images/Proof_Annotation.png" alt="Proofreader Dojo and 3D Annotator" width="1000">
</p>
<p align="center">
  <font size="5"> <b>Figure 4. Proofreader Dojo and 3D Annotator</b> </font>
</p>

<BR><BR>

- (Ref1) Dr. Torsten Bullmann conducted a parameter survey for the best segmentation of mitochondria, membranes, and PSDs.
	- <https://github.com/tbullmann/imagetranslation-tensorflow>
