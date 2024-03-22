import React, { useState } from 'react';
import { View, Alert, Platform, PermissionsAndroid, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { launchImageLibrary } from 'react-native-image-picker';
import axios from 'axios';

const UploadVideoPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = async () => {
    if (Platform.OS === 'android') {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.READ_EXTERNAL_STORAGE,
        {
          title: "Permission to access storage",
          message: "App needs access to your storage to upload video",
          buttonNeutral: "Ask Me Later",
          buttonNegative: "Cancel",
          buttonPositive: "OK"
        }
      );
      if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
        Alert.alert("Storage Permission Denied");
        return;
      }
    }

    launchImageLibrary({ mediaType: 'video' }, (response) => {
      if (response.didCancel) {
        console.log('User cancelled video picker');
      } else if (response.errorCode) {
        console.log('ImagePicker Error: ', response.errorMessage);
      } else {
        const source = { uri: response.assets[0].uri };
        console.log(source);
        setSelectedFile(source);
      }
    });
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('video', {
      uri: selectedFile.uri,
      type: 'video/mp4', // or the correct type based on the file
      name: 'upload.mp4',
    });

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data.message);
      Alert.alert('Video uploaded successfully!');
      setSelectedFile(null);
    } catch (error) {
      console.error('Error uploading video:', error);
      Alert.alert('Error', 'Could not upload the video. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
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
    backgroundColor: '#0066cc', // Blue background for buttons
    paddingVertical: 10,
    paddingHorizontal: 20,
    margin: 5,
    borderRadius: 20, // Rounded corners
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3, // Shadow for Android
  },
  buttonText: {
    color: '#fff', // White text color
    fontSize: 16,
    textAlign: 'center',
  },
});


export default UploadVideoPage;
