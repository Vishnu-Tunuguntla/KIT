import React, { useState } from 'react';
import { Linking, View, Alert, TouchableOpacity, Text, StyleSheet, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

const UploadVideoPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState(''); // New state for file name

  const getPermissionAsync = async () => {
    if (Platform.OS !== 'web') {
      const { status } = await ImagePicker.getMediaLibraryPermissionsAsync(false);
      if (status !== 'granted') {
        const { status: newStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (newStatus !== 'granted') {
          Alert.alert(
            'Camera Roll Permission Required',
            'Please go to your settings and grant permission for camera roll access.',
            [
              { text: 'Cancel', style: 'cancel' },
              { text: 'Settings', onPress: () => Linking.openSettings() },
            ],
            { cancelable: false },
          );
          return false;
        }
      }
    }
    return true;
  };
  

  const handleFileChange = async () => {
    const hasPermission = await getPermissionAsync();
    if (!hasPermission) return;

    try {
      let result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Videos,
        allowsEditing: true,
        quality: 1,
      });

      if (!result.cancelled && result.assets && result.assets.length > 0) {
  const video = result.assets[0]; // Get the first video from the assets array
  console.log(video);
  setSelectedFile({ uri: video.uri });
  setFileName(video.fileName); // Set the file name from the fileName property
} else {
  console.error('No video available', result);
}

    } catch (E) {
      console.error('Error selecting the video:', E);
      Alert.alert('Error', 'Could not select the video. Please try again.');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('video', {
      uri: selectedFile.uri,
      type: 'video/mp4',
      name: fileName, // Use the state for file name
    });

    try {
      const response = await axios.post('http://34.233.181.229:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data.message);
      Alert.alert('Video uploaded successfully!');
      setSelectedFile(null);
      setFileName(''); // Reset file name
    } catch (error) {
      console.error('Error uploading video:', error);
      Alert.alert('Error', 'Could not upload the video. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
      {/* Display the file name here */}
      {fileName ? (
        <Text style={styles.fileNameText}>{fileName}</Text>
      ) : null}
      <TouchableOpacity style={styles.buttonStyle} onPress={handleFileChange}>
        <Text style={styles.buttonText}>Select Video</Text>
      </TouchableOpacity>
      {selectedFile && (
        <TouchableOpacity style={styles.buttonStyle} onPress={handleUpload}>
          <Text style={styles.buttonText}>Upload Video</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonStyle: {
    backgroundColor: '#0066cc',
    paddingVertical: 10,
    paddingHorizontal: 20,
    margin: 5,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
  },
  fileNameText: { // New style for file name text
    color: '#000', // Black text color
    fontSize: 14,
    margin: 5,
    textAlign: 'center',
  },
});

export default UploadVideoPage;
