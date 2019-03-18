[Japanese version here](Workflow2.ja.md)

- [How to use: Dojo proofreader](HowToUse.md#Dojo-proofreader)
- [How to use: 3D annotator](HowToUse.md#3D-annotator)
- [How to use: 2D DNN](HowToUse.md#2D-DNN)
- [How to use: 3D FFN](HowToUse.md#3D-FFN)
- [How to use: 2D and 3D filters](HowToUse.md#2D-and-3D-filters)
- [Example workflow1: Mitochondria segmentation by use of 2D DNN](Workflow1.md)
- [Example workflow2: Membrane segmentation by use of 3D FFN](Workflow2.md) 


## Example workflow 2: Membrane segmentation by use of 3D Flood Filling Networks (FFN)

Here we try automated membrane segmentation of a stack of EM images from mouse somatosensory cortex. The target EM stack was obtained by Kasthuri et al. ( Cell 162(3):648-61, 2015 ). They used an automatic tape-collecting ultra-microtome system (ATUM) for SEM imaging (ATUM/SEM). The EM stack was originally arranged for ISBI 2013 challenge ([SNEMI3D](http://brainiac2.mit.edu/SNEMI3D/)), and we here reuse it. The EM images are open to public under Open Data Commons Attribution License (ODC-By) v1.0. The original images were passed through the Contrast Limited Adaptive Histogram Equalization filter (CLAHE; blocksize 127,　Histogram bins 256, max slope 1.50).

- https://neurodata.io/data/kasthuri15/
- https://opendatacommons.org/licenses/by/1-0/
- http://docs.neurodata.io/kasthuri2015/kasthuri15docs.html


#### Target EM images and ground truth

1. Download the file "ExampleFFN.zip" from the link below and unzip it on your UNI-EM installed PC. Copy and paste the unzipped contents to the "data" folder of UNI-EM ([UNI-EM]). Here the training image is stored in "[UNI-EM]/data/_3DNN_training_images" (0000.png, ..., 0099.png; 8bit, grayscale png), and the ground truth segmentation is stored in "[UNI-EM]/data/_3DNN_ground_truth"  (0000.png, ..., 0099.png; 16bit, grayscale png; **Fig. 1**). The software Vast lite is recommend to make such ground truth segmentation ( https://software.rc.fas.harvard.edu/lichtman/vast/ ).

- ExampleFFN.zip 522MB: https://www.dropbox.com/s/cztcf8w0ywj1pmz/ExampleFFN.zip?dl=0
<BR>
<p align="center">
  <img src="Images/FFN_GT.png" alt="2D DNN Training" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 1. Training EM image and membrane ground truth segmentation</b> </font>
</p>
<BR>

#### Preprocessing

2. Launch UNI-EM.

3. Select "Segmentation → 3D FFN" from a UNI-EM dropdown menu to launch the dialogue, 3D FFN.
	- Select Preprocessing tab (**Fig. 2a**).
	- Confirm that "Training Image Folder" ( [UNI-EM]/data/_3DNN_training_images ) has the training EM images (**Fig. 2b**), "Ground Truth Folder" ( [UNI-EM]/data/_3DNN_ground_truth ) has the ground truth images (**Fig. 2c**), and the empty "FFN File Folder" ( [UNI-EM]/data/ffn ) exists (**Fig. 2d**). The training EM images are shown in the left thumbnail, and the ground truth are shown in the right thumbnail (**Fig. 2e**).

4. Start preprocessing by clicking the "Execute" button (**Fig. 2f**). Four intermediate files are generated in the FFN File Folder. It takes 6-60 min, depending mainly on image volume. Users will see progress messages in the console window (shown below).
	- "grayscale_maps.h5: a hdf5 file of training EM images
	- "groundtruth.h5": a hdf5 file of ground truth images
	- "af.h5": a intermediate file for FFN
	- "tf_record_file": a intermediate file for FFN

```Preprocessing
        "grayscale_maps.h5" file (training image) was generated.
	"groundtruth.h5" file (ground truth) was generated.
	FFN Preparation
	Start compute_partitions.
	I0217 21:49:47.965403 20392 compute_partitions.py:189] Done processing 2
	I0217 21:49:49.039531 20392 compute_partitions.py:189] Done processing 3
        ...
	I0217 21:52:07.314850 20392 compute_partitions.py:191] Nonzero values: 8875887
	Start build_coordinates.
        ...
	I0217 21:52:10.161867  4268 build_coordinates.py:76] Partition counts:
	I0217 21:52:10.161867  4268 build_coordinates.py:78]  0: 2319505
	I0217 21:52:10.162837  4268 build_coordinates.py:78]  1: 22446
        ...
	I0217 21:52:10.164829  4268 build_coordinates.py:78]  13: 71675
	I0217 21:52:10.164829  4268 build_coordinates.py:80] Resampling and shuffling coordinates.
	I0217 21:52:38.350505  4268 build_coordinates.py:88] Saving coordinates.
```

<BR>
<p align="center">
  <img src="Images/FFN_Prep.png" alt="2D DNN Training" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 2. Preprocessing of FFN</b> </font>
</p>
<BR>


#### Training

5. Select the training tab in the FFN dialogue (**Fig. 2a**).
	- Set the parameter Max Training Steps. It is necessary to train the tensorflow model over several million times, and it takes over one week for precise inference with a NVIDIA GTX1080ti-equipped PC. The training program outputs a tensorflow model every 3000 steps. Users can restart the training from the latest model even if the training process is interrupted. The training program automatically read the latest model from the Tensorflow Model Folder. The training process ends if it reaches the Max Training Steps. Users can execute additional training by setting the larger Max Training Steps if the training appears to be insufficient.
	- Check "Sparse Z" if the z-pitch (nm/pixel) of the EM image is smaller than the xy-pitch (nm/pixel). Here please check it because the target EM images have a 29-nm z pitch and a 3-nm xy pitch ( Cell 162(3):648-61, 2015 ). Internally, the parameters are set as :
		- "depth":12,"fov_size":[33,33,33],"deltas":[8,8,8] for checked
		- "depth":9,"fov_size":[33,33,17],"deltas":[8,8,4] for unchecked

	- Confirm that the rows "Ground Truth h5 File", "Tensorflow Record File", and "Tensorflow Record File" specify the files generated in the preprocessing step.
	- Confirm that the empty "Tensorflow Model Folder" exists.

6. Start training by clicking the "Execute" button. Users will see the following progress messages in the console window:
```FFN Training
        ...
	INFO:tensorflow:global_step/sec: 9.96695
	I0217 23:14:35.690611  2272 tf_logging.py:115] global_step/sec: 9.96695
	INFO:tensorflow:global_step/sec: 9.93734
	I0217 23:14:45.753664  2272 tf_logging.py:115] global_step/sec: 9.93734
	INFO:tensorflow:Saving checkpoints for 5724 into C:[UNI-EM]\data\_3DNN_model_tensorflow\model.ckpt.
	I0217 23:14:48.400605  2272 tf_logging.py:115] Saving checkpoints for 5724 into C:[UNI-EM]\data\_3DNN_model_tensorflow\model.ckpt.
I0217 23:14:48.805234  2272 train.py:699]
        ...
```


#### Inference

7. Select the inference tab in the FFN dialogue (**Fig. 2a**).
	- Confirm that the target EM images are located in the "Target Image Folder" (sequentially numbered image files; 8bit, grayscale png).
	- Confirm that the "Output Inference Folder" exists. Inferred segmentation will be stored in this folder.
	- Specify the Tensorflow Model File. The tensorflow model file consists of the three files ”model.ckpt-XXXXX.data-00000-of-00001", "model.ckpt-XXXXX.index", and "model.ckpt-4000000.meta". Specify the common prefix of those files: "model.ckpt-XXXXX".
	- Check "Sparse Z" if the user check it in the process of training.

8. Start inference by clicking the "Execute" button. The inference program firstly generates the hdf5 style file of target EM images "grayscale_inf.h5" and the parameter file "inference_params.pbtxt" in the FFN File Folder. Then, the inference starts based on those intermediate files. Users will see progress messages in the console window (shown below). Inference is finished if the message "Executor shutdown complete" appears. Confirm that the file "0/0/seg-0_0_0.npz" has been generated in the Output Inference Folder. This is the inferred segmentation. 

```FFN Inference
	...
        I0215 19:10:57.461078 15336 inference.py:554] [cl 0] Starting segmentation at (91, 489, 338) (zyx)
        I0215 19:10:57.474040 15336 inference.py:554] [cl 0] Failed: weak seed
        I0215 19:10:57.475013 15336 inference.py:554] [cl 0] Starting segmentation at (91, 495, 365) (zyx)
        I0215 19:10:57.487977 15336 inference.py:554] [cl 0] Failed: too small: 27
        I0215 19:10:57.504959 15336 inference.py:554] [cl 0] Segmentation done.
        I0215 19:10:57.504959 15336 inference.py:303] Deregistering client 0
        I0215 19:10:57.505930 14064 executor.py:200] client 0 terminating
        I0215 19:11:00.035366 15336 executor.py:169] Requesting executor shutdown.
        I0215 19:11:00.036337 14064 executor.py:191] Executor shut down requested.
        I0215 19:11:00.044339 15336 executor.py:172] Executor shutdown complete.
```

#### Postprocessing

9. Select the postprocessing tab in the FFN dialogue (**Fig. 2a**).

10. Confirm that the inferred segmentation file "seg-0_0_0.npz" was specified in the Target Inference File.

11. Set Output Filetype. The 8-bit color PNG style is recommended for visual inspection of the png files, and the 16-bit gray scale PNG style is recommended for further proofreading, 3D visualization, and annotation.

12. Start postprocessing by clicking the "Execute" button. Confirm that the inferred segmentation files 0000.png, 0001.png, ..., 0099.png were generated in the Output Segmentation Folder.

<BR>

#### Proofreading, annotation, and visualization

13. Select "Dojo → Import EM Stack/Segmentation" from the UNI-EM dropdown menu to launch the dialogue "Import Images & Segments".
	- Set "Source Image Folder" as **[UNI-EM]/data/_3DNN_test_images** .
	- Set "Source Segmentation Folder" as **[UNI-EM]/data/_3DNN_inference** .
	- Create a file folder and set it as "Destination Dojo Folder". Dojo style files will be generated in this folder.

14. Generate the Dojo style files by clicking the "OK" button. The software Dojo will be launched after the file generation (**Fig. 3a**).

15. Inspect successful segmentation visually through manipulating the bottom slice bar (**Fig. 3b**), top Zoom bar (**Fig. 3c**), and top Opacity bar (**Fig. 3d**).

16. Correct erroneous segmentation by entering the mode "Adjust". Click an icon whose shape has a fused two area (**Fig. 3e**). In the adjust mode, users can fill voids by dragging the circled cursor from a filled area. The +/- keys change its radius. Press the Tab key to verify the change, or the Esc key to cancel the change. Users can erase unnecessary areas by dragging the circled cursor after clicking the eraser icon (**Fig. 3f**).

17. Save the segmentation after proofreading. Users can also export the segmentation by selecting "Dojo → Export Segmentation" from the UNI-EM dropdown menu. The export file style is sequential png/tiff images.

18. Select "Annotator → Open" from the UNI-EM dropdown menu to launch the 3D Annotator. Users can visually inspect the 3D shapes of target objects, save 3D images, annotate the target objects, and locate markers (**Fig. 3g**). Refer [3D Annotator](../README.md#3D-Annotator) for detail.


<p align="center">
  <img src="Images/Proof_Annotation.png" alt="Proofreader Dojo and 3D Annotator" width="1000">
</p>
<p align="center">
  <font size="5"> <b>Figure 3. Proofreader Dojo and 3D Annotator</b> </font>
</p>

<BR><BR>
