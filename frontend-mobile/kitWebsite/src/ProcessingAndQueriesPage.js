import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, Image, Alert, ScrollView } from 'react-native';
import axios from 'axios';
import Video from 'react-native-video';
import { TouchableOpacity } from 'react-native';

function ProcessingAndQueriesPage() {
  const [queryResult, setQueryResult] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const isImage = (url) => {
    return url && typeof url === 'string' && url.startsWith('data:image/');
  };

  const handleQuery = async (endpoint) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/${endpoint}`);
      setQueryResult(response.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error('Error querying data:', error);
      Alert.alert('Error', 'Error querying data. Please try again.');
    }
  };
  const handleDelete = async (endpoint) => {
    try {
      const response = await axios.delete(`http://127.0.0.1:5000/api/${endpoint}`);
      setQueryResult(response.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error('Error querying data:', error);
      Alert.alert('Error', 'Error querying data. Please try again.');
    }
  };
  const handleExecute = async (endpoint) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/api/${endpoint}`);
      setQueryResult(response.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error('Error querying data:', error);
      Alert.alert('Error', 'Error querying data. Please try again.');
    }
  };


  const handleClear = () => {
    setQueryResult([]);
    setCurrentIndex(0);
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % queryResult.length);
  };

  const handlePrevious = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + queryResult.length) % queryResult.length);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.header}>Processing and Queries</Text>
      <View style={styles.ButtonContainer}>
      <TouchableOpacity style={styles.buttonStyle} onPress={() => handleQuery('query-all-videos')}>
  <Text style={styles.buttonText}>Query All Videos</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleQuery('query-unprocessed-videos')}>
  <Text style={styles.buttonText}>Query Unprocessed Videos</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleQuery('query-processed-videos')}>
  <Text style={styles.buttonText}>Query Processed Videos</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleQuery('query-frames')}>
  <Text style={styles.buttonText}>Query Frames</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleDelete('delete-all-videos')}>
  <Text style={styles.buttonText}>Delete All Videos</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleDelete('delete-all-frames')}>
  <Text style={styles.buttonText}>Delete All Frames</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleDelete('delete-all-data')}>
  <Text style={styles.buttonText}>Delete All Data</Text>
</TouchableOpacity>
<TouchableOpacity style={styles.buttonStyle} onPress={() => handleExecute('execute-extraction-analysis')}>
  <Text style={styles.buttonText}>Execute Extraction and Analysis</Text>
</TouchableOpacity>

      </View>

      <View style={styles.resultContainer}>
        {queryResult.length === 0 ? (
          <Text>No data available.</Text>
        ) : isImage(queryResult[currentIndex]) ? (
          <Image source={{ uri: queryResult[currentIndex] }} style={styles.image} />
        ) : (
          <Video
            source={{ uri: queryResult[currentIndex] }}
            style={styles.video}
            controls={true}
            onError={(e) => {
              console.error('Failed to load video:', e);
              Alert.alert('Error', 'Failed to load video');
            }}
          />
        )}
      </View>
      {queryResult.length > 1 && (
        <View style={styles.navigationButtons}>
          <Button title="Previous" onPress={handlePrevious} />
          <Button title="Next" onPress={handleNext} />
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    paddingTop: 50,
    paddingBottom: 10,
    paddingHorizontal: 10,
    backgroundColor: '#f5f5f5', // Light gray background
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333', // Darker text for better contrast
    marginBottom: 30,
    textAlign: 'center', // Center the title
  },
  ButtonContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center', // Center buttons in the view
    marginBottom: 30,
  },
  buttonStyle: {
    backgroundColor: '#0066cc', // A blue shade for buttons
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
  resultContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    width: '100%',
  },
  image: {
    width: '100%', // Full width
    height: 200,
    borderRadius: 10, // Rounded corners for images
    marginBottom: 20,
  },
  video: {
    width: '100%', // Full width
    height: 200,
    borderRadius: 10, // Rounded corners for videos
  },
  navigationButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 20,
  },
});

// To use the button styles, you'll need to replace the <Button> component 
// with something more customizable like <TouchableOpacity> because the default 
// <Button> component doesn't support much styling.

// Inside the component, replace <Button> with <TouchableOpacity> like so:

<TouchableOpacity 
  style={styles.buttonStyle} 
  onPress={() => handleQuery('query-all-videos')}
>
  <Text style={styles.buttonText}>Query All Videos</Text>
</TouchableOpacity>

// Do this for each button, modifying the onPress prop as necessary.


export default ProcessingAndQueriesPage;
