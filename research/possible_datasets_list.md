# Conducting Motion Datasets for Gesture Recognition

## Most Relevant: Actual Conducting Datasets

### 1. ConductorMotion100
- **Source**: [Research repositories via Baidu Cloud/Google Drive](https://github.com/ConductorMotion/ConductorMotion100) 
- **Data Format**: 2D keypoints (13 upper body points in MS COCO format) + synchronized Mel spectrograms
- **Size**: 100 hours total (90h training, 5h validation, 5h test)
- **Synchronized Music**: Yes - Mel spectrograms at 90 Hz aligned with 30 fps motion
- **Relevance**: ★★★★★ Largest conducting dataset available, specifically designed for music-driven conducting motion generation

### 2. University of Edinburgh Orchestral Conducting Dataset  
- **Source**: [Edinburgh DataShare](https://doi.org/10.7488/ds/2223)
- **Data Format**: C3D motion capture files from 9-camera Qualisys system
- **Size**: 54 recordings (6 conductors × 3 pieces × 3 trials)
- **Synchronized Music**: Yes - with string ensemble performances
- **Relevance**: ★★★★★ High-precision motion capture for detailed conducting analysis, though limited scale

### 3. IRCAM IDEA Open Movement Dataset
- **Source**: [IRCAM Research](https://www.ircam.fr/)
- **Data Format**: IMU sensor data focusing on conductor's right hand
- **Size**: Multiple conducting recordings with two different conductors
- **Synchronized Music**: Yes - with live electronics and instrumental ensemble
- **Relevance**: ★★★★☆ Specialized for real-time conducting gesture following systems

### 4. University of Southampton "Capturing the Contemporary Conductor"
- **Source**: Contact University of Southampton (research dataset)
- **Data Format**: Multi-modal (Vicon motion capture, 360° video, stereo audio, Kinect, EMG)
- **Size**: Multiple professional conductors across three movement types
- **Synchronized Music**: Yes - multi-microphone with SMPTE time code sync
- **Relevance**: ★★★★☆ Most comprehensive multi-modal conducting dataset but limited access

### 5. MIT Conductor's Jacket Dataset (Historical)
- **Source**: MIT Media Lab archives
- **Data Format**: 16-channel sensor data (muscle tension, acceleration, physiological)
- **Size**: 12 hours from 6 subjects (3 professional, 3 students)
- **Synchronized Music**: Yes - during rehearsals and performances
- **Relevance**: ★★★☆☆ First comprehensive conducting dataset with physiological data, housed in MIT Museum

## Moderately Relevant: Music-Motion Datasets

### 6. MOSA (Music mOtion with Semantic Annotation)
- **Source**: [GitHub repository](https://github.com/yufenhuang/MOSA-Music-mOtion-and-Semantic-Annotation-dataset)
- **Data Format**: High-quality 3D motion capture with note-level semantic annotations
- **Size**: 742 performances by 23 professional musicians, >30 hours, 570K notes
- **Synchronized Music**: Yes - note-by-note alignment with pitch, beat, phrase, dynamics
- **Relevance**: ★★★★☆ Best dataset for understanding music-motion relationships in performance contexts

### 7. PianoMotion10M
- **Source**: Research paper dataset
- **Data Format**: MANO hand model parameters, audio, MIDI, video
- **Size**: 116 hours, 10 million hand poses from 1,966 piano videos
- **Synchronized Music**: Yes - audio-MIDI-motion alignment
- **Relevance**: ★★★☆☆ Excellent for hand gesture analysis but limited to piano performance

### 8. Expressive Musical Gestures Dataset (Goldsmiths)
- **Source**: [Goldsmiths GitLab](https://gitlab.doc.gold.ac.uk/expressive-musical-gestures/dataset)
- **Data Format**: Motion capture and EMG data
- **Size**: 5 violinists, 2 pianists performing pedagogical phrases
- **Synchronized Music**: Yes - with variations in dynamics, tempo, articulation
- **Relevance**: ★★★★☆ High relevance for expressive gesture analysis, though limited scale

### 9. AIST++ Dance Motion Dataset
- **Source**: [Google Research](https://aistdancedb.ongaaccel.jp)
- **Data Format**: 3D keypoints, SMPL parameters, multi-view videos
- **Size**: 5.2 hours, 1,408 sequences, 30 subjects, 10 dance genres
- **Synchronized Music**: Yes - music-choreography splits with different BPMs
- **Relevance**: ★★★☆☆ Useful for rhythmic movement patterns, though focused on dance

### 10. Motorica Dance Dataset
- **Source**: [GitHub](https://github.com/simonalexanderson/MotoricaDanceDataset)
- **Data Format**: BVH motion capture from 17 cameras at 120 fps
- **Size**: 6 hours across 8 dance styles
- **Synchronized Music**: Yes - high-quality audio-motion synchronization
- **Relevance**: ★★★☆☆ Good for expressive movement patterns with precise temporal alignment

## Least Relevant: General Motion Datasets

### 11. Motion-X++
- **Source**: [Research dataset](https://motion-x-dataset.github.io)
- **Data Format**: SMPL-X whole-body parameters including face and hands
- **Size**: 19.5M poses, 120K sequences, 45.3K audio files
- **Synchronized Music**: Partial - includes musical performances with audio
- **Relevance**: ★★★☆☆ Contains some musical instrument playing but primarily general motion

### 12. AMASS (Archive of Motion Capture as Surface Shapes)
- **Source**: [AMASS Database](https://amass.is.tue.mpg.de/)
- **Data Format**: SMPL body model parameters, 3D meshes
- **Size**: 40+ hours, 300+ subjects, 11,000+ motions from 15 datasets
- **Synchronized Music**: No - general motion capture compilation
- **Relevance**: ★★☆☆☆ Large unified dataset likely containing some expressive movements

### 13. CMU Motion Capture Database
- **Source**: [CMU Graphics Lab](http://mocap.cs.cmu.edu/)
- **Data Format**: ASF/AMC files, BVH format available
- **Size**: 140+ subjects, thousands of sequences
- **Synchronized Music**: No - includes dance sequences but no audio sync
- **Relevance**: ★★☆☆☆ Free access with dance categories that may contain conducting-like gestures

### 14. Human3.6M
- **Source**: [Human3.6M](http://vision.imar.ro/human3.6m/description.php)
- **Data Format**: 3D joint positions, high-resolution RGB videos
- **Size**: 3.6M poses, 11 actors, 17 scenarios
- **Synchronized Music**: No - daily activities and conversations
- **Relevance**: ★★☆☆☆ May include some expressive gestures during discussions

### 15. NTU RGB+D 120
- **Source**: Available through registration
- **Data Format**: RGB videos, depth maps, 3D skeletal data
- **Size**: 114,480 samples, 120 actions
- **Synchronized Music**: No - action recognition focused
- **Relevance**: ★★☆☆☆ Includes gesturing actions but not music-specific

## Key Recommendations

**For conducting motion generation research**, the optimal approach combines:

1. **Primary dataset**: ConductorMotion100 for large-scale conducting patterns
2. **Quality reference**: Edinburgh dataset for precise motion analysis  
3. **Expressive context**: MOSA for understanding music-motion relationships
4. **Supplementary data**: AIST++ for rhythmic movement understanding

**Critical limitations** across datasets include limited 3D conducting data, varying synchronization quality, and most datasets focusing on dance rather than conducting. The **ConductorMotion100** represents the current state-of-the-art for scale, while **Edinburgh** provides the highest motion capture precision for conducting-specific research.